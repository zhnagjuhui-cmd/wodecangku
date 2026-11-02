# A 工作日志

2026-11-02（本批末次记录 UTC 10:31:44；浏览访问按日期记录，不虚构精确秒）：

1. 阅读工作树根 AGENTS.md；仅新增本研究子目录。
2. 浏览工具逐一打开五篇 PubMed 主报告记录，读取文献身份与 Abstract Methods/Results/Interpretation；将论文声明的注册号与独立注册核验区分。
3. 逐一访问期刊正文入口：NEJM 两项与 Lancet 三项均返回 403；NEJM 两项 appendix PDF 入口也返回 403。Lancet 三项的附件直链未取得，不能猜测后标为已下载。
4. 四个 ClinicalTrials.gov 研究页仅得到 11 行动态页面壳；四个 API v2 studies URL 由浏览工具报告不可访问。注册号来自论文，注册字段与版本历史未核验。
5. RELIEF 检索未确认对应 NCT。打开 DRKS 官方记录及 EudraCT 结果页，核实替代注册身份；发现官方附件但没有读取内容。不得把此发现写成全文已审阅。
6. 没有保存论文 PDF、没有生成医学图表、没有冻结证据或启动 B。

可追溯性说明：SOURCE_INVENTORY.csv 和 STUDY_VERIFICATION.md 是本次访问后的人工转录记录；不是网页原始快照。公开 URL 可复查；访问时间变化可能改变页面。失败结果仅代表本次工具路径，不证明论文不可合法获取。

本地自查：运行目录内 CSV/JSON/必需文件结构检查；最终内容等待独立验收。

7. 后续改用获准的本地 urllib 直接请求 ClinicalTrials.gov API，四项均成功；保存未经修改 JSON、SHA-256 和 selected_fields。已读当前身份/状态/入组数/主要终点，历史版本与全文一致性仍 UNVERIFIED。此条更新第 4 条网页访问失败后的获取层级。
