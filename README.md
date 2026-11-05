# ShadowCoach

ShadowCoach verbindet VS Code über einen lokalen MCP-Server mit der
Intervals.icu-REST-API. So kann der ausgewählte KI-Assistent Trainings- und
Wellnessdaten auf Anfrage abrufen und auswerten.

## Was ShadowCoach kann

Der Server bietet drei Werkzeuge:

- **`get_activities`** – Aktivitäten für einen Zeitraum abrufen. Ausgewählte
  Felder sind Aktivitätstyp, Startzeit, Dauer, Distanz, Höhenmeter, Leistung,
  Herzfrequenz, Geschwindigkeit, Trainingsbelastung, Intensitätsfaktor und
  Kilojoule. Standardmäßig werden die letzten 30 Tage und höchstens 25
  Aktivitäten abgefragt; pro Anfrage sind bis zu 100 möglich.
- **`get_wellness`** – Wellnessdaten für einen Zeitraum abrufen, darunter CTL,
  ATL, TSB, HRV, Ruhepuls, Schlaf sowie subjektive Erholungswerte. Standardmäßig
  gilt derselbe 30-Tage-Zeitraum.
- **`intervals_api_request`** – beliebige Intervals.icu-API-Routen aufrufen.
  Damit lassen sich beispielsweise geplante Workouts oder Detaildaten abfragen.
  Antworten dieses Werkzeugs sind ungefiltert.

Die ersten beiden Werkzeuge liefern ausgewählte **Rohdaten**, keine
vorberechneten Analysen. Der KI-Assistent kann die abgerufenen Werte auf deine
Frage hin zusammenfassen, vergleichen oder interpretieren. Die dafür
verfügbaren Kennzahlen hängen von den gelieferten API-Feldern ab. Zum Beispiel
sind Aktivitätsname und RPE derzeit nicht in der Feld-Auswahl von
`get_activities`; sie können über den allgemeinen REST-Aufruf abgefragt werden.

## Einrichtung

Voraussetzungen: Python 3.11 oder neuer und [`uv`](https://docs.astral.sh/uv/)
im `PATH`.

1. Repository in VS Code öffnen.
2. Im Repository-Ordner `.env` aus der Vorlage erstellen und die eigenen
   Zugangsdaten eintragen:

   ```powershell
   Copy-Item .env.example .env
   ```

   `.env` benötigt `INTERVALS_API_KEY` und `INTERVALS_ATHLETE_ID`. Den API-Key
   findest du in deinem Intervals.icu-Konto. Die Datei wird nicht versioniert.
3. In VS Code den MCP-Server `shadowcoach-intervals` starten beziehungsweise
   nach der Einrichtung neu starten. Die Konfiguration liegt in
   `.vscode/mcp.json`; `uv` richtet die Projektabhängigkeiten beim ersten Start
   ein.
4. Im VS Code Chat eine Frage zu den Daten stellen. Beispiele stehen in der
   [Kurzanleitung](docs/anwender.md).

## Sicherheit und Datenschutz

- Der Server kommuniziert per HTTPS mit `https://intervals.icu/api/v1`.
- API-Key und Athlete-ID bleiben in der lokalen, ignorierten `.env`.
- API-Antworten werden an den in VS Code ausgewählten KI-Assistenten
  weitergegeben. Lokale Serverausführung bedeutet nicht automatisch lokale
  Modellverarbeitung.
- `intervals_api_request` kann mit den Methoden GET, POST, PUT, PATCH, DELETE,
  HEAD und OPTIONS Daten lesen oder ändern. **Jede Anfrage außer GET erfordert
  eine ausdrückliche Bestätigung**; ohne MCP-Elicitation wird sie abgebrochen.
  Prüfe Methode, Ziel, Parameter und Nutzdaten sorgfältig.

Details zu Feldern und Verhalten stehen in der
[Anforderungsspezifikation](docs/anforderung.md).
Ein mögliches standardisiertes Wellness-/Recovery-Analysewerkzeug ist im
[Recovery-Konzept](docs/wellness-recovery.md) beschrieben; es ist noch nicht
implementiert.
