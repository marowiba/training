# ShadowCoach – Kurzanleitung

ShadowCoach verbindet VS Code mit deinen Intervals.icu-Daten. Stelle Fragen im
Chat; der Assistent ruft die nötigen Daten über den lokalen MCP-Server ab und
wertet sie auf Anfrage aus.

## Beispiele

- „Fasse meine Aktivitäten der letzten 14 Tage nach Dauer und Trainingsbelastung zusammen.“
- „Vergleiche meine HRV und meinen Ruhepuls aus den letzten vier Wochen.“
- „Nenne meine letzten fünf Aktivitäten mit Namen und RPE.“
- „Welche drei Workouts sind als Nächstes geplant?“

Aktivitäten und Wellness werden über spezialisierte Werkzeuge mit einer
begrenzten Feldauswahl gelesen. Für zusätzliche Intervals.icu-Daten kann der Assistent den allgemeinen REST-Aufruf nutzen; dessen Antworten sind ungefiltert. Es gibt keine automatische Synchronisierung, Auswertung im Hintergrund oder automatische Trainingssteuerung.

Wellness-Auswertungen sind aktuell KI-gestützte Interpretationen der verfügbaren
Rohdaten, keine standardisierte Recovery-Analyse. Das geplante Konzept ist unter
[Wellness- und Recovery-Analyse](wellness-recovery.md) beschrieben.

## Wichtig

Lesezugriffe (GET) werden ohne Bestätigung ausgeführt. Bei jeder Anfrage, die Daten ändern oder löschen könnte, musst du die konkrete Aktion ausdrücklich bestätigen. Prüfe dabei Methode, Ziel und Nutzdaten. Teile niemals deinen API-Key im Chat; er gehört ausschließlich in die lokale `.env`.

Die API-Daten werden dem in VS Code verwendeten KI-Assistenten übergeben. Beachte daher auch die Datenschutz- und  Datenverarbeitungsregeln des ausgewählten Modellanbieters.
