---
name: ild-literature-search
description: Retrieve ILD trial publication metadata and abstracts from PubMed and Europe PMC with saved queries, timestamps, response hashes, and explicit candidate selection. Use for SENSCIS, INBUILD, TRAIL1, RELIEF and U-ILD evidence intake; never claim full-text retrieval.
---

# ILD 文献检索

从本技能目录的真实脚本运行查询；不要以 SKILL.md 存在代替执行。

依赖：Python 3.12+、httpx；网络遵循继承代理、CA 与允许名单，TLS 验证开启。无需密钥、收费服务或浏览器。

```bash
<python> <skill-root>/scripts/search_trials.py --out <new-output-dir>
```

- 仅使用 PubMed ESearch/EFetch 和 Europe PMC core，保存查询式、候选 PMID、原始响应、HTTP 状态、UTC 时间、SHA-256。
- 选择规则必须命中原始结果论文题名；不按搜索第一条默认纳入，不混入方案、二次分析或综述。未找到唯一匹配时标为阻塞。
- U-ILD 指吡非尼酮用于未分类进展性纤维化 ILD 的 phase 2 原始研究，本次标签释义需在报告中保留。
- 只获取元数据与摘要；对没有全文、不能核验的字段保留空缺。Crossref 不可用不阻塞该合法路径。
- 输出记录供 ild-evidence-check 读取；拒绝覆盖目录。原始摘要快照默认本地保存，提交公开仓库前按许可检查。
- 修正解析后可用 `--replay <previous-run-dir>` 离线重解析已保存响应，检查查询和源哈希并保留原获取时间；必须标记本地重放，不能冒充新网络请求。
