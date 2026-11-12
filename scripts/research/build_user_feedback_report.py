"""Generate a review copy of the report in output/research without replacing the archived PDF."""

from pathlib import Path
import json, math, re
from html import escape
from urllib.parse import urlsplit
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle

ROOT = Path(__file__).resolve().parents[2]
RESEARCH_DIR = ROOT / 'docs/research/2026-11-06-user-feedback'
OUT = ROOT / 'output/research/Hiking_App_User_Feedback_Research_ZH_2026-11-06.pdf'
AUDIT = ROOT / 'tmp/research/user-feedback-layout-audit.json'
SOURCES = json.loads((RESEARCH_DIR / 'sources.json').read_text(encoding='utf-8'))
SRC = {s['id']: s for s in SOURCES}
OUT.parent.mkdir(parents=True, exist_ok=True)
AUDIT.parent.mkdir(parents=True, exist_ok=True)
pdfmetrics.registerFont(TTFont('CN', '/Library/Fonts/Arial Unicode.ttf'))
pdfmetrics.registerFont(TTFont('Hei', '/System/Library/Fonts/STHeiti Medium.ttc'))
pdfmetrics.registerFont(TTFont('Latin', '/System/Library/Fonts/Supplemental/Arial.ttf'))
pdfmetrics.registerFont(TTFont('LatinBold', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'))
pdfmetrics.registerFontFamily('CN', normal='CN', bold='Hei', italic='CN', boldItalic='Hei')

W, H = 595.276, 841.89
M, CW = 45, W - 90
INK = colors.HexColor('#18352E')
TEXT = colors.HexColor('#253A35')
MUTED = colors.HexColor('#60736B')
GREEN = colors.HexColor('#22735C')
PALE = colors.HexColor('#EDF4EF')
PAPER = colors.HexColor('#FBFCF9')
LINE = colors.HexColor('#D8E3DB')
ORANGE = colors.HexColor('#BA653D')

styles = {
    'body': ParagraphStyle('body', fontName='CN', fontSize=11.2, leading=19.0, textColor=TEXT, wordWrap='CJK', spaceAfter=0),
    'small': ParagraphStyle('small', fontName='CN', fontSize=9.1, leading=14.4, textColor=MUTED, wordWrap='CJK'),
    'table': ParagraphStyle('table', fontName='CN', fontSize=9.6, leading=15.5, textColor=TEXT, wordWrap='CJK'),
    'headcell': ParagraphStyle('headcell', fontName='Hei', fontSize=9.7, leading=14.5, textColor=colors.white, wordWrap='CJK'),
    'h2': ParagraphStyle('h2', fontName='Hei', fontSize=15.0, leading=21.5, textColor=INK, wordWrap='CJK'),
    'h3': ParagraphStyle('h3', fontName='Hei', fontSize=11.8, leading=18.4, textColor=GREEN, wordWrap='CJK'),
    'quote': ParagraphStyle('quote', fontName='Hei', fontSize=16.8, leading=27.0, textColor=INK, wordWrap='CJK'),
    'ref': ParagraphStyle('ref', fontName='CN', fontSize=9.5, leading=13.9, textColor=TEXT, wordWrap='CJK'),
    'refsmall': ParagraphStyle('refsmall', fontName='CN', fontSize=8.5, leading=12.7, textColor=MUTED, wordWrap='CJK'),
}

c = canvas.Canvas(str(OUT), pagesize=(W,H), pageCompression=1)
c.setTitle('徒步辅助软件用户反馈研究：AllTrails 与同类产品的痛点及项目机会')
c.setAuthor('Codex · 为 HikingProject 编制')
c.setSubject('中文桌面研究；跨平台用户反馈、竞品分析、MVP 建议；2026-11-06')
c.setKeywords('hiking, AllTrails, Gaia GPS, komoot, 用户反馈, 产品痛点, 徒步, MVP')
page = 0
y = 0
audits = []

def refs(*ids):
    return ' '.join(f'<link href="{escape(SRC[i]["url"], quote=True)}" color="#22735C">[S{i:02}]</link>' for i in ids)

def para(txt, style='body', x=M, width=CW, gap=9):
    global y
    p = Paragraph(txt, styles[style])
    _, ht = p.wrap(width, 1000)
    if y-ht < 53:
        raise RuntimeError(f'Page {page} overflow: y={y:.1f}, h={ht:.1f}, text={txt[:60]}')
    p.drawOn(c, x, y-ht)
    y -= ht + gap
    return ht

def start(title, section, subtitle=None):
    global page, y
    if page:
        audits.append({'page':page,'bottom_y':round(y,1)})
        c.showPage()
    page += 1
    c.setFillColor(PAPER); c.rect(0,0,W,H,fill=1,stroke=0)
    c.setStrokeColor(LINE); c.setLineWidth(.7); c.line(M,H-54,W-M,H-54)
    c.setFont('LatinBold',8.2); c.setFillColor(GREEN); c.drawString(M,H-39,'HIKING / PRODUCT RESEARCH')
    c.setFont('CN',8.3); c.setFillColor(MUTED); c.drawRightString(W-M,H-39,section)
    c.setFont('CN',8); c.drawString(M,29,'公开资料桌面研究  |  检索截止 2026-11-06')
    c.setFont('Latin',8.5); c.drawRightString(W-M,29,f'{page:02} / 15')
    c.bookmarkPage(f'page{page}')
    c.addOutlineEntry(title, f'page{page}', level=0, closed=False)
    y = H - 78
    p = Paragraph(title, ParagraphStyle('title',fontName='Hei',fontSize=22,leading=31,textColor=INK,wordWrap='CJK'))
    _,ht=p.wrap(CW,1000); p.drawOn(c,M,y-ht); y -= ht+10
    if subtitle: para(subtitle,'small',gap=17)
    else: y -= 8

def h2(t): para(t,'h2',gap=9)
def h3(t): para(t,'h3',gap=5)
def note(t, tone='green'):
    global y
    width=CW; pad=13
    p=Paragraph(t,styles['small']); _,ht=p.wrap(width-2*pad,1000)
    if y-ht-2*pad < 52: raise RuntimeError(f'Note overflow p{page}')
    c.setFillColor(PALE if tone=='green' else colors.HexColor('#F8EEE5'))
    c.roundRect(M,y-ht-2*pad,width,ht+2*pad,5,fill=1,stroke=0)
    c.setFillColor(GREEN if tone=='green' else ORANGE); c.rect(M,y-ht-2*pad,3,ht+2*pad,fill=1,stroke=0)
    p.drawOn(c,M+pad,y-ht-pad); y -= ht+2*pad+13

def table(headers,rows,widths):
    global y
    data=[[Paragraph(str(t),styles['headcell']) for t in headers]]
    data += [[Paragraph(str(t),styles['table']) for t in row] for row in rows]
    t=Table(data,colWidths=widths,hAlign='LEFT')
    t.setStyle(TableStyle([
      ('BACKGROUND',(0,0),(-1,0),GREEN),('VALIGN',(0,0),(-1,-1),'TOP'),
      ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
      ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
      ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,PALE]),
      ('LINEBELOW',(0,0),(-1,0),.5,GREEN),('LINEBELOW',(0,1),(-1,-1),.4,LINE),
    ]))
    _,ht=t.wrap(CW,1000)
    if y-ht<53: raise RuntimeError(f'Table overflow page {page} ({ht:.1f}, y={y:.1f})')
    t.drawOn(c,M,y-ht); y -= ht+13

def pain(n,title,level,feedback,interpretation,opportunity):
    global y
    h2(f'{n:02}  {title}')
    para(level,'small',gap=7)
    para('<b>证据：</b>'+feedback,gap=7)
    para('<b>需求含义：</b>'+interpretation,gap=7)
    note('<b>项目切入点：</b>'+opportunity)

# 1 / Cover
start('徒步辅助软件\n用户反馈研究'.replace('\n','<br/>'),'RESEARCH BRIEF')
para('AllTrails 与同类产品的痛点、证据边界及项目机会','h3',gap=15)
para('研究日期：2026 年 11 月 6 日  |  中文报告  |  面向项目立项','small',gap=17)

# Native vector topographic illustration, intentionally decorative rather than geographic.
top=y; boxh=159
c.setFillColor(INK); c.roundRect(M,top-boxh,CW,boxh,7,fill=1,stroke=0)
c.saveState(); p=c.beginPath(); p.rect(M,top-boxh,CW,boxh); c.clipPath(p,stroke=0)
for k in range(10):
    p=c.beginPath()
    for j in range(100):
        x=M+j*CW/99
        yy=top-boxh+20+k*14+14*math.sin(j*.07+k*.3)+7*math.sin(j*.17+k*.1)
        if j==0:p.moveTo(x,yy)
        else:p.lineTo(x,yy)
    c.setStrokeColor(colors.HexColor('#416758'));c.setLineWidth(.65);c.drawPath(p)
p=c.beginPath();p.moveTo(M+40,top-boxh+35);p.curveTo(M+150,top-boxh+105,M+210,top-boxh+15,M+270,top-boxh+91);p.curveTo(M+320,top-boxh+150,M+390,top-boxh+61,M+460,top-boxh+121)
c.setStrokeColor(colors.HexColor('#EEC584'));c.setLineWidth(2.6);c.drawPath(p)
for xx,yy in [(M+40,top-boxh+35),(M+460,top-boxh+121)]:
    c.setFillColor(colors.HexColor('#EEC584'));c.circle(xx,yy,4,fill=1,stroke=0)
c.restoreState();y=top-boxh-22
para('最值得优先验证的产品方向：<br/>让用户知道信息是否可靠，并在无网时顺利完成徒步。','quote',gap=15)
para('本次检索反复出现的摩擦，集中在离线可用性、路线与路况可信度、导航界面、付费预期和隐私控制。它们跨越多个产品，但公开评论不能用来计算故障率。'+refs(3,4,10,13,22,23),gap=13)
table(['研究覆盖','交付内容'],[
 ['8 款主要参照产品<br/>另补充 2 款中文产品','9 类痛点与证据强弱<br/>AllTrails 专项复核'],
 ['36 个精选来源页面<br/>用户反馈＋官方资料＋评测','MVP 优先级、验证任务<br/>可点击引用与来源目录'],
],[CW*.44,CW*.56])
para('编制方式：AI 辅助公开网页检索与归纳，未进行用户访谈或应用实测。报告中的产品建议均为待验证假设。','small')

# 2 / Method
start('研究范围与阅读方法','01 / 方法','以可追溯反馈发现问题，再用官方资料校准产品事实。')
h2('覆盖哪些产品与场景')
para('主要参照 AllTrails、Gaia GPS、komoot、Wikiloc、Outdooractive、FarOut、Organic Maps 和 Plan My Walk；补充两步路、六只脚。覆盖找路线、行前准备、途中导航、记录、分享与订阅体验。新西兰作为本地化案例，不预设你的最终市场。')
h2('如何检索与筛选')
para('使用中英文组合检索：产品名＋review / complaint / offline / GPS / battery / subscription / privacy，以及“离线地图、轨迹、闪退、广告、评价”等。渠道包括 Reddit、App Store、Trustpilot、GitHub 用户讨论、产品帮助中心及 NZ Mountain Safety Council。')
para('重点采用 2025-2026 年材料；少量较早评论用于观察长期需求，并在正文标明。36 个来源是精选页面，不是 36 名用户或完整评论样本。同一帖子下的附和不算独立抽样；转述同一事件的文章不重复计作新证据。')
table(['证据类别','本报告怎样使用'],[
 ['用户原始反馈','证明某种体验或需求被报告过；不自动证明原因、普遍程度或当前仍存在。'],
 ['官方说明／品牌回复','核对当前功能、已知限制与回应；修复计划不等于修复效果已经实测。'],
 ['编辑评测','作为交叉参照，尤其用于产品定位；不把编辑意见当作用户总体意见。'],
 ['研究判断','从反馈推导项目机会、优先级和验收建议；明确标为建议或假设。'],
],[CW*.27,CW*.73])
note('<b>证据强弱：</b>“较强”表示多来源出现相似主题，或有官方资料佐证；“中等”表示少量具体案例；“探索性”表示样本旧、稀少或只是相邻场景。该等级衡量结论依据，不是投诉发生率。')
para('<b>局限：</b>公开网页受登录、地区和搜索排序影响，英文论坛材料更丰富；负面关键词检索会放大不满。未全量抓取、未访谈、未实际安装测试，不计算投诉百分比或跨商店星级排名。排除了无法追溯的 SEO 汇编、夸张救命宣传与无来源统计。','small')
para('<b>阅读导航：</b>第 3 页竞品；第 4 页 AllTrails；第 5-9 页痛点；第 10 页地域；第 11-12 页项目与验证；第 13-15 页来源。正文 [Sxx] 和来源标题均可点击。','small')

# 3 / Landscape
start('竞品对照：各自解决了什么','02 / 竞品','这里比较价值与摩擦，不以单一评分给产品排座次。')
table(['产品／主要价值','反馈与限制','对新项目的提示'],[
 ['<b>AllTrails</b><br/>路线发现、社区评论','用户喜欢找路线；也报告离线入口、导航干扰。'+refs(1,4,5),'保留低门槛发现体验；重点验证途中使用。'],
 ['<b>Gaia GPS</b><br/>地图、图层与记录','离线下载需会员；历史下载异常及隐私预期冲突。'+refs(9,10,11,12),'专业地图能力之外，下载状态和默认权限也影响信任。'],
 ['<b>komoot</b><br/>路线规划与跟随','规划能力获赞；离线无法自动重算或编辑。'+refs(13,14),'规划完成不代表偏航后仍能完成任务。'],
 ['<b>Wikiloc</b><br/>用户轨迹与地区覆盖','发现路线受挫；重复或低质量轨迹需筛选。'+refs(17,21),'路线数量需要配合去重、筛选和质量解释。'],
 ['<b>Outdooractive</b><br/>规划、记录与领队使用','有路线编辑、帮助入口投诉；也有 GPX 和人工支持好评。'+refs(22),'高频编辑操作和帮助入口应容易找到。'],
 ['<b>FarOut</b><br/>长线指南、航点信息','水源等评论具有价值；更新后步骤与界面负担被抱怨。'+refs(23,24,25),'结构化航点信息值得借鉴；保持任务路径稳定。'],
 ['<b>Organic Maps</b><br/>免费离线地图、隐私','无需注册；路网缺失和定制规划仍有用户诉求。'+refs(27,28),'低成本与隐私不能独自解决路线信息质量。'],
 ['<b>Plan My Walk</b><br/>新西兰行前规划','整合官方提醒与行程信息；定位为规划工具。'+refs(30,31,32),'本地权威信息与导航体验之间存在整合空间。'],
],[CW*.24,CW*.43,CW*.33])
note('<b>一个容易误判的比较：</b>Wikiloc 免费离线底图与 Premium 的 Outdoor Navigation 是不同能力；Gaia 免费 GPS 定位也不等于免费离线地图。应按完整使用任务比较，而非只看“支持离线”标签。'+refs(9,18,19,20))

# 4 / AllTrails
start('AllTrails：问题需要按版本拆开','03 / 重点产品','保留其路线发现优势，核对历史投诉是否已经被回应。')
h2('值得保留的基础体验')
para('App Store 的可见评论赞赏路线发现、行前评论与记录；Wikiloc 用户的对比帖也认为 AllTrails 在陌生地区浏览和按距离、环线筛选更顺手。这些是具体体验，不代表全部用户，但说明新项目需要兼顾“找到想去的地方”。'+refs(1,17))
table(['时间／证据','反馈或变化','研究结论'],[
 ['2025-06<br/>离线登录屏 '+refs(3),'用户称已下载地图被登录页面阻挡；品牌账号提出潜在修复版本。','历史故障有回应。未实测，不断言该问题至今未修复。'],
 ['2025-11<br/>会员调整 '+refs(6),'品牌承认 Peak 推出时的访问变化引发不满，宣布免费桌面规划等调整。','“所有自定义规划都必须 Peak”是过度概括。'],
 ['2026-04<br/>离线检索 '+refs(4),'用户称下载后的公园／路线在离线入口中难以找到；品牌称非预期行为。','地图文件存在、离线内容可找到，是两项不同验收。'],
 ['2026 年<br/>地图界面 '+refs(5),'Android 用户要求地图优先；回复说明部分面板可折叠，用户仍抱怨状态重置。','包含可发现性和状态保持问题，不能简单写成“无法折叠”。'],
],[CW*.22,CW*.43,CW*.35])
h2('截至检索日，官方已经提供哪些能力')
para('2026-10-28 的帮助页把离线路线／公园／区域、Trail Conditions、Community Heatmap 等列入 Plus；Peak 包含进阶路线构建及多日规划工具。因此，“添加天气、热力图或 AI 规划”本身不足以构成清晰差异。'+refs(2))
note('<b>更有价值的问题：</b>用户能否解释地图为什么可信、证明所需内容已经离线可用，并在岔路口快速完成一次操作？这比只比较功能数量更适合作为项目研究方向。')

# 5 / Priority overview
start('九类痛点与建议优先级','04 / 痛点总览','优先级是本报告的项目判断；不是市场投诉排名。')
table(['痛点','证据强度','关键影响','建议'],[
 ['01 离线任务不完整 '+refs(3,4,10,14),'较强','到达无网区域才发现地图、搜索或改线不可用','P0'],
 ['02 路线与路况可信度 '+refs(8,15,28),'中等','路线存在、允许通行、当前可走被混淆','P0'],
 ['03 难度与个人能力不匹配 '+refs(1,29),'探索性','简单标签难以表达技术与体能要求','P1'],
 ['04 路线发现与信息筛选 '+refs(17,21),'中等','陌生地区难找合适路线；重复轨迹增加负担','P1'],
 ['05 GPS、后台记录与电量 '+refs(7,35),'较强（机制有佐证）','定位异常、轨迹断点和长时使用的不确定性','P0'],
 ['06 导航界面与改版负担 '+refs(5,13,22,23),'较强','地图被遮挡；常用功能难找、路径变长','P0'],
 ['07 订阅与权益预期 '+refs(6,13,36),'较强','收费变化与推销干扰引发不信任','P1'],
 ['08 隐私与分享控制 '+refs(11,12),'中等（默认值有佐证）','公开范围与用户预期不一致','P0 基线'],
 ['09 跨工具与设备断层 '+refs(11,16,33),'中等','路线、版本、航点与提醒在多处维护','P1'],
],[CW*.39,CW*.20,CW*.31,CW*.10])
note('<b>P0：</b>首版必须具备的可靠性与基本使用条件。<b>P1：</b>原型阶段重点验证，再决定投入。离线、隐私和状态提示是进入该品类的基础；差异化更可能来自它们与可信路线信息、低操作负担的组合。')
para('未给出“多少百分比用户抱怨某问题”：当前样本不是随机抽样，商店展示和论坛参与方式也不同。个别高影响故障即使频率未知，也值得列为可靠性测试场景。','small')

# 6 / offline + trust
start('关键时刻：能用，且知道能否相信','05 / 痛点详解')
pain(1,'离线承诺与实际任务脱节','证据较强 | AllTrails、Gaia GPS、komoot、Wikiloc',
 'AllTrails 有离线入口和登录阻挡报告；Gaia 下载异常案例后续恢复。komoot 官方明确，离线跟随可用，但自动重算、编辑、实时位置分享需联网。'+refs(3,4,10,14),
 '“离线”是多项能力：打开地图、查找路线、读取航点、查看缓存信息、记录与返程。用户容易把收藏、下载路线和下载底图理解成同一件事。Wikiloc 的流程也要求分别保存路线和地图。'+refs(19),
 '制作“出发行程包”：显示地图覆盖范围、路线、航点、内容时间和下载校验结果；提供一键离线演练。已进入行程时保留本地读取能力，账户更新不打断当前任务。')
pain(2,'地图上的线不能解释当前通行条件','证据中等 | 路网问题与可通行性需要分别判断',
 'komoot 私地／消失道路案例来自骑行，只能辅助说明共用路网风险；Organic Maps 的徒步讨论提到 OSM 缺路与连接错误。AllTrails 官方则已使用私地和关闭标签。'+refs(15,28,8),
 '路线几何、访问权限、季节路况和最后核实时间是不同信息。热门轨迹或热力数据只能说明有人活动过；从这些资料不能推出“今天适合我走”。',
 '每段路线显示来源、更新时间及“官方／社区／未核实”状态；将封闭、泥泞、积雪、水源等报告绑定路段与发生日期。冲突信息并排展示，过期信息明确降级。')
para('以上设计是研究建议。离线缓存的路况需要显示缓存时间；它不会因下载完成就变成实时信息。','small')
h3('容易遗漏的内容：照片与航点评论')
para('FarOut 官方教程提醒提前下载地图类型与航点照片，并通过评论日期判断信息时效。由此可见，行程包的验收不能只检查底图；也应明确哪些辅助资料已保存、哪些需要连接后才能更新。'+refs(26),gap=0)

# 7 / fit + discovery
start('出发之前：适合我，也找得到','06 / 痛点详解')
pain(3,'单一难度标签难表达个人适配','探索性证据 | 需求合理，但近期独立样本不足',
 'AllTrails 2020 年评论指出 easy / moderate / hard 与个人感受不总一致；Organic Maps 2026 年单例称等高线不足以判断山脊陡峭程度。两者都提示“看懂难度”需要更多信息。'+refs(1,29),
 '本研究不能据此断言当前所有难度评级失准。可验证的假设是：体能、技术暴露、路面、过河、负重和季节，比一个综合标签更能帮助选择。',
 '保留距离与爬升等客观信息，将体力需求和技术需求分开；先让用户选择儿童同行、避开暴露路段、可用时长等条件。推荐结果说明匹配原因，不给无依据的安全分数。')
pain(4,'有很多轨迹，仍难找到一条合适路线','证据中等 | Wikiloc 对比帖与编辑评测交叉支持',
 'Wikiloc 用户在旅行时难以按所在区域发现路线；The Trek 指出用户轨迹库中存在重复与质量筛选负担。与此同时，AllTrails 的浏览方式被部分用户视为优势。'+refs(17,21),
 '需求从“给我更多路线”转向“在有限时间内理解差异并做决定”。重复轨迹、起点不同和过时记录，会让路线数量变成比较成本。',
 '按路线主体合并重复记录，再展示不同起点／方向／长度的变体；比较预计时长、爬升、交通、设施与近期报告。允许用户直接筛“环线、半天内、最近有人反馈”。')
note('<b>冷启动策略：</b>先做一个区域内少量可核对路线，手工建立来源和更新流程。路线数量、社区活跃度与数据维护成本需要分别验证；不以复制其他平台内容作为数据来源方案。')

# 8 / recording + interface
start('行进途中：少操作，状态清楚','07 / 痛点详解')
pain(5,'定位、后台记录与电量难同时放心','机制证据较强 | 实际耗电差异尚未实测',
 'AllTrails 的 Android 指南说明后台省电策略可能中断记录，且定位模式有功耗差异；六只脚商店页面也提示后台 GPS 用电。评论中的轨迹问题不能一律归因于地图算法。'+refs(7,35),
 '用户通常只看到一条突然拉直的轨迹，不知道是权限、系统暂停、定位质量还是应用异常。定位显示、记录保存和统计精度也应分开评估。',
 '行前检查权限和后台记录；途中显示最后定位时间、精度范围与记录状态。中断段明确标记，不用直线伪装连续轨迹；提供轻量导航模式，并在多机型上记录每小时耗电。')
pain(6,'功能越来越多，地图和关键操作被挤压','跨产品证据较强 | AllTrails、FarOut、Outdooractive、komoot',
 'AllTrails 用户要求地图优先；FarOut 用户抱怨切换剖面、路线等步骤增多，Android 评论区曾被按钮挤占；Outdooractive 用户报告反转路线或打印入口难找。'+refs(5,23,24,22),
 '这里既有界面密度，也有操作可发现性与改版学习成本。部分操作实际存在，因此修复方向可能是减少步骤、记住状态，而非增加功能。',
 '导航默认展示地图、当前位置和下一关键点；统计按需展开，折叠状态持续保留。回到当前位置、返程轨迹、暂停和保存设置固定入口。导航期间不插入评分或升级提示。')
para('需保留反例：FarOut 同帖不同机型体验不同；Outdooractive 也有路线规划与支持服务好评。优先复现具体场景，不把界面争议写成全平台失效。'+refs(24,22),'small')

# 9 / business privacy interoperability
start('长期信任：费用、隐私与可迁移性','08 / 痛点详解')
h2('07  订阅问题不只在于价格')
para('AllTrails 的会员争议及后续调整、komoot 的订阅投诉，以及用户对分享／升级提示的抱怨，指向“买到什么、以后会否变化、如何退出”的不确定性。没有证据支持所有人都拒绝付费。'+refs(6,13,36),gap=7)
note('<b>建议：</b>用具体任务解释免费与收费边界；显示续费日期和购买渠道；导航中不促销。地区包、短期通行证、年度方案仅作为定价访谈选项，不能当作已验证需求。')
h2('08  轨迹分享默认值影响信任')
para('Gaia 用户抱怨轨迹公开并提出迁移需求；官方现行文档说明接受隐私弹窗后，新轨迹默认公开，但既有轨迹保留原设置。两者并不完全一致，不能直接认定历史数据被统一改公开。'+refs(11,12),gap=7)
note('<b>建议：</b>新轨迹默认私密；分享时预览接收者看到的范围，支持隐藏起终点与撤销。批量导出和可见性检查应容易完成；“与同行者分享”与“向公众发布”用不同入口。')
h2('09  多工具协作带来版本与信息断层')
para('新西兰讨论中出现搭配规划、地图和官方封闭信息的做法；Gaia 用户需要无网分享 GPX／KML。komoot 明确，已导出的 GPX 与已传送设备的路线不会随原路线自动更新。'+refs(11,16,33),gap=7)
note('<b>建议：</b>以一个行程组织路线、关键点、提醒与备用文件；标注路线版本和导出时间。首版优先做好 GPX 导入／导出和离线行程摘要，之后再评估手表与多平台双向同步。')
para('这三项首先解决控制感。用户愿意迁移的程度、可接受收费和设备生态，都还需要访谈验证。','small')

# 10 / local
start('地域视角：中文产品与新西兰','09 / 本地化','不同地区的数据与使用习惯，可能比通用功能表更影响体验。')
h2('两步路、六只脚：作为补充样本')
para('<b>两步路：</b>商店页面呈现轨迹、无网记录、约伴和社区等价值；可见历史评论既赞赏记录能力，也在 2019 年提到改版复杂化。2026 年更新记录含广告展示限制、弱网体验及卡顿修复。它们说明产品持续调整，不能证明这些旧问题目前仍普遍存在。'+refs(34))
para('<b>六只脚：</b>可见 2025 年评论提到闪退、易用性与广告；页面同时列出离线地图和轨迹能力。但这次可访问的台湾区页面只有 6 个评分，样本很小，不能代表中国大陆总体用户，更不适合直接与 AllTrails 星级比较。'+refs(35))
note('<b>中文市场待验证：</b>路线来源与最近通行情况、领队分享轨迹、离线下载步骤、广告干扰、不同手机后台记录。公开中文网页原始反馈较少，下一阶段应补充本地访谈，不用转载测评凑结论。')
h2('新西兰：已有本地规划工具可作为参照')
para('Plan My Walk 整合 DOC／地方机构提醒、MetService 天气及行程共享，并提供路线、营地和山屋信息。其 FAQ 也承认路线库并不完整，支持下载行程 PDF。'+refs(31,32))
para('官方把它定位为规划工具，不应视为自动救援服务；2026 年现行页面又说明，符合设备、运营商和套餐要求时，可经卫星使用。因此不能沿用“离开蜂窝网络就一定不能访问”的旧概括。'+refs(30,31))
h2('给项目的本地化假设')
para('若先在新西兰试点，可选择一个可维护区域，把官方提醒、出行日期、路线来源与离线行程包放在同一流程。面向中文用户时优先验证双语地名、难度解释和本地规则理解。以上是市场切入假设，尚未验证用户是否会切换产品或付费。')
para('离线位置、蜂窝实时分享与卫星连接是不同能力；任何共享状态都应显示最近上传时间和实际连接条件。','small')

# 11 / MVP
start('建议的首版：可信的离线行程助手','10 / 项目机会','以下为研究建议，不是已经验证的市场结论或开发承诺。')
note('<b>目标用户假设：</b>在一个地区进行半日或一日徒步、需要自己选路线和做准备的人。<br/><b>核心任务：</b>选定适合的路线，知道信息更新时间，把行程准备好，并在无网时看图、跟随和返程。')
table(['优先级','首版范围','为什么先做'],[
 ['P0','少量可核对路线；来源、最后核实时间、关闭／未知状态','建立可解释的数据基础，控制维护成本。'],
 ['P0','地图＋路线＋航点的离线包；下载完成校验；离线演练','直接回应下载成功但实际任务失败的反馈。'],
 ['P0','地图优先导航；定位／记录状态；已走轨迹和本地保存','可靠完成途中核心任务，减少操作负担。'],
 ['P0','默认私密；本地读取；分享范围预览','让用户清楚控制轨迹和行程可见性。'],
 ['P1','结构化路况上报；发生时间与有效期；冲突并列','把社区内容变成可判断的信息。'],
 ['P1','距离／爬升／路面等筛选；路线变体；GPX 导入导出','降低选择与迁移成本，再验证复杂规划需求。'],
],[CW*.11,CW*.53,CW*.36])
h2('暂缓投入的方向')
para('全国或全球大而全路线库、完整社交动态流、多品牌手表双向同步、多日自动规划、物种识别和泛化 AI 聊天。它们会增加内容、同步与维护成本；当前证据更支持先验证一个完整可靠的徒步任务。')
h2('数据机制比功能名字更关键')
para('路线、路段、航点和路况报告分开存储；每条报告保留发生时间、提交时间、来源和适用范围。首版可人工核对重点路线；再验证授权数据接口、更新周期和内容维护成本。AI 如用于摘要，应保留原始出处，缺信息时明确留空。')

# 12 / Validation
start('下一步验证：用真实任务检验机会','11 / 研究与验收','以下样本数和阈值是建议的探索方案，不是已完成研究或行业标准。')
h2('先验证用户是否真的需要换工具')
para('建议访谈 12-15 人，覆盖新手、经常徒步者和领队；不要只招募不满意的用户。让对方复盘最近一次真实徒步：用了哪些工具、哪一步失败、如何补救、是否付费，以及保留现有产品的原因。')
table(['验证任务','观察指标／建议验收'],[
 ['无网冷启动：下载后重启，关闭网络，再找路线','地图、轨迹、航点可读；本地搜索可用；不被登录页阻挡。测试包内任务全部完成。'],
 ['缺文件／缓存过期／下载中断','不显示虚假的“已就绪”；指出缺失范围和更新时间；可恢复下载。'],
 ['锁屏记录、切换应用、系统回收后恢复','记录中断可见；已保存轨迹可恢复。分别记录定位误差、缺段与电量，不混成一个分数。'],
 ['岔路口查看、回到当前位置、查看返程轨迹','记录成功率、操作次数与耗时。核心入口目标不超过 2 次操作，并测试设置是否保持。'],
 ['同一路线出现旧好评与新关闭提醒','用户能识别最新来源和不确定性；不能只因星级或热度忽略冲突。'],
 ['导入／导出／分享','轨迹点、时间与航点信息符合约定；私密数据不会默认公开；收件方能看懂版本和时间。'],
],[CW*.37,CW*.63])
h2('四周探索节奏')
para('<b>第 1 周：</b>访谈与竞品任务观察，选定区域和用户。<br/><b>第 2 周：</b>制作行前检查与导航原型，测试信息理解。<br/><b>第 3 周：</b>实现最小离线闭环，做多机型中断恢复测试。<br/><b>第 4 周：</b>在可控、熟悉路线做实地验证，记录失败，再决定扩大范围。')
note('<b>继续投入的依据：</b>用户在真实任务中更快判断信息、能独立准备离线包，并愿意在下一次行程继续使用。<br/><b>仍待回答：</b>首发地区、用户经验、手机平台、数据维护方式、可接受费用，以及相对现有工具的切换收益。')

# 13-15 / References
for group in range(3):
    lo=group*12+1; hi=lo+11
    start(f'来源目录 {group+1} / 3','12 / 可追溯来源',f'S{lo:02}-S{hi:02}  |  所有来源访问日期：2026-11-06。点击标题打开原文。')
    for s in SOURCES[group*12:(group+1)*12]:
        domain=urlsplit(s['url']).netloc.removeprefix('www.')
        title=f'<b>[S{s["id"]:02}]</b> <link href="{escape(s["url"],quote=True)}" color="#22735C">{escape(s["title"])}</link>'
        para(title,'ref',gap=2)
        para(escape(f'{s["publisher"]} | {s["type"]} | {s["date"]}'),'refsmall',gap=2)
        para(escape(s['scope']),'refsmall',gap=6)
    if group==2:
        para('日期说明：少数页面只提供相对时间，或搜索索引与页面相对日期不一致，已保留不确定性。产品能力以检索时可见官方说明校准，未验证所有地区、账户或设备。','small',gap=0)

audits.append({'page':page,'bottom_y':round(y,1)})
assert page==15,page
c.save()
AUDIT.write_text(json.dumps(audits,ensure_ascii=False,indent=2), encoding='utf-8')
print(str(OUT))
print(json.dumps(audits,ensure_ascii=False))
