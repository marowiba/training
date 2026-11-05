"""Read-only MCP tools for selected Intervals.icu training data."""

from __future__ import annotations

import base64
import json
import os
import re
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Literal, TypeGuard, cast
from urllib.parse import unquote

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession
from pydantic import BaseModel, Field

API_BASE_URL = "https://intervals.icu/api/v1"
API_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}
load_dotenv(Path(__file__).resolve().parents[1] / ".env")
ATHLETE_ID = os.environ.get("INTERVALS_ATHLETE_ID", "")
API_KEY = os.environ.get("INTERVALS_API_KEY", "")

ACTIVITY_FIELDS = (
    "id",
    "type",
    "start_date_local",
    "moving_time",
    "elapsed_time",
    "distance",
    "total_elevation_gain",
    "average_watts",
    "icu_weighted_avg_watts",
    "average_heartrate",
    "max_heartrate",
    "average_speed",
    "max_speed",
    "icu_training_load",
    "icu_intensity_factor",
    "kilojoules",
)
WELLNESS_FIELDS = (
    "date",
    "ctl",
    "atl",
    "tsb",
    "hrv",
    "hrvSDNN",
    "restingHR",
    "sleepSecs",
    "sleepScore",
    "soreness",
    "fatigue",
    "stress",
)

mcp = FastMCP("ShadowCoach Intervals.icu")


class WriteConfirmation(BaseModel):
    confirmed: Literal["Ja", "Nein"] = Field(
        default="Nein",
        description="Bestätigung der Ausführung der nicht-lesenden Anfrage.",
    )


def _validate_configuration() -> None:
    if not API_KEY:
        raise RuntimeError("INTERVALS_API_KEY muss in der Workspace-.env gesetzt sein.")
    if not re.fullmatch(r"(?:i[0-9]+|[0-9]+)", ATHLETE_ID):
        raise RuntimeError("INTERVALS_ATHLETE_ID in der Workspace-.env muss numerisch oder i-prefixed sein.")


def _date_range(oldest: str | None, newest: str | None) -> tuple[str, str]:
    today = date.today()
    end = date.fromisoformat(newest) if newest else today
    start = date.fromisoformat(oldest) if oldest else end - timedelta(days=30)
    if start > end:
        raise ValueError("oldest darf nicht nach newest liegen.")
    if (end - start).days >= 366:
        raise ValueError("Der angefragte Zeitraum darf höchstens 366 Tage umfassen.")
    return start.isoformat(), end.isoformat()


def _is_record_list(payload: Any) -> TypeGuard[list[dict[str, Any]]]:
    if not isinstance(payload, list):
        return False

    rows = cast(list[Any], payload)
    for row in rows:
        if not isinstance(row, dict):
            return False
    return True


def _project_rows(payload: Any, fields: tuple[str, ...]) -> list[dict[str, Any]]:
    if not _is_record_list(payload):
        raise ValueError("Intervals.icu lieferte eine ungültige Listenstruktur.")
    return [{field: row[field] for field in fields if field in row} for row in payload]


def _build_api_url(path: str) -> str:
    if (
        not path.startswith("/")
        or path.startswith("//")
        or "\\" in path
        or "?" in path
        or "#" in path
        or any(ord(char) < 32 for char in path)
    ):
        raise ValueError("path muss ein API-Pfad wie /athlete/{id}/activities sein.")
    if any(segment in {".", ".."} for segment in unquote(path).split("/")):
        raise ValueError("path darf keine relativen Pfadsegmente enthalten.")
    return f"{API_BASE_URL}{path}"


def _response_body(response: httpx.Response) -> Any:
    if not response.content:
        return None

    content_type = response.headers.get("content-type", "").lower()
    if "json" in content_type:
        return response.json()

    try:
        return response.content.decode("utf-8")
    except UnicodeDecodeError:
        return {"encoding": "base64", "data": base64.b64encode(response.content).decode("ascii")}


async def _confirm_non_read_request(
    ctx: Context[ServerSession, Any, Any],
    method: str,
    url: str,
    query: dict[str, Any] | None,
    body: Any,
    body_base64: str | None,
    content_type: str | None,
) -> None:
    if method == "GET":
        return

    details: dict[str, Any] = {
        "method": method,
        "url": url,
        "query": query,
        "content_type": content_type,
        "body": body,
        "body_base64": body_base64,
    }
    confirmation = await ctx.elicit(
        message=(
            "Sicherheitsabfrage: Diese nicht-lesende Intervals.icu-Anfrage wird erst "
            "nach deiner ausdrücklichen Bestätigung ausgeführt. Prüfe Methode, Ziel "
            "und Nutzdaten genau. Die Anfrage kann Daten ändern oder löschen.\n\n"
            f"{json.dumps(details, ensure_ascii=False, indent=2, default=str)}"
        ),
        schema=WriteConfirmation,
    )
    if confirmation.action != "accept" or confirmation.data.confirmed != "Ja":
        raise PermissionError("Intervals.icu-Aufruf abgebrochen: nicht bestätigt.")


async def _get_rows(
    resource: str,
    oldest: str | None,
    newest: str | None,
    fields: tuple[str, ...],
    limit: int | None = None,
) -> str:
    _validate_configuration()
    start, end = _date_range(oldest, newest)
    params: dict[str, str | int] = {"oldest": start, "newest": end}
    if limit is not None:
        if not 1 <= limit <= 100:
            raise ValueError("limit muss zwischen 1 und 100 liegen.")
        params["limit"] = limit

    url = f"{API_BASE_URL}/athlete/{ATHLETE_ID}/{resource}"
    async with httpx.AsyncClient(
        auth=httpx.BasicAuth("API_KEY", API_KEY),
        headers={"Accept": "application/json"},
        timeout=30.0,
    ) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        payload = response.json()

    return json.dumps(_project_rows(payload, fields), ensure_ascii=False)


@mcp.tool()
async def intervals_api_request(
    ctx: Context[ServerSession, Any, Any],
    method: str,
    path: str,
    query: dict[str, Any] | None = None,
    body: Any = None,
    body_base64: str | None = None,
    content_type: str | None = None,
) -> str:
    """Ruft beliebige Intervals.icu-API-Routen auf; unterstützt Lese- und Schreibmethoden.

    path muss relativ zur API-Basis-URL angegeben werden, z. B.
    /athlete/i12345/activities. JSON-Antworten werden vollständig und ungefiltert
    zurückgegeben; Nicht-Text-Antworten werden als Base64 kodiert.
    """
    _validate_configuration()
    method = method.upper()
    if method not in API_METHODS:
        raise ValueError(f"Nicht unterstützte HTTP-Methode: {method}")
    url = _build_api_url(path)
    if body is not None and body_base64 is not None:
        raise ValueError("body und body_base64 dürfen nicht gleichzeitig gesetzt sein.")

    await _confirm_non_read_request(
        ctx,
        method,
        url,
        query,
        body,
        body_base64,
        content_type,
    )

    headers = {"Accept": "application/json"}
    request_options: dict[str, Any] = {}
    if body_base64 is not None:
        try:
            request_options["content"] = base64.b64decode(body_base64, validate=True)
        except ValueError as exc:
            raise ValueError("body_base64 ist kein gültiger Base64-String.") from exc
    elif isinstance(body, (dict, list, int, float, bool)):
        request_options["json"] = body
    elif body is not None:
        request_options["content"] = body
    if content_type:
        headers["Content-Type"] = content_type

    async with httpx.AsyncClient(
        auth=httpx.BasicAuth("API_KEY", API_KEY),
        headers=headers,
        timeout=60.0,
    ) as client:
        response = await client.request(
            method,
            url,
            params=query,
            **request_options,
        )
        response.raise_for_status()

    return json.dumps(
        {
            "status_code": response.status_code,
            "content_type": response.headers.get("content-type"),
            "body": _response_body(response),
        },
        ensure_ascii=False,
    )


@mcp.tool()
async def get_activities(
    oldest: str | None = None,
    newest: str | None = None,
    limit: int = 25,
) -> str:
    """Liest Aktivitäten im Zeitraum; gibt nur ausgewählte Trainingskennzahlen zurück."""
    return await _get_rows("activities", oldest, newest, ACTIVITY_FIELDS, limit)


@mcp.tool()
async def get_wellness(oldest: str | None = None, newest: str | None = None) -> str:
    """Liest Wellnessdaten im Zeitraum; gibt nur ausgewählte Kennzahlen zurück."""
    return await _get_rows("wellness", oldest, newest, WELLNESS_FIELDS)


if __name__ == "__main__":
    _validate_configuration()
    mcp.run(transport="stdio")
