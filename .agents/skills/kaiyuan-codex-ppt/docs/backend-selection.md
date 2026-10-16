# 内置图像后端与依赖

唯一生成路径是 codex-imagegen-batch → 当前 Codex 会话的内置图像工具。Python 适配器不会生成或上传图片，不需要外部服务地址、图片 URL 或第三方密钥。

```sh
python3 {skill_root}/scripts/image_gen.py check
```

依赖发现顺序：显式 --image-skill / KAIYUAN_CODEX_IMAGEGEN_SKILL_DIR，随后同级 codex-imagegen-batch，随后 CODEX_HOME/skills/codex-imagegen-batch。输出区分 dependency_available 和 tool_availability；脚本检查成功不代表 worker 拥有图像工具。

主代理与每个子代理分别检查工具、读取其当前参数。缺少依赖或工具时记录阻塞；不得切换外部后端、上传图片换 URL 或启动其他 CLI 会话冒充内置调用。工具可能随宿主变化；适配器当前记录 image_gen.imagegen，遇到不同正式工具名称时应显式更新匹配契约，而不是伪造名称。

样张阶段确认项目 image_policy，后续页面继承。它是项目授权记录，不改变 codex-imagegen-batch 的默认规则。可批准接受实际尺寸、等比留边等处理，以及有限的质量重试。自动重试只适用于已拿到并检查过的结果；超时和结果不确定时不自动重发。

依赖只包含 codex-imagegen-batch、当前会话图像工具、Python 及 requirements.txt 中的本地库。运行环境可选独立安装；已有满足依赖的 Python 也可直接执行。
