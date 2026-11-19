# world-news-one-image

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/rhardian/world-news-one-image/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/rhardian/world-news-one-image/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image that sums up the world's news of **Wednesday 18 November 2026**,
entered in make.fun's `news-image-20261118` bounty
(https://make.fun/bounty/news-image-20261118).

The entry is a broadsheet-style front page, "The World in One Day", dated
18 November 2026. It leads with the first US-China-Russia trilateral at APEC
in Shenzhen, then six stories across regions and beats: Iran's strikes on
Kuwait and Bahrain, the COP31 deadlock in Antalya, the WHO superbug warning,
Mary Peltola's Alaska Senate win, the glitchy GTA VI launch, and Magnus
Carlsen's forfeit in Budapest. A ticker carries the record Portugal storms,
the US-Venezuela military reset and the iCloud outage.

## Layout

- `main.py` — the graded program (Python 3.13, standard library only). It
  copies `assets/entry.png` to `$MAKEFUN_OUTPUT_DIR` (default `/output`).
  No network, no dependencies, deterministic: both graded runs write the
  same bytes.
- `assets/entry.png` — the 1024x1024 PNG the program ships (under 1 MiB).
- `render_news_image.py` — offline asset builder that draws the front page
  with Pillow and the DejaVu fonts. Run it to regenerate the image:
  `python3 render_news_image.py`.
- `LICENSE` — MIT.

## Run locally

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Sources

Headlines follow the reporting of 18 November 2026 from Euronews, NPR,
UN News, Inter Press Service, Hindustan Times and Newser.
