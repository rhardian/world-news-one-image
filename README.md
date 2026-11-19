# world-news-one-image

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/rhardian/world-news-one-image/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/rhardian/world-news-one-image/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

One image that sums up the world's news of **Wednesday 18 November 2026**,
entered in make.fun's `news-image-20261118` bounty
(https://make.fun/bounty/news-image-20261118).

The entry is a broadsheet-style front page, "The World in One Day", dated
18 November 2026. It leads with Xi greeting Trump on the tarmac as APEC opens
in Shenzhen, then six feature stories: Iran's drone strikes on Gulf bases,
the EU's €45bn Ukraine loan proposal, Voyager 1 reaching one light-day from
Earth, the Dow's 561-point fall after hawkish Fed minutes, the WHO superbug
warning, and the COP31 draft split. A numbers strip, a UTC timeline and seven
region boxes carry 54 stories in total, each happened or first reported on
18 November 2026. A red DATE CHECK band lists what was deliberately left out
(Tuesday's Nvidia results, the Peltola race call, the Kerch bridge strike,
the Knesset speaker vote) and what had not happened yet (Thursday's
trilateral talks, Anthropic's first trade and GTA VI's US release; Friday's
Akvan landfall and COP31 close). One-party claims are attributed.

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

Headlines follow the reporting of 18 November 2026 from Reuters, AFP, AP,
Al Jazeera, Euronews, UN News, NASA/JPL, ONS, ECB, RNZ, PACNEWS, allAfrica,
Times of Israel, Kyiv Independent, CNBC, ESPN, Politico and NPR.
