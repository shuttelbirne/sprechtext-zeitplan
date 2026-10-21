#!/usr/bin/env python3
"""Sprechzeit eines lokalen UTF-8-Texts mit expliziten Pausen schätzen."""

import argparse
import json
import math
import re
from pathlib import Path


PAUSE = re.compile(r"\[Pause:\s*(\d+(?:[.,]\d+)?)\s*(s|min)\s*\]", re.I)
REGIE = re.compile(r"\[Regie:[^\]\n]*\]", re.I)
WORDS = re.compile(r"\b\w+(?:[-’']\w+)*\b", re.UNICODE)


def calculate(text, slow_wpm=90, fast_wpm=130):
    """Berechnet eine Spanne; Sprechtempo ist eine Planungsannahme."""
    if not (math.isfinite(slow_wpm) and math.isfinite(fast_wpm)):
        raise ValueError("Das Sprechtempo muss endlich sein.")
    if slow_wpm <= 0 or fast_wpm < slow_wpm:
        raise ValueError("Erforderlich: 0 < langsam <= schnell.")

    # Regie und Markdown-Überschriften sind keine gesprochenen Zeilen.
    spoken = REGIE.sub("", text)
    spoken = re.sub(r"(?m)^\s*#{1,6}\s+.*$", "", spoken)
    pauses = 0.0

    def remove_pause(match):
        nonlocal pauses
        duration = float(match.group(1).replace(",", "."))
        if not math.isfinite(duration):
            raise ValueError("Eine Pause ist zu groß.")
        pauses += duration * (60 if match.group(2).lower() == "min" else 1)
        return " "

    spoken = PAUSE.sub(remove_pause, spoken)
    if re.search(r"\[Pause\b", spoken, re.I):
        raise ValueError("Ungültige Pause. Beispiel: [Pause: 10 s] oder [Pause: 0,5 min].")
    count = len(WORDS.findall(spoken))
    shortest = count / fast_wpm * 60 + pauses
    longest = count / slow_wpm * 60 + pauses
    if not (math.isfinite(shortest) and math.isfinite(longest)):
        raise ValueError("Die berechnete Dauer ist zu groß.")
    return {
        "words": count,
        "pause_seconds": pauses,
        "slow_wpm": slow_wpm,
        "fast_wpm": fast_wpm,
        "shortest_seconds": math.ceil(shortest),
        "longest_seconds": math.ceil(longest),
    }


def duration(seconds):
    return f"{seconds // 60}:{seconds % 60:02d}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="lokale TXT-Datei in UTF-8")
    parser.add_argument("--langsam", type=float, default=90, help="Wörter/Minute, Standard 90")
    parser.add_argument("--schnell", type=float, default=130, help="Wörter/Minute, Standard 130")
    parser.add_argument("--json", action="store_true", help="maschinenlesbare Ausgabe")
    args = parser.parse_args()
    try:
        result = calculate(args.file.read_text(encoding="utf-8-sig"), args.langsam, args.schnell)
    except (OSError, UnicodeError, ValueError) as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Wörter: {result['words']}")
        print(f"Explizite Pausen: {result['pause_seconds']:g} Sekunden")
        print(f"Sprechtempo: {args.langsam:g} bis {args.schnell:g} Wörter/Minute")
        print(f"Geplante Dauer: {duration(result['shortest_seconds'])} bis "
              f"{duration(result['longest_seconds'])} Minuten")


if __name__ == "__main__":
    main()
