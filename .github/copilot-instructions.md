# Sicherheitsregel für Intervals.icu

Vor jeder Anfrage an `intervals_api_request`, deren HTTP-Methode nicht `GET` ist,
musst du den Nutzer mit `ask_user` zur konkreten Aktion befragen. Nenne in der Abfrage
Methode, API-Pfad, Parameter und Nutzdaten und warte auf ein ausdrückliches Ja,
bevor du das Werkzeug aufrufst. Die Bestätigung gilt nur für exakt diese Anfrage;
bei Änderungen erneut fragen. Bei Ablehnung, Unklarheit oder fehlender
Bestätigung nicht aufrufen. Die MCP-seitige Elicitation ist eine zusätzliche
Pflichtprüfung und darf nicht umgangen werden.
