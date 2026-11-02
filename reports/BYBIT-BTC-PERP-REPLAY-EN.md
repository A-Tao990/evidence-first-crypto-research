# BTC perpetual futures: three pre-registered replays, no edge after costs

*Written Nov 2026 by an independent researcher, with AI coding agents (Codex, Claude Code). Public Bybit v5 market data only; no account data, keys or orders are used or shown. Not investment advice.*

**Bottom line:** I tested simple, well-known BTCUSDT perpetual rules on public history with rules frozen before looking at results. Each failed on the out-of-sample part after fees and slippage. "No edge found" in these narrow tests is not "no edge exists", but it is a good reason not to put money behind them.

## Method (same discipline as the other reports here)
- Rules, parameters and stop logic **frozen before** computing results; no re-tuning after seeing numbers.
- Fixed size 0.001 BTC, no compounding, so results are per-trade economics, not account growth.
- Taker fee assumed 0.055% per side; adverse slippage 2 bps per side; a **stress** branch adds 3 bps more per side.
- Funding: actual settled historical rates; entries on signals use only information known at that time (funding-based signals are delayed one hour).
- Sizes are in USDT per 0.001 BTC; fills are hourly/1-minute **proxies**, not tick-level fills, and mark-price triggers are modelled separately from trade prices.
- Look-ahead guards: 14 regression tests (prefix invariance, signal known-time, next-open entry, stop never loosened, no same-bar reversal, funding sign/time, missing-bar rejection).

## Test 1 — 90 days, 1-minute data, breakout channel length 10 / 20 / 40
Breakout of an N-bar channel on 15-minute bars, filtered by a 1-hour EMA, long and short. Development = first 60 days, test = last 30 days.

| Channel | Dev trades | Dev net (USDT) | Test trades | Test net (USDT) | Test net, stress costs |
|---|---:|---:|---:|---:|---:|
| 10 | 294 | −33.33 | 161 | −25.51 | −33.55 |
| 20 | 209 | −23.11 | 116 | −14.57 | −20.36 |
| 40 | 142 | −14.34 | 84 | −13.40 | −17.59 |

Shorter channels trade more and lose more. 40 loses less, but its test-period average net R is worse than 20's, so I did not pick a winner.

## Test 2 — 730 days, 4-hour EMA16/64 trend (low turnover)
Closed 4h bars only; entry at the next hour's open plus slippage; initial stop 3×ATR(14) on mark price, tightened (never loosened) on closed 4h bars; exit on trend failure or 14 days. Data: 2024-07-28 → 2026-07-28 (18,544 hourly bars, 2,320 funding settlements).

| 365-day window | Trades | Gross after slippage | Fees | Funding | **Net** | Net, +3 bps stress | Net without best trade |
|---|---:|---:|---:|---:|---:|---:|---:|
| Development | 34 | +21.79 | 3.20 | −0.68 | **+17.91** | +16.16 | +1.13 |
| Test | 34 | −5.04 | 3.30 | −0.06 | **−8.40** | −10.20 | −16.06 |

Lower turnover did cut fees, but gross was already negative in the test year, before fees. A positive full-period sum would have hidden the late-period failure. The candidate was rejected and I did not keep scanning EMA or ATR settings.

## Test 3 — extreme funding-rate reversal
Fade the market when the last settled funding rate was ≥ 0.03% in absolute value (entry delayed one hour; exit when funding normalises, on reversal, or after 24h).
- Development year: 16 trades, net +2.87 — but **−1.57 without the best trade**.
- Test year: **0 triggers**. That is "no opportunity", not "verified safe" and not "profitable".
- This test reused the data from Test 2, so it is exploratory, not a fresh hold-out. Verdict: insufficient signal coverage, no promotion. I did not lower the threshold to manufacture trades.

## What I take from this
1. Costs decide these strategies; the best-looking in-sample number was one trade away from negative.
2. Always read out-of-sample and "without the best trade" next to the headline.
3. A rule with zero trigger events in the test period has not been tested.

## Limits
Proxies, not tick data; fees assumed, not historical; no liquidation or margin modelling; BTCUSDT only; short windows. Code is not included in this repository yet because it depends on a larger private bot codebase; the method and numbers above are what I can stand behind. Corrections and independent replications are welcome via issues.
