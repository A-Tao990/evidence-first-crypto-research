# Evidence-first crypto research

A small, honest collection: **negative results** from testing a dozen on-chain / prediction-market "ways to make money", plus the **reproducible scripts** behind two of them.

Built by John together with AI coding agents (Codex, Claude Code). I set goals, make judgment calls and verify results; the agents write and run much of the code. Everything here uses **public data only**; there are no keys, wallet addresses, or account data in this repo.

## What is inside
- `reports/NEGATIVE-RESULTS-EN.md` / `reports/NEGATIVE-RESULTS-ZH.md` - the write-up: method, results table, two data traps I fell into, lessons.
- `scripts/btc_5m_reversal_test.py` - does BTC reverse after a large 5-minute candle? Out-of-sample split + permutation test. Uses Binance public market data.
- `scripts/lp_replay_bnb_usdt.py` - replay a concentrated-liquidity position vs hold vs a lending rate, sweeping the unknown "how concentrated is my liquidity" factor. Uses GeckoTerminal public candles.
- `reports/BYBIT-BTC-PERP-REPLAY-EN.md` / `-ZH.md` - three pre-registered BTC perpetual replays (channel breakout, 4h trend, funding reversal): no edge after costs. Report and numbers only; code not included yet.
- `vietnam-payments/BLUEPRINT-EN.md` / `BLUEPRINT-ZH.md` - a one-page blueprint for putting crypto behind Vietnam's local payment rails (VietQR / MoMo / ZaloPay), each claim labelled observed / reported / hypothesis.

## Method in one paragraph
Always compare against a **random baseline** under the same exit rules; fix thresholds on the **first half**, test on the **unseen second half**; run a **permutation test**; treat fees/slippage/latency as **variables**; and make sure the replay data source **matches the settlement data source**.

## Run
```bash
python3 scripts/btc_5m_reversal_test.py --pages 9
python3 scripts/lp_replay_bnb_usdt.py --pool 0x172fcd41e0913e95784454622d1c3724f546f849 --fee 0.0001
```
Python 3.9+, standard library only. Results shift with the data window (it is a rolling window of recent bars); the report's numbers are from a 2026-10-31 snapshot.

## Caveats
Not investment advice. Samples are short and limited. **"No edge found" is not "no edge exists".** Corrections and independent reproductions are welcome via issues.

## License
MIT.
