<!-- ppt-master-schema: spec-lock/v1 -->
# Execution Lock

## canvas
- viewBox: 0 0 1280 720
- format: PPT 16:9

## communication
- primary_language: zh-CN
- audience: 呼吸科及风湿科专业医生
- objective: 解读RELIEF研究并验证课件工作流，使听众准确区分主要分析、敏感性分析与外推边界。
- core_message: RELIEF提示潜在肺功能获益，但提前终止及不确定性要求谨慎解读。
- consumption_mode: balanced

## mode
- mode: custom
- mode_behavior: 以样本和终点建立边界，再将统计估计分行展示，最后用事件计数与限制完成谨慎判断。

## visual_style
- visual_style: custom
- visual_style_behavior: 分隔线和非等重分栏形成研究解读节奏；首屏大数字，中页统计表，末页计数与边界对照；平面无纹理与装饰。

## colors
- background: #FFFFFF
- secondary_bg: #F2F6F6
- primary: #8C0D27
- accent: #087B78
- secondary_accent: #64748B
- body_text: #24323D
- rule: #D7E0E4

## typography
- font_family: Noto Sans CJK SC, DejaVu Sans, sans-serif
- title_family: Noto Sans CJK SC, DejaVu Sans, sans-serif
- body_family: Noto Sans CJK SC, DejaVu Sans, sans-serif
- body: 24
- title: 40
- subtitle: 30
- lead: 28
- annotation: 18
- footnote: 14
- hero: 88

## icons
- library: none
- inventory: none

## page_rhythm
- P01: anchor
- P02: dense
- P03: dense

## pptx_structure
- mode: flat

## forbidden
- `mask`, `<style>`, `class`, external CSS, `<foreignObject>`, `textPath`, `@font-face`, `<animate*>`, `<set>`, `<script>` / event attributes, `<iframe>`
- HTML named entities in text; write typography as raw Unicode and escape XML reserved characters
- 不新增医学数字，不把敏感性分析写成主要分析，不把死亡计数写成生存获益。
