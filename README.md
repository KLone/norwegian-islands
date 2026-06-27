# Norwegian Islands Player

A PWA for drilling and shadowing Norwegian language islands — sentence sets sourced from Kirk's daughter, organized by topic.

**Player URL:** *(set this after pushing to GitHub Pages)*

---

## Using on iPhone

1. Open the URL above in Safari
2. Tap the Share button → **Add to Home Screen**
3. On first open (with WiFi), all audio is downloaded and cached
4. After that, the app works fully offline

---

## Modes

- **Recall** — English prompt → pause → Norwegian question (if present) → English answer → pause → Norwegian answer. Use this while actively drilling.
- **Shadow** — Norwegian only (question + answer). Use once an island is memorized, for fluency maintenance.

---

## Running locally

Serve from the `player/` directory:

```bash
cd language-learning/norwegian/player
python3 -m http.server 8766
```

Then open `http://localhost:8766/player.html` in a browser.
On iPhone over WiFi, use your Mac's local IP instead of `localhost`.

---

## Adding a new island

1. Add cards to `code/sentences.json` following the existing format:

```json
{
  "island_num": 2,
  "island_slug": "family",
  "card_type": "core",
  "card_num": 1,
  "q_en": "English prompt or question",
  "q_no": "Norsk spørsmål (or empty string if no clean question)",
  "a_en": "English answer",
  "a_no": "Norsk svar"
}
```

2. Run from `code/`:

```bash
cd code
python3 generate_audio.py --all
python3 generate_playlist.py
python3 generate_text.py
```

3. Push to GitHub:

```bash
cd ..
git add .
git commit -m "Add [island name] island"
git push
```

4. Open the player on your phone with WiFi — new content syncs automatically.

---

## Directory structure

```
player/
  player.html          # PWA player
  playlist.json        # Generated — all cards and audio paths
  manifest.json        # PWA manifest
  sw.js                # Service worker (offline caching)
  icon.svg             # Home screen icon (Norwegian flag)
  README.md
  code/
    sentences.json     # Source content — edit this to add islands
    generate_audio.py  # Generates MP3 segments (Google Cloud TTS nb-NO)
    generate_playlist.py  # Generates playlist.json for the player
    generate_text.py   # Generates plain text reference file
    audio/
      segments/        # Individual TTS segments
  islands/
    daily-exchanges/
      audio/           # recall + shadow MP3s per card
      text/            # Plain text reference
```

---

## Islands

| # | Island | Source | Status |
|---|--------|--------|--------|
| 1 | Daily Exchanges | Daughter batch 1 | ☐ Audio pending |

---

## Audio voice

- Norwegian: `nb-NO-Neural2-F` (Google Cloud TTS)
- English: `en-US-Neural2-C`
- API key stored in Apple Keychain as `google_tts_api_key`
