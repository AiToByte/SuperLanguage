# -*- coding: utf-8 -*-
"""Finance module configuration (财务商务英语)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_shared"))
from toolkit import ModuleConfig  # noqa: E402

CONFIG = ModuleConfig(
    MODULE="Finance",
    PROJECT_TITLE="SuperLanguage 365-Day Finance English Learning Plan",
    MODULE_TAG="Finance · 财务商务英语",
    STAGE_TITLE="财务全流程 12 个月主题递进",
    DIFFICULTY_NOTE="B2–C1",
    EXAMPLE_NOTE="真实财务职场场景（结账、预算、审计、估值、投融资），且以目标词开头",
    ACCENT="1F5C3F",
    ACCENT_SOFT="EEF6F1",
    PHASES=[
        (1, 1, "财务基础与会计术语（Accounting Fundamentals & Terminology）",
         "Accounting Fundamentals & Terminology"),
        (2, 2, "三大报表与勾稽关系（Financial Statements & Articulation）",
         "Financial Statements & Articulation"),
        (3, 3, "成本核算与费用管理（Cost Accounting & Expense Management）",
         "Cost Accounting & Expense Management"),
        (4, 4, "预算、预测与计划（Budgeting & Forecasting）",
         "Budgeting & Forecasting"),
        (5, 5, "资金、现金与营运资本（Treasury, Cash & Working Capital）",
         "Treasury, Cash & Working Capital"),
        (6, 6, "财务分析与关键指标（Financial Analysis & KPIs）",
         "Financial Analysis & KPIs"),
        (7, 7, "投资与资本预算（Investment & Capital Budgeting）",
         "Investment & Capital Budgeting"),
        (8, 8, "融资、股权与资本结构（Financing, Equity & Capital Structure）",
         "Financing, Equity & Capital Structure"),
        (9, 9, "税务、审计与内控（Tax, Audit & Internal Control）",
         "Tax, Audit & Internal Control"),
        (10, 10, "估值方法与建模（Valuation & Financial Modelling）",
         "Valuation & Financial Modelling"),
        (11, 11, "上市公司、披露与资本市场（Public Markets, Disclosure & Markets）",
         "Public Markets, Disclosure & Capital Markets"),
        (12, 12, "财务战略与高阶商务表达（Financial Strategy & Executive Expression）",
         "Financial Strategy & Executive Expression"),
    ],
)