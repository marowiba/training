# Wellness- und Recovery-Analyse

## Ziel

Eine standardisierte Recovery-Analyse soll Wellness-Messwerte wie HRV,
Ruhepuls, Schlaf, Müdigkeit und Stress mit der Trainingsbelastung in Beziehung
setzen. Sie soll Veränderungen sichtbar machen, nicht medizinisch diagnostizieren
oder eigenständig Trainingsentscheidungen treffen.

## Stand heute

Der MCP-Server liefert Wellness- und Aktivitätsrohwerte. Eine fest definierte
Recovery-Auswertung ist noch nicht implementiert. Der KI-Assistent kann die
vorhandenen Werte auf eine Chatfrage hin interpretieren; diese Auswertung ist
aber nicht notwendigerweise jedes Mal nach denselben Regeln standardisiert.

`get_wellness` liefert unter anderem HRV, Ruhepuls, Schlaf, Müdigkeit, Stress
sowie CTL, ATL und TSB. `get_activities` liefert Zeitstempel und
Trainingsbelastung, aber derzeit weder Aktivitätsnamen noch RPE. Für zusätzliche
Aktivitätsfelder kann der allgemeine REST-Aufruf verwendet werden.

## Vorschlag für eine standardisierte Analyse

1. **Daten prüfen:** Verfügbarkeit und Anzahl der Messwerte für HRV, Ruhepuls,
   Schlaf und subjektive Wellness-Angaben ausweisen. Fehlende Werte nicht als
   normale Werte behandeln.
2. **Zeiträume festlegen:** Zum Beispiel die letzten 7 Tage mit einer
   persönlichen 28-Tage-Baseline vergleichen. Baseline-Fenster und erforderliche
   Mindestabdeckung sind vor der Implementierung verbindlich festzulegen.
3. **Vergleich berechnen:** Tages- oder Wochenwerte den persönlichen
   Referenzwerten gegenüberstellen und Abweichungen samt Einheit anzeigen.
   Trainingsbelastung und zeitliche Nähe zu Aktivitäten als Kontext ergänzen.
4. **Ergebnis strukturieren:** Zeitraum, Datenabdeckung, Vergleich, auffällige
   Veränderungen und vorsichtige Zusammenfassung in einem festen Format
   ausgeben.
5. **Validieren:** Berechnungen und Fälle mit lückenhaften Daten automatisiert
   testen. Korrelationen als Beobachtungen, nicht als Ursache-Wirkungs-Beweis
   formulieren.

Für eine reproduzierbare Umsetzung bietet sich ein eigenes MCP-Werkzeug wie
`get_recovery_analysis` an. Es würde Daten abrufen und die festgelegten Regeln
deterministisch berechnen, statt die Berechnung allein dem Chatmodell zu
überlassen. Wearable-Daten müssen dafür bereits in Intervals.icu verfügbar sein;
ShadowCoach importiert sie nicht automatisch.

## Nutzung als Enduser

Nach Implementierung könnte der Nutzer im VS-Code-Chat zum Beispiel fragen:

> „Führe den Recovery-Check für die letzten 7 Tage aus und vergleiche HRV,
> Ruhepuls und Schlaf mit meiner persönlichen Baseline. Berücksichtige die
> Trainingsbelastung und weise auf fehlende Messwerte hin.“

Bis dahin kann dieselbe Frage an den Assistenten gestellt werden, der die
verfügbaren Rohdaten abruft und interpretiert. Das Ergebnis ist dann eine
KI-gestützte Einzelfallauswertung und keine garantierte, reproduzierbare
Standardanalyse.

## Grenzen

- Die Aussagekraft hängt von Vollständigkeit und Qualität der in Intervals.icu
  gespeicherten Daten ab.
- HRV und andere Wellness-Messwerte schwanken; einzelne Abweichungen erlauben
  keine sichere Aussage über Stress, Erholung oder Gesundheit.
- Ergebnisse sind Trainingsinformation und keine medizinische Beratung.
