#!/usr/bin/env python3
"""Translate a day's English report markdown into _src/fa/<ticker>/<date>/."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = [
    "final_trade_decision.md",
    "trader_investment_plan.md",
    "investment_plan.md",
    "market_report.md",
    "news_report.md",
    "sentiment_report.md",
    "fundamentals_report.md",
]

SYSTEM = """You translate financial research markdown from English into formal Persian.
Rules:
- Return only the translated markdown. No preface.
- Keep the markdown structure: headings, lists, tables, bold, code, links, horizontal rules.
- Keep ticker symbols, indicator names, and abbreviations in Latin: BTC-USD, GC=F, MACD, RSI, ATR, EMA, SMA, ETF.
- Do not change any number, date, percentage, or price. You may write digits in Persian.
- Translate these labels exactly, including the bold markers and the colon:
  **Rating**: -> **رتبه**:
  **Recommendation**: -> **توصیه**:
  **Rationale**: -> **استدلال**:
  **Strategic Actions**: -> **اقدام‌های راهبردی**:
  **Executive Summary**: -> **خلاصه اجرایی**:
  **Investment Thesis**: -> **تز سرمایه‌گذاری**:
  **Price Target**: -> **هدف قیمتی**:
  **Time Horizon**: -> **افق زمانی**:
  **Action**: -> **اقدام**:
  **Reasoning**: -> **استدلال**:
  **Entry Price**: -> **قیمت ورود**:
  **Stop Loss**: -> **حد زیان**:
  **Position Sizing**: -> **اندازه موقعیت**:
  **Overall Sentiment:** -> **احساس کلی:**
  **Confidence:** -> **اطمینان:**
  FINAL TRANSACTION PROPOSAL: -> **پیشنهاد نهایی معامله:**
- Use these words: Underweight=کم‌وزن, Overweight=بیش‌وزن, Bearish=نزولی, Bullish=صعودی, Neutral=خنثی, Mixed=مختلط, Sell=فروش, Buy=خرید, Hold=نگهداری.
- Confidence values: Low=پایین, Medium=متوسط, High=بالا.
- not provided = ارائه نشده.
- Match a formal desk-research tone. Do not add facts."""


def translate(client: OpenAI, model: str, text: str) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": text},
        ],
    )
    out = (response.choices[0].message.content or "").strip()
    if out.startswith("```"):
        out = out.split("\n", 1)[1]
        out = out.rsplit("```", 1)[0].strip()
    if not out:
        raise RuntimeError("empty translation")
    return out + "\n"


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: translate_fa.py TICKER YYYY-MM-DD")
    ticker, date = sys.argv[1], sys.argv[2]
    model = os.environ.get("OPENAI_TRANSLATE_MODEL", "gpt-6-luna")
    client = OpenAI()
    source = ROOT / ticker / date / "reports"
    target = ROOT / "_src" / "fa" / ticker / date
    target.mkdir(parents=True, exist_ok=True)
    wrote = 0
    for name in SECTIONS:
        src = source / name
        if not src.exists():
            continue
        dest = target / name
        dest.write_text(translate(client, model, src.read_text(encoding="utf-8")), encoding="utf-8")
        print(dest.relative_to(ROOT))
        wrote += 1
    if wrote == 0:
        raise SystemExit(f"no English markdown in {source}")


if __name__ == "__main__":
    main()
