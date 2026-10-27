<!-- ppt-master-schema: design-spec/v1 -->
# RELIEF Evidence Review - Design Spec

## I. Project Information

| Item | Value |
| --- | --- |
| Project Name | relief-ppt-master |
| Canvas Format | ppt169, 1280 × 720 |
| Page Count | 3 |
| Primary Language | zh-CN |
| Target Audience | 呼吸科及风湿科专业医生 |
| Communication Intent | 解读RELIEF研究设计、主要结果和证据局限，同时验证ppt-master完整制作流程 |
| Desired Audience Outcome | 准确区分主要分析、敏感性分析和临床外推边界 |
| Core Message / Ask / Action | RELIEF提示潜在肺功能获益，但提前终止及不确定性要求谨慎解读 |
| Delivery Context | 三页中文学术研究解读，由讲者配合讲者备注讲解 |
| Artifact Afterlife | 可编辑医学课件测试及GitHub工作流验证成果 |
| Reading Mode | balanced |
| Content Strategy | 仅使用既有证据；允许重组表达，不改变数字，不新增研究结论 |
| Design Style | custom：以研究数字建立问题、以统计对照展示证据、以分层边界结束 |
| Formula Policy | text-only |
| AI Image Acquisition Path | not applicable；image_usage=none |
| Generation Mode | continuous |
| Spec Refinement | disabled |
| Speaker Notes | enabled — 用户明确要求逐页中文讲者备注 |
| Custom Animations | disabled — 本轮委托后的Stage-2决定 |
| Narration Audio | disabled — 本轮委托后的Stage-2决定 |
| Created Date | 2026-10-26 |

## II. Canvas Specification

| Property | Value |
| --- | --- |
| Format | PPT 16:9 |
| Dimensions | 1280 × 720 |
| viewBox | `0 0 1280 720` |
| Margins | 左右56px；顶部40px；底部32px |
| Content Area | x=56..1224；y=40..688 |

## III. Visual Theme

### Theme Style

- **Mode**: custom
- **Visual style**: custom
- **Theme**: 医学证据解读，非推广材料
- **Tone**: 精确、克制、对不确定性透明
- **Mode Behavior**: 以127例和48周建立研究边界，继而将主要分析和敏感性分析分行展示，最后将临床解读与不能推断的结论分离。
- **Visual Style Behavior**: 使用明确分隔线和非等重分栏，首屏用大数字带动研究问题，中页以紧凑而可读的统计表为主，末页用左侧事件计数与右侧解释边界形成对照；平面无纹理，不做装饰插图。

### Color Scheme

| Role | HEX | Purpose |
| --- | --- | --- |
| Background | #FFFFFF | 画布 |
| Secondary background | #F2F6F6 | 数据与结论区域 |
| Primary | #8C0D27 | 标题及关键研究数字 |
| Accent | #087B78 | 有边界的结论 |
| Secondary accent | #64748B | 标签与辅助说明 |
| Body text | #24323D | 正文及数据 |
| Rule | #D7E0E4 | 表格与分隔线 |

## IV. Typography System

### Font Plan

| Role | Character (Reference) | Primary | English if non-English | Fallback tail |
| --- | --- | --- | --- | --- |
| Title | sans，粗体层级 | Noto Sans CJK SC | DejaVu Sans | sans-serif |
| Body | sans，中性易读 | Noto Sans CJK SC | DejaVu Sans | sans-serif |

- **Title stack**: Noto Sans CJK SC, DejaVu Sans, sans-serif
- **Body stack**: Noto Sans CJK SC, DejaVu Sans, sans-serif

### Font Size Hierarchy

| Purpose | Anchor Size (px) |
| --- | ---: |
| Body | 24 |
| Title | 40 |
| Subtitle | 30 |
| Lead | 28 |
| Annotation | 18 |
| Footnote | 14 |
| Hero | 88 |

## V. Layout Principles

### Page Structure

- **Header area**: 章节标识、结论式标题；不使用Logo或通用装饰。
- **Content area**: 三页分别采用数字锚点与研究信息、三列结果表、事件计数与局限对照；不机械复用卡片网格。
- **Footer area**: 每页两个短引用行，DOI和PMID可见；页码右对齐。

### Spacing Specification

| Element | Current Project |
| --- | --- |
| Safe margin | 56px水平，32px垂直 |
| Content block gap | 24–40px |
| Icon-text gap | 不使用图标 |

## VI. Icon Usage Specification

- **Primary bundled library**: none

| Icon Path | Suitable Scenarios |
| --- | --- |

## VIII. Image Resource List

| Filename | Dimensions | Ratio | Purpose | Type | Layout pattern | Crop Policy | Acquire Via | Status | Reference | text_policy | page_role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## IX. Content Outline

### Part 1: RELIEF研究解读

#### Slide 01 - 研究问题与入组边界

- **Audience move**: 从泛指非IPF治疗转向理解RELIEF所覆盖的混合入组人群和48周肺功能终点。
- **Layout**: 左侧以127例为视觉锚点并显示64/63分组；右侧用研究设计、疾病范围、干预和主要终点四段信息；下方单行谨慎结论。
- **Title**: RELIEF：127例，检验非IPF进展性ILD
- **Core message**: 本研究是四类非IPF进展性ILD的混合人群Ⅱb期试验，不能直接证明每个亚型疗效。
- **Content**: 德国17中心；随机、双盲、安慰剂对照Ⅱb期；127例随机，吡非尼酮64例、安慰剂63例；入组四类CTD-ILD、纤维化NSIP、慢性过敏性肺炎、石棉肺；既有治疗下仍进展，在原治疗基础上加药，吡非尼酮递增至801 mg每日3次；48周主要终点是FVC占预计值百分比的绝对变化。结论条：四类疾病的混合证据，不能替代亚型独立验证。
- **Cover impact**: 以127例的有限样本规模作为真实研究钩子，旁列64/63分配，避免纯标题封面。
- **Visualization**: 研究设计信息通过分组与阅读顺序表达；数字文本不按数值映射形状面积或长度。

#### Slide 02 - 统计结果与不确定性

- **Audience move**: 从只看P值转向同时读效应量、区间和统计程序。
- **Layout**: 主要分析与两种估计分成三行，稳定列分别为分析、结果、解释边界；表下强调区间跨零和程序差异。
- **Title**: 主要分析提示获益，效应估计仍不确定
- **Core message**: P=0.043不能替代对区间和统计方法的解读。
- **Content**: 第一行主要分析ITT秩ANCOVA，P=0.043，SSD插补及死亡最差秩；第二行Hodges–Lehmann组间差1.69个百分点，95% CI −0.65至4.03；第三行预设纵向斜率敏感性分析3.53个百分点，95% CI 0.21至6.86，死亡按预设处理。正差支持吡非尼酮；不同统计估计/检验程序必须分别解读。明确数据为原论文已发表汇总数据，不是个体患者数据。
- **Visualization**: results-table为自定义三列四行纯文字统计表，各单元格保留对应分析及CI；不画未经来源支持的个体点或时间曲线。
- **Native-ready**: results-table=yes

#### Slide 03 - 安全性与结论边界

- **Audience move**: 从肺功能信号转向不夸大生存获益、理解提前终止与外推局限。
- **Layout**: 左侧两条事件计数，右侧三条解释边界；底部以一句结论收束。
- **Title**: 可以看到信号，不能越过证据边界
- **Core message**: 结果需谨慎解读，少量事件不支持死亡获益判断。
- **Content**: 吡非尼酮vs安慰剂死亡1/64 vs 5/63；严重感染类事件5/64 vs 10/63。事件数为描述性计数，不证明生存获益或安全等效。招募缓慢触发无效性中期分析并提前终止；缺失数据与人群异质性限制外推。结论：谨慎支持进一步研究，不能据此宣称生存获益或指南推荐。
- **Visualization**: 描述性计数按事件种类纵向排列，对照组顺序一致；局限采用独立文字段落，不画比例图。
- **Closing impact**: 用“谨慎支持进一步研究”与“不能宣称生存获益”并列完成判断，不使用空泛结束页。

## X. Speaker Notes Requirements

- **Generation**: enabled
- **Filename**: match each SVG filename under `notes/`
- **Content**: 每页中文讲稿说明如何阅读、数据口径及局限。所有页引用Behr J et al. Lancet Respir Med. 2021;9:476–486，PMID33798455，DOI10.1016/S2213-2600(20)30554-3。说明仅引用已发表汇总数据，来源为既有RELIEF摘要和已核验PDF；首页侧栏DOI异常及未核对附录在备注中保留。不新增文献或推荐。
- **Total duration**: 约4分钟
- **Notes style**: 专业、克制、解释性
- **Presentation purpose**: explain, teach, record
