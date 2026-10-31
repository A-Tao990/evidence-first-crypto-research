#!/usr/bin/env python3
"""Replay a concentrated-liquidity (Uniswap-v3 style) position on a volatile pair vs HODL vs a lending rate.

Public data only (GeckoTerminal OHLCV). No keys. Example (Pancake v3 USDT/WBNB 0.01% pool on BSC):
    python3 lp_replay_bnb_usdt.py --pool 0x172fcd41e0913e95784454622d1c3724f546f849 --fee 0.0001
The unknown is how concentrated YOUR liquidity is vs the pool average (k). We sweep k instead of guessing.
"""
import argparse, json, math, time, urllib.request

G = "https://api.geckoterminal.com/api/v2/networks/bsc/pools/%s"
H = {"accept": "application/json;version=20230302", "user-agent": "lp-replay/1"}

def get(url):
    for _ in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=25))
        except Exception:
            time.sleep(6)
    raise SystemExit("could not fetch " + url)

def mk(p, v, w):
    pa, pb = p * (1 - w), p * (1 + w); sa, sb, sp = map(math.sqrt, (pa, pb, p))
    return {"pa": pa, "pb": pb, "L": v / (p * (1 / sp - 1 / sb) + sp - sa)}

def value(pos, p):
    sa, sb = math.sqrt(pos["pa"]), math.sqrt(pos["pb"]); sp = math.sqrt(min(max(p, pos["pa"]), pos["pb"]))
    return pos["L"] * (sp - sa) + pos["L"] * (1 / sp - 1 / sb) * p

def sim(bars, fee, w, k, tvl, v0=20.0, gas=0.04, slip=0.0005):
    pos, fees, reb = mk(bars[0][1], v0, w), 0.0, 0
    for _, o, h, l, c, vol in bars:
        inr = max(0.0, min(1.0, (min(h, pos["pb"]) - max(l, pos["pa"])) / (h - l))) if h > l else float(pos["pa"] <= c <= pos["pb"])
        fees += value(pos, c) * (fee * vol / tvl) * k * inr
        if c < pos["pa"] or c > pos["pb"]:
            v = value(pos, c) * (1 - slip) - gas; pos = mk(c, v, w); reb += 1
    return value(pos, bars[-1][4]) + fees, fees, reb

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", required=True); ap.add_argument("--fee", type=float, required=True)
    ap.add_argument("--lending-apy", type=float, default=0.045)
    a = ap.parse_args()
    meta = get(G % a.pool)["data"]["attributes"]; tvl = float(meta["reserve_in_usd"])
    raw = get(G % a.pool + "/ohlcv/hour?aggregate=1&limit=1000&token=quote")["data"]["attributes"]["ohlcv_list"]
    bars = sorted(raw); days = len(bars) / 24
    hold = 10 / bars[0][1] * bars[-1][4] + 10; lend = 20 * (1 + a.lending_apy * days / 365)
    print("pool TVL $%.1fM, %.1f days | 50/50 hold %.2f | lending %.2f (start value 20)" % (tvl / 1e6, days, hold, lend))
    for w in (0.02, 0.05, 0.10):
        for k in (1, 2, 4):
            end, fees, reb = sim(bars, a.fee, w, k, tvl)
            print("range +-%d%% k=%d: end %.2f fees %.2f rebalances %d" % (w * 100, k, end, fees, reb))

if __name__ == "__main__":
    main()
