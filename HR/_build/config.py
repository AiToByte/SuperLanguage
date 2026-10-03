# -*- coding: utf-8 -*-
"""HR module configuration (人力资源商务英语 + 科技行业术语)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_shared"))
from toolkit import ModuleConfig  # noqa: E402

CONFIG = ModuleConfig(
    MODULE="HR",
    PROJECT_TITLE="SuperLanguage 365-Day HR English Learning Plan",
    MODULE_TAG="HR · 人力资源商务英语 + 科技行业术语",
    STAGE_TITLE="HR 全业务链 12 个月主题递进",
    DIFFICULTY_NOTE="B2–C1",
    EXAMPLE_NOTE="HR 真实职场场景（面试、绩效面谈、员工关系、跨部门汇报），且以目标词开头",
    ACCENT="5B2C6F",
    ACCENT_SOFT="F6F2FA",
    PHASES=[
        (1, 1, "招聘与猎头（Recruitment, Sourcing, Talent Acquisition, Candidate Experience）",
         "Recruitment, Sourcing, Talent Acquisition & Candidate Experience"),
        (2, 2, "入职与团队融入（Onboarding, Orientation, Team Integration, Probation）",
         "Onboarding, Orientation, Team Integration & Probation"),
        (3, 3, "组织发展与人才盘点（OD, Talent Review, Succession Planning, Competency）",
         "Organisational Development, Talent Review, Succession & Competency"),
        (4, 4, "绩效管理与考核（Performance Management, OKRs, KPIs, 360 Feedback）",
         "Performance Management, OKRs, KPIs & 360 Feedback"),
        (5, 5, "薪酬福利与激励（C&B, Compensation, Equity, Incentives, Benefits）",
         "Compensation & Benefits, Equity, Incentives & Benefits Package"),
        (6, 6, "培训、学习与发展（L&D, Training, Leadership Coaching, Upskilling）",
         "Learning & Development, Training, Leadership Coaching & Upskilling"),
        (7, 7, "员工关系与离职管理（Employee Relations, Offboarding, Retention, Exit）",
         "Employee Relations, Offboarding, Retention & Exit Interviews"),
        (8, 8, "劳动法务、合规与风控（Labor Law, Compliance, Risk Management, Contracts）",
         "Employment Law, Compliance, Risk Management & Contracts"),
        (9, 9, "企业文化与员工关怀（Corporate Culture, D&I, Engagement, Wellness）",
         "Corporate Culture, Diversity & Inclusion, Engagement & Wellness"),
        (10, 10, "HR 数字化转型与科技术语（HR Tech, HRIS, People Analytics, Agile HR）",
         "HR Digital Transformation, HR Tech, People Analytics & Agile HR"),
        (11, 11, "跨部门沟通与高管汇报（Stakeholder Management, Business Partnering）",
         "Stakeholder Management, Business Partnering & Executive Alignment"),
        (12, 12, "高阶职场领导力与商业敏锐度（Leadership, Business Acumen, Strategy）",
         "Leadership, Business Acumen & Strategic Planning"),
    ],
)