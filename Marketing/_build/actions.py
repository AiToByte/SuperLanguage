# -*- coding: utf-8 -*-
"""Marketing module action tree: 9 scenarios (7 shared + marketing office + incremental)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_shared"))
from common_actions import build_categories  # noqa: E402

OFFICE_NOTE = ("本场景为市场营销专属办公动作库，覆盖调研与洞察、品牌与内容、"
               "投放与渠道、活动与公关、数据与复盘五大工作块，以及日常办公动作。")

OFFICE_ACTIONS = [
    # --- 调研与洞察 ---
    ("做桌面研究", "doing desk research"),
    ("设计问卷", "designing the questionnaire"),
    ("发放问卷", "distributing the survey"),
    ("清洗数据", "cleaning the data"),
    ("做交叉分析", "cross-tabulating the findings"),
    ("撰写调研报告", "writing the research report"),
    ("做用户访谈", "interviewing users"),
    ("整理竞品资料", "compiling competitor materials"),
    ("做市场规模测算", "sizing the addressable market"),
    ("建立调研看板", "building the research dashboard"),
    ("验证假设", "testing the hypothesis"),
    ("总结关键发现", "summarising the key findings"),
    # --- 品牌与内容 ---
    ("撰写品牌故事", "writing the brand story"),
    ("打磨文案", "polishing the copy"),
    ("写标题", "writing headlines"),
    ("写产品描述", "writing product descriptions"),
    ("准备发布会材料", "preparing the launch deck"),
    ("校对外文物料", "proofreading the materials"),
    ("统一品牌语调", "aligning the brand tone"),
    ("整理素材库", "organising the asset library"),
    ("做内容日历", "planning the content calendar"),
    ("撰写邮件营销", "writing the email campaign"),
    ("撰写社媒文案", "writing the social posts"),
    ("审核合规表述", "checking the advertising claims"),
    # --- 投放与渠道 ---
    ("搭建广告计划", "building the ad campaign"),
    ("设置定向", "setting the targeting"),
    ("分配预算", "allocating the budget"),
    ("监控投放数据", "monitoring campaign data"),
    ("调整出价", "adjusting the bids"),
    ("撰写落地页", "writing the landing page"),
    ("做A/B测试", "running the A/B test"),
    ("计算转化率", "calculating the conversion rate"),
    ("优化转化路径", "optimising the conversion path"),
    ("管理合作渠道", "managing partner channels"),
    ("撰写投放复盘", "writing the campaign review"),
    ("对接代理商", "briefing the agency"),
    # --- 活动与公关 ---
    ("策划活动", "planning the campaign"),
    ("撰写活动方案", "writing the campaign proposal"),
    ("协调场地", "coordinating the venue"),
    ("筹备发布会", "preparing the launch event"),
    ("准备媒体通稿", "preparing the press release"),
    ("安排媒体采访", "arranging the media interview"),
    ("管理嘉宾名单", "managing the guest list"),
    ("现场执行", "running the on-site event"),
    ("跟进媒体反馈", "following up on media coverage"),
    ("撰写危机声明", "writing the holding statement"),
    ("维护公关日历", "maintaining the PR calendar"),
    ("邀约媒体", "pitching to journalists"),
    # --- 数据与复盘 ---
    ("搭建指标体系", "setting up the metrics framework"),
    ("做数据看板", "building the dashboard"),
    ("分析转化漏斗", "analysing the funnel"),
    ("拆解渠道表现", "breaking down channel performance"),
    ("计算客户获取成本", "calculating customer acquisition cost"),
    ("计算生命周期价值", "calculating lifetime value"),
    ("做周度复盘", "running the weekly review"),
    ("做月度复盘", "running the monthly review"),
    ("输出数据结论", "drawing conclusions from the data"),
    ("对齐指标口径", "aligning metric definitions"),
    ("检查数据质量", "checking data quality"),
    ("汇报营销效果", "reporting marketing performance"),
    ("提出优化建议", "proposing optimisation ideas"),
    ("搭建归因模型", "building the attribution model"),
    ("跟踪竞品动态", "tracking competitor activity"),
    # --- 日常办公 ---
    ("敲键盘", "typing"),
    ("盯屏幕", "staring at the screen"),
    ("记笔记", "taking notes"),
    ("翻页", "turning the page"),
    ("头脑风暴", "brainstorming"),
    ("整理桌面", "clearing my desk"),
    ("写邮件", "writing an email"),
    ("发邮件", "sending an email"),
    ("回复邮件", "replying to emails"),
    ("开线上会", "joining an online meeting"),
    ("共享屏幕", "sharing my screen"),
    ("把自己静音", "muting myself"),
    ("接电话", "answering a phone call"),
    ("打印文件", "printing the document"),
    ("扫描文件", "scanning the document"),
]

INCREMENTAL_EXTRA = [
    ("处理舆情", "handling negative chatter"),
    ("回应差评", "responding to a bad review"),
    ("紧急下架物料", "pulling material from publication"),
    ("补发遗漏名单", "resending a missed mailing list"),
    ("核对投放数据异常", "checking a spend anomaly"),
    ("更新竞品监测表", "updating the competitor tracker"),
    ("准备客户演示", "preparing the client demo"),
    ("配合拍摄现场", "supporting the shoot"),
    ("处理活动物料延误", "resolving a logistics delay"),
    ("接待媒体来访", "hosting a media visit"),
]

CATEGORIES = build_categories(
    OFFICE_ACTIONS,
    incremental_extra=INCREMENTAL_EXTRA,
    office_note=OFFICE_NOTE,
    office_name_cn="市场营销办公与工作日常",
    office_name_en="Marketing Office & Desk Routine",
)
