from pathlib import Path
import json,csv
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
B=Path(__file__).resolve().parents[1]; P=B/'presentations'; L=B/'literature'
r=json.loads((L/'original_records.json').read_text())
rows=[
['SENSCIS','31112379','10.1056/NEJMoa1903076','随机、双盲、安慰剂对照；SSc-ILD','576例接受至少一剂；注册入组580例，口径不同','52周FVC年下降率','尼达尼布150 mg bid vs 安慰剂；差41.0 mL/年，95%CI 2.9–79.0；P=0.04；缺失数据敏感性分析P=0.06–0.10'],
['INBUILD','31566307','10.1056/NEJMoa1908681','随机、双盲、安慰剂对照Ⅲ期；进展性纤维化ILD','663例接受治疗','52周FVC年下降率；总体及UIP样两个人群','尼达尼布150 mg bid vs 安慰剂；总体差107.0 mL/年，95%CI 65.4–148.5；P<0.001'],
['TRAIL1','36075242','10.1016/S2213-2600(22)00260-0','随机、双盲、安慰剂对照Ⅱ期；RA-ILD','123例随机（63/60）','52周FVC%较基线下降≥10%或死亡复合终点','吡非尼酮2403 mg/日 vs 安慰剂；7/63 vs 9/60；OR 0.67，95%CI 0.22–2.03，P=0.48；提前终止'],
['RELIEF','33798455','10.1016/S2213-2600(20)30554-3','随机、双盲、安慰剂对照Ⅱb期；四类非IPF进展性ILD','127例随机（64/63）','48周FVC占预计值百分比的绝对变化；ITT秩ANCOVA','吡非尼酮加至801 mg tid vs 安慰剂，均加原治疗；P=0.043；Hodges–Lehmann差1.69个百分点，95%CI −0.65–4.03；提前终止'],
['U-ILD','31578169','10.1016/S2213-2600(19)30341-8','随机、双盲、安慰剂对照Ⅱ期；不可分类进展性纤维化ILD','253例随机（127/126）；安全集127/124','24周每日家庭肺功能测定的FVC预测变化','吡非尼酮2403 mg/日 vs 安慰剂；主要终点预设模型无法应用；医院测量次要终点差95.3 mL，95%CI 35.9–154.6，P=0.002']]
with (L/'evidence.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['研究','PMID','DOI','设计与人群','样本量及口径','主要终点','已发表汇总结果与局限']);w.writerows(rows)
text='# 五项研究证据核验\n\n检索日期：2026-10-26。原始数据指原论文公开报告的汇总数据，不是个体患者数据。\n\n'
for row in rows:
 name,pmid,doi,design,n,end,result=row
 text+=f'## {name}\n\n- 题名：{r[name]["title"]}\n- 作者：{r[name]["authorString"]}\n- 期刊发表年：{r[name]["pubYear"]}（TRAIL1在线2022/期刊2023；U-ILD在线2019/期刊2020）\n- PMID：[{pmid}](https://pubmed.ncbi.nlm.nih.gov/{pmid}/)；DOI：[原文](https://doi.org/{doi})\n- 设计：{design}；样本：{n}\n- 主要终点：{end}\n- 汇总结果：{result}\n- 核验依据：Europe PMC MED 原始题录及摘要（{name}_search.json）、Crossref DOI元数据（{name}_crossref.json）。全文状态及注册交叉核验见报告。\n\n'
(L/'evidence.md').write_text(text)
summary='''# RELIEF 中文证据摘要

Behr J, et al. Lancet Respir Med. 2021;9:476–486. PMID 33798455. DOI: 10.1016/S2213-2600(20)30554-3。

德国17中心随机、双盲、安慰剂对照Ⅱb期研究，纳入127例既有治疗下仍进展的非IPF纤维化ILD（CTD-ILD、纤维化NSIP、慢性过敏性肺炎、石棉肺）。吡非尼酮组64例，对照63例；在原治疗基础上加药，目标801 mg每日三次，观察48周。

主要终点为基线至48周FVC占预计值百分比的绝对变化。ITT分析采用秩ANCOVA、预设SSD缺失值插补及死亡者最差秩处理：P=0.043。Hodges–Lehmann组间差1.69个百分点，95%CI −0.65至4.03。两者统计估计/检验方法不同，不应以P值替代该区间的不确定性。预设纵向斜率敏感性分析（死亡按预设处理）差3.53个百分点，95%CI 0.21至6.86。

安全性：死亡1/64 vs 5/63；严重感染类事件5/64 vs 10/63。这些是描述性计数，不支持死亡获益结论。研究因招募缓慢触发的无效性中期分析而提前终止，样本不足、缺失数据和人群异质性限制外推；不能据此认定每个ILD亚型疗效或推断药物间优劣。

证据角色：对入组的混合非IPF进展性ILD人群为直接随机研究证据，但结论需谨慎；对特定亚型疗效仅可作为间接支持。本测试不评价当前指南或获批适应证。

来源：机构公开存档PDF（11页），PDF物理第1页摘要、第3–4页方法及第6–8页结果。题名、作者、正文页眉DOI及摘要均已核对。首页侧栏另印有30532-4，与正文页眉/题录不同，保留此版本异常；本稿引用经MED和Crossref共同核实的30554-3。未取得附录，不宣称附录核验。

下载入口：https://push-zb.helmholtz-muenchen.de/deliver.php?id=32778
全文仅留本地，版权为Elsevier；公开可读不等于可重新发布。
'''
(L/'RELIEF_summary_zh.md').write_text(summary)
prs=Presentation();prs.slide_width=Inches(13.333);prs.slide_height=Inches(7.5)
red='8C0D27';teal='087B78';gray='303A42'
def box(s,x,y,w,h,t,size=20,color=gray,bold=False):
 sh=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h));tf=sh.text_frame;tf.word_wrap=True
 for i,line in enumerate(t.split('\n')):
  p=tf.paragraphs[0] if i==0 else tf.add_paragraph();p.text=line;p.font.name='Noto Sans CJK SC';p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=RGBColor.from_string(color)
 return sh
def slide(title,conclusion,note):
 s=prs.slides.add_slide(prs.slide_layouts[6]);box(s,.55,.35,12.2,.8,title,29,red,True)
 box(s,.55,5.95,12.2,.65,conclusion,20,teal,True)
 box(s,.55,6.75,12.2,.5,'Behr J, et al. Lancet Respir Med. 2021;9:476–486. PMID:33798455 | DOI:10.1016/S2213-2600(20)30554-3',11)
 s.notes_slide.notes_text_frame.text=note+'\n原文来源：https://doi.org/10.1016/S2213-2600(20)30554-3；PMID 33798455。机构存档PDF已读取；原文及附录的核验边界见证据摘要。'
 return s
notes=[
'本页先界定适用人群。RELIEF纳入德国17中心、四类非IPF进展性纤维化ILD，随机127例，吡非尼酮64例、安慰剂63例。两组均在原治疗基础上加试验药。主要终点是48周FVC占预计值百分比的绝对变化，不是死亡。数据来自原PDF第1页摘要及第3至4页方法。研究提前终止，因此不能把混合人群结果外推为每个亚型的确证疗效。',
'本页展示原文汇总统计，非个体原始数据。先读预设ITT秩ANCOVA主要分析P=0.043，再读Hodges–Lehmann差1.69个百分点及95%置信区间−0.65到4.03；区间跨零，必须保留。P值与该估计并非同一统计程序，不应将其强行解释为一致。第三行是预设纵向斜率敏感性分析，差3.53个百分点，95%置信区间0.21到6.86，含预设死亡处理；不能替代主要终点。来源为PDF第1页及结果部分。',
'安全性按原文计数报告：死亡1/64与5/63，严重感染类事件5/64与10/63。样本和事件数很少，不作死亡获益或安全等效判断。试验因招募缓慢触发的无效性中期分析提前终止，结论依赖缺失数据处理且人群异质。原PDF正文页眉与MED/Crossref DOI一致，但首页侧栏有不同DOI，已记录版本异常；未读取附录。该课件仅为技术测试件，不代表当前指南推荐或适应证审核。']
s=slide('RELIEF：非IPF进展性ILD的Ⅱb期试验','适用边界：四类疾病的混合人群；不能认定各亚型独立获益',notes[0])
box(s,.7,1.5,11.9,3.9,'随机 · 双盲 · 安慰剂对照 | 德国17中心\n127例随机：吡非尼酮64例 / 安慰剂63例\nCTD-ILD、纤维化NSIP、慢性过敏性肺炎、石棉肺\n既有治疗下仍进展；试验药加于原治疗\n主要终点：48周FVC占预计值百分比的绝对变化\n吡非尼酮递增至801 mg，每日3次',23)
s=slide('主要分析提示获益，效应大小仍有不确定性','提前终止 + 缺失数据：敏感性分析不能替代主要分析',notes[1])
data=[['分析（均为已发表汇总数据）','结果','统计边界'],['主要：ITT秩ANCOVA','P=0.043','SSD插补；死亡最差秩'],['Hodges–Lehmann组间差','1.69个百分点','95%CI −0.65～4.03'],['预设纵向斜率敏感性分析','3.53个百分点','95%CI 0.21～6.86']]
t=s.shapes.add_table(4,3,Inches(.7),Inches(1.6),Inches(11.9),Inches(3.5)).table
for i,row in enumerate(data):
 for j,val in enumerate(row):
  c=t.cell(i,j);c.text=val
  for p in c.text_frame.paragraphs:p.font.name='Noto Sans CJK SC';p.font.size=Pt(18);p.font.color.rgb=RGBColor.from_string(gray)
box(s,.75,5.25,11.8,.45,'差值方向：正值支持吡非尼酮；不同估计/检验方法应分别解读。',15)
s=slide('安全性与局限决定解读边界','谨慎支持进一步研究；不能据此宣称生存获益或指南推荐',notes[2])
box(s,.7,1.45,12,4.3,'死亡：1/64 vs 5/63（吡非尼酮 vs 安慰剂）\n严重感染类事件：5/64 vs 10/63\n仅为描述性事件计数；不证明死亡获益或安全等效\n招募缓慢触发无效性中期分析，研究提前终止\n缺失数据、人群异质性与样本量限制外推\n全文已核验；附录未获取；测试件尚未完成PPT渲染验收',22)
prs.save(P/'RELIEF_3slides_test.pptx')
(P/'speaker_notes_zh.md').write_text('\n\n'.join(f'## 第{i+1}页\n{n}' for i,n in enumerate(notes)))
(P/'outline.md').write_text('技术测试件，按用户三页任务直接执行；未走正式课件的大纲/样张审批流程。\n1. 研究设计与人群：127例、64/63，48周主要终点；原生文本。\n2. 结果：P值、效应量与CI、敏感性分析区别；原生表格。\n3. 安全性与局限：事件计数、提前终止及外推限制；原生文本。\n每页有来源脚注及中文讲者备注。')
print('Generated',P/'RELIEF_3slides_test.pptx')
