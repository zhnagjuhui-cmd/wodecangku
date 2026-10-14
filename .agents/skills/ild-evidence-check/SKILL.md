---
name: ild-evidence-check
description: Verify retrieved ILD evidence records against hashed PubMed XML and Europe PMC responses, matching publication identity and abstract numerical tokens. Reject altered sources or metadata before downstream medical document generation.
---

# ILD 证据核验

依赖：Python 标准库。无需网络、浏览器或服务密钥。

```bash
<python> <skill-root>/scripts/verify_evidence.py --records <records.json> --out <new-verification.json>
```

- 核验源响应 SHA-256、PMID、题名、DOI、年份、提取的 PubMed 摘要是否与 XML 一致。
- 对 Europe PMC 独立索引比对身份、摘要数字集合及完整性；相同论文的两个索引不是独立临床证据。
- 任一不一致输出失败且返回非零，不能生成 PASS 假象。数字集合一致仅为机械比对，不能替代上下文、统计学或专业审阅。
- 下游文档必须消费此核验结果，记录来源位置与 records.json 哈希；仅摘要明确标记，不推断全文模型或未报告结果。
- 禁止编造、遮蔽阴性终点、敏感性分析或把替代终点写成生存获益。
