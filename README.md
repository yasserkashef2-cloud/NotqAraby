# صوتي عربي — interactive virtual book

A static, offline-capable interactive edition of the course materials «صوتي عربي: فصحى – عامية – دارجة». Open `index.html` in a browser (a web server or GitHub Pages is needed for YouTube playback).

## Contents of the folder

- `index.html` — the page shell
- `assets/` — css, js (app + generated `data.js`), fonts, images extracted from the Word file, audio/video
- `_generator/` — everything needed to rebuild (Python 3, `lxml`, `markdown`)
- `SOURCES_REPORT.md`, `QA_SUMMARY.md` — reports

## Rebuild

```
python3 -I _generator/parse_docx.py   # Word file -> data/source.json
python3 -I _generator/build.py        # pages -> assets/js/data.js, reports
python3 -I _generator/verify.py       # source-fidelity check
```

## Publishing on GitHub Pages

Put the folder contents at the repository root (public repository on the free plan), then Settings → Pages → deploy from the `main` branch root. Check the TS Hiba licence first (see `SOURCES_REPORT.md` §6).

## Editing

- Questions and prompts: `_generator/edu_items.py`; unit-level pages: `edu_units.py`; word glosses: `data/glosses.txt`; text glossaries: `edu_gloss.py`.
- Source-error flags: `data_flags.py` (the Word text is never edited).
- Withheld texts and the private-text slot: `SOURCES_REPORT.md` §4.
