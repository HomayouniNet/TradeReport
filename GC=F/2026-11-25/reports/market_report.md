## GC=F — trend and indicator review  
**As of 2026-11-25**

### Indicator set selected

The eight indicators below cover short-, medium-, and long-term trend, momentum, volatility, and risk. The Bollinger upper and lower bands are treated as a pair, rather than as separate signals.

### Current technical picture

**Trend — strongly bearish across the selected horizons.** GC=F closed at **3599.30** on 2026-11-25, below its **10 EMA (3712.97)**, **50 SMA (4065.67)**, and **200 SMA (4423.29)**. All three averages are above the close, with the longer averages especially far away; this is consistent with a substantial ongoing downtrend, not just a short-term pullback. The moving averages are also declining in their recent readings, reinforcing that interpretation.

**Momentum — downside remains dominant, but the close is not deeply oversold by RSI.** MACD is **−139.817**, with its signal at **−108.227** and histogram at **−31.5902**. The negative MACD and histogram indicate bearish momentum, and the MACD remains below its signal. RSI is **32.90**: weak and close to the conventional oversold threshold of 30, but not below it. That leaves room for further weakness; RSI alone is not a reversal confirmation.

**Volatility and bands — wide range, with price near the lower band.** The Bollinger middle line is **3874.55**, upper band **4243.15**, and lower band **3505.96**. The close is above the lower band but well below the middle line, a location consistent with persistent weakness. ATR is **104.65**, signaling meaningful daily-range risk. Traders should account for that volatility when sizing positions and setting exits; tight stops may be vulnerable to ordinary price movement.

### Price action and execution considerations

Recent closes show a steep decline from **4170.10 on 2026-10-15** to **3515.40 on 2026-11-20**, followed by a partial recovery: **3651.40 on 2026-11-23**, **3561.90 on 2026-11-24**, and **3599.30 on 2026-11-25**. That sequence shows a bounce from the 2026-11-20 close, but not a sustained recovery: the latest close remains below all three selected moving averages, and MACD remains negative and below its signal.

The 2026-11-25 bar deserves caution as confirmation: its reported volume was **1,264**, versus **263,138** on 2026-11-24, and its reported high-low range was only **22.20**. This unusually low reported volume and narrow range may reflect an abbreviated or otherwise atypical session; the available data do not establish the reason. Treat that day’s close as the verified latest observation, but avoid reading too much into it as evidence of a broad shift in participation.

**Actionable framework:** A bearish bias remains better supported than a bullish reversal thesis, but the low RSI and recent bounce argue against treating a short entry as risk-free or chasing weakness without a plan. A more convincing change in trend would require follow-through and a move back above short-term trend measures; a move toward or through the 10 EMA would be an initial test, not by itself proof of reversal. If considering a countertrend long, seek confirmation in price action and improving momentum rather than relying on RSI proximity to 30 alone. In either direction, account for the **104.65 ATR** and the possibility that the latest session’s unusually low volume makes its close less representative.

### Selected indicators and use

| Indicator | Latest verified value | Why it is useful for GC=F now |
|---|---:|---|
| `close_10_ema` | 3712.97 | Responsive short-term trend reference; close below it indicates near-term weakness. |
| `close_50_sma` | 4065.67 | Medium-term trend filter; helps distinguish a short bounce from a broader recovery. |
| `close_200_sma` | 4423.29 | Longer-term trend benchmark; the large separation from the close underscores the broader bearish backdrop. |
| `macd` | −139.817 | Momentum and trend-change context; negative and below its signal, with a negative histogram. |
| `rsi` | 32.9025 | Gauges momentum exhaustion; weak and near, but above, the conventional oversold threshold. |
| `boll_ub` | 4243.15 | Upper volatility-band reference; pairs with the lower band to frame the current range. |
| `boll_lb` | 3505.96 | Lower volatility-band reference; the close is above it but remains far below the middle line. |
| `atr` | 104.649 | Volatility-based risk context for position sizing and stop placement. |