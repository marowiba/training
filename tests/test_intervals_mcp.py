import asyncio
import base64
import json

import httpx
import pytest

import scripts.intervals_mcp as intervals_mcp
from mcp.server.elicitation import AcceptedElicitation, DeclinedElicitation
from scripts.intervals_mcp import (
    ACTIVITY_FIELDS,
    API_BASE_URL,
    WELLNESS_FIELDS,
    _build_api_url,
    _date_range,
    _project_rows,
)


def test_activity_projection_excludes_unselected_fields():
    rows = _project_rows(
        [{"id": "a1", "type": "Ride", "name": "Private route", "latitude": 52.5}],
        ACTIVITY_FIELDS,
    )

    assert rows == [{"id": "a1", "type": "Ride"}]


def test_wellness_projection_excludes_unselected_fields():
    rows = _project_rows(
        [{"date": "2026-11-05", "hrv": 55, "notes": "private note"}],
        WELLNESS_FIELDS,
    )

    assert rows == [{"date": "2026-11-05", "hrv": 55}]


def test_date_range_defaults_to_last_30_days():
    oldest, newest = _date_range(None, "2026-11-05")

    assert oldest == "2026-10-06"
    assert newest == "2026-11-05"


@pytest.mark.parametrize(
    ("oldest", "newest"),
    [
        ("2026-11-06", "2026-11-05"),
        ("2025-11-04", "2026-11-05"),
        ("not-a-date", "2026-11-05"),
    ],
)
def test_date_range_rejects_invalid_ranges(oldest, newest):
    with pytest.raises(ValueError):
        _date_range(oldest, newest)


def test_projection_rejects_invalid_api_shape():
    with pytest.raises(ValueError, match="ungültige Listenstruktur"):
        _project_rows({"error": "bad response"}, ACTIVITY_FIELDS)


def test_api_path_uses_fixed_intervals_base_url():
    assert _build_api_url("/athlete/i12345/activities") == (
        f"{API_BASE_URL}/athlete/i12345/activities"
    )


@pytest.mark.parametrize(
    "path",
    [
        "https://example.com/activities",
        "//example.com/activities",
        "/athlete/../activities",
        "/athlete/%2e%2e/activities",
        "/athlete/i12345/activities?limit=5",
        "/athlete/i12345\\activities",
    ],
)
def test_api_path_rejects_non_api_or_ambiguous_paths(path):
    with pytest.raises(ValueError):
        _build_api_url(path)


def test_general_api_tool_sends_authenticated_request_and_returns_unfiltered_json(monkeypatch):
    observed = {}

    def handle_request(request):
        observed["method"] = request.method
        observed["url"] = str(request.url)
        observed["authorization"] = request.headers["authorization"]
        observed["body"] = json.loads(request.content)
        return httpx.Response(200, json={"name": "Activity title", "rpe": 7})

    original_async_client = httpx.AsyncClient
    transport = httpx.MockTransport(handle_request)
    monkeypatch.setattr(intervals_mcp, "API_KEY", "test-secret")
    monkeypatch.setattr(intervals_mcp, "ATHLETE_ID", "i12345")
    monkeypatch.setattr(
        intervals_mcp.httpx,
        "AsyncClient",
        lambda **kwargs: original_async_client(transport=transport, **kwargs),
    )

    class ConfirmingContext:
        async def elicit(self, message, schema):
            observed["confirmation_message"] = message
            observed["confirmation_schema"] = schema
            return AcceptedElicitation(data=schema(confirmed="Ja"))

    result = asyncio.run(
        intervals_mcp.intervals_api_request(
            ConfirmingContext(),
            "POST",
            "/athlete/i12345/events",
            query={"oldest": "2026-11-05"},
            body={"name": "Workout"},
        )
    )

    assert observed["method"] == "POST"
    assert observed["url"] == f"{API_BASE_URL}/athlete/i12345/events?oldest=2026-11-05"
    assert observed["authorization"] == (
        "Basic " + base64.b64encode(b"API_KEY:test-secret").decode("ascii")
    )
    assert observed["body"] == {"name": "Workout"}
    assert "POST" in observed["confirmation_message"]
    assert "/athlete/i12345/events" in observed["confirmation_message"]
    assert '"name": "Workout"' in observed["confirmation_message"]
    assert json.loads(result)["body"] == {"name": "Activity title", "rpe": 7}


def test_non_read_api_tool_does_not_send_request_without_confirmation(monkeypatch):
    requested = False

    def handle_request(_request):
        nonlocal requested
        requested = True
        return httpx.Response(200, json={})

    original_async_client = httpx.AsyncClient
    transport = httpx.MockTransport(handle_request)
    monkeypatch.setattr(intervals_mcp, "API_KEY", "test-secret")
    monkeypatch.setattr(intervals_mcp, "ATHLETE_ID", "i12345")
    monkeypatch.setattr(
        intervals_mcp.httpx,
        "AsyncClient",
        lambda **kwargs: original_async_client(transport=transport, **kwargs),
    )

    class DecliningContext:
        async def elicit(self, message, schema):
            return DeclinedElicitation()

    with pytest.raises(PermissionError, match="nicht bestätigt"):
        asyncio.run(
            intervals_mcp.intervals_api_request(
                DecliningContext(),
                "DELETE",
                "/athlete/i12345/events/123",
            )
        )

    assert not requested


def test_non_read_api_tool_fails_closed_when_elicitation_is_unavailable(monkeypatch):
    requested = False

    def handle_request(_request):
        nonlocal requested
        requested = True
        return httpx.Response(200, json={})

    original_async_client = httpx.AsyncClient
    transport = httpx.MockTransport(handle_request)
    monkeypatch.setattr(intervals_mcp, "API_KEY", "test-secret")
    monkeypatch.setattr(intervals_mcp, "ATHLETE_ID", "i12345")
    monkeypatch.setattr(
        intervals_mcp.httpx,
        "AsyncClient",
        lambda **kwargs: original_async_client(transport=transport, **kwargs),
    )

    class UnsupportedContext:
        async def elicit(self, message, schema):
            raise RuntimeError("Client does not support elicitation")

    with pytest.raises(RuntimeError, match="does not support elicitation"):
        asyncio.run(
            intervals_mcp.intervals_api_request(
                UnsupportedContext(),
                "PUT",
                "/athlete/i12345/events/123",
                body={"name": "Updated workout"},
            )
        )

    assert not requested


def test_get_request_does_not_require_confirmation(monkeypatch):
    original_async_client = httpx.AsyncClient
    transport = httpx.MockTransport(
        lambda _request: httpx.Response(200, json={"result": "ok"})
    )
    monkeypatch.setattr(intervals_mcp, "API_KEY", "test-secret")
    monkeypatch.setattr(intervals_mcp, "ATHLETE_ID", "i12345")
    monkeypatch.setattr(
        intervals_mcp.httpx,
        "AsyncClient",
        lambda **kwargs: original_async_client(transport=transport, **kwargs),
    )

    class UnexpectedConfirmationContext:
        async def elicit(self, message, schema):
            raise AssertionError("GET must not ask for write confirmation")

    result = asyncio.run(
        intervals_mcp.intervals_api_request(
            UnexpectedConfirmationContext(),
            "GET",
            "/athlete/i12345/activities",
        )
    )

    assert json.loads(result)["body"] == {"result": "ok"}
