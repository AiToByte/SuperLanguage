# -*- coding: utf-8 -*-
"""Legal module configuration (法律英语)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_shared"))
from toolkit import ModuleConfig  # noqa: E402

CONFIG = ModuleConfig(
    MODULE="Legal",
    PROJECT_TITLE="SuperLanguage 365-Day Legal English Learning Plan",
    MODULE_TAG="Legal · 法律英语",
    STAGE_TITLE="法律实务 12 个月主题递进",
    DIFFICULTY_NOTE="B2–C1",
    EXAMPLE_NOTE="真实法律实务场景（合同、诉讼、合规、谈判、知识产权），且以目标词开头",
    ACCENT="5B3A29",
    ACCENT_SOFT="F7F0EC",
    PHASES=[
        (1, 1, "法律体系与法院结构（Legal System & Court Structure）",
         "Legal System & Court Structure"),
        (2, 2, "合同基础与条款语言（Contract Fundamentals & Clauses）",
         "Contract Fundamentals & Clauses"),
        (3, 3, "合同起草与修订（Contract Drafting & Revision）",
         "Contract Drafting & Revision"),
        (4, 4, "违约救济与争议解决（Breach, Remedies & Dispute Resolution）",
         "Breach, Remedies & Dispute Resolution"),
        (5, 5, "诉讼程序与证据（Litigation Procedure & Evidence）",
         "Litigation Procedure & Evidence"),
        (6, 6, "合规、监管与监管调查（Compliance, Regulation & Enforcement）",
         "Compliance, Regulation & Enforcement"),
        (7, 7, "公司治理与商事交易（Corporate Governance & Commercial Transactions）",
         "Corporate Governance & Commercial Transactions"),
        (8, 8, "知识产权与技术保护（Intellectual Property & Technology）",
         "Intellectual Property & Technology"),
        (9, 9, "劳动用工与雇佣法（Employment & Labour Law）",
         "Employment & Labour Law"),
        (10, 10, "数据保护与网络安全（Data Protection & Cybersecurity）",
         "Data Protection & Cybersecurity"),
        (11, 11, "并购、融资与交易文件（Mergers, Financing & Transaction Documents）",
         "Mergers, Financing & Transaction Documents"),
        (12, 12, "法律谈判、诉讼策略与高阶表达（Negotiation, Strategy & Advocacy）",
         "Negotiation, Strategy & Advocacy"),
    ],
)
