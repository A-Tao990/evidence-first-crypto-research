#!/usr/bin/env python3
"""Does BTC 5-minute direction reverse after a large candle? Out-of-sample + permutation test.

Public data only (Binance public market-data mirror). No keys. Usage:
    python3 btc_5m_reversal_test.py --pages 9 --quantile 0.9
Idea: define "large" from the FIRST half only, test on the SECOND half, then shuffle up/down labels
to see how often chance alone does as well. Always compare against 50% and your real fee break-even.
"""
import argparse, json, random, time, urllib.request

API = "https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval={iv}&limit=1000{end}"

def klines(iv, pages):
    bars, end = [], ""
    for _ in range(pages):
        data = json.load(urllib.request.urlopen(API.format(iv=iv, end=end), timeout=30))
        bars = data + bars
        end = "&endTime=%d" % (data[0][0] - 1)
        time.sleep(0.3)
    return sorted({b[0]: b for b in bars}.values())

def reversal_rate(ret, lo, hi, thr):
    wins = n = 0
    for i in range(lo, hi - 1):
        if abs(ret[i]) >= thr:
            n += 1
            wins += (ret[i + 1] > 0) == (ret[i] < 0)   # bet against the large candle
    return wins, n

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--interval", default="5m")
    ap.add_argument("--pages", type=int, default=9)
    ap.add_argument("--quantile", type=float, default=0.9)
    ap.add_argument("--permutations", type=int, default=2000)
    a = ap.parse_args()
    bars = klines(a.interval, a.pages)
    o = [float(b[1]) for b in bars]; c = [float(b[4]) for b in bars]
    ret = [c[i] / o[i] - 1 for i in range(len(c))]
    n = len(ret); half = n // 2
    print("bars", n, "P(up) %.4f" % (sum(r > 0 for r in ret) / n))
    thr = sorted(abs(r) for r in ret[:half])[int(half * a.quantile)]     # threshold from first half only
    w1, n1 = reversal_rate(ret, 1, half, thr)
    w2, n2 = reversal_rate(ret, half, n, thr)
    print("threshold %.3f%% | first half %.1f%% (n=%d) | OUT-OF-SAMPLE second half %.1f%% (n=%d)"
          % (thr * 100, 100 * w1 / n1, n1, 100 * w2 / n2, n2))
    thr_all = sorted(abs(r) for r in ret)[int(n * a.quantile)]
    ow, on = reversal_rate(ret, 1, n, thr_all)
    obs = ow / on
    rng = random.Random(1); sign = [1 if r > 0 else -1 for r in ret]; mag = [abs(r) for r in ret]; hits = 0
    for _ in range(a.permutations):
        s = sign[:]; rng.shuffle(s); r2 = [s[i] * mag[i] for i in range(n)]
        hits += reversal_rate(r2, 1, n, thr_all)[0] / on >= obs
    print("full-sample reversal rate %.1f%% (n=%d); permutation p = %.4f" % (100 * obs, on, hits / a.permutations))
    print("Reminder: at price 0.50 with a 2% fee the break-even win rate is ~51%. Check settlement price source and other horizons.")

if __name__ == "__main__":
    main()
