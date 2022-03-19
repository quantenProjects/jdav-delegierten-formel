# JDAV Delegierten Formel

Repo mit Tools zur Formel, mit der die JDAV ihre Delegiertenanzahl berechnet.

Nach Beschluss des Bundesjugendleitertags 2021.

## Inhalt

* `data`: Eine Beispieldatei mit dem CSV Format für die Tools und das Bild der Formel
* `delegierten-berechnung`: Das Python-Tool, um die Delegiertenanzahl zu berechnen
* `erklaervideo`: Die Manim-Sourcen für das Erklärvideo zur Formel
* `jdav-calc-rust`: Eine weitere Implementierung der Berechnung in Rust
* `tools`: Zwei kleine Tools: Vergleichen von CSV-Dateien und Erzeugen von Zufallsdaten

## Die Formel™ (einfach. niederschwellig. elegant.)

![Screenshot der Formel](data/formel.png)

```tex
d_n = 1 + (D-k) \cdot \left(\frac{1}{2} \frac{\mathrm{JL}_n}{\mathrm{JL}_\mathrm{gesamt}} + \frac{1}{2} \frac{\sqrt{M_n}}{\sum_{i=1}^{k} \sqrt{M_i}}\right)
```

Nach BJO 2021, beschlossen vom digitalen Bundesjugendleitertag der JDAV am 03.10.2021 in München sowie der Hauptversammlung des DAV am 29./30.10.2021 in Friedrichshafen.

