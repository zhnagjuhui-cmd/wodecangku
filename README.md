# ILD 研究与 Codex Skill 工作区

技能唯一源码位于 [`.agents/skills/`](.agents/skills/)，供仓库内的 Codex 任务发现和调用。原 `skills/` 已迁移；重复 ZIP 已移除。各技能用途不同，均予保留。

| 技能 | 使用场景 | 云端依赖与限制 |
| --- | --- | --- |
| `medical-slide-source-update` | 医学照片/截图PPT整理、文献核验与原图更新、讲稿及资料包同步 | 文献检索需网络；本地文件须先上传；PPT编辑/渲染需可用工具；打包脚本仅需Python标准库 |
| `medical-evidence-ppt` | 医学证据、大纲、样张、可编辑课件 | 检索需网络；原流程依赖 presentations 能力，云端缺少时必须说明并确认可用制作工具 |
| `ppt-image-reconstruction` | 图片重建为可编辑 PPT | 需输入图片及可用的 PPTX 制作、渲染工具 |
| `ppt-master` | 通用可编辑 PPT、模板、增强 | 按技能路由安装依赖；保留上游完整性校验及署名 |
| `kaiyuan-xianfeng-ppt-skill` | 统一视觉的图片式 PPT | 依赖同仓库 `gpt-image-2`、图片接口密钥和网络；整页图片不是完全可编辑 PPT |
| `guizang-ppt-skill` | 横向翻页 HTML 演示 | 静态 HTML 可离线交付；浏览器验证需要浏览器运行环境 |
| `dashi-ppt` | 多主题 HTML 演示、导出 | Node.js 20+、npm；首次依赖安装与浏览器安装需要网络 |
| `gpt-image-2` | 图片接口客户端 | Python requests、兼容服务商接口和密钥；不是免费或内置模型能力 |

## Codex 云端使用

1. 在 Codex 云端连接本仓库，选择最新 `main`，启动新任务。
2. 执行 `python3 scripts/check_skills.py` 检查目录与必需文件。
3. 在任务中明确技能，例如：`使用 $medical-evidence-ppt，为 CTD-ILD 学术会议整理循证大纲，先提交大纲等待确认。`
4. 根据所选技能安装依赖，阅读其 `SKILL.md`；不要一次加载所有技能。

如果当前云端界面没有列出仓库技能，可明确要求：`读取 .agents/skills/medical-evidence-ppt/SKILL.md 并按其流程执行。` 目录就绪不代表模型接口、浏览器、网络或 presentations 工具已经提供。

## 环境准备

Python 示例（在云端环境的 setup 阶段运行，按任务需要选择）：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install requests Pillow python-pptx PyYAML
```

PPT Master 的可选依赖见其 `requirements.txt`；Dashi 按其渲染脚本安装项目依赖。Linux 中渲染 PDF/PPTX 可能需要 LibreOffice、字体或浏览器，须按实际任务配置并验证。

图片生成时，在云端环境的安全配置中提供 `LK888_API_KEY`、`LK888_BASE_URL`（或客户端支持的对应变量），并确保执行图片生成的阶段可以访问该服务。不要把密钥写进提示词、日志或仓库。本仓库未配置或验证收费图片接口。

开源先锋的 wrapper 默认优先发现同级 `gpt-image-2`；可用 `KAIYUAN_GPT_IMAGE_2_SKILL_DIR` 指定替代路径。仅检查后端路径：

```bash
.venv/bin/python .agents/skills/kaiyuan-xianfeng-ppt-skill/scripts/image_gen.py check
```

## 输出与来源

沿用原工作区的医学证据规范。文献保存到 `literature/`，课件及备注保存到 `presentations/`。不得虚构证据、把整页图片称为完全可编辑 PPT，或伪造医学影像。

各技能原有许可证、署名和赞助说明保留。无许可证的目录未额外授予开源许可。去重仅处理重复分发副本，模板、图标等运行所需素材维持原路径。

结构依据：[OpenAI 技能文档](https://learn.chatgpt.com/docs/build-skills)。本次已验证目录与文件完整性；尚未在真实 Codex 云端完成课件生成或收费接口调用测试。
