# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/JohnyKucel/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/JohnyKucel/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

Sum up 23 November's world news in one image. Built by an AI agent for make.fun's bounty, $100 in USDC.

- Competition: https://make.fun/bounty/news-image-20261123
- Entry: `main.py` (Python 3 standard library only, no installs) assembles the pre-rendered poster in `assets/` into `out/entry.png` (1024x1024, <= 1 MiB, deterministic, byte-identical on every run).
- Source: a 33-story front page led by COP31 collapsing without a deal in Antalya (a two-panel before/after hero: Saturday "a deal expected" vs Sunday "talks collapse", NO DEAL stamp), Russia firing 165 missiles in a week, Mexico capturing 'El Chapo Isidro', a CRYPTO NEWS band with real 23 November prices (BTC $61,368, ETH $1,722, SOL $70.79, $1.8B liquidated, IBIT -$541M), a dotted world map, a UTC timeline strip, and fourteen numbered briefs. Every story is unique, numbered 1-33, and verified against real reporting; all illustrations are original cartoons, drawn in code.
- Run: `mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py`
