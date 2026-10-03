# -*- coding: utf-8 -*-
"""Finance module action tree: 9 scenarios (7 shared + finance office + incremental)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_shared"))
from common_actions import build_categories  # noqa: E402

OFFICE_NOTE = ("本场景为财务专属办公动作库，覆盖账务与结账、对账与报表、"
               "预算与资金、管理与分析、税务与审计五大工作块，以及日常办公动作。")

OFFICE_ACTIONS = [
    # --- 账务与结账 ---
    ("整理凭证", "collecting the vouchers"),
    ("录入凭证", "posting the vouchers"),
    ("编制记账凭证", "preparing the journal entry"),
    ("编制日记账", "writing up the journal"),
    ("更新总账", "updating the general ledger"),
    ("编制试算平衡表", "preparing the trial balance"),
    ("结账", "closing the books"),
    ("计提折旧", "booking the depreciation"),
    ("摊销费用", "amortising the expense"),
    ("计提税金", "accruing the tax"),
    ("核对发票", "checking the invoices"),
    ("处理报销单", "processing the expense claims"),
    # --- 对账与报表 ---
    ("与银行对账", "reconciling with the bank"),
    ("与客户对账", "reconciling with customers"),
    ("与供应商对账", "reconciling with suppliers"),
    ("函证应收余额", "confirming receivable balances"),
    ("编制账龄分析", "preparing the ageing analysis"),
    ("编制往来对账表", "preparing the reconciliation statement"),
    ("编制财务报表", "preparing the financial statements"),
    ("出具管理报表", "preparing the management report"),
    # --- 预算与资金 ---
    ("编制预算表", "preparing the budget"),
    ("汇总预算数据", "consolidating the budget data"),
    ("跟踪预算差异", "tracking budget variances"),
    ("编制资金计划", "preparing the cash plan"),
    ("测算现金流", "modelling the cash flow"),
    ("安排付款", "scheduling the payments"),
    ("申请付款审批", "requesting payment approval"),
    ("管理银行账户", "managing the bank accounts"),
    ("办理银行开户", "opening a bank account"),
    ("盘点现金", "counting the cash on hand"),
    ("购买理财产品", "buying a wealth management product"),
    # --- 管理与分析 ---
    ("做滚动预测", "rolling the forecast forward"),
    ("做敏感性分析", "running a sensitivity analysis"),
    ("搭建财务模型", "building the financial model"),
    ("更新估值模型", "updating the valuation model"),
    ("做同业对标", "benchmarking against peers"),
    ("制作图表", "charting the numbers"),
    ("写财务分析报告", "writing the financial analysis"),
    ("向管理层汇报", "reporting to management"),
    ("参加财务例会", "attending the finance meeting"),
    ("解答业务提问", "answering business questions"),
    ("审核合同条款", "reviewing the contract terms"),
    # --- 税务与审计 ---
    ("整理税务资料", "preparing the tax records"),
    ("申报增值税", "filing the VAT return"),
    ("汇算清缴", "completing the annual tax filing"),
    ("对接审计师", "liaising with the auditor"),
    ("准备审计底稿", "preparing the audit workpapers"),
    ("回复审计问询", "answering audit queries"),
    ("盘点固定资产", "counting the fixed assets"),
    ("处理内控缺陷", "remediating the control weakness"),
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
    ("处理银行退票", "chasing a returned payment"),
    ("补办发票", "reissuing a lost invoice"),
    ("催收应收账款", "chasing overdue receivables"),
    ("处理坏账核销", "writing off bad debt"),
    ("盘点保险柜", "counting the petty cash safe"),
    ("应对汇率波动", "dealing with currency volatility"),
    ("解冻银行账户", "unfreezing a bank account"),
    ("复核付款审批", "rechecking the payment approval"),
    ("提交监管报表", "submitting the regulatory return"),
    ("配合外部审计", "cooperating with external audit"),
]

CATEGORIES = build_categories(
    OFFICE_ACTIONS,
    incremental_extra=INCREMENTAL_EXTRA,
    office_note=OFFICE_NOTE,
    office_name_cn="财务办公与工作日常",
    office_name_en="Finance Office & Desk Routine",
)