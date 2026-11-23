# -*- coding: utf-8 -*-
"""Build bilingual HTML desk reports from the daily markdown files."""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "_src"

SECTIONS = [
    ("final_trade_decision.md", "final", "Final decision", "تصمیم نهایی"),
    ("trader_investment_plan.md", "trader", "Trader plan", "طرح معامله‌گر"),
    ("investment_plan.md", "plan", "Investment plan", "طرح سرمایه‌گذاری"),
    ("market_report.md", "market", "Market", "بازار و تکنیکال"),
    ("news_report.md", "news", "News and macro", "اخبار و کلان"),
    ("sentiment_report.md", "sentiment", "Sentiment", "احساس بازار"),
    ("fundamentals_report.md", "fundamentals", "Fundamentals", "بنیادی"),
]

ASSETS = {
    "GC=F": {
        "en": "Gold futures",
        "fa": "قرارداد آتی طلا",
        "contract_en": "Gold Dec 26, COMEX",
        "contract_fa": "طلای دسامبر ۲۰۲۶، COMEX",
        "kind": "gold",
    },
    "BTC-USD": {
        "en": "Bitcoin",
        "fa": "بیت‌کوین",
        "contract_en": "BTC-USD spot",
        "contract_fa": "بیت‌کوین به دلار",
        "kind": "btc",
    },
}

MONTHS_FA = [
    "",
    "فروردین",
    "اردیبهشت",
    "خرداد",
    "تیر",
    "مرداد",
    "شهریور",
    "مهر",
    "آبان",
    "آذر",
    "دی",
    "بهمن",
    "اسفند",
]
MONTHS_EN = [
    "",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]
WEEKDAYS_EN = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
WEEKDAYS_FA = ["دوشنبه", "سه‌شنبه", "چهارشنبه", "پنجشنبه", "جمعه", "شنبه", "یکشنبه"]

FA_LABELS = [
    ("**Overall Sentiment:**", "**احساس کلی:**"),
    ("**Confidence:**", "**اطمینان:**"),
    ("**Rating**:", "**رتبه:**"),
    ("**Recommendation**:", "**توصیه:**"),
    ("**Rationale**:", "**استدلال:**"),
    ("**Strategic Actions**:", "**اقدام‌های راهبردی:**"),
    ("**Executive Summary**:", "**خلاصه اجرایی:**"),
    ("**Investment Thesis**:", "**تز سرمایه‌گذاری:**"),
    ("**Price Target**:", "**هدف قیمتی:**"),
    ("**Time Horizon**:", "**افق زمانی:**"),
    ("**Action**:", "**اقدام:**"),
    ("**Reasoning**:", "**استدلال:**"),
    ("**Entry Price**:", "**قیمت ورود:**"),
    ("**Stop Loss**:", "**حد زیان:**"),
    ("**Position Sizing**:", "**اندازه موقعیت:**"),
    ("FINAL TRANSACTION PROPOSAL:", "**پیشنهاد نهایی معامله:**"),
    ("not provided", "ارائه نشده"),
    ("(Score:", "(امتیاز:"),
    ("**Mixed**", "**مختلط**"),
    ("**Bearish**", "**نزولی**"),
    ("**Bullish**", "**صعودی**"),
    ("**Neutral**", "**خنثی**"),
    ("**Underweight**", "**کم‌وزن**"),
    ("**Overweight**", "**بیش‌وزن**"),
    ("**SELL**", "**فروش**"),
    ("NO TRADE — wait for current price and weekly market data",
     "بدون معامله — تا رسیدن قیمت جاری و دادهٔ هفتگی بازار صبر شود"),
    ("Avoid fresh longs; consider shorts only after confirmation, with ATR-adjusted risk.",
     "از خرید تازه پرهیز شود؛ فروش فقط پس از تأیید و با ریسک متناسب با ATR بررسی شود."),
    ("Avoid chasing GC=F after the sharp weekly drop; maintain a cautious, tactically bearish bias and wait for price confirmation before entering or adding to a short position.",
     "پس از افت شدید هفتگی، قیمت را تعقیب نکنید؛ سوگیری را محتاط و متمایل به نزول نگه دارید و پیش از ورود یا افزودن به موقعیت فروش، منتظر تأیید قیمت بمانید."),
]


def gregorian_to_jalali(gy: int, gm: int, gd: int) -> tuple[int, int, int]:
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if gy > 1600:
        jy = 979
        gy -= 1600
    else:
        jy = 0
        gy -= 621
    gy2 = gy + 1 if gm > 2 else gy
    days = (
        365 * gy
        + (gy2 + 3) // 4
        - (gy2 + 99) // 100
        + (gy2 + 399) // 400
        - 80
        + gd
        + g_d_m[gm - 1]
    )
    jy += 33 * (days // 12053)
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if days > 365:
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if days < 186:
        jm = 1 + days // 31
        jd = 1 + (days % 31)
    else:
        jm = 7 + (days - 186) // 30
        jd = 1 + ((days - 186) % 30)
    return jy, jm, jd


def persian_ratio(text: str) -> float:
    letters = [ch for ch in text if ch.isalpha()]
    if not letters:
        return 0.0
    fa = sum(1 for ch in letters if "\u0600" <= ch <= "\u06FF")
    return fa / len(letters)


def inline(text: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", escaped)
    escaped = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<a href="\2">\1</a>',
        escaped,
    )
    return escaped


def render_math(lines: list[str]) -> str:
    text = " ".join(part.strip() for part in lines if part.strip())
    text = re.sub(r"\\text\{([^}]*)\}", r"\1", text)
    text = text.replace("\\", "")
    return f'<p class="formula">{inline(text)}</p>'


def split_row(row: str) -> list[str]:
    row = row.strip()
    if row.startswith("|"):
        row = row[1:]
    if row.endswith("|"):
        row = row[:-1]
    return [cell.strip() for cell in row.split("|")]


def is_separator(cells: list[str]) -> bool:
    if not cells:
        return False
    return all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells)


def alignment(cell: str) -> str:
    cell = cell.replace(" ", "")
    if cell.startswith(":") and cell.endswith(":"):
        return "center"
    if cell.endswith(":"):
        return "end"
    return "start"


def render_table(rows: list[str]) -> str:
    parsed = [split_row(row) for row in rows]
    aligns: list[str] = []
    body_start = 0
    header: list[str] | None = None
    if len(parsed) >= 2 and is_separator(parsed[1]):
        header = parsed[0]
        aligns = [alignment(cell) for cell in parsed[1]]
        body_start = 2
    elif parsed and is_separator(parsed[0]):
        body_start = 1
    width = max(len(row) for row in parsed)
    if aligns:
        aligns = (aligns + ["start"] * width)[:width]

    def cells(row: list[str], tag: str) -> str:
        padded = row + [""] * (width - len(row))
        parts = []
        for index, value in enumerate(padded):
            align = aligns[index] if aligns else "start"
            parts.append(f'<{tag} style="text-align:{align}">{inline(value)}</{tag}>')
        return "<tr>" + "".join(parts) + "</tr>"

    chunks = ['<div class="table-wrap"><table>']
    if header is not None:
        chunks.append("<thead>" + cells(header, "th") + "</thead>")
    body_rows = parsed[body_start:]
    if body_rows:
        chunks.append("<tbody>" + "".join(cells(row, "td") for row in body_rows) + "</tbody>")
    chunks.append("</table></div>")
    return "".join(chunks)


def md_to_html(src: str) -> str:
    lines = src.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out: list[str] = []
    para: list[str] = []
    i = 0
    n = len(lines)

    def flush() -> None:
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    while i < n:
        stripped = lines[i].strip()
        if not stripped:
            flush()
            i += 1
            continue
        if stripped in {"---", "***", "___"}:
            flush()
            out.append("<hr>")
            i += 1
            continue
        if stripped.startswith("\\["):
            flush()
            math_lines: list[str] = []
            rest = stripped[2:].strip()
            if rest.endswith("\\]"):
                math_lines.append(rest[:-2].strip())
                i += 1
                out.append(render_math(math_lines))
                continue
            if rest:
                math_lines.append(rest)
            i += 1
            while i < n:
                piece = lines[i].strip()
                if piece == "\\]":
                    i += 1
                    break
                if piece.endswith("\\]"):
                    math_lines.append(piece[:-2].strip())
                    i += 1
                    break
                math_lines.append(piece)
                i += 1
            out.append(render_math(math_lines))
            continue
        if stripped.startswith("#"):
            flush()
            level = len(stripped) - len(stripped.lstrip("#"))
            level = min(max(level, 1), 6)
            text = stripped[level:].strip()
            tag = "h3" if level <= 2 else "h4"
            out.append(f"<{tag}>{inline(text)}</{tag}>")
            i += 1
            continue
        if stripped.startswith(">"):
            flush()
            quote: list[str] = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append("<blockquote><p>" + inline(" ".join(quote)) + "</p></blockquote>")
            continue
        if stripped.startswith("|"):
            flush()
            rows: list[str] = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            out.append(render_table(rows))
            continue
        if re.match(r"^(?:[-*]|\d+\.)\s+", stripped):
            flush()
            ordered = bool(re.match(r"^\d+\.\s+", stripped))
            items: list[str] = []
            while i < n:
                match = re.match(r"^(?:[-*]|\d+\.)\s+(.*)$", lines[i].strip())
                if not match:
                    break
                items.append(match.group(1))
                i += 1
            tag = "ol" if ordered else "ul"
            lis = "".join(f"<li>{inline(item)}</li>" for item in items)
            out.append(f"<{tag}>{lis}</{tag}>")
            continue
        para.append(stripped)
        i += 1
    flush()
    return "\n".join(out)


def localize_fa(text: str) -> str:
    text = text.replace("**Confidence:** Low", "**اطمینان:** پایین")
    text = text.replace("**Confidence:** High", "**اطمینان:** بالا")
    text = text.replace("**Confidence:** Medium", "**اطمینان:** متوسط")
    for src, dst in FA_LABELS:
        text = text.replace(src, dst)
    for src, dst in (
        ("Underweight", "کم‌وزن"),
        ("Overweight", "بیش‌وزن"),
        ("Bearish", "نزولی"),
        ("Bullish", "صعودی"),
        ("Neutral", "خنثی"),
        ("Mixed", "مختلط"),
        ("Sell", "فروش"),
        ("Hold", "نگهداری"),
    ):
        text = re.sub(rf"\b{src}\b", dst, text)
    return text


def load_section(asset: str, date: str, filename: str, lang: str) -> str | None:
    override = SRC / lang / asset / date / filename
    original = ROOT / asset / date / "reports" / filename
    if lang == "fa" and override.exists():
        return override.read_text(encoding="utf-8")
    if lang == "en" and override.exists():
        return override.read_text(encoding="utf-8")
    if not original.exists():
        return None
    text = original.read_text(encoding="utf-8")
    ratio = persian_ratio(text)
    if lang == "fa":
        if ratio < 0.25 and not override.exists():
            raise FileNotFoundError(f"Missing Persian source: {override}")
        return localize_fa(text)
    if ratio > 0.25 and not override.exists():
        raise FileNotFoundError(f"Missing English source: {override}")
    return text


def first_match(text: str, pattern: str) -> str:
    match = re.search(pattern, text)
    return re.sub(r"\*\*", "", match.group(1)).strip() if match else ""


def badge_class(label: str) -> str:
    key = label.lower()
    if any(word in key for word in ("sell", "bear", "under", "فروش", "نزول", "کم‌وزن", "کم وزن")):
        return "warn"
    if any(word in key for word in ("buy", "bull", "over", "صعود", "خرید")):
        return "good"
    if any(word in key for word in ("mixed", "neutral", "مختلط", "خنثی")):
        return "mixed"
    return "neutral"


RATING_FA = {
    "Underweight": "کم‌وزن",
    "Sell": "فروش",
    "Bearish": "نزولی",
    "Bullish": "صعودی",
    "Mixed": "مختلط",
    "Neutral": "خنثی",
    "Buy": "خرید",
    "Overweight": "بیش‌وزن",
    "Hold": "نگهداری",
}
RATING_EN = {value: key for key, value in RATING_FA.items()}


def display_badge(label: str, lang: str) -> str:
    match = re.match(r"^(\D+?)(?:\s+(.+))?$", label.strip())
    core = match.group(1).strip() if match else label.strip()
    score = (match.group(2) or "") if match else ""
    if lang == "fa":
        fa = RATING_FA.get(core, core)
        en = core if core in RATING_FA else RATING_EN.get(core, "")
        text = f"{fa} · {en}" if en and en != fa else fa
    else:
        en = RATING_EN.get(core, core)
        fa = RATING_FA.get(en, "")
        text = f"{en} · {fa}" if fa and fa != en else en
    if score:
        text = f"{text} {score}"
    return text


def fa_digits(value: str) -> str:
    return str(value).translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))


def format_dates(date: str) -> dict[str, str]:
    year, month, day = (int(part) for part in date.split("-"))
    from datetime import date as date_cls

    weekday = date_cls(year, month, day).weekday()
    jy, jm, jd = gregorian_to_jalali(year, month, day)
    return {
        "iso": date,
        "en": f"{WEEKDAYS_EN[weekday]}, {day} {MONTHS_EN[month]} {year}",
        "fa": f"{WEEKDAYS_FA[weekday]} {day} {MONTHS_EN[month]} {year}",
        "jalali": f"{WEEKDAYS_FA[weekday]} {fa_digits(jd)} {MONTHS_FA[jm]} {fa_digits(jy)}",
    }


CSS = r"""
:root {
  --paper: #f4f0e6;
  --card: #fffdf8;
  --ink: #1c1915;
  --muted: #6d655c;
  --line: #e3d9c8;
  --accent: #8d5a16;
  --accent-soft: #f3e4cc;
  --warn: #8d2f24;
  --warn-soft: #f8e4df;
  --good: #1d6b45;
  --good-soft: #e3f2e9;
  --mixed: #3e5c4e;
  --mixed-soft: #e4eee8;
  --shadow: 0 16px 40px rgba(58, 42, 18, 0.06);
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  color: var(--ink);
  background:
    radial-gradient(1200px 400px at 100% -10%, rgba(141, 90, 22, 0.08), transparent 50%),
    var(--paper);
  font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
  font-size: 16.5px;
  line-height: 1.65;
}
body.lang-fa {
  font-family: Vazirmatn, "Segoe UI", Tahoma, sans-serif;
  font-size: 17px;
  line-height: 1.95;
}
body.kind-btc {
  --accent: #c2410c;
  --accent-soft: #fde6d8;
  background:
    radial-gradient(1200px 400px at 100% -10%, rgba(194, 65, 12, 0.08), transparent 50%),
    var(--paper);
}
a { color: var(--accent); }
.wrap { width: min(920px, calc(100% - 32px)); margin: 0 auto; }
.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 18px 0 8px;
}
.brand {
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--muted);
  font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
}
.lang { display: flex; gap: 6px; }
.lang a {
  text-decoration: none;
  color: var(--ink);
  border: 1px solid var(--line);
  background: transparent;
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 13px;
}
.lang a.on { background: var(--ink); color: #fffdf8; border-color: var(--ink); }
.hero { padding: 12px 0 8px; }
.kicker {
  margin: 0 0 8px;
  color: var(--accent);
  font-weight: 600;
  font-size: 14px;
}
h1 {
  font-family: "Source Serif 4", Georgia, serif;
  font-weight: 650;
  font-size: clamp(34px, 5vw, 52px);
  line-height: 1.15;
  margin: 0;
  letter-spacing: -0.03em;
}
body.lang-fa h1, body.lang-fa h2, body.lang-fa h3, body.lang-fa h4 {
  font-family: Vazirmatn, Tahoma, sans-serif;
  letter-spacing: 0;
}
.sub { margin: 8px 0 0; color: var(--muted); }
.badges { display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0 4px; }
.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 14px;
  font-weight: 600;
  background: var(--accent-soft);
  color: var(--accent);
}
.badge.warn { background: var(--warn-soft); color: var(--warn); }
.badge.good { background: var(--good-soft); color: var(--good); }
.badge.mixed { background: var(--mixed-soft); color: var(--mixed); }
.badge.neutral { background: #eeeae3; color: #4d463f; }
.badge small { font-weight: 500; opacity: 0.8; }
.toc {
  position: sticky;
  top: 0;
  z-index: 4;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 12px 0;
  background: color-mix(in srgb, var(--paper) 92%, transparent);
  backdrop-filter: blur(8px);
}
.section { scroll-margin-top: 72px; }
.toc a {
  flex: 0 0 auto;
  text-decoration: none;
  color: var(--ink);
  border: 1px solid var(--line);
  background: var(--card);
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 13px;
}
.section {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 18px;
  box-shadow: var(--shadow);
  padding: 22px 22px 8px;
  margin: 0 0 16px;
}
.section h2 { margin: 0 0 8px; font-size: 28px; line-height: 1.3; }
.section h3 { margin: 1.3em 0 0.4em; font-size: 22px; line-height: 1.35; }
.section h4 { margin: 1.1em 0 0.3em; font-size: 18px; }
.section p { margin: 0.7em 0; }
.section ul, .section ol { margin: 0.6em 0 0.8em; padding-inline-start: 1.3em; }
.section li { margin: 0.28em 0; }
.section hr { border: 0; border-top: 1px solid var(--line); margin: 1.2em 0; }
blockquote {
  margin: 1em 0;
  padding: 10px 14px;
  border-inline-start: 3px solid var(--accent);
  background: var(--accent-soft);
  border-radius: 0 12px 12px 0;
}
body.lang-fa blockquote { border-radius: 12px 0 0 12px; }
code {
  font-family: "IBM Plex Mono", Consolas, monospace;
  font-size: 0.86em;
  background: #f3ecdf;
  padding: 0.05em 0.35em;
  border-radius: 5px;
}
.formula {
  font-family: "IBM Plex Sans", "Segoe UI", sans-serif;
  text-align: center;
  background: #f7f3ea;
  border-radius: 10px;
  padding: 10px 12px;
}
.table-wrap { overflow-x: auto; margin: 0.8em 0 1em; }
table { width: 100%; border-collapse: collapse; font-size: 14.5px; line-height: 1.55; }
th, td { border-bottom: 1px solid var(--line); padding: 8px 10px; vertical-align: top; }
th { font-size: 12.5px; color: var(--muted); font-weight: 650; }
footer {
  color: var(--muted);
  font-size: 13px;
  padding: 8px 0 36px;
}
@media print {
  body { background: white; }
  .toc, .lang { display: none; }
  .section { box-shadow: none; break-inside: avoid; }
}
"""


def page_html(asset: str, date: str, lang: str, sections: list[dict], meta: dict) -> str:
    info = ASSETS[asset]
    dates = format_dates(date)
    fa = lang == "fa"
    title_asset = info["fa"] if fa else info["en"]
    title = f"{title_asset} — {dates['jalali'] if fa else dates['en']}"
    doc_title = f"{asset} · {title}"
    kicker = f"{asset} · {info['contract_fa'] if fa else info['contract_en']}"
    sub = dates["jalali"] + " · " + dates["en"] if fa else dates["en"]
    if fa:
        note = "بازنویسی فارسی گزارش همان روز. اعداد، نمادها و سطوح قیمتی از متن اصلی حفظ شده‌اند."
    else:
        note = "Desk rendering of the daily research notes. Figures and levels follow the source reports."
    origin = meta.get("origin_note", "")
    badges = []
    for item in meta.get("badges", []):
        shown = display_badge(item["label"], lang)
        badges.append(
            f'<span class="badge {badge_class(item["label"])}">{html.escape(shown)}'
            f' <small>{html.escape(item["caption"])}</small></span>'
        )
    toc = "".join(
        f'<a href="#{section["id"]}">{html.escape(section["nav"])}</a>' for section in sections
    )
    body = []
    for section in sections:
        body.append(
            f'<section class="section" id="{section["id"]}">'
            f'<h2>{html.escape(section["nav"])}</h2>'
            f'{section["html"]}</section>'
        )
    other_href = "report.html" if fa else "report-fa.html"
    self_href = "report-fa.html" if fa else "report.html"
    en_class = "" if fa else "on"
    fa_class = "on" if fa else ""
    origin_html = f"<p>{html.escape(origin)}</p>" if origin else ""
    return f"""<!DOCTYPE html>
<html lang="{"fa" if fa else "en"}" dir="{"rtl" if fa else "ltr"}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(doc_title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&family=Vazirmatn:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
{CSS}
</style>
</head>
<body class="lang-{lang} kind-{info["kind"]}">
<div class="wrap">
  <div class="topbar">
    <div class="brand">Trade Desk</div>
    <nav class="lang">
      <a class="{en_class}" href="{other_href if fa else self_href}">English</a>
      <a class="{fa_class}" href="{self_href if fa else other_href}">فارسی</a>
    </nav>
  </div>
  <header class="hero">
    <p class="kicker">{html.escape(kicker)}</p>
    <h1>{html.escape(title_asset)}</h1>
    <p class="sub">{html.escape(sub)}</p>
    <div class="badges">{''.join(badges)}</div>
  </header>
  <nav class="toc">{toc}</nav>
  {''.join(body)}
  <footer>
    <p>{html.escape(note)}</p>
    {origin_html}
  </footer>
</div>
</body>
</html>
"""


def collect_badges(joined: str, lang: str) -> list[dict]:
    badges = []
    rating = first_match(joined, r"\*\*(?:Rating|رتبه)\*\*:\s*(.+)")
    recommendation = first_match(joined, r"\*\*(?:Recommendation|توصیه)\*\*:\s*(.+)")
    action = first_match(joined, r"\*\*(?:Action|اقدام)\*\*:\s*(.+)")
    sentiment = first_match(joined, r"\*\*(?:Overall Sentiment|احساس کلی):\*\*\s*\*\*(.+?)\*\*")
    if not sentiment:
        sentiment = first_match(joined, r"\*\*(?:Overall Sentiment|احساس کلی):\*\*\s*(.+)")
    score = first_match(joined, r"(?:Score|امتیاز):\s*([0-9۰-۹]+(?:[./٫][0-9۰-۹]+)?)")
    caption_rating = "رتبه" if lang == "fa" else "Rating"
    caption_action = "اقدام معامله‌گر" if lang == "fa" else "Trader action"
    caption_sent = "احساس" if lang == "fa" else "Sentiment"
    primary = rating or recommendation
    if primary:
        badges.append({"label": primary.split("(")[0].strip(" ."), "caption": caption_rating})
    if action:
        badges.append({"label": action.split("(")[0].strip(" ."), "caption": caption_action})
    if sentiment:
        label = sentiment.split("(")[0].strip(" .")
        if score:
            if lang == "fa":
                pretty = fa_digits(score.replace("٫", ".").split("/")[0]).replace(".", "٫")
                label = f"{label} {pretty} از ۱۰"
            else:
                label = f"{label} {score if '/' in score else score + '/10'}"
        badges.append({"label": label, "caption": caption_sent})
    return badges


def build_one(asset: str, date: str, lang: str) -> Path:
    sections = []
    raw_parts = []
    for filename, sid, en_nav, fa_nav in SECTIONS:
        text = load_section(asset, date, filename, lang)
        if text is None:
            continue
        raw_parts.append(text)
        sections.append({
            "id": sid,
            "nav": fa_nav if lang == "fa" else en_nav,
            "html": md_to_html(text),
        })
    if not sections:
        raise RuntimeError(f"No sections for {asset} {date} {lang}")
    joined = "\n".join(raw_parts)
    ratio = persian_ratio(joined)
    origin = ""
    if lang == "en" and ratio > 0.15:
        origin = ""
    source_dir = ROOT / asset / date / "reports"
    source_sample = next(source_dir.glob("*.md")).read_text(encoding="utf-8")
    source_is_fa = persian_ratio(source_sample) > 0.25
    if lang == "fa" and not source_is_fa:
        origin = "این صفحه ترجمهٔ فارسی گزارش انگلیسی همین تاریخ است."
    if lang == "en" and source_is_fa:
        origin = "This page is an English translation of the Persian source report for this date."
    meta = {"badges": collect_badges(joined, lang), "origin_note": origin}
    target = ROOT / asset / date / ("report-fa.html" if lang == "fa" else "report.html")
    target.write_text(page_html(asset, date, lang, sections, meta), encoding="utf-8")
    return target


def build_index(entries: list[tuple[str, str]]) -> None:
    cards = []
    for asset, date in entries:
        info = ASSETS[asset]
        dates = format_dates(date)
        href_en = f"{asset}/{date}/report.html"
        href_fa = f"{asset}/{date}/report-fa.html"
        cards.append(
            f"""<article class="section kind-card {info['kind']}">
              <p class="kicker">{html.escape(asset)}</p>
              <h2>{html.escape(info['fa'])}</h2>
              <p>{html.escape(dates['jalali'])}</p>
              <p class="sub">{html.escape(dates['en'])}</p>
              <div class="badges">
                <a class="badge" href="{html.escape(href_en)}">English</a>
                <a class="badge neutral" href="{html.escape(href_fa)}">فارسی</a>
              </div>
            </article>"""
        )
    document = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>گزارش‌های تحلیلی</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&display=swap" rel="stylesheet">
<style>
{CSS}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }}
.kind-card h2 {{ font-size: 28px; }}
.kind-card.btc {{ --accent: #c2410c; --accent-soft: #fde6d8; }}
a.badge {{ text-decoration: none; }}
</style>
</head>
<body class="lang-fa">
<div class="wrap">
  <header class="hero">
    <p class="kicker">Trade Desk</p>
    <h1>گزارش‌های روزانه</h1>
    <p class="sub">هر روز دو صفحه دارد: متن اصلی انگلیسی و ترجمهٔ فارسی. گزارش ۲۲ نوامبر طلا از اول فارسی بوده و صفحهٔ انگلیسی‌اش ترجمه است.</p>
  </header>
  <div class="grid">
    {''.join(cards)}
  </div>
  <footer><p>صفحات را می‌توان جداگانه باز کرد یا از همین فهرست وارد شد.</p></footer>
</div>
</body>
</html>
"""
    (ROOT / "index.html").write_text(document, encoding="utf-8")


def discover() -> list[tuple[str, str]]:
    found = []
    for asset in ASSETS:
        base = ROOT / asset
        if not base.exists():
            continue
        for child in sorted(base.iterdir(), reverse=True):
            if (child / "reports").is_dir():
                found.append((asset, child.name))
    return found


def main() -> None:
    entries = discover()
    written = []
    for asset, date in entries:
        for lang in ("en", "fa"):
            written.append(build_one(asset, date, lang))
    build_index(entries)
    for path in written:
        print(path.relative_to(ROOT))
    print("index.html")


if __name__ == "__main__":
    main()
