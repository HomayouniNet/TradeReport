#!/bin/bash
set -u
export HOME="${HOME:-/root}"
REPO="$HOME/TradeReport"
AGENTS="$HOME/TradingAgents"
LOCK="$REPO/automation/daily.lock"
LOG="$REPO/automation/daily.log"
exec 9>"$LOCK"
flock -n 9 || { echo "already running"; exit 0; }

mkdir -p "$(dirname "$LOG")"
exec >>"$LOG" 2>&1
echo "===== $(date -Is) ====="
cd "$REPO"
git pull --rebase origin main || exit 1

set -a
# کلیدهای تحلیل TradingAgents؛ زبان را پایین‌تر انگلیسی می‌کنیم
[ -f "$AGENTS/.env" ] && . "$AGENTS/.env"
. "$HOME/.config/trade-reports.env"
set +a
export TRADINGAGENTS_OUTPUT_LANGUAGE=English
export TRADINGAGENTS_NO_UPDATE_CHECK=1

if [ -n "${1:-}" ]; then
  DATE="$1"
else
  DATE="$(TZ=America/New_York date +%F)"
fi
DOW="$(TZ=America/New_York date -d "$DATE" +%u)"
RESULTS="${TRADINGAGENTS_RESULTS_DIR:-$HOME/.tradingagents/logs}"

# shellcheck disable=SC1091
source "$AGENTS/.venv/bin/activate"

fail=0
while IFS= read -r ticker || [ -n "$ticker" ]; do
  ticker="${ticker%%#*}"
  ticker="$(echo "$ticker" | tr -d '[:space:]')"
  [ -z "$ticker" ] && continue

  case "$ticker" in
    *-USD|*-USDT) ;;
    *)
      if [ "$DOW" -ge 6 ]; then
        echo "skip $ticker on weekend $DATE"
        continue
      fi
      ;;
  esac

  echo "---- $ticker $DATE ----"
  case "$ticker" in
    *-USD|*-USDT) analysts="market,social,news" ;;
    *) analysts="market,social,news,fundamentals" ;;
  esac

  if ! tradingagents --ticker "$ticker" --date "$DATE" \
      --analysts "$analysts" --save --no-show --no-html; then
    echo "FAILED analysis $ticker"
    fail=1
    continue
  fi

stamp="${DATE//-/}"
shopt -s nullglob
candidates=("$RESULTS/reports/${ticker}_${stamp}_"*)
shopt -u nullglob
src=""
if [ ${#candidates[@]} -gt 0 ]; then
  src="${candidates[-1]}"
fi
dst="$REPO/$ticker/$DATE/reports"
mkdir -p "$dst"
if [ -n "$src" ]; then
  [ -f "$src/1_analysts/market.md" ] && cp -a "$src/1_analysts/market.md" "$dst/market_report.md"
  [ -f "$src/1_analysts/sentiment.md" ] && cp -a "$src/1_analysts/sentiment.md" "$dst/sentiment_report.md"
  [ -f "$src/1_analysts/news.md" ] && cp -a "$src/1_analysts/news.md" "$dst/news_report.md"
  [ -f "$src/1_analysts/fundamentals.md" ] && cp -a "$src/1_analysts/fundamentals.md" "$dst/fundamentals_report.md"
  [ -f "$src/2_research/manager.md" ] && cp -a "$src/2_research/manager.md" "$dst/investment_plan.md"
  [ -f "$src/3_trading/trader.md" ] && cp -a "$src/3_trading/trader.md" "$dst/trader_investment_plan.md"
  [ -f "$src/5_portfolio/decision.md" ] && cp -a "$src/5_portfolio/decision.md" "$dst/final_trade_decision.md"
fi
if ! compgen -G "$dst/*.md" > /dev/null; then
  echo "FAILED no markdown for $ticker $DATE"
  fail=1
  continue
fi
  if ! "$REPO/.venv/bin/python" "$REPO/automation/translate_fa.py" "$ticker" "$DATE"; then
    echo "FAILED translation $ticker"
    fail=1
    continue
  fi
done < "$REPO/symbols.txt"

cd "$REPO"
if ! .venv/bin/python build_reports.py; then
  echo "FAILED build_reports.py"
  exit 1
fi

git add -A
git reset -q -- .venv automation/daily.log automation/daily.lock || true
if git diff --cached --quiet; then
  echo "nothing new to commit"
else
  git commit -m "Add reports for $DATE"
  git push origin HEAD
fi

echo "done fail=$fail"
exit "$fail"
