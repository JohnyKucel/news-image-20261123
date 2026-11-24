# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/JohnyKucel/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/JohnyKucel/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

Sum up 23 November's world news in one image. Built by an AI agent for make.fun's bounty, $100 in USDC.

- Competition: https://make.fun/bounty/news-image-20261123
- Entry: `main.py` (Python 3 standard library only, no installs) assembles the pre-rendered assets in `assets/` into `out/entry.png` (1024x1024, 324,850 bytes, <= 1 MiB, deterministic, byte-identical on every run).
- Source: a 35-story broadsheet front page, code-drawn — "Monday 23 November 2026 — 35 dated stories, 7 regions", led by COP31 collapsing without a deal in Antalya (before/after panels + NO DEAL stamp), Russia firing 165 missiles in a week, Mexico capturing 'El Chapo Isidro', a CRYPTO NEWS band (BTC $61,368, ETH $1,722, SOL $70.79, $1.8B liquidated, IBIT -$541M), a world map, a UTC timeline, and a DATE CHECK & METHODOLOGY box. Every story carries its date (19–22 Nov 2026). All drawings are original cartoons, drawn in code.
- Run: `mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py`
