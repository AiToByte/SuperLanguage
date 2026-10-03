# -*- coding: utf-8 -*-
"""Legal module action tree: 9 scenarios (7 shared + legal office + incremental)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_shared"))
from common_actions import build_categories  # noqa: E402

OFFICE_NOTE = ("本场景为法律专属办公动作库，覆盖合同与文件、检索与研究、"
               "沟通与会议、诉讼与争议、合规与尽调五大工作块，以及日常办公动作。")

OFFICE_ACTIONS = [
    # --- 合同与文件 ---
    ("起草合同", "drafting the contract"),
    ("审阅合同", "reviewing the contract"),
    ("修订条款", "revising the clause"),
    ("比对版本差异", "comparing the version changes"),
    ("标注修改痕迹", "marking up the revisions"),
    ("定稿合同", "finalising the contract"),
    ("归档已签合同", "filing the executed contract"),
    ("核对签署页", "checking the signature page"),
    ("管理合同台账", "maintaining the contract register"),
    ("设置合同到期提醒", "setting the renewal reminder"),
    ("续签合同", "renewing the contract"),
    ("终止合同", "terminating the contract"),
    ("整理签署流程", "organising the signature workflow"),
    ("核对授权文件", "checking the power of attorney"),
    ("用印审批", "approving the company seal"),
    # --- 检索与研究 ---
    ("检索判例", "searching case law"),
    ("检索法规", "searching the legislation"),
    ("查阅合同范本", "reviewing the precedent contract"),
    ("做法律尽职调查", "running the legal due diligence"),
    ("撰写法律意见书", "writing the legal opinion"),
    ("撰写法律备忘录", "writing the legal memorandum"),
    ("更新法规动态", "updating on the regulatory changes"),
    ("核实法条", "verifying the statutory provision"),
    ("整理判例摘要", "summarising the case"),
    ("分析先例", "analysing the precedent"),
    ("评估法律风险", "assessing the legal risk"),
    ("编写尽调问题清单", "preparing the due diligence request list"),
    # --- 沟通与会议 ---
    ("与客户开会", "meeting the client"),
    ("参加内部法务会", "attending the in-house legal meeting"),
    ("汇报法律风险", "reporting the legal exposure"),
    ("回复业务部门咨询", "answering the business query"),
    ("与对方律师沟通", "corresponding with the other side's counsel"),
    ("准备谈判要点", "preparing the negotiation points"),
    ("参加调解会议", "attending the mediation"),
    ("记录会议纪要", "taking the meeting minutes"),
    ("确认会议结论", "confirming the meeting outcome"),
    ("解释法律条款", "explaining the legal clause"),
    ("提醒合规期限", "reminding of the compliance deadline"),
    ("答复监管问询", "responding to the regulator's enquiry"),
    # --- 诉讼与争议 ---
    ("起草起诉状", "drafting the statement of claim"),
    ("准备答辩状", "preparing the defence"),
    ("整理证据材料", "organising the evidence bundle"),
    ("制作证据清单", "preparing the exhibit list"),
    ("申请财产保全", "applying for the asset preservation"),
    ("申请强制执行", "applying for the enforcement"),
    ("出庭", "attending the hearing"),
    ("与对方协商和解", "negotiating the settlement"),
    ("评估和解方案", "evaluating the settlement offer"),
    ("起草和解协议", "drafting the settlement agreement"),
    ("复核判决书", "reviewing the judgment"),
    ("研究管辖权", "researching the jurisdiction"),
    # --- 合规与尽调 ---
    ("执行内控检查", "running the compliance check"),
    ("核查交易对手", "screening the counterparty"),
    ("反洗钱核查", "conducting the AML checks"),
    ("申报关联交易", "filing the related-party disclosure"),
    ("参与监管检查", "participating in the regulatory inspection"),
    ("整改合规问题", "remediating the compliance finding"),
    ("完善制度文件", "updating the policy document"),
    ("培训业务部门", "training the business teams"),
    ("监测诉讼风险敞口", "monitoring the litigation exposure"),
    ("更新合规手册", "refreshing the compliance manual"),
    ("跟踪监管处罚动态", "tracking the enforcement developments"),
    ("复核授权审批链", "reviewing the approval chain"),
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
    ("处理律所函件", "handling the law firm letter"),
    ("回函催告", "sending the demand letter"),
    ("更新诉讼台账", "updating the litigation register"),
    ("准备证据原件", "producing the original evidence"),
    ("安排证人作证", "preparing the witness"),
    ("应对突发调查", "responding to the surprise inspection"),
    ("补签遗漏附件", "executing the missing annex"),
    ("办理工商变更", "filing the corporate amendment"),
    ("核对董事会决议", "checking the board resolution"),
    ("配合监管问询答复", "supporting the regulatory response"),
]

CATEGORIES = build_categories(
    OFFICE_ACTIONS,
    incremental_extra=INCREMENTAL_EXTRA,
    office_note=OFFICE_NOTE,
    office_name_cn="法律办公与工作日常",
    office_name_en="Legal Office & Desk Routine",
)
