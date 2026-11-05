Wenn der Appetit erst mal geweckt ist, eröffnet die direkte Anbindung über ein lokales MCP-Analyse-Center in VS Code völlig neue Möglichkeiten. Statt mühsam durch Web-Oberflächen zu klicken oder Tabellen zu exportieren, kannst du den KI-Assistenten direkt im Chat komplexe, bereichsübergreifende Fragen zu deinen Trainingsdaten stellen.

Hier sind konkrete Analyse-Szenarien, die ein solches MCP-basiertes System direkt aus deinen Intervals.icu-Daten auslesen und auswerten kann:

### 1. Form- & Belastungssteuerung (CTL / ATL / TSB)

* **Tapering- und Peak-Planung:** Lass dir genau berechnen, wie sich deine Formkurve (Training Stress Balance) bei einem bestimmten Trainingsvolumen in den kommenden Wochen entwickelt – ideal für den Aufbau auf Saisonhöhepunkte.
* **Überlastungs-Early-Warning:** Der Assistent kann prüfen, ob deine akute Belastung (ATL) deine langfristige Fitness (CTL) zu schnell übersteigt und Warnungen ausgeben, bevor du in ein Übertraining läufst.

### 2. Polarisation & Intensitätsverteilung (Polarized Training)

* **80/20-Check:** Automatische Auswertung der wöchentlichen Trainingszeit: Wie viel Prozent fährst du wirklich im Grundlagenbereich (Zone 2) im Vergleich zu hochintensiven Intervallen?
* **Disziplin-Erkennung:** Aufteilung der Einheiten nach Polarisation – laufen die MyWhoosh-Indoor-Einheiten sauber strukturiert, während Outdoor-Gravel-Fahrten oft zu intensiv geraten?

### 3. Indoor vs. Outdoor Performance-Vergleich

* **Watt-Effizienz-Analyse:** Vergleiche deine Leistungsdaten auf dem Smart Trainer (MyWhoosh / Virtual Rides) direkt mit deinen Outdoor-Gravel- oder Straßentouren von Garmin. Wie stark bricht die Durchschnittsleistung draußen (durch Abfahrten, Wind und Ampeln) im Vergleich zu den cleanen Indoor-Intervallen ein?
* **Herzfrequenz-Leistungs-Ratio (EF - Efficiency Factor):** Analyse, ob sich dein Puls bei gleicher Wattzahl über die Monate hinweg verbessert hat (Indikator für aerobe Entwicklung).

### 4. Wellness- & Recovery-Korrelation (Stress & Wearable-Integration)

* **Subtile Stressererkennung & HRV-Baseline:** Auswertung schleichender Belastungen (z. B. via Cirqa Band / HRV-Daten). Der Assistent vergleicht tägliche HRV- und Ruhepuls-Werte (RHR) mit deiner persönlichen 7- bis 30-Tage-Baseline, um verdeckten Alltags- oder Trainingsstress vor dem Auftreten von Symptomen zu identifizieren.
* **HRV vs. Workout-Performance:** Verknüpfung von Wellness-Daten (Morgen-HRV, Schlafscore, subjektive Müdigkeit) mit den darauffolgenden Workout-Ergebnissen. *Beispiel-Frage an den Chat:* „Zeige mir meine Intervalle an Tagen, an denen meine HRV unter dem 7-Tage-Schnitt lag – wie stark ist der Leistungseinbruch?“
* **Erholungs-Mismatch & Konsistenz:** Erkennung von unvollständiger Regeneration: Bleibt die HRV trotz eingeplantem Ruhetag niedrig? Das System schlägt ggf. eine erzwungene Pause oder Anpassung der Wochenstruktur vor.

### 5. Power-Profile & Schwachstellen-Analyse

* **Leistungs-Dauer-Kurve:** Automatisiertes Auslesen deiner Peak-Werte (von 5 Sekunden bis zur FTP) direkt aus der API. Der Assistent kann erkennen, in welchen Bereichen (z. B. anaerobe Kapazität vs. lange Ausdauer) sich deine Werte verbessern oder stagnieren.

---

### Wie sieht das in der Praxis aus?

Du tippst künftig einfach im VS Code Chat:

> *„Analysiere meine letzten 4 Wochen: Wie gut habe ich mein Zone-2-Ziel gehalten, zeigt meine HRV vom Cirqa Band Anzeichen von schleichendem Stress und war die letzte Belastungswoche zu hart?“*

Der MCP-Server holt sich im Hintergrund sekundenschnell die Rohdaten von Intervals.icu, filtert sie sauber und liefert dir direkt im Editor eine fundierte, strukturierte Auswertung, die du auf Wunsch direkt in deinem Markdown-Journal (`memo/`) abspeichern kannst.