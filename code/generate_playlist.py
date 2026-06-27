"""
generate_playlist.py

Reads sentences.json and generates playlist.json for the Norwegian island player.
Each card produces two entries (recall + shadow) with ordered segments:
  { text, audio, lang, role }

Recall sequence per card:
  EN question → [NO question →] EN sent 1 → NO sent 1 → EN sent 2 → NO sent 2 → ...

Shadow sequence per card:
  [NO question →] NO sent 1 → NO sent 2 → ...

Cards without a Norwegian question (q_no == "") omit the NO question segment.

Audio paths are relative to the player/ directory (one level up from code/).

Usage:
  python3 generate_playlist.py
"""

import json
import os
import re

INPUT_FILE  = "sentences.json"
OUTPUT_FILE = "../playlist.json"
TMP_DIR     = "code/audio/segments"   # relative to player/ (where player is served from)


def split_sentences(text):
    parts = re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÚÜÑA-ZÆØÅ])', text)
    return [p.strip() for p in parts if p.strip()]


def seg(text, audio, lang, role):
    return {"text": text, "audio": audio, "lang": lang, "role": role}


def tmp(filename):
    return f"{TMP_DIR}/{filename}"


def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        cards = json.load(f)

    playlist = []

    for card in cards:
        num = card["island_num"]
        slug = card["island_slug"]
        ctype = card["card_type"]
        cnum = card["card_num"]
        stem = f"island-{num:02d}-{slug}-{ctype}-{cnum}"

        has_no_q = bool(card.get("q_no", "").strip())
        en_sents = split_sentences(card["a_en"])
        no_sents = split_sentences(card["a_no"])

        label = f"{ctype.title()} {cnum}"
        island_name = slug.replace("-", " ").title()

        # ── Recall ──────────────────────────────────────────────────────────
        recall_segs = [
            seg(card["q_en"], tmp(f"{stem}-q-en.mp3"), "en", "question"),
        ]
        if has_no_q:
            recall_segs.append(seg(card["q_no"], tmp(f"{stem}-q-no.mp3"), "no", "question"))
        for i, (en_s, no_s) in enumerate(zip(en_sents, no_sents), 1):
            recall_segs.append(seg(en_s, tmp(f"{stem}-a-en-s{i:02d}.mp3"), "en", "answer"))
            recall_segs.append(seg(no_s, tmp(f"{stem}-a-no-s{i:02d}.mp3"), "no", "answer"))

        playlist.append({
            "island": island_name,
            "card": label,
            "mode": "recall",
            "stem": stem,
            "segments": recall_segs,
        })

        # ── Shadow ──────────────────────────────────────────────────────────
        shadow_segs = []
        if has_no_q:
            shadow_segs.append(seg(card["q_no"], tmp(f"{stem}-q-no.mp3"), "no", "question"))
        for i, no_s in enumerate(no_sents, 1):
            shadow_segs.append(seg(no_s, tmp(f"{stem}-a-no-s{i:02d}.mp3"), "no", "answer"))

        playlist.append({
            "island": island_name,
            "card": label,
            "mode": "shadow",
            "stem": stem,
            "segments": shadow_segs,
        })

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(playlist, f, ensure_ascii=False, indent=2)

    card_count = len(cards)
    print(f"Written {len(playlist)} entries ({card_count} cards × 2 modes) to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
