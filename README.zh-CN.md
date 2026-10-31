# 证据优先的加密研究

一个小而诚实的合集：对十几个链上和预测市场"赚钱方法"的**负结果**，以及其中两个方向的**可复现脚本**。

由 John 与 AI 编程助手（Codex、Claude Code）协作完成：目标、判断和验证由我负责，助手写并运行大部分代码。这里**只用公开数据**，仓库里没有密钥、钱包地址或账户数据。

## 内容
- `reports/NEGATIVE-RESULTS-ZH.md` / `NEGATIVE-RESULTS-EN.md`：文章（方法、结果表、我踩过的两个数据坑、总结）。
- `scripts/btc_5m_reversal_test.py`：BTC 大 K 线之后会反转吗？样本外切分加置换检验，用币安公开行情。
- `scripts/lp_replay_bnb_usdt.py`：回放集中流动性做市 vs 持有 vs 借贷利率，对"我的流动性有多集中"这个未知量做敏感性扫描，用 GeckoTerminal 公开 K 线。

## 方法
任何信号都要对照**随机基线**；用**前半段**定阈值、在**没见过的后半段**检验；做**置换检验**；把手续费、滑点、延迟当变量；并确保回放的数据源**和结算的数据源一致**。

## 运行
```bash
python3 scripts/btc_5m_reversal_test.py --pages 9
python3 scripts/lp_replay_bnb_usdt.py --pool 0x172fcd41e0913e95784454622d1c3724f546f849 --fee 0.0001
```
Python 3.9+，只用标准库。结果会随数据窗口滚动而变化；文章里的数字来自 2026-10-31 的快照。

## 免责声明
不是投资建议。样本短且有限，**"没发现优势"不等于"不存在优势"**。欢迎通过 issue 指正和复现。

## 许可
MIT。
