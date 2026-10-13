# ILD 医学研究与课件制作工作区

## 项目目标
围绕 IPF、CTD-ILD、PPF 建立可追溯的医学文献检索、
循证评价、医学课件与患者教育素材制作流程。

## 文献检索
- 优先 PubMed、期刊官方网站、临床试验注册平台及权威指南。
- 记录标题、作者、发表年份、DOI、PMID、研究类型和来源链接。
- 区分已发表结果、会议摘要、预印本及正在进行的研究。
- 无法访问全文时明确说明，不得虚构全文内容。

## 医学循证规范
- 核对研究人群、样本量、干预、对照、主要终点、
  效应量及安全性。
- 区分 IPF、CTD-ILD、PPF 及具体亚型的证据适用范围。
- 区分指南推荐、获批适应证、探索性证据及超说明书应用。
- 不得虚构统计数据、引用或研究结论。

## PPT 制作
- 默认中文，面向呼吸科及风湿科专业医生。
- 优先使用真实临床研究数据制作可编辑统计图。
- 每页包含核心结论、数据来源、文献脚注和讲者备注。
- 可用时调用经过验证的医学循证PPT及PPT制作 Skills；
  不可用时明确报告，不得假装调用。

## 输出规范
- 文献整理保存到 literature/。
- PPT及脚本保存到 presentations/。
- 自动化脚本保存到 scripts/。
- 输出完成后检查文件是否存在、可打开及引用是否可追溯。
- 不得未经明确授权发布项目或上传患者隐私资料。


## Repository skills for Codex

- Canonical skills live only in `.agents/skills/`. Read the selected SKILL.md before using its workflow.
- Use `python3 scripts/check_skills.py` to validate discovery and required files.
- Read README.md for routing, cloud dependencies and limitations. Select the skill that matches the requested output; do not load every skill.
- Keep upstream attribution, integrity checks and licenses. Do not merge distinct workflows because they both produce presentations.
- Cloud tasks cannot access the author's local files or assume presentations tools, API credentials, browser installations or network access. Check required capabilities and report missing prerequisites honestly.
- Secrets belong in the cloud environment configuration, never in tracked files or logs.
