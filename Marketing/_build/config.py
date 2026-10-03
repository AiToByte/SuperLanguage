# -*- coding: utf-8 -*-
"""Marketing module configuration (市场营销英语)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_shared"))
from toolkit import ModuleConfig  # noqa: E402

CONFIG = ModuleConfig(
    MODULE="Marketing",
    PROJECT_TITLE="SuperLanguage 365-Day Marketing English Learning Plan",
    MODULE_TAG="Marketing · 市场营销英语",
    STAGE_TITLE="营销全链路 12 个月主题递进",
    DIFFICULTY_NOTE="B2–C1",
    EXAMPLE_NOTE="真实营销职场场景（调研、品牌、内容、投放、销售、数据复盘），且以目标词开头",
    ACCENT="7A3B1F",
    ACCENT_SOFT="F8F0EA",
    PHASES=[
        (1, 1, "营销基础与市场调研（Marketing Fundamentals & Research）",
         "Marketing Fundamentals & Research"),
        (2, 2, "消费者行为与人群洞察（Consumer Behaviour & Segmentation）",
         "Consumer Behaviour & Segmentation"),
        (3, 3, "品牌定位与品牌管理（Brand Positioning & Brand Management）",
         "Brand Positioning & Brand Management"),
        (4, 4, "内容营销与故事表达（Content Marketing & Storytelling）",
         "Content Marketing & Storytelling"),
        (5, 5, "社交媒体与社群运营（Social Media & Community）",
         "Social Media & Community"),
        (6, 6, "数字广告与效果投放（Digital Advertising & Paid Media）",
         "Digital Advertising & Paid Media"),
        (7, 7, "SEO 与可发现性（SEO & Discoverability）",
         "SEO & Discoverability"),
        (8, 8, "公关、活动与整合传播（PR, Events & Integrated Communications）",
         "PR, Events & Integrated Communications"),
        (9, 9, "销售流程与客户关系（Sales Process & CRM）",
         "Sales Process & CRM"),
        (10, 10, "营销数据分析与度量（Marketing Analytics & Measurement）",
         "Marketing Analytics & Measurement"),
        (11, 11, "电商、渠道与增长运营（E-commerce, Channels & Growth）",
         "E-commerce, Channels & Growth"),
        (12, 12, "营销战略与高阶商务表达（Marketing Strategy & Executive Expression）",
         "Marketing Strategy & Executive Expression"),
    ],
)
