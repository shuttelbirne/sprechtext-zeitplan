# Sprechtext-Zeitplan

Ein kleines Python-Werkzeug für die Vorbereitung von Vorlesetexten. Es zählt Wörter, addiert ausdrücklich markierte Pausen und berechnet eine Zeitspanne aus zwei frei wählbaren Sprechgeschwindigkeiten.

Das Werkzeug läuft lokal. Es verwendet nur die Python-Standardbibliothek und enthält keine Netzwerkaufrufe, Konten oder KI-Anbindung. Es verändert die eingegebene Datei nicht.

## Starten

Voraussetzung: Python 3.8 oder neuer. Den Text als UTF-8-TXT-Datei speichern; PDF und DOCX werden nicht direkt eingelesen.

```sh
python3 sprechzeit.py beispiel.txt
python3 sprechzeit.py mein-text.txt --langsam 80 --schnell 110
python3 sprechzeit.py mein-text.txt --json
```

Die Standardwerte 90 und 130 Wörter pro Minute sind veränderbare Planungsannahmen. Sie sind keine gemessenen Werte für eine bestimmte Person oder Textart. Lies einen Abschnitt laut mit der Stoppuhr und passe die Werte an deine Sprechweise an.

## Pausen und Regie

```text
# Überschrift, wird nicht gesprochen
[Regie: leise lesen]
Dieser Satz wird mitgezählt.
[Pause: 10 s]
Dieser Satz ebenfalls.
[Pause: 0,5 min]
```

Unterstützt werden Sekunden (`s`) und Minuten (`min`), Dezimalpunkt und Dezimalkomma. Eine unvollständige oder unbekannte Pausenmarkierung führt zu einer Fehlermeldung. Einzeilige Regiehinweise im Format `[Regie: ...]` und Markdown-Überschriften werden nicht mitgezählt. Andere Anmerkungen zählen als Text; entferne sie vorher aus deiner Arbeitskopie.

Die Rechnung lautet: Wortzahl geteilt durch Wörter pro Minute, mal 60, plus Pausen. Die Ausgabe wird auf ganze Sekunden aufgerundet. Zahlen, Abkürzungen und zusammengesetzte Wörter können beim tatsächlichen Sprechen mehr Zeit benötigen, als die reine Wortzählung erfasst.

Der Rechner prüft weder Inhalt noch Eignung eines Textes. Er ersetzt das tatsächliche Probelesen nicht.

Die [Rechenhilfe mit Beispiel und ausfüllbarem Arbeitsblatt](https://telegra.ph/Wie-lange-dauert-ein-Sprechtext-Eine-Rechenhilfe-mit-Pausen-10-21) erklärt die Planung auch ohne Python: Wortzahl, eigenes Sprechtempo und feste Pausen werden getrennt berechnet.

## Projektbezug

Das Werkzeug ergänzt die Arbeit mit deutschsprachigen Sprechvorlagen von [RauschSkripte](https://rauschskripte.de/), einem Angebot von Rauschwerk Verlag. Dort gibt es Hypnose-Sprechtexte als PDF und DOCX für Erwachsene; der Katalog umfasst auch erotische und BDSM-bezogene Themen.

Für die Vorbereitung eines solchen Textes gibt es außerdem den frei zugänglichen Ratgeber [Absprachen und Einwilligung bei Hypnose-Skripten](https://rauschskripte.de/wissen/hypnose-skript-einwilligung/). Die Skriptdateien und ihre Nutzungsrechte sind kein Bestandteil dieses Repositorys.

## Prüfen

```sh
python3 -m unittest -v
```

Die Prüfungen decken bekannte Zeitwerte, Pausen, Regie, Unicode-Wörter und fehlerhafte Eingaben ab.
