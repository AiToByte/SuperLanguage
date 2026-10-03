# -*- coding: utf-8 -*-
"""IT module configuration (商务英语 + 科技行业术语)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_shared"))
from toolkit import ModuleConfig  # noqa: E402

CONFIG = ModuleConfig(
    MODULE="IT",
    PROJECT_TITLE="SuperLanguage 365-Day English Learning Plan",
    MODULE_TAG="IT · 商务英语 + 科技英语",
    STAGE_TITLE="六阶段主题递进（商务 + 科技双场景）",
    DIFFICULTY_NOTE="B2–C1",
    EXAMPLE_NOTE="真实科技公司与商务办公场景，且以目标词开头",
    ACCENT="1F3864",
    ACCENT_SOFT="F2F5FA",
    PHASES=[
        (1, 2, "团队协作、敏捷开发 (Agile/Scrum)、项目管理与日常沟通",
         "Team Collaboration, Agile/Scrum, Project Management & Everyday Communication"),
        (3, 4, "产品设计、用户体验 (UX/UI)、数据分析与指标增长",
         "Product Design, UX/UI, Data Analytics & Growth Metrics"),
        (5, 6, "技术架构、云计算、DevOps、网络安全与系统部署",
         "Architecture, Cloud, DevOps, Cybersecurity & Deployment"),
        (7, 8, "人工智能 (AI)、自动化、前沿科技趋势与数据挖掘",
         "AI, Automation, Emerging Technology & Data Mining"),
        (9, 10, "商务谈判、跨部门沟通、绩效评估与战略规划",
         "Negotiation, Cross-functional Communication, Performance & Strategy"),
        (11, 12, "行业风向、投融资、市场营销与高阶职场表达",
         "Industry Trends, Investment & Funding, Marketing & Executive Expression"),
    ],
)