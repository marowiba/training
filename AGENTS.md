# Sicherheitsregeln für Intervals.icu-Aktionen

- Behandle API-Aufrufe als nicht lesend, wenn ihre HTTP-Methode nicht `GET` ist.
- Rufe `intervals_api_request` für eine nicht lesende Anfrage niemals direkt auf:
  Verwende zuerst `ask_user`, um Methode, API-Pfad, Parameter und Nutzdaten in
  einer Sicherheitsabfrage zu nennen und warte auf eine ausdrückliche
  Bestätigung für genau diese Anfrage. Frage nicht nur im Fließtext.
- Eine frühere allgemeine Bitte, eine Vermutung, eine Zustimmung des Agenten oder
  eine Bestätigung für eine andere Anfrage gilt nicht als Freigabe. Bei geänderten
  Methoden, Pfaden, Parametern oder Nutzdaten ist erneut nachzufragen.
- Bei Ablehnung, unklarer Antwort oder fehlender Möglichkeit zur Sicherheitsabfrage
  darf der API-Aufruf nicht ausgeführt werden.
- Der MCP-Server verlangt zusätzlich eine Elicitation-Bestätigung. Ist diese
  Funktion im MCP-Client nicht verfügbar, muss der Aufruf fehlschlagen; die
  Sicherheitsabfrage darf nicht umgangen werden.
