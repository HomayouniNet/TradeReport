# GC=F (Gold Dec 26, CMX) — technical read as of 2026-11-27

## Indicator selection

The eight selected indicators cover trend at three speeds, momentum, volatility and risk. Bollinger upper and lower bands are used together as one volatility envelope; they are not treated as separate trading signals.

| Indicator | Why it fits this context |
|---|---|
| `close_10_ema` | A responsive short-term reference for testing whether the latest rebound is gaining traction. |
| `close_50_sma` | Medium-term trend context; helps distinguish a short-lived bounce from a broader recovery. |
| `close_200_sma` | Long-term trend filter. |
| `macd` | Momentum direction and strength; the verified snapshot also provides its signal and histogram values. |
| `rsi` | Checks whether selling pressure is easing, without treating an oversold reading as a buy signal by itself. |
| `boll_ub` | Upper edge of the volatility envelope; useful context for a possible recovery and current range. |
| `boll_lb` | Lower edge of the same envelope; helps assess how far price has moved through the recent range. |
| `atr` | Volatility-aware risk and position-sizing context. |

## What the data says

**The prevailing trend is bearish, although the latest session rebounded.** GC=F closed at **3,668.50** on Nov. 27, above the prior session’s 3,561.90 close on Nov. 24 and Nov. 25’s 3,535.80 close. The Nov. 27 session ranged from **3,578.80 to 3,712.80**. This is a constructive short-term recovery in the recent price sequence, but not yet evidence of a trend reversal.

Price remains below all three selected moving averages: the **10 EMA is 3,695.44**, the **50 SMA is 4,049.78**, and the **200 SMA is 4,415.82**. The 10 EMA is close enough to be an immediate recovery test, but GC=F closed below it. The longer averages are also declining in the supplied series: the 50 SMA moved from 4,280.58 on Nov. 2 to 4,049.78 on Nov. 27, while the 200 SMA moved from 4,516.05 to 4,415.82. That combination argues for treating the recent bounce cautiously.

**Momentum remains weak, but the oversold reading has eased.** The verified MACD is **−139.21**, below its signal at **−115.23**, with a negative histogram of **−23.98**—a bearish momentum configuration. RSI is **38.86**, below the neutral 50 level. It had fallen to **21.57 on Nov. 20** and was **29.16 on Nov. 25** before rising to its current reading. That recovery suggests selling pressure has moderated, but RSI below 50 does not yet confirm a sustained momentum shift.

**The volatility envelope is wide; neither band is a guaranteed turning point.** The verified Bollinger middle line is **3,853.23**, with an upper band of **4,234.57** and a lower band of **3,471.90**. The close is inside the envelope—below its middle line and above its lower band. The Nov. 25 intraday low of **3,425.20** was below the lower-band reading reported for Nov. 27; the bands are recalculated as prices change, so this comparison does not establish a floor or a confirmed bounce.

ATR is **116.83** on Nov. 27, and the supplied indicator series rises from 76.18 on Oct. 28 to 116.83. This elevated and increasing volatility makes tight stops and fixed-size positions more vulnerable to ordinary price swings. ATR is a sizing and risk-management input, not a directional forecast.

## Conditional trading framework

- **For a recovery attempt:** GC=F would first need to close above the **3,695.44 10 EMA** and show follow-through. The **3,853.23 Bollinger middle line** is a further reference to monitor, not a guaranteed resistance level. A single close above the 10 EMA would be an early improvement, not confirmation of a broader reversal while price remains below the 50 and 200 SMAs.
- **For bearish continuation:** Watch whether GC=F loses the recent **3,425.20 intraday low from Nov. 25**. A move below it would make a fresh lower low; it should not be interpreted in advance as a support test or a predetermined target.
- **For execution and risk:** Use ATR to account for the current volatility when setting position size and stop distance. The Nov. 27 session high and low, and the moving-average or Bollinger readings above, are observable reference points—not stand-alone entry or stop instructions.
- **Overall:** The Nov. 27 rebound and RSI recovery are encouraging short-term developments, but the declining moving averages, price below those averages, and negative MACD keep the evidence tilted bearish. A trend-change thesis would need stronger confirmation than one rebound session.

| Key point | Verified evidence | Practical interpretation |
|---|---|---|
| Latest session | Nov. 27 close 3,668.50; range 3,578.80–3,712.80 | Rebound in the recent sequence, but the close remains below the 10 EMA. |
| Trend | 10 EMA 3,695.44; 50 SMA 4,049.78; 200 SMA 4,415.82 | Trend filters remain bearish; monitor for price recovery and improvement in average slopes. |
| Momentum | RSI 38.86; MACD −139.21; signal −115.23; histogram −23.98 | Oversold pressure has eased, but momentum is still bearish and RSI remains below 50. |
| Volatility | Bollinger middle 3,853.23; bands 4,234.57 / 3,471.90; ATR 116.83 | Wide price swings call for volatility-aware sizing; bands are not hard support or resistance. |
| Recovery check | 10 EMA at 3,695.44, followed by Bollinger middle at 3,853.23 | Closes above these references with follow-through would strengthen the recovery case; they do not alone confirm a reversal. |
| Downside check | Nov. 25 intraday low 3,425.20 | A move below it would establish a fresh lower low, not prove that level is support. |