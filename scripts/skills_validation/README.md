# 本地技能验证与最小研究流程

实际结果、失败命令和限制见根目录 SKILLS_VALIDATION_REPORT.md。七项上游技能保持不变，新增三项 ILD CLI 技能。

## 调用

不依赖调用者当前目录：

```bash
/workspace/wodecangku/.venv-skills-validation/bin/python /workspace/wodecangku/scripts/run_ild_skill.py --list
```

运行五项研究的元数据检索 → 来源核验 → 中文 Markdown/DOCX：

```bash
bash /workspace/wodecangku/scripts/skills_validation/run_research_pipeline.sh /workspace/wodecangku/outputs/NEW_RUN_NAME
```

第一阶段须具有执行沙箱允许的网络访问，且资源仍在云端允许名单中；保留继承代理与 TLS 校验。目录已存在即拒绝覆盖。失败退出，不进入下游阶段。脚本仅调用 CLI，不会向当前模型会话动态注册平台技能。

## 环境复现

验证环境 `.venv-skills-validation` 使用 `--system-site-packages` 继承已有 PDF、PPTX、DOCX、httpx 库；它不是从空白操作系统建立的完全独立环境。`venv_freeze.txt` 是观察快照，包含临时源路径，不能直接作为可移植安装锁。

常规软件包网络允许时可在新的 venv 安装 `requirements.txt`；本次包源安装尝试失败，未宣称这条路径成功。已实际运行的替代方案：

```bash
bash scripts/skills_validation/bootstrap_github_deps.sh
```

它仅从允许的官方 GitHub 上游取得 requests 2.32.5 与 urllib3 1.26.20，核对固定 commit，在隔离 venv 中本地构建安装，不修改全局包或代理。urllib3 1.26.20 为 requests 允许的兼容版本，本次用其 setuptools 构建路径；不代表已经验证最新 2.x 分支。其余现有库仍需预先存在；导入失败时如实报告。

## 验收范围

三项研究技能已联网获取、交叉核验并生成重读后的文档。核验是元数据、源哈希、提取一致性及数字 token 集合比较，不替代效应方向、统计模型、偏倚风险或临床结论审阅。未请求受限全文。

原始响应和带完整摘要的 records.json 仅留本地；版本提交包括元数据目录、检索 URL/哈希、命令日志与衍生成果，复核时可联网重新获取。没有自动向 GitHub 上传或合并主分支。
