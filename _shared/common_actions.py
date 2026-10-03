# -*- coding: utf-8 -*-
"""Shared daily-life action categories + assembly helper.

Every module reuses the same seven personal scenarios (ids 1, 2, 3, 5, 6, 7, 8)
so that all SuperLanguage modules stay byte-identical where they overlap, and
only supplies its own:

  * id 4  office / desk routine for that profession
  * id 9  emergency + incremental bucket (common baseline, module extras)
"""
from __future__ import annotations

DAILY_CATEGORIES = [
    {
        "id": 1,
        "name_cn": "晨间与洗漱",
        "name_en": "Morning & Grooming",
        "actions": [
            ("醒来", "waking up"),
            ("起床", "getting up"),
            ("拉开窗帘", "pulling the curtains open"),
            ("洗脸", "washing my face"),
            ("洗手", "washing my hands"),
            ("刷牙", "brushing my teeth"),
            ("漱口", "rinsing my mouth"),
            ("洗澡", "having a shower"),
            ("刮胡子", "shaving"),
            ("梳头", "combing my hair"),
            ("扎头发", "tying my hair back"),
            ("涂护肤品", "applying moisturiser"),
            ("涂防晒", "putting on sunscreen"),
            ("画眉", "filling in my eyebrows"),
            ("挑选衣服", "picking out my clothes"),
            ("穿衣服", "getting dressed"),
            ("穿鞋", "putting on my shoes"),
            ("系腰带", "fastening my belt"),
            ("整理包", "packing my bag"),
            ("晾毛巾", "hanging the towel out"),
            ("打开冰箱", "opening the fridge"),
            ("出门前照镜子", "checking the mirror"),
        ],
    },
    {
        "id": 2,
        "name_cn": "居家与家务",
        "name_en": "Home & Chores",
        "actions": [
            ("整理床铺", "making the bed"),
            ("叠被子", "folding the quilt"),
            ("扫地", "sweeping the floor"),
            ("拖地", "mopping the floor"),
            ("吸尘", "vacuuming"),
            ("倒垃圾", "taking out the rubbish"),
            ("洗碗", "washing the dishes"),
            ("擦桌子", "wiping the table"),
            ("擦窗户", "cleaning the windows"),
            ("擦灶台", "wiping down the hob"),
            ("整理书桌", "tidying my desk"),
            ("收拾客厅", "tidying the living room"),
            ("叠衣服", "folding the laundry"),
            ("晾衣服", "hanging the laundry out"),
            ("收衣服", "bringing the laundry in"),
            ("换床单", "changing the bedsheets"),
            ("浇花", "watering the plants"),
            ("修剪植物", "trimming the plants"),
            ("给宠物喂食", "feeding my pet"),
            ("补充日用品", "restocking household supplies"),
        ],
    },
    {
        "id": 3,
        "name_cn": "饮食与烹饪",
        "name_en": "Dining & Cooking",
        "actions": [
            ("烧水", "boiling water"),
            ("冲咖啡", "brewing coffee"),
            ("泡茶", "making tea"),
            ("洗菜", "washing the vegetables"),
            ("切菜", "chopping vegetables"),
            ("切肉", "slicing the meat"),
            ("削皮", "peeling it"),
            ("腌肉", "marinating the meat"),
            ("热锅", "heating the pan"),
            ("炒菜", "stir-frying"),
            ("煮面", "cooking noodles"),
            ("煮饭", "cooking rice"),
            ("煲汤", "making soup"),
            ("蒸菜", "steaming the food"),
            ("烤箱预热", "preheating the oven"),
            ("烘焙", "baking"),
            ("用微波炉加热", "heating it in the microwave"),
            ("倒水", "pouring water"),
            ("洗水果", "washing the fruit"),
            ("摆餐具", "laying the table"),
            ("收拾厨房", "tidying the kitchen"),
            ("点外卖", "ordering takeaway"),
            ("打包剩饭", "packing the leftovers"),
        ],
    },
    {
        "id": 5,
        "name_cn": "通勤与出行",
        "name_en": "Commute & Travel",
        "actions": [
            ("锁门", "locking the door"),
            ("下楼", "going downstairs"),
            ("等公交", "waiting for the bus"),
            ("挤上公交", "squeezing onto the bus"),
            ("赶地铁", "rushing for the metro"),
            ("刷卡入闸", "tapping through the gates"),
            ("换乘", "changing lines"),
            ("等红灯", "waiting for the lights"),
            ("过马路", "crossing the road"),
            ("走路", "walking"),
            ("骑共享单车", "riding a shared bike"),
            ("打车", "hailing a taxi"),
            ("开车", "driving"),
            ("系安全带", "fastening my seat belt"),
            ("踩刹车", "braking"),
            ("看导航", "checking the navigation"),
            ("找车位", "looking for parking"),
            ("停车", "parking"),
            ("坐电梯", "taking the lift"),
            ("提行李", "carrying my luggage"),
            ("办登机牌", "getting my boarding pass"),
            ("托运行李", "checking my bag"),
            ("过安检", "going through security"),
            ("登机", "boarding the plane"),
            ("在登机口等待", "waiting at the gate"),
            ("买机票", "booking a flight"),
            ("订酒店", "booking a hotel"),
            ("赶飞机", "catching my flight"),
            ("误机", "missing my flight"),
            ("打车去机场", "taking a taxi to the airport"),
        ],
    },
    {
        "id": 6,
        "name_cn": "运动与健身",
        "name_en": "Fitness & Wellness",
        "actions": [
            ("热身", "warming up"),
            ("拉伸", "stretching"),
            ("举重", "lifting weights"),
            ("做深蹲", "doing squats"),
            ("做俯卧撑", "doing push-ups"),
            ("卷腹", "doing crunches"),
            ("平板支撑", "holding a plank"),
            ("开合跳", "doing jumping jacks"),
            ("跳绳", "skipping rope"),
            ("跑步机跑步", "running on a treadmill"),
            ("户外跑步", "running outdoors"),
            ("快走", "walking briskly"),
            ("骑动感单车", "spinning"),
            ("游泳", "swimming"),
            ("爬山", "hiking"),
            ("做瑜伽", "doing yoga"),
            ("做普拉提", "doing pilates"),
            ("补充水分", "drinking more water"),
            ("补充电解质", "replenishing electrolytes"),
            ("记录热量", "logging my calories"),
            ("称体重", "weighing myself"),
            ("测心率", "checking my heart rate"),
            ("深呼吸", "breathing deeply"),
            ("按摩放松", "giving myself a massage"),
            ("吃维生素", "taking vitamins"),
            ("午睡", "taking a nap"),
            ("早睡", "going to bed early"),
        ],
    },
    {
        "id": 7,
        "name_cn": "休闲与社交",
        "name_en": "Leisure & Socialising",
        "actions": [
            ("刷短视频", "scrolling through short videos"),
            ("刷手机", "scrolling through my phone"),
            ("看朋友圈", "browsing my feed"),
            ("发朋友圈", "posting to my feed"),
            ("点赞", "liking a post"),
            ("评论", "leaving a comment"),
            ("转发", "sharing a post"),
            ("私信", "sending a private message"),
            ("听播客", "listening to a podcast"),
            ("听有声书", "listening to an audiobook"),
            ("听音乐", "listening to music"),
            ("唱 KTV", "singing karaoke"),
            ("看剧", "watching a drama"),
            ("看电影", "watching a film"),
            ("看综艺", "watching a variety show"),
            ("看动漫", "watching an anime"),
            ("看纪录片", "watching a documentary"),
            ("看球赛", "watching a match"),
            ("打游戏", "playing games"),
            ("玩桌游", "playing board games"),
            ("打麻将", "playing mahjong"),
            ("遛狗", "walking the dog"),
            ("撸猫", "petting the cat"),
            ("陪家人聊天", "chatting with my family"),
            ("打电话", "making a phone call"),
            ("视频通话", "having a video call"),
            ("聊天打屁", "having a chat"),
            ("参加聚会", "going to a get-together"),
            ("聚餐", "having dinner with friends"),
            ("喝下午茶", "having afternoon tea"),
            ("逛超市", "shopping at the supermarket"),
            ("逛街", "browsing the shops"),
            ("旅游", "travelling"),
            ("拍照", "taking photos"),
            ("修图", "editing photos"),
            ("在沙发上发呆", "zoning out"),
            ("写博客", "writing a blog post"),
            ("钓鱼", "fishing"),
            ("泡吧", "going to a bar"),
        ],
    },
    {
        "id": 8,
        "name_cn": "晚间与睡眠",
        "name_en": "Evening & Sleep",
        "actions": [
            ("卸妆", "removing my makeup"),
            ("洁面", "cleansing my face"),
            ("涂爽肤水", "applying toner"),
            ("涂晚霜", "applying night cream"),
            ("敷面膜", "putting on a face mask"),
            ("泡脚", "soaking my feet"),
            ("泡澡", "soaking in a bath"),
            ("冥想", "meditating"),
            ("收拾玩具", "tidying the toys"),
            ("写日记", "keeping a diary"),
            ("整理明天要做的事", "preparing tomorrow's tasks"),
            ("拉上遮光帘", "drawing the blackout curtains"),
            ("调暗灯光", "dimming the lights"),
            ("关电视", "switching off the TV"),
            ("关灯", "turning off the light"),
            ("睡前刷手机", "scrolling before bed"),
            ("听白噪音", "listening to white noise"),
            ("调闹钟", "setting my alarm"),
            ("关掉闹钟", "turning off the alarm"),
            ("躺下", "lying down"),
            ("躺平", "lying flat"),
            ("盖被子", "tucking myself in"),
            ("侧睡", "sleeping on my side"),
            ("敷眼罩", "putting on an eye mask"),
            ("喝一杯温水", "drinking warm water"),
            ("吃褪黑素", "taking melatonin"),
            ("数羊", "counting sheep"),
            ("熬夜", "staying up late"),
            ("失眠", "having insomnia"),
            ("打了个盹", "dozing off"),
            ("半梦半醒", "drifting in and out of sleep"),
            ("陷入沉睡", "falling into a deep sleep"),
            ("说梦话", "talking in my sleep"),
            ("打呼噜", "snoring"),
            ("做梦", "dreaming"),
        ],
    },
]

# Baseline for scenario 9 (emergency + incremental). Modules may extend it.
BASELINE_INCREMENTAL = [
    # --- emergencies ---
    ("应急处理客诉", "handling an urgent complaint"),
    ("应对裁员公告", "preparing a redundancy announcement"),
    ("处理劳动仲裁", "handling an employment tribunal"),
    ("配合监管检查", "cooperating with an inspection"),
    ("应对集体事件", "managing a group incident"),
    ("处理系统故障", "handling a system outage"),
    ("处理工伤事故", "dealing with a workplace accident"),
    ("处理数据泄露", "handling a data breach"),
    ("紧急通知全员", "notifying everyone urgently"),
    ("临时替补排班", "covering a rota gap"),
    ("应急改期面试", "rescheduling interviews at short notice"),
    ("帮同事顶岗", "covering for a colleague"),
    ("抢救丢失的档案", "recovering a misplaced file"),
    ("凌晨值守", "covering an out-of-hours shift"),
    # --- office incremental ---
    ("订会议室", "booking a meeting room"),
    ("认领工位", "claiming a desk"),
    ("打印门禁卡", "printing an access card"),
    ("整理通讯录", "updating the contact list"),
    ("清理共享盘", "clearing the shared drive"),
    ("备份工作文件", "backing up work files"),
    ("设置自动回复", "setting an out-of-office reply"),
    ("转发客户邮件", "forwarding a client email"),
    ("起草内部通告", "drafting an internal notice"),
    ("统计加班时长", "totalling overtime hours"),
    ("核对考勤异常", "chasing attendance exceptions"),
    ("收拾会议室", "tidying the meeting room"),
    ("浇办公室绿植", "watering the office plants"),
    ("换打印机纸", "refilling the printer paper"),
    ("订下午茶", "ordering afternoon tea"),
    ("帮新人带路", "showing a new joiner around"),
    ("跑腿取快递", "collecting a parcel"),
]

INCREMENTAL_NOTE = ("本场景为应急与增量桶：既收录突发情形下的处置动作，"
                    "也用于归入后续补充的未覆盖动作。")


def build_categories(office_actions, incremental_extra=None,
                     office_note=None, office_name_cn="办公室日常工作",
                     office_name_en="Office & Desk Routine",
                     incremental_note=INCREMENTAL_NOTE):
    """Assemble the canonical nine scenarios (ids 1..9) for one module.

    Parameters
    ----------
    office_actions : list[tuple[str, str]]
        Scenario 4 - this profession's desk routine.
    incremental_extra : list[tuple[str, str]], optional
        Module-specific additions to scenario 9. Duplicate Chinese actions are
        rejected so the shared validator can stay strict.
    """
    office = {
        "id": 4,
        "name_cn": office_name_cn,
        "name_en": office_name_en,
        "actions": list(office_actions),
    }
    if office_note:
        office["note"] = office_note

    incremental_actions = list(BASELINE_INCREMENTAL)
    for item in (incremental_extra or []):
        cn = item[0]
        if any(cn == existing[0] for existing in incremental_actions):
            raise ValueError(f"duplicate incremental action: {cn}")
        incremental_actions.append(item)

    incremental = {
        "id": 9,
        "name_cn": "应急与增量补充",
        "name_en": "Custom & Incremental",
        "note": incremental_note,
        "actions": incremental_actions,
    }

    by_id = {c["id"]: c for c in DAILY_CATEGORIES}
    by_id[4] = office
    by_id[9] = incremental
    return [by_id[i] for i in sorted(by_id)]