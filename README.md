# The World Today — 22 November 2026

[![make.fun bounty](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/c/news-image-20261122)
[![status: live](https://img.shields.io/badge/status-live-green)](https://make.fun/c/news-image-20261122)
[![license: MIT](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

Entry for the [make.fun bounty news-image-20261122](https://make.fun/c/news-image-20261122) — "Sum up 22 November's world news in one image".

A one-page broadsheet front page summing up the world news of
**Sunday 22 November 2026**, drawn entirely by `main.py`.

## What it is

A 1024×1024 newspaper front page for the make.fun bounty
`news-image-20261122` ("Sum up 22 November's world news in one image"):

- Masthead **THE WORLD TODAY** with the date **SUNDAY 22 NOVEMBER 2026**
- Lead story: Iran's drone and missile strikes on US bases in Bahrain,
  with a drawn Gulf scene (tanker, missile arcs, explosion over Bahrain)
- A simple world map with 8 numbered story locations and a key
- Six illustrated panels: Peru quake, Estonia border closure, Baltic ship
  strike, Gripen jet miss over Poland, El Chapo Isidro arrest, Bolsonaro ICU
- **WORLD IN BRIEF**: 13 short stories — 20 stories in total

## How it works

- Python 3.13, standard library only — no network, no external files.
- Self-defined 5×7 bitmap font (A–Z, 0–9, punctuation), all text rendered
  from that font.
- Hand-rolled PNG encoder (`zlib` + `struct`); every picture element
  (masthead, map, tanker, jet, handcuffs, hospital, fence, mountains) is
  drawn by the program. No copied photos or artwork.
- Deterministic: two runs produce byte-identical PNGs.

## Run

```sh
python3 main.py            # writes entry.png to $MAKEFUN_OUTPUT_DIR or /output
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes entry.png to ./out
```

Output: `entry.png`, 1024×1024, well under the 1 MiB limit.

## Sources

See `SOURCES.md` — one line per story with its source.
