# GC=F — Technical trend report  
**As of 2026-11-26**

## Data note

The downloaded OHLCV file and the verified snapshot disagree on the latest row: the file reports a **2026-11-26 close of 3592.80** and volume of **81,686**, while the verified snapshot reports **3593.50** and volume of **81,698**. Per the verification instruction, this report uses the snapshot as the source of truth for the latest price and indicator values; the discrepancy is unresolved.

The verified snapshot’s latest row is **open 3619.80, high 3634.70, low 3578.80, close 3593.50**. This is a single-day data point, not evidence by itself of a trend reversal.

## Trend and momentum

**The technical picture is bearish overall, with a small latest-session recovery that has not yet changed the broader trend readings.** The recent-closes series falls from 4181.10 on October 16 to 3593.50 on November 26. Within that period, GC=F closed at 3515.40 on November 20, rebounded to 3651.40 on November 23, then closed at 3561.90 and 3535.80 on November 24 and 25, before the latest close at 3593.50.

The latest close is **below all three selected moving averages**: the 10 EMA at 3681.80, the 50 SMA at 4048.28, and the 200 SMA at 4415.45. The supplied indicator history shows both SMAs declining through the latest reading. The 10 EMA has also moved lower in recent sessions. This alignment points to weakness across short-, medium-, and longer-term trend measures; it does not establish where a reversal will occur.

Momentum measures reinforce that caution. MACD is **-145.193**, with its signal at **-116.431** and histogram at **-28.763** in the verified snapshot. The MACD line remains below both zero and its signal, consistent with bearish momentum rather than a confirmed bullish crossover. RSI is **33.73**: weak and near the commonly watched oversold threshold, but above 30 on the latest reading. The RSI tool output shows it reached 21.57 on November 20 and subsequently recovered, so the latest bounce coincides with some improvement from an extremely weak reading. That alone is not a reversal signal, especially while price remains below the moving averages and MACD remains negative.

## Volatility and price location

The latest Bollinger readings are **middle 3849.48, upper 4239.39, and lower 3459.58**. The verified close is below the middle line but above the lower band. Thus, price remains in the lower portion of the recent band range, but it is not below the lower band on the latest reading. The lower band should be treated as a volatility envelope—not as confirmed support—and the wide range between the bands reflects substantial recent price variability.

ATR is **111.26**. The ATR indicator history rises from 77.41 on October 27 to 111.26 on November 26, indicating that recent daily ranges have become larger. That matters for execution: fixed, tight stops may be more exposed to ordinary price noise, while position size and risk limits should account for the wider movement range. ATR is a volatility measure, not a forecast of direction.

## Actionable, conditional read

- **For trend-following traders:** The indicator balance still favors caution toward bullish exposure. A recovery above the 10 EMA at 3681.80 would be an initial short-term improvement to monitor, but not sufficient on its own to confirm a larger trend change. A stronger reversal case would require follow-through and improvement in momentum, with the 50 SMA and Bollinger middle line remaining higher hurdles.
- **For traders considering a countertrend long:** RSI’s recovery from its November 20 extreme and the latest positive close-to-close move may justify watching for stabilization, but neither confirms that selling pressure has ended. Consider requiring evidence such as sustained closes above the 10 EMA and improving MACD before treating a bounce as more than tactical.
- **For downside-risk monitoring:** The recent verified closes include 3515.40 on November 20 and 3535.80 on November 25; the downloaded price file lists a November 25 low of 3425.20. These are dated reference points to monitor, **not confirmed support levels**. A move below recent lows would be a reason to reassess downside risk, not proof of a particular next target.
- **For risk management:** With ATR at 111.26, use volatility-aware position sizing and avoid assuming that a narrow stop will be reliable. The reading can help frame risk, but it does not prescribe a specific stop distance.

## Indicators selected

Eight indicators were selected to cover distinct roles: three trend horizons, momentum confirmation, overbought/oversold context, volatility range, and volatility-aware risk management. The two Bollinger bands are retained together to show the current envelope; the verified snapshot also supplies the middle line for context. MACD was selected rather than adding its signal and histogram as separate requested indicators, though the verified snapshot provides those values for interpretation.

| Indicator | Latest reading | Role in this market context |
|---|---:|---|
| `close_10_ema` | 3681.80 | Short-term trend reference; close remains below it. |
| `close_50_sma` | 4048.28 | Medium-term trend filter; price is below a declining average. |
| `close_200_sma` | 4415.45 | Longer-term trend benchmark; also above price and declining. |
| `macd` | -145.193 | Momentum measure; negative, with verified MACD below its signal. |
| `rsi` | 33.73 | Momentum-extreme context; weak and near 30, but not below it on the latest reading. |
| `boll_ub` | 4239.39 | Upper volatility boundary; helps frame band width and upside range. |
| `boll_lb` | 3459.58 | Lower volatility boundary; close remains above it, but it is not confirmed support. |
| `atr` | 111.26 | Volatility input for risk sizing and stop planning; recent reading is elevated versus the supplied earlier history. |