## GC=F — market and indicator report  
**As of 2026-11-23** · Resolved instrument: Gold Dec 26, CMX

### Data note

The stock-data feed and verified snapshot differ for 2026-11-23: the feed reports a close of **3623.50** and volume of **63,354**, while the verified snapshot reports a close of **3623.70** and volume of **63,392**. I use the **verified snapshot** as the source of truth below.

### Selected indicators

The eight selected indicators cover longer- and shorter-term trend, momentum, and risk/volatility. The two Bollinger Bands are treated as one envelope for interpreting price location.

| Indicator | Verified value / reading | Why it is useful here |
|---|---:|---|
| `close_10_ema` | 3772.37 | Short-term trend and potential reclaim level |
| `close_50_sma` | 4096.30 | Medium-term trend filter |
| `close_200_sma` | 4437.90 | Longer-term trend context |
| `macd` | -128.691 | Momentum and trend-direction check |
| `rsi` | 31.1087 | Helps distinguish persistent weakness from a possible oversold rebound |
| `atr` | 102.086 | Volatility-aware risk and position sizing |
| `boll_ub` | 4251.98 | Upper boundary of the recent volatility envelope |
| `boll_lb` | 3590.86 | Lower boundary; useful for judging whether price is pressing or recovering from the band |

I have not included MACD signal and histogram as separate selections because they are closely related to MACD; nor have I added VWMA, which would contribute less distinct information than the chosen trend and volatility measures.

### Trend and price structure

The verified 2026-11-23 OHLCV row for **GC=F** is **O 3570.50, H 3629.60, L 3552.30, C 3623.70**, on volume of **63,392**. The close was higher than the verified 2026-11-20 close of **3515.40**, marking a rebound in the latest session after several lower closes. That is a short-term improvement, but it does not by itself establish a trend reversal.

The broader trend evidence remains bearish: the 2026-11-23 close is below the 10 EMA (**3772.37**), 50 SMA (**4096.30**), and 200 SMA (**4437.90**). The separation from the longer averages underscores how much recovery would be needed to change the medium- and long-term picture. For now, rallies toward the 10 EMA are worth monitoring as tests of short-term trend, not assuming they will hold as support.

### Momentum and volatility

MACD is **negative at -128.691**; the verified MACD signal is also negative (**-91.7275**) and the histogram is **-36.9637**. This is consistent with bearish momentum still in place. RSI is **31.1087**, near the commonly watched 30 threshold. It signals weak momentum and proximity to oversold territory, but is not, on its own, a buy signal—especially while price remains below all three selected moving averages.

ATR is **102.086**, indicating substantial recent daily range. A fixed, tight stop may therefore be vulnerable to ordinary price movement; traders may want to size positions and set risk limits with current volatility in mind. ATR is a volatility measure, not a directional signal.

The close of **3623.70** is above the verified lower Bollinger Band (**3590.86**) and well below the upper band (**4251.98**). The close’s position just above the lower boundary is consistent with recent downside pressure, while the rebound from 2026-11-20 is a tentative stabilizing sign. A band touch or move back inside the envelope does not establish a durable bottom; price confirmation is still needed.

### Actionable scenarios to monitor

- **Bearish continuation:** Watch whether GC=F closes below the lower Bollinger Band (**3590.86**) and whether subsequent trading extends weakness. A break would reinforce downside risk, but should be judged alongside price follow-through rather than treated as a standalone signal.
- **Short-term stabilization:** The latest rebound is more credible if GC=F can hold above the lower-band area and then reclaim the 10 EMA (**3772.37**). RSI recovery and improvement in MACD would provide additional confirmation; neither is established by the current snapshot.
- **Larger trend repair:** Reclaiming the 10 EMA alone would not reverse the broader trend. The 50 SMA (**4096.30**) and 200 SMA (**4437.90**) remain progressively higher trend hurdles.
- **Risk management:** Given ATR near **102**, consider volatility-adjusted sizing and allow for wider price fluctuations. These indicator levels are reference points, not guaranteed support or resistance.

**Overall:** GC=F remains in a pronounced downtrend by moving-average alignment and negative MACD. Near-oversold RSI and the latest higher close offer a possible early stabilization signal, but they are not yet enough to confirm reversal. The next useful evidence is whether price holds above the lower Bollinger Band and can reclaim the 10 EMA, with the larger averages still acting as broader trend tests.

| Key point | Evidence for GC=F | Trading interpretation |
|---|---|---|
| Overall trend | Close 3623.70 below 10 EMA 3772.37, 50 SMA 4096.30, and 200 SMA 4437.90 | Bearish across short, medium, and long horizons |
| Momentum | MACD -128.691; RSI 31.1087 | Momentum remains weak; RSI is near oversold, not a reversal confirmation |
| Latest price action | Verified close rose from 3515.40 on 2026-11-20 to 3623.70 on 2026-11-23 | Rebound is tentative; monitor for follow-through |
| Bollinger position | Close 3623.70 versus lower band 3590.86 | Near the lower band; watch for a hold or confirmed break |
| Volatility | ATR 102.086 | Use volatility-aware position sizing and risk limits |
| Reversal checkpoints | 10 EMA 3772.37; 50 SMA 4096.30 | Reclaiming the 10 EMA may improve the short-term picture; the 50 SMA is a larger trend hurdle |
| Data quality | Feed close/volume differ from verified snapshot | Verified snapshot values used for exact claims |