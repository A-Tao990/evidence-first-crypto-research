# We tested a dozen "ways to make money" on-chain. None had an edge after costs: an evidence-first negative-results report

Author: John (built together with AI coding agents Codex and Claude Code; I own goals, judgment and verification)
Scope: a very small amount of real money plus a lot of read-only replay to test on-chain and prediction-market strategies. **No addresses, order IDs or keys are included; data comes from public endpoints so every result can be reproduced.**

## Why publish this
The internet is full of "50% APY" and "90% win rate". I wanted to know: **after real costs, against a random baseline, on data the rule never saw, what is left?** Answer: of the directions I tested, none made money after costs. That is a useful result, so here it is.

## Method (more important than the results)
1. **Always beat a random baseline**: compare every signal with random-time entries under the same exit rules. Random entries are often negative by themselves, so "did it make money" alone fools you.
2. **Out-of-sample**: fix thresholds on the first half, test on the unseen second half.
3. **Permutation test**: shuffle up/down labels and ask how often chance does as well.
4. **Cost sensitivity**: treat fees, slippage, gas and latency as variables, not a single optimistic number.
5. **Check the data source before trusting a result** (two traps below).
6. **Use small real money to calibrate costs, never for trial and error.**

## Results at a glance
| Direction | What I did | Result |
|---|---|---|
| BSC spot short-term (post-surge pullback) | 2 real small fills; replay over 22 tokens x 11 days, 80 exit-parameter combos | Net loss live; in replay the entry rule was no better than random (-1.51% vs -1.40% at 1.2% cost); **none of 80 parameter sets had a positive mean in either the training or test half** |
| BNB-USDT liquidity provision | 41.7 days of hourly bars, ranges ±2/5/10% | Fee APR about 28% (conservative) to 114% (optimistic), depending on my concentration vs the pool; **could not show it beats 4.5% lending**; narrow ranges lose to rebalancing costs |
| Official meme-coin "signals" | Official backtest win rate 58-90%; I pulled price paths for the latest 90 signals and replayed | **Real win rate 2-35%.** Break-even only under the unrealistic assumption of filling at the alert price; with a 10%+ entry premium every rule averaged -10% to -72% |
| Prediction markets: complementary arbitrage | 385 binary markets | YES+NO sums to about 1 and the fee is 2%, so no room |
| Prediction markets: daily temperature | Public weather data vs market quotes | I first saw a "100x mispricing", **but I had used a gridded model instead of airport observations**; against METAR the market was right |
| Prediction markets: price touch | Binance candles vs BTC/ETH/SOL touch markets | Long-shot overpricing of about 1% per event, but it equals selling lottery tickets: near-total loss in the tail, correlated across strikes |
| BTC 5-minute direction | 31 days, 9,000 bars | After a large candle the next one tends to reverse, **55.9% out-of-sample, permutation p<0.001**; but it fails at 15 minutes (45-48% OOS) and settles on a different price feed, **so not shown to be tradable** |
| AI forecasts of BTC 15-minute direction | 220 real forecasts from an earlier model | 54.5% hit rate, about ±3.4% error, **not statistically significant** |
| Perp funding rates | Current rates on 896 perpetuals | BTC about +11% annualized gross, about 7-9% after fees and margin; high-funding small caps are traps |
| Full-chain stablecoin yield scan | about 16k pools, 104 chains | Highest yields are synthetic dollars or credit products; one 13.1% pool's own stablecoin had already depegged -1.34%; bridging costs eat the spread |

## Two traps I fell into (more useful than the results)
1. **A mean return of 140 million percent.** One replay printed "+139,835,773%". Not a miracle: I had picked the wrong pool for 10 tokens and the price units did not match. **For extreme results, suspect the data first.**
2. **A model is not an observation.** Open weather data is a gridded model that differs from airport observations by 2-4 °C, and I concluded the market was mispriced. **The replay data source must match the settlement data source.**

## What I learned
- "Win rate" is not "profit". The official "win" often just means the price once exceeded the alert price.
- The random baseline is often negative because of costs. **Without it, you cannot tell whether you have an edge.**
- At small size, structural yield (lending, market making) tops out at a few to low-teens percent a year; directional "high returns" are almost always lotteries.
- A pattern that shows up only at the shortest horizon and vanishes when you lengthen it is usually a microstructure artifact.

## Disclaimer
Not investment advice. Samples are short (days to about six weeks) and tokens are limited; **"no edge found" is not "no edge exists".** All numbers come from public data and my own replay and may contain errors. Corrections and reproductions are welcome.
