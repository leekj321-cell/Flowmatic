from __future__ import annotations

from datetime import date
from html import escape
import json
from pathlib import Path
import re

from factory_os_v2 import (
    ASSET_PATH as FACTORY_OS_ASSET_PATH,
    CERTIFIED_CORE,
    BEFORE_AFTER,
    COMPONENT_CONTEXT,
    DEPLOYMENT_MODES,
    DOMAINS,
    EVIDENCE,
    HOME_OVERRIDES,
    OUTCOMES,
    PAGES as FACTORY_OS_PAGES,
    PLATFORM,
    QUALITY_CURRENT,
    ROADMAP as FACTORY_OS_ROADMAP,
)


BASE_URL = "https://flowmatic-os.com"
CONTACT_EMAIL = "contact@flowmatic-os.com"
CONTACT_ENDPOINT = "https://formspree.io/f/xojgorkl"
CSS_HREF = "/style-v5.20.css?v=5.24"
SCRIPT_SRC = "/script.js?v=5.19"
NC_DEMO_SRC = "/nc-demo-lite.js?v=1.0"
BRAND_PATH = "/assets/branding"
BRAND_VERSION = "20260803.2"
BRAND_MARK = f"{BRAND_PATH}/flowmatic-logo-mark.svg"
OG_IMAGE = f"{BASE_URL}{BRAND_PATH}/flowmatic-og.png"
QR_SIGNATURE = f"{BRAND_PATH}/flowmatic-qr-contact-signature.svg"


LANGS = {
    "ko": {
        "label": "KR",
        "name": "한국어",
        "dir": "ltr",
        "skip": "본문으로 건너뛰기",
        "open": "메뉴 열기",
        "nav": {"approach": "설계 원칙", "flow": "작동 방식", "products": "Intelligence", "contact": "파일럿 상담"},
        "home": "홈",
        "all_products": "전체 제품 보기",
        "product_demo": "제품 데모",
        "development_preview": "개발 프리뷰",
        "demo_available": "데모 제공",
        "see_how": "작동 방식 보기",
        "pilot": "파일럿 상담",
        "contact": "문의",
        "related": "관련 제품",
        "status": "상태",
        "current_scope": "현재 보여주는 범위",
        "pilot_input": "파일럿에서 검증할 입력",
        "pilot_result": "파일럿에서 확인할 결과",
        "video_unavailable": "브라우저에서 영상을 재생할 수 없습니다. 아래 설명으로 핵심 흐름을 확인하세요.",
        "selected_interest": "선택된 관심 제품",
    },
    "en": {
        "label": "EN",
        "name": "English",
        "dir": "ltr",
        "skip": "Skip to content",
        "open": "Open menu",
        "nav": {"approach": "Approach", "flow": "How it works", "products": "Intelligence", "contact": "Discuss a pilot"},
        "home": "Home",
        "all_products": "All products",
        "product_demo": "Product demo",
        "development_preview": "Development preview",
        "demo_available": "Demo available",
        "see_how": "See how it works",
        "pilot": "Discuss a pilot",
        "contact": "Contact",
        "related": "Related products",
        "status": "Status",
        "current_scope": "Current scope shown",
        "pilot_input": "Input to verify in pilot",
        "pilot_result": "Result to confirm in pilot",
        "video_unavailable": "This browser cannot play the video. Use the summary below to review the workflow.",
        "selected_interest": "Selected product interest",
    },
    "ar": {
        "label": "العربية",
        "name": "العربية",
        "dir": "rtl",
        "skip": "تجاوز إلى المحتوى",
        "open": "فتح القائمة",
        "nav": {"approach": "النهج", "flow": "طريقة العمل", "products": "الذكاء", "contact": "ناقش مشروعًا تجريبيًا"},
        "home": "الرئيسية",
        "all_products": "كل المنتجات",
        "product_demo": "عرض المنتج",
        "development_preview": "معاينة تطوير",
        "demo_available": "العرض متاح",
        "see_how": "شاهد طريقة العمل",
        "pilot": "ناقش مشروعًا تجريبيًا",
        "contact": "تواصل",
        "related": "منتجات مرتبطة",
        "status": "الحالة",
        "current_scope": "النطاق المعروض حاليًا",
        "pilot_input": "المدخلات التي سيتم التحقق منها",
        "pilot_result": "النتيجة التي سيتم تأكيدها",
        "video_unavailable": "لا يستطيع هذا المتصفح تشغيل الفيديو. راجع الملخص أسفل المشغل.",
        "selected_interest": "المنتج محل الاهتمام",
    },
}


CONTACT_FORM = {
    "ko": {
        "organization": "회사 / 조직",
        "name": "이름",
        "product": "관심 제품",
        "brief": "운영 문제 / 입력 신호 / 목표 KPI",
        "brief_template": "해결하려는 문제 :\n사용 가능한 입력 신호 :\n목표 KPI :",
        "contact": "이메일 주소 / 휴대폰 번호(국가)",
        "submit": "문의 보내기",
        "copy": "이메일 주소 복사",
        "copied": "이메일 주소를 복사했습니다.",
        "copy_failed": "복사하지 못했습니다. 이메일 주소를 직접 선택해 주세요.",
        "required": "필수 항목을 입력해 주세요.",
        "sending": "문의 내용을 전송하고 있습니다.",
        "sent": "문의가 전송되었습니다. 확인 후 연락드리겠습니다.",
        "failed": "전송하지 못했습니다. 잠시 후 다시 시도해 주세요.",
        "unavailable": "문의 전송 설정을 확인하고 있습니다.",
    },
    "en": {
        "organization": "Company / organization",
        "name": "Name",
        "product": "Product interest",
        "brief": "Operational problem / input signals / target KPI",
        "brief_template": "Problem to solve:\nAvailable input signals:\nTarget KPI:",
        "contact": "Email address / mobile number (country)",
        "submit": "Send inquiry",
        "copy": "Copy email address",
        "copied": "Email address copied.",
        "copy_failed": "Could not copy automatically. Please select the email address.",
        "required": "Complete the required fields.",
        "sending": "Sending your inquiry.",
        "sent": "Your inquiry has been sent. We will be in touch.",
        "failed": "The inquiry could not be sent. Please try again shortly.",
        "unavailable": "The inquiry delivery setup is being checked.",
    },
    "ar": {
        "organization": "الشركة / المؤسسة",
        "name": "الاسم",
        "product": "المنتج محل الاهتمام",
        "brief": "المشكلة التشغيلية / إشارات الإدخال / مؤشر KPI المستهدف",
        "brief_template": "المشكلة المراد حلها:\nإشارات الإدخال المتاحة:\nمؤشر KPI المستهدف:",
        "contact": "عنوان البريد / رقم الجوال (الدولة)",
        "submit": "إرسال الاستفسار",
        "copy": "نسخ عنوان البريد",
        "copied": "تم نسخ عنوان البريد.",
        "copy_failed": "تعذر النسخ تلقائيًا. يرجى تحديد عنوان البريد يدويًا.",
        "required": "يرجى إكمال الحقول المطلوبة.",
        "sending": "جارٍ إرسال استفسارك.",
        "sent": "تم إرسال استفسارك. سنتواصل معك قريبًا.",
        "failed": "تعذر إرسال الاستفسار. يرجى المحاولة بعد قليل.",
        "unavailable": "يجري التحقق من إعداد إرسال الاستفسارات.",
    },
}


CONTACT_PRODUCT_OPTIONS = [
    ("all", "All / undecided"),
    ("quality", "Quality Intelligence"),
    ("machining-intelligence", "Machining Intelligence"),
    ("operations-intelligence", "Operations Intelligence"),
    ("logistics-intelligence", "Logistics Intelligence"),
    ("platform", "Platform / Control Tower"),
]

LEGACY_INTEREST_MAP = {
    "nc": "machining-intelligence",
    "ct": "machining-intelligence",
    "work-standard": "machining-intelligence",
    "tms": "machining-intelligence",
    "amr": "logistics-intelligence",
}


HOME = {
    "ko": {
        "title": "Flowmatic | 제조 현장 운영 인텔리전스",
        "description": "Flowmatic은 카메라, NC 코드, 작업자 입력을 운영 이벤트로 바꾸고 알림·검토·호출·안내에 연결하는 제조 현장 운영 인텔리전스입니다.",
        "eyebrow": "제조 현장 운영 인텔리전스",
        "h1": "Elegant Engineering.|Intelligent Operations.|Flowmatic.",
        "body": "현장 신호를 Event로 구조화하고, 도메인별 판단을 사람과 설비의 후속 행동에 연결하는 Engineering Intelligence 플랫폼.",
        "primary": "시스템 보기",
        "secondary": "로드맵 보기",
        "support": "기존 설비와 업무체계를 유지한 채 단절된 운영 정보를 연결합니다.",
        "brand_subcopy": "Engineering Intelligence for the physical world.",
        "problem_title": "운영 신호는 실시간.|판단은 사후.",
        "problem_body": "지연·위험·자재 요구 등 핵심 이벤트가 분산되어 대응 시점을 놓칩니다.",
        "strategy_title": "현장 변경 최소화.|운영 가시성 우선.",
        "strategy_body": "기존 설비와 작업 방식은 유지합니다. 신호를 Event로 구조화하고 책임 있는 후속 행동과 KPI를 연결합니다. 자동화는 검증 결과에 따라 단계적으로 적용합니다.",
        "flow_title": "Observe → Eventize →|Act → Confirm",
        "flow_body": "신호 수집, Event 변환, 행동 연결, 결과 확인의 4단계 운영 구조입니다.",
        "products_title": "제품별 구현 상태와|검증 범위.",
        "products_body": "CT·NC는 공개 데모, Quality는 작동 프로토타입, Work Standard·TMS·Fleet는 개발 범위로 구분합니다.",
        "workflow_title": "Demo workflows",
        "workflow_body": "공개 데모와 검증 가능한 구현 범위만 표시합니다.",
        "pilot_title": "기존 라인 유지.|단일 Event 파일럿.",
        "deploy_note": "파일럿 설계 항목: 배포 구조, 데이터 위치·보관 기간, 접근 권한, 기존 시스템 연동 범위.",
        "contact_title": "기존 라인 유지.|단일 Event 검증.",
        "contact_body": "운영 문제, 입력 신호, 목표 KPI를 기준으로 파일럿 범위를 정의합니다.",
        "contact_cta": "파일럿 상담 요청",
        "contact_fallback": "공식 이메일로 파일럿 범위를 문의할 수 있습니다.",
    },
    "en": {
        "title": "Flowmatic | Operational Intelligence for Manufacturing",
        "description": "Flowmatic turns camera, NC-code, and operator signals into actionable manufacturing events, alerts, reviews, guidance, and material calls.",
        "eyebrow": "Operational Intelligence for Manufacturing",
        "h1": "Elegant Engineering.|Intelligent Operations.|Flowmatic.",
        "body": "Flowmatic turns factory motion into events, events into decisions, and decisions into coordinated action.",
        "primary": "Explore the System",
        "secondary": "See the Roadmap",
        "support": "A factory does not need one more system. It needs operations to flow.",
        "brand_subcopy": "Engineering Intelligence for the physical world.",
        "problem_title": "Production keeps moving.|Decisions arrive late.",
        "problem_body": "The field never stops. Important events and the next action often appear too late.",
        "strategy_title": "Read the flow|before changing the field.",
        "strategy_body": "Start with the line as it is. Keep the equipment, workflow, and people already creating value. Make the event visible first, connect one next action, and automate only after the value is proven.",
        "flow_title": "Observe → Eventize →|Act → Confirm",
        "flow_body": "Flowmatic uses one operating logic: observe the signal, turn it into an event, connect a next action, and confirm the response.",
        "products_title": "Product status and pilot scope|should be explicit.",
        "products_body": "CT and NC include working demos. Quality shows its working prototype and integration status. Work Standard, TMS, and Fleet show their current development scope.",
        "workflow_title": "Demo workflows",
        "workflow_body": "Without verified customer metrics, the site shows only workflows that can be inspected through actual demos.",
        "pilot_title": "Validate one event|without replacing the line.",
        "deploy_note": "Deployment architecture, data location, retention, access control, and integration scope are confirmed during pilot design.",
        "contact_title": "Validate one event|without replacing the line.",
        "contact_body": "Share the problem, available input signals, and target KPI. We will turn them into a focused pilot scope.",
        "contact_cta": "Request a pilot discussion",
        "contact_fallback": "Use the official email to discuss a pilot scope.",
    },
    "ar": {
        "title": "Flowmatic | ذكاء تشغيلي للتصنيع",
        "description": "يحوّل Flowmatic إشارات المصنع إلى أحداث تشغيلية قابلة للتنفيذ وتنبيهات ومراجعات وإرشادات وطلبات مواد.",
        "eyebrow": "ذكاء تشغيلي للتصنيع",
        "h1": "Elegant Engineering.|Intelligent Operations.|Flowmatic.",
        "body": "يحوّل Flowmatic حركة المصنع إلى أحداث، والأحداث إلى قرارات، والقرارات إلى أفعال منسقة بين الإنسان والآلة.",
        "primary": "استكشف النظام",
        "secondary": "شاهد خارطة الطريق",
        "support": "لا يحتاج المصنع إلى نظام إضافي، بل يحتاج إلى تدفق العمليات.",
        "brand_subcopy": "Engineering Intelligence for the physical world.",
        "problem_title": "الإنتاج يستمر بالحركة.|والقرارات تصل متأخرة.",
        "problem_body": "الميدان لا يتوقف. وغالبًا ما تظهر الأحداث المهمة والإجراء التالي بعد فوات الوقت.",
        "strategy_title": "اقرأ التدفق|قبل تغيير الميدان.",
        "strategy_body": "ابدأ من الخط كما هو. حافظ على المعدات وسير العمل والأشخاص الذين يصنعون القيمة. اجعل الحدث مرئيًا أولًا، ثم اربطه بإجراء تالٍ واحد، ولا تؤتمت إلا بعد إثبات القيمة.",
        "flow_title": "الرصد → تحويل الإشارة إلى حدث →|ربط الإجراء → التأكيد",
        "flow_body": "يستخدم Flowmatic منطق تشغيل واحدًا: قراءة الإشارة، تحويلها إلى حدث، ربطها بإجراء تالٍ، ثم تأكيد الاستجابة.",
        "products_title": "يجب أن تكون حالة المنتج|ونطاق التحقق واضحين.",
        "products_body": "يتضمن CT وNC عروضًا عملية. وتعرض Quality النموذج الأولي العامل وحالة التكامل، بينما تعرض Work Standard وTMS وFleet نطاق التطوير الحالي.",
        "workflow_title": "تدفقات العروض",
        "workflow_body": "من دون مقاييس عملاء موثقة، يعرض الموقع فقط التدفقات التي يمكن فحصها من خلال العروض الفعلية.",
        "pilot_title": "تحقق من حدث واحد|من دون استبدال الخط.",
        "deploy_note": "يتم تأكيد بنية النشر وموقع البيانات وفترة الاحتفاظ وصلاحيات الوصول ونطاق التكامل أثناء تصميم المشروع التجريبي.",
        "contact_title": "تحقق من حدث واحد|من دون استبدال الخط.",
        "contact_body": "شارك المشكلة وإشارات الإدخال المتاحة ومؤشر KPI المستهدف، وسنحدد نطاقًا تجريبيًا مركزًا.",
        "contact_cta": "اطلب نقاشًا تجريبيًا",
        "contact_fallback": "استخدم البريد الرسمي لمناقشة نطاق مشروع تجريبي.",
    },
}

for _lang, _values in HOME_OVERRIDES.items():
    HOME[_lang].update(_values)


PROBLEM_CARDS = {
    "ko": [
        ("01", "사이클 손실|조기 식별", "대응 가능 시점에 지연 구간을 식별합니다."),
        ("02", "가공 전|경로 위험 검토", "NC 코드의 위험 이동을 가공 전에 시각화합니다."),
        ("03", "자재 부족|선제 대응", "라인 정지 전에 자재 요구 Event를 생성합니다."),
        ("04", "숙련 판단|표준화", "개인 경험을 반복 가능한 작업 기준으로 전환합니다."),
    ],
    "en": [
        ("01", "See cycle loss|sooner.", "Find the delay while there is still time to respond."),
        ("02", "See risk|before cutting.", "Bring risky tool moves out of the code and into view."),
        ("03", "Call material|before waiting.", "Share demand before the line begins to wait."),
        ("04", "Turn know-how|into a shared standard.", "Make expert judgment easier to share and repeat."),
    ],
    "ar": [
        ("01", "اكتشف فقد الدورة|مبكرًا.", "اكتشف التأخير بينما لا يزال هناك وقت للاستجابة."),
        ("02", "شاهد الخطر|قبل التشغيل.", "أخرج حركات الأداة الخطرة من الكود واجعلها مرئية."),
        ("03", "اطلب المواد|قبل الانتظار.", "شارك الطلب قبل أن يبدأ الخط بالانتظار."),
        ("04", "حوّل الخبرة|إلى معيار مشترك.", "اجعل حكم الخبير أسهل في المشاركة والتكرار."),
    ],
}


PRINCIPLES = {
    "ko": [
        ("01", "기존 자산|유지", "검증된 설비·업무 절차·현장 경험을 유지합니다."),
        ("02", "관찰|우선", "자동화 전에 신호와 Event를 정의합니다."),
        ("03", "단일 행동|연결", "Event별 알림·검토·안내·호출을 지정합니다."),
        ("04", "Human-in-the-loop", "반복은 자동화하고 승인·예외는 담당자가 결정합니다."),
    ],
    "en": [
        ("01", "Build on|what works.", "Keep the equipment, workflow, and experience that already create value."),
        ("02", "Observe|before automating.", "Make the event visible and reliable before automating the response."),
        ("03", "Connect one|next action.", "Turn each event into a clear guide, alert, call, or review."),
        ("04", "Keep people|in command.", "Automate repetition. Keep approval and exceptions human."),
    ],
    "ar": [
        ("01", "ابنِ على|ما يعمل.", "حافظ على المعدات وسير العمل والخبرة التي تصنع القيمة."),
        ("02", "راقب|قبل الأتمتة.", "اجعل الحدث مرئيًا وموثوقًا قبل أتمتة الاستجابة."),
        ("03", "اربط|إجراءً واحدًا.", "حوّل كل حدث إلى إرشاد أو تنبيه أو طلب أو مراجعة واضحة."),
        ("04", "أبقِ الإنسان|صاحب القرار.", "أتمت التكرار واترك الموافقة والاستثناءات للإنسان."),
    ],
}


FLOW_STEPS = {
    "ko": [
        ("관찰", "카메라·NC 코드·작업자 입력에서 현장 신호를 수집합니다."),
        ("이벤트화", "원시 신호를 지연·위험·수요 Event로 변환합니다."),
        ("행동 연결", "Event별 알림·검토·안내·호출을 지정합니다."),
        ("확인", "사람 또는 설비의 응답을 기록하고 Event를 종결합니다."),
    ],
    "en": [
        ("Observe", "Read signals from real work: camera, NC code, operator input, and field data."),
        ("Eventize", "Turn raw signals into operational events such as delay, risk, and demand."),
        ("Act", "Connect the event to one next action: alert, review, guide, or call."),
        ("Confirm", "Confirm the human or equipment response and close the event."),
    ],
    "ar": [
        ("الرصد", "قراءة إشارات العمل الفعلي مثل الكاميرا وبرنامج NC ومدخلات المشغّل."),
        ("تحويل الإشارة إلى حدث", "تحويل الإشارات الخام إلى أحداث تشغيلية مثل التأخير والخطر والطلب."),
        ("ربط الإجراء", "ربط الحدث بإجراء تالٍ واحد: تنبيه أو مراجعة أو إرشاد أو طلب."),
        ("التأكيد", "تأكيد استجابة الإنسان أو المعدّة وإغلاق الحدث."),
    ],
}


PILOT_STEPS = {
    "ko": [
        ("01", "Event 정의", "사이클 완료·경로 위험·작업 단계·공구 부족·자재 요구 중 하나를 선정합니다."),
        ("02", "입력 검증", "카메라·NC 파일·작업자 입력·기준 데이터·인터페이스를 검증합니다."),
        ("03", "행동 지정", "알림·검토·안내·호출 중 하나를 연결합니다."),
        ("04", "KPI 평가", "합의된 KPI를 기준으로 확대 적용 여부를 결정합니다."),
    ],
    "en": [
        ("01", "Choose one event", "Pick cycle complete, path risk, work step, tool shortage, or material demand."),
        ("02", "Confirm the input", "Check camera, NC file, operator input, reference data, or interface."),
        ("03", "Connect the action", "Connect one alert, review, guide, or call."),
        ("04", "Verify the KPI", "Use the agreed KPI to decide whether to continue."),
    ],
    "ar": [
        ("01", "اختيار حدث", "اختر اكتمال دورة أو خطر مسار أو خطوة عمل أو نقص أداة أو طلب مواد."),
        ("02", "تأكيد الإدخال", "تحقق من الكاميرا أو ملف NC أو إدخال المشغّل أو البيانات المرجعية أو الواجهة."),
        ("03", "ربط الإجراء", "اربط تنبيهًا أو مراجعة أو إرشادًا أو طلبًا واحدًا."),
        ("04", "تأكيد KPI", "استخدم مؤشر KPI المتفق عليه لتقرير الاستمرار."),
    ],
}


STRATEGIC_NARRATIVE = {
    "ko": {
        "title": "Cycle Time에서|Factory OS까지",
        "body": "Flowmatic은 처음부터 거대한 Factory OS를 판매하지 않는다. 가장 먼저 공장에서 누구나 이해할 수 있는 진실, Cycle Time에서 시작한다.",
        "support": "Flowmatic CT는 공장의 시간축을 만든다. 그 시간축은 Event DB가 되고, Event DB는 가공, 품질, 작업자 부하, 자재 흐름, 업무배정, 이동형 자동화를 하나로 연결한다.",
        "steps": ["CT", "Event DB", "NC / Quality / Human Factors", "Material Flow", "Operator / Fleet", "Mobile Automation", "Factory OS"],
    },
    "en": {
        "title": "From Cycle Time|to Factory OS",
        "body": "Flowmatic does not begin by selling a giant Factory OS. It starts with the smallest visible truth in the factory: cycle time.",
        "support": "Flowmatic CT creates the factory time axis. That time axis becomes Event DB. Event DB connects machining, quality, human workload, material flow, task assignment, and mobile automation.",
        "steps": ["CT", "Event DB", "NC / Quality / Human Factors", "Material Flow", "Operator / Fleet", "Mobile Automation", "Factory OS"],
    },
    "ar": {
        "title": "من زمن الدورة|إلى Factory OS",
        "body": "لا يبدأ Flowmatic ببيع نظام مصنع ضخم. يبدأ من الحقيقة الأصغر والأوضح في المصنع: زمن الدورة.",
        "support": "ينشئ Flowmatic CT محور الزمن في المصنع. يتحول هذا المحور إلى Event DB يربط التشغيل والجودة وعبء العمل وتدفق المواد وتوزيع المهام والأتمتة المتنقلة.",
        "steps": ["CT", "Event DB", "NC / Quality / Human Factors", "Material Flow", "Operator / Fleet", "Mobile Automation", "Factory OS"],
    },
}


AXIS_NARRATIVE = {
    "ko": {
        "copy": "Flowmatic CT는 공장의 시간축을 만듭니다. Flowmatic Quality는 그 시간 안에서 어떤 결과가 만들어졌는지를 기록합니다. Event DB는 언제 작업이 일어났고, 어떤 품질 결과로 이어졌으며, 다음에 어떤 행동이 필요한지를 연결합니다.",
        "ct": "공장 시간축",
        "quality": "결과축",
        "down": "CT 시간축을 Event DB에 연결",
        "up": "Quality 결과축을 Event DB에 연결",
    },
    "en": {
        "copy": "Flowmatic CT creates the factory time axis. Flowmatic Quality records the outcome created on that time axis. Event DB connects when work happened, what result it produced, and what action should follow.",
        "ct": "Factory Time Axis",
        "quality": "Outcome Axis",
        "down": "Connect the CT time axis to Event DB",
        "up": "Connect the Quality outcome axis to Event DB",
    },
    "ar": {
        "copy": "ينشئ Flowmatic CT محور الزمن في المصنع. ويسجل Flowmatic Quality النتيجة التي تشكلت على هذا المحور. ويربط Event DB وقت حدوث العمل والنتيجة التي أنتجها والإجراء الذي ينبغي أن يتبع.",
        "ct": "محور زمن المصنع",
        "quality": "محور النتائج",
        "down": "ربط محور زمن CT بقاعدة Event DB",
        "up": "ربط محور نتائج Quality بقاعدة Event DB",
    },
}


MATERIAL_FLOW = {
    "ko": {
        "title": "자재 흐름 운영지능",
        "statement": "재고의 실제 위치에서|라인사이드 투입까지",
        "body": "Flowmatic은 공장을 측정하는 데서 멈추지 않는다. 측정된 사실을 자재 이동, 작업 배정, 라스트미터 실행으로 연결한다.",
        "support": "Flowmatic은 사람이 부족을 발견하기 전에 자재가 흐르도록 만든다.",
        "flow": ["Drone Inventory", "Material Truth", "AMR Dispatch", "Last-meter Docking", "Line-side Input", "Verification"],
        "cards": [
            ("Drone Inventory", "드론은 이동형 재고 센서가 된다. 파렛트 위치, 랙 상태, 재고 불일치, 빈 랙, 실제 자재 유무를 확인한다.", ["Stock_Counted", "Stock_Mismatch", "Pallet_Located", "Pallet_Missing", "Wrong_Location", "Empty_Rack", "Material_Available"]),
            ("AMR Material Feeding", "AMR는 라인이 멈춘 뒤 호출되는 것이 아니라, 멈추기 전에 배차된다. Flowmatic은 CT, 소비속도, 자재 위치, Agent 상태를 기반으로 보급 Task를 생성한다.", ["Shortage_Risk", "Replenishment_Task", "AMR_Dispatched"]),
            ("Last-meter Logistics", "라인 근처까지 가져오는 것만으로는 충분하지 않다. Flowmatic은 도킹, 매거진 장착, 빈 용기 회수, 투입 완료 확인까지 라스트미터를 닫는다.", ["AMR_Arrived", "Docking_Complete", "Magazine_Loaded", "Material_Input_Confirmed", "Empty_Magazine_Removed", "Line_Replenished", "AMR_Released"]),
        ],
    },
    "en": {
        "title": "Material Flow Intelligence",
        "statement": "From inventory truth|to line-side input",
        "body": "Flowmatic does not stop at measuring the factory. It connects measurement to material movement, task assignment, and last-meter execution.",
        "support": "Flowmatic makes material flow before people have to notice the shortage.",
        "flow": ["Drone Inventory", "Material Truth", "AMR Dispatch", "Last-meter Docking", "Line-side Input", "Verification"],
        "cards": [
            ("Drone Inventory", "Drones become mobile inventory sensors. They verify pallet location, rack status, stock mismatch, empty racks, and actual material availability.", ["Stock_Counted", "Stock_Mismatch", "Pallet_Located", "Pallet_Missing", "Wrong_Location", "Empty_Rack", "Material_Available"]),
            ("AMR Material Feeding", "AMRs are dispatched before the line stops. Flowmatic uses CT, consumption speed, material location, and agent availability to create replenishment tasks.", ["Shortage_Risk", "Replenishment_Task", "AMR_Dispatched"]),
            ("Last-meter Logistics", "Delivery near the line is not enough. Flowmatic closes the last meters: docking, magazine loading, empty container removal, and input confirmation.", ["AMR_Arrived", "Docking_Complete", "Magazine_Loaded", "Material_Input_Confirmed", "Empty_Magazine_Removed", "Line_Replenished", "AMR_Released"]),
        ],
    },
    "ar": {
        "title": "ذكاء تدفق المواد",
        "statement": "من حقيقة المخزون|إلى إدخال جانب الخط",
        "body": "لا يتوقف Flowmatic عند قياس المصنع. يربط القياس بحركة المواد وتوزيع المهام وتنفيذ آخر أمتار.",
        "support": "يجعل Flowmatic المواد تتحرك قبل أن يلاحظ الناس النقص.",
        "flow": ["Drone Inventory", "Material Truth", "AMR Dispatch", "Last-meter Docking", "Line-side Input", "Verification"],
        "cards": [
            ("Drone Inventory", "تتحول الطائرات المسيّرة إلى حساسات مخزون متنقلة تتحقق من موقع المنصات وحالة الرفوف والتباين والرفوف الفارغة وتوفر المواد.", ["Stock_Counted", "Stock_Mismatch", "Pallet_Located", "Pallet_Missing", "Wrong_Location", "Empty_Rack", "Material_Available"]),
            ("AMR Material Feeding", "يتم إرسال AMR قبل توقف الخط. يستخدم Flowmatic زمن الدورة وسرعة الاستهلاك وموقع المادة وحالة الوكلاء لإنشاء مهام التزويد.", ["Shortage_Risk", "Replenishment_Task", "AMR_Dispatched"]),
            ("Last-meter Logistics", "الوصول قرب الخط لا يكفي. يغلق Flowmatic آخر الأمتار: الإرساء، تحميل المجلة، إزالة الحاوية الفارغة، وتأكيد الإدخال.", ["AMR_Arrived", "Docking_Complete", "Magazine_Loaded", "Material_Input_Confirmed", "Empty_Magazine_Removed", "Line_Replenished", "AMR_Released"]),
        ],
    },
}


MOBILE_AUTOMATION = {
    "ko": {
        "title": "물류를 넘어,|이동형 자동화로",
        "body": "Flowmatic은 자재만 움직이는 것이 아니다. 자동화 능력 자체를 필요한 곳으로 이동시킨다.",
        "support": "모든 설비 주변에 고정 자동화를 구축하는 대신, Flowmatic은 지금 자동화가 필요한 설비로 이동형 자동화를 보낸다.",
        "highlight": "AMR는 단순 운반차량이 아니다. Flowmatic 안에서 AMR는 이동형 실행 플랫폼이 된다.",
        "safety": "PLC와 설비 컨트롤러는 설비 내부 제어와 안전을 담당한다. Flowmatic은 기존 설비 주변의 외부 공정흐름, 이동형 자동화 Task, 자재 흐름, 완료 검증을 조정한다.",
        "levels": [
            ("Level 1", "운반 Agent", "창고에서 라인으로, 라인에서 완제품으로, 빈 파렛트를 투입 지점으로 이동한다."),
            ("Level 2", "라스트미터 물류", "도킹, 매거진 정렬, 라인사이드 투입, 빈 용기 회수를 닫는다."),
            ("Level 3", "이동형 머신텐딩", "AMR + 로봇암이 로딩, 언로딩, 지그 배치, 트레이 교환, 사이클 시작 요청을 수행한다."),
            ("Level 4", "유연한 라인 자동화", "하나의 이동형 자동화 셀이 여러 설비를 지원한다."),
            ("Level 5", "재구성 가능한 공장 자동화", "Orchestrator가 손실, 우선순위, 생산계획에 따라 자동화 능력을 배정한다."),
        ],
    },
    "en": {
        "title": "Beyond Logistics:|Mobile Automation",
        "body": "Flowmatic does not stop at moving materials. It moves automation itself.",
        "support": "Instead of building fixed automation around every machine, Flowmatic brings mobile automation to the machine that needs it now.",
        "highlight": "AMR is not only a vehicle. In Flowmatic, it becomes a mobile execution platform.",
        "safety": "PLC and machine controllers remain responsible for internal machine control and safety. Flowmatic coordinates external process orchestration, mobile automation tasks, material flow, and verification around existing machines.",
        "levels": [
            ("Level 1", "Transport Agent", "Warehouse to line. Line to finished goods. Empty pallet to input point."),
            ("Level 2", "Last-meter Logistics", "Docking, magazine alignment, line-side input, empty container return."),
            ("Level 3", "Mobile Machine Tending", "AMR + robot arm performs loading, unloading, jig placement, tray exchange, and cycle start request."),
            ("Level 4", "Flexible Line Automation", "A mobile automation cell serves multiple machines without fixed automation around every line."),
            ("Level 5", "Reconfigurable Factory Automation", "Automation capability becomes assignable by the Orchestrator according to loss, priority, and production plan."),
        ],
    },
    "ar": {
        "title": "ما بعد اللوجستيات:|الأتمتة المتنقلة",
        "body": "لا يكتفي Flowmatic بتحريك المواد. بل ينقل قدرة الأتمتة نفسها.",
        "support": "بدل بناء أتمتة ثابتة حول كل آلة، يرسل Flowmatic الأتمتة المتنقلة إلى الآلة التي تحتاجها الآن.",
        "highlight": "AMR ليس مركبة فقط. داخل Flowmatic يصبح منصة تنفيذ متنقلة.",
        "safety": "تبقى PLC ومتحكمات الماكينات مسؤولة عن التحكم الداخلي والسلامة. ينسق Flowmatic تدفق العملية الخارجي، ومهام الأتمتة المتنقلة، وتدفق المواد، والتحقق حول المعدات القائمة.",
        "levels": [
            ("Level 1", "Transport Agent", "من المخزن إلى الخط، ومن الخط إلى البضائع النهائية، ومنصة فارغة إلى نقطة الإدخال."),
            ("Level 2", "Last-meter Logistics", "الإرساء، محاذاة المجلة، إدخال جانب الخط، وإرجاع الحاوية الفارغة."),
            ("Level 3", "Mobile Machine Tending", "AMR + ذراع روبوت ينفذ التحميل والتفريغ ووضع الجيج وتبديل الصواني وطلب بدء الدورة."),
            ("Level 4", "Flexible Line Automation", "خلية أتمتة متنقلة تخدم عدة آلات دون أتمتة ثابتة حول كل خط."),
            ("Level 5", "Reconfigurable Factory Automation", "تصبح قدرة الأتمتة قابلة للتوزيع بواسطة Orchestrator حسب الخسارة والأولوية وخطة الإنتاج."),
        ],
    },
}


ORCHESTRATOR = {
    "ko": {
        "title": "Orchestrator는|가장 가까운 Agent를 고르지 않는다.",
        "body": "Flowmatic은 전체 공장손실을 가장 적게 만드는 Agent를 선택한다.",
        "agents": ["Operator", "Inspector", "Maintenance Engineer", "Production Engineer", "AMR", "AGV", "Forklift", "Drone", "Collaborative Robot", "Mobile Automation Cell", "AMR + Robot Arm"],
        "cost": ["Production Loss", "Travel Time", "Waiting Time", "Deadline Risk", "Skill Mismatch", "Workload", "Task Switching", "Safety Risk", "Battery Risk", "Payload Constraint", "Automation Capability Fit"],
        "notes": [
            "사람에게는 인지부하, 숙련도, 안전, 작업전환이 중요하다.",
            "AMR에는 배터리, 적재량, 경로, 충전상태가 중요하다.",
            "이동형 자동화 셀에는 설비 호환성, 도킹, 로봇 도달범위, 그리퍼, I/O 허가가 중요하다.",
        ],
    },
    "en": {
        "title": "The Orchestrator|does not choose the nearest agent.",
        "body": "Flowmatic chooses the agent that minimizes total factory loss.",
        "agents": ["Operator", "Inspector", "Maintenance Engineer", "Production Engineer", "AMR", "AGV", "Forklift", "Drone", "Collaborative Robot", "Mobile Automation Cell", "AMR + Robot Arm"],
        "cost": ["Production Loss", "Travel Time", "Waiting Time", "Deadline Risk", "Skill Mismatch", "Workload", "Task Switching", "Safety Risk", "Battery Risk", "Payload Constraint", "Automation Capability Fit"],
        "notes": [
            "For people, cognitive load, skill, safety, and task switching matter.",
            "For AMRs, battery, payload, route, and charging state matter.",
            "For mobile automation cells, compatibility, docking, robot reach, gripper, and I/O permission matter.",
        ],
    },
    "ar": {
        "title": "Orchestrator|لا يختار الأقرب فقط.",
        "body": "يختار Flowmatic الوكيل الذي يقلل خسارة المصنع الكلية.",
        "agents": ["Operator", "Inspector", "Maintenance Engineer", "Production Engineer", "AMR", "AGV", "Forklift", "Drone", "Collaborative Robot", "Mobile Automation Cell", "AMR + Robot Arm"],
        "cost": ["Production Loss", "Travel Time", "Waiting Time", "Deadline Risk", "Skill Mismatch", "Workload", "Task Switching", "Safety Risk", "Battery Risk", "Payload Constraint", "Automation Capability Fit"],
        "notes": [
            "بالنسبة للناس، الحمل المعرفي والمهارة والسلامة وتبديل المهام مهمة.",
            "بالنسبة إلى AMR، البطارية والحمولة والمسار وحالة الشحن مهمة.",
            "بالنسبة لخلايا الأتمتة المتنقلة، التوافق والإرساء ومدى الروبوت والقابض وتصريح I/O مهمة.",
        ],
    },
}


BROWNFIELD = {
    "ko": {
        "title": "Brownfield 공장을 위한 전략",
        "body": "Flowmatic은 이미 설비를 보유한 공장을 위해 설계된다. 라인 전체를 새로 구축하는 대신, 기존 자산 위에 감지, Event, 자재 흐름, 업무배정, 이동형 자동화를 더한다.",
        "cards": ["Existing Machines", "Event Layer", "Material Flow", "Mobile Automation", "Reconfigurable Brownfield Factory"],
        "points": ["기존 설비를 사용한다.", "감지능력을 더한다.", "Event 이력을 축적한다.", "자재 흐름을 조정한다.", "필요한 곳에 이동형 자동화를 보낸다.", "공장 전체를 갈아엎지 않고 생산성을 끌어올린다."],
    },
    "en": {
        "title": "Built for|Brownfield Factories",
        "body": "Flowmatic is designed for factories that already have machines. Instead of rebuilding the entire line, Flowmatic adds sensing, events, material flow, task orchestration, and mobile automation around existing assets.",
        "cards": ["Existing Machines", "Event Layer", "Material Flow", "Mobile Automation", "Reconfigurable Brownfield Factory"],
        "points": ["Use existing machines.", "Add sensing.", "Build Event history.", "Coordinate material flow.", "Send mobile automation where needed.", "Improve productivity without rebuilding the entire factory."],
    },
    "ar": {
        "title": "مصمم لمصانع|Brownfield",
        "body": "صُمم Flowmatic للمصانع التي تمتلك آلات بالفعل. بدل إعادة بناء الخط بالكامل، يضيف الاستشعار والأحداث وتدفق المواد وتنسيق المهام والأتمتة المتنقلة حول الأصول القائمة.",
        "cards": ["Existing Machines", "Event Layer", "Material Flow", "Mobile Automation", "Reconfigurable Brownfield Factory"],
        "points": ["استخدم الآلات القائمة.", "أضف الاستشعار.", "ابنِ سجل Event.", "نسق تدفق المواد.", "أرسل الأتمتة المتنقلة حيث تلزم.", "حسّن الإنتاجية دون إعادة بناء المصنع بالكامل."],
    },
}


ROADMAP = {
    "ko": [
        ("Phase 1", "Model-free CT", "공장의 시간축을 만든다."),
        ("Phase 2", "Event DB", "Cycle을 재사용 가능한 공장 Event로 전환한다."),
        ("Phase 3", "NC + Quality", "실제 시간, 프로그램 로직, 품질결과를 연결한다."),
        ("Phase 4", "Material Flow", "자재 부족을 예측하고, 자재 위치를 확인하고, 보급을 배차한다."),
        ("Phase 5", "Operator + Fleet", "사람, AMR, 지게차, 드론에게 Task를 배정한다."),
        ("Phase 6", "Last-meter Logistics", "운반과 실제 라인 투입 사이의 마지막 간극을 닫는다."),
        ("Phase 7", "Mobile Automation", "자동화 능력 자체를 필요한 설비로 이동시킨다."),
        ("Phase 8", "Factory OS", "공장을 재구성 가능한 Engineering Intelligence 시스템으로 운영한다."),
    ],
    "en": [
        ("Phase 1", "Model-free CT", "Create the factory time axis."),
        ("Phase 2", "Event DB", "Turn cycles into reusable factory events."),
        ("Phase 3", "NC + Quality", "Connect actual time, program logic, and quality outcomes."),
        ("Phase 4", "Material Flow", "Predict shortages, locate material, dispatch replenishment."),
        ("Phase 5", "Operator + Fleet", "Assign tasks to people, AMRs, forklifts, and drones."),
        ("Phase 6", "Last-meter Logistics", "Close the gap between delivery and actual line-side input."),
        ("Phase 7", "Mobile Automation", "Move automation capability to machines that need it now."),
        ("Phase 8", "Factory OS", "Coordinate the factory as a reconfigurable Engineering Intelligence system."),
    ],
    "ar": [
        ("Phase 1", "Model-free CT", "إنشاء محور زمن المصنع."),
        ("Phase 2", "Event DB", "تحويل الدورات إلى أحداث مصنع قابلة لإعادة الاستخدام."),
        ("Phase 3", "NC + Quality", "ربط الوقت الفعلي ومنطق البرنامج ونتائج الجودة."),
        ("Phase 4", "Material Flow", "توقع النقص، تحديد موقع المواد، وإرسال التزويد."),
        ("Phase 5", "Operator + Fleet", "توزيع المهام على الناس وAMR والرافعات والطائرات المسيّرة."),
        ("Phase 6", "Last-meter Logistics", "إغلاق الفجوة بين التسليم والإدخال الفعلي بجانب الخط."),
        ("Phase 7", "Mobile Automation", "نقل قدرة الأتمتة إلى الآلات التي تحتاجها الآن."),
        ("Phase 8", "Factory OS", "تنسيق المصنع كنظام Engineering Intelligence قابل لإعادة التكوين."),
    ],
}


FINAL_VISION = {
    "ko": {
        "title": "사람이 없는 공장이|목표가 아니다.",
        "body": "Flowmatic이 만들려는 것은 사람이 좋은 제품을 만들기 위해 시스템과 싸우지 않아도 되는 공장이다.",
        "lines": ["작업자는 무엇을 해야 할지 찾느라 시간을 쓰지 않는다.", "엔지니어는 반복 측정과 보고서 정리에 시간을 쓰지 않는다.", "관리자는 뒤늦은 보고를 기다리지 않는다.", "설비는 이유 없이 대기하지 않는다.", "자재는 사람이 부족을 발견할 때까지 기다리지 않는다.", "AMR는 특정 라인에 묶이지 않는다.", "재고의 진실은 실사 때만 드러나지 않는다.", "이동형 자동화는 필요한 설비로 이동한다.", "품질문제는 개인의 부주의로만 결론나지 않는다.", "숙련자의 경험은 퇴사와 함께 사라지지 않는다."],
        "close": "Flowmatic은 엔지니어링 판단을 운영지능으로 바꾼다.",
    },
    "en": {
        "title": "Not a factory|without people.",
        "body": "Flowmatic is trying to create a factory where people no longer need to fight the system to produce good work.",
        "lines": ["Operators do not waste time searching for what to do.", "Engineers do not waste time measuring and cleaning reports.", "Managers do not wait for delayed summaries.", "Machines do not wait without explanation.", "Materials do not wait for people to notice shortage.", "AMRs are not trapped as line-dedicated assets.", "Inventory truth is not discovered only during audit.", "Mobile automation moves to where it is needed.", "Quality problems are not reduced to personal blame.", "Skilled knowledge does not disappear when people leave."],
        "close": "Flowmatic turns engineering judgment into operating intelligence.",
    },
    "ar": {
        "title": "ليس مصنعًا|بلا أشخاص.",
        "body": "يريد Flowmatic مصنعًا لا يضطر فيه الناس إلى مقاومة النظام لإنتاج عمل جيد.",
        "lines": ["لا يضيع المشغّلون وقتهم في البحث عما يجب فعله.", "لا يضيع المهندسون وقتهم في القياس المتكرر وتنظيف التقارير.", "لا ينتظر المديرون ملخصات متأخرة.", "لا تنتظر الآلات بلا تفسير.", "لا تنتظر المواد حتى يلاحظ الناس النقص.", "لا تبقى AMR أصولًا مقيدة بخط واحد.", "لا تظهر حقيقة المخزون فقط أثناء الجرد.", "تتحرك الأتمتة المتنقلة إلى حيث تلزم.", "لا تُختزل مشاكل الجودة في لوم شخصي.", "لا تختفي خبرة المهرة عندما يغادرون."],
        "close": "يحوّل Flowmatic الحكم الهندسي إلى ذكاء تشغيلي.",
    },
}


PRODUCTS = {
    "nc": {
        "name": "G-code Intelligence",
        "class": "flowmatic-nc",
        "status": "demo",
        "video": "/flowmatic_nc_demo",
        "title": {
            "ko": "G-code Intelligence | 가공 전 공구 경로 검토",
            "en": "G-code Intelligence | Pre-cut Toolpath Review",
            "ar": "G-code Intelligence | مراجعة مسار الأداة قبل التشغيل",
        },
        "description": {
            "ko": "NC/G-code를 공구 경로, 예상 사이클타임, 검토 지점으로 바꿔 가공 전에 확인합니다.",
            "en": "Turn NC and G-code into visible toolpaths, estimated cycle time, and review points before machining.",
            "ar": "حوّل NC وG-code إلى مسارات أداة مرئية وزمن دورة تقديري ونقاط مراجعة قبل التشغيل.",
        },
        "outcome": {"ko": "가공 전 공구 경로 검토", "en": "Pre-cut toolpath review", "ar": "مراجعة مسار الأداة قبل التشغيل"},
        "card_desc": {"ko": "G-code를 공구 움직임과 사이클타임, 검토 지점으로 바꿉니다.", "en": "Turn G-code into visible motion, cycle time, and review points.", "ar": "حوّل G-code إلى حركة مرئية وزمن دورة ونقاط مراجعة."},
        "cta": {"ko": "NC 데모 보기", "en": "View NC demo", "ar": "شاهد عرض NC"},
        "hero": {"ko": "가공 전|공구 경로 검토", "en": "See the toolpath|before cutting.", "ar": "شاهد مسار الأداة|قبل التشغيل."},
        "hero_body": {"ko": "NC 코드를 해석해 공구 움직임·예상 사이클타임·위험 경로를 시각화합니다.", "en": "Read the code and rebuild the motion. Review the path before the machine runs.", "ar": "اقرأ الكود وأعد بناء الحركة. راجع المسار قبل تشغيل الماكينة."},
        "steps": {
            "ko": [("01", "NC 프로그램 해석", "공구·이송·좌표·인덱스 동작을 추출합니다."), ("02", "공구 움직임 재구성", "공구의 이동 위치와 순서를 시각화합니다."), ("03", "가공 전 검토", "예상 사이클타임과 위험 경로를 확인합니다.")],
            "en": [("01", "Parse the NC program.", "Extract tools, feeds, coordinates, and index moves."), ("02", "Reconstruct the motion.", "Show where the tool moves and in what order."), ("03", "Review before cutting.", "Check cycle time and risky moves before the machine runs.")],
            "ar": [("01", "حلّل برنامج NC.", "استخرج الأدوات والتغذية والإحداثيات وحركات الفهرسة."), ("02", "أعد بناء الحركة.", "اعرض أين تتحرك الأداة وبأي ترتيب."), ("03", "راجع قبل التشغيل.", "تحقق من زمن الدورة والحركات الخطرة قبل تشغيل الماكينة.")],
        },
        "audiences": {"ko": ["CNC 프로그래머", "생산기술 엔지니어", "가공 검토 담당자"], "en": ["CNC programmers", "Manufacturing engineers", "Machining reviewers"], "ar": ["مبرمجو CNC", "مهندسو الإنتاج", "مسؤولو مراجعة التشغيل"]},
        "inputs": {"ko": ["NC/G-code 프로그램", "저장소에 이미 사용 중인 공구·좌표·이송 정보"], "en": ["NC/G-code program", "Tool, coordinate, and feed data already used in the program"], "ar": ["برنامج NC/G-code", "معلومات الأدوات والإحداثيات والتغذية الموجودة في البرنامج"]},
        "events": {"ko": ["급속 이동 검토 지점", "경로 위험 후보", "사이클타임 검토"], "en": ["Rapid move review point", "Path risk candidate", "Cycle-time review"], "ar": ["نقطة مراجعة حركة سريعة", "مرشح خطر مسار", "مراجعة زمن الدورة"]},
        "outputs": {"ko": ["공구 경로 시각화", "이동 순서", "예상 사이클타임", "가공 전 검토 지점"], "en": ["Toolpath visualization", "Movement sequence", "Estimated cycle time", "Review points before machining"], "ar": ["تصور مسار الأداة", "تسلسل الحركة", "زمن دورة تقديري", "نقاط مراجعة قبل التشغيل"]},
        "conditions": {"ko": ["지원 형식은 대상 컨트롤러와 실제 프로그램으로 검증", "첫 파일럿은 하나의 설비 또는 프로그램 계열로 제한"], "en": ["Supported formats are verified with the target controller and real program", "First pilot is limited to one machine or program family"], "ar": ["يتم التحقق من الصيغ المدعومة باستخدام وحدة التحكم والبرنامج الفعلي", "يقتصر أول مشروع تجريبي على معدة واحدة أو عائلة برامج واحدة"]},
        "kpis": {"ko": ["가공 전 검토 시간", "가공 전에 발견한 검토 항목 수", "프로그램 수정 반복 횟수"], "en": ["Pre-machining review time", "Review items found before machining", "Program revision iterations"], "ar": ["وقت المراجعة قبل التشغيل", "عدد عناصر المراجعة المكتشفة قبل التشغيل", "عدد تكرارات تعديل البرنامج"]},
        "pilot_scope": {"ko": "한 개 설비 · 한 개 공정 · 대표 NC 프로그램 세트", "en": "One machine · one process · representative NC program set", "ar": "معدة واحدة · عملية واحدة · مجموعة برامج NC ممثلة"},
        "related": ["tms", "work-standard"],
    },
    "ct": {
        "name": "Flowmatic CT",
        "class": "flowmatic-ct",
        "status": "demo",
        "video": "/flowmatic_ct_demo",
        "title": {"ko": "Flowmatic CT | Model-free Cycle Intelligence", "en": "Flowmatic CT | Model-free Cycle Intelligence", "ar": "Flowmatic CT | ذكاء دورة بلا نموذج"},
        "description": {"ko": "학습데이터, 라벨링, GPU 추론, 전용 객체모델 없이 사용자가 지정한 움직임을 Cycle Event, Gantt, 이상 Cycle 증거영상으로 변환합니다.", "en": "Measure cycle events, Gantt timelines, and abnormal-cycle evidence without training data, labeling, GPU inference, or a custom object model.", "ar": "يقيس أحداث الدورة ومخططات Gantt وأدلة الدورات غير الطبيعية دون بيانات تدريب أو وسم أو استدلال GPU أو نموذج كائن مخصص."},
        "outcome": {"ko": "Model-free Cycle Intelligence", "en": "Model-free Cycle Intelligence", "ar": "ذكاء دورة بلا نموذج"},
        "card_desc": {"ko": "대상을 선택하고 ROI를 정의한 뒤 사이클을 측정해 손실을 드러냅니다.", "en": "Select a target, define the ROI, measure the cycle, and reveal the loss.", "ar": "حدد الهدف، عرّف ROI، قِس الدورة، واكشف الخسارة."},
        "cta": {"ko": "CT 데모 보기", "en": "View CT demo", "ar": "شاهد عرض CT"},
        "hero": {"ko": "Select. Define.|Measure. Reveal.", "en": "Select. Define.|Measure. Reveal.", "ar": "حدد. عرّف.|قِس. اكشف."},
        "hero_body": {"ko": "학습데이터·라벨링·GPU 추론·전용 객체모델 없이 지정 움직임을 추적합니다. CSRT·ROI·결정론적 상태머신이 Cycle Event·Gantt·이상 Cycle 증거영상으로 변환합니다.", "en": "Flowmatic CT does not need training data, labeling, GPU inference, or a custom object model. A user selects the motion that represents the process cycle. CSRT tracking, ROI logic, and a deterministic state machine convert that motion into cycle events, Gantt charts, and abnormal-cycle evidence.", "ar": "لا يحتاج Flowmatic CT إلى بيانات تدريب أو وسم أو استدلال GPU أو نموذج كائن مخصص. يحدد المستخدم الحركة التي تمثل دورة العملية، ثم تحولها CSRT وROI ومنطق الحالة الحتمي إلى أحداث دورة ومخططات Gantt وأدلة دورة غير طبيعية."},
        "steps": {
            "ko": [("01", "기준 영역 관찰", "고정 카메라와 ROI로 반복 위치를 추적합니다."), ("02", "사이클 경계 검출", "움직임 변화에서 시작과 종료를 판정합니다."), ("03", "시간 데이터 생성", "검출 Event를 사이클타임과 공정 타임라인으로 변환합니다.")],
            "en": [("01", "Watch a reference area.", "Observe repeated positions with a fixed camera and ROI."), ("02", "Detect the cycle boundary.", "Detect start and finish from changes in field movement."), ("03", "Build time data.", "Turn detected events into cycle time and a process timeline.")],
            "ar": [("01", "راقب منطقة مرجعية.", "راقب المواضع المتكررة بكاميرا ثابتة وROI."), ("02", "اكتشف حدود الدورة.", "اكتشف البداية والنهاية من تغيرات حركة الميدان."), ("03", "ابنِ بيانات الوقت.", "حوّل الأحداث المكتشفة إلى زمن دورة وخط زمني للعملية.")],
        },
        "audiences": {"ko": ["생산기술 엔지니어", "라인 관리자", "개선 활동 담당자"], "en": ["Manufacturing engineers", "Line managers", "Improvement teams"], "ar": ["مهندسو الإنتاج", "مديرو الخطوط", "فرق التحسين"]},
        "inputs": {"ko": ["User-selected Target", "CSRT Tracking", "Bird’s-eye ROI", "Deterministic State Machine"], "en": ["User-selected Target", "CSRT Tracking", "Bird’s-eye ROI", "Deterministic State Machine"], "ar": ["User-selected Target", "CSRT Tracking", "Bird’s-eye ROI", "Deterministic State Machine"]},
        "events": {"ko": ["사이클 시작", "사이클 종료", "사이클 완료", "변동 검토 후보"], "en": ["Cycle start", "Cycle end", "Cycle complete", "Variation review candidate"], "ar": ["بداية الدورة", "نهاية الدورة", "اكتمال الدورة", "مرشح مراجعة التغير"]},
        "outputs": {"ko": ["Cycle Event", "Gantt", "Abnormal-cycle Evidence"], "en": ["Cycle Event", "Gantt", "Abnormal-cycle Evidence"], "ar": ["Cycle Event", "Gantt", "Abnormal-cycle Evidence"]},
        "conditions": {"ko": ["고정된 카메라 위치", "검증 가능한 ROI", "조명과 시야 변화 확인", "영상 저장·보관 범위 사전 합의"], "en": ["Fixed camera position", "Verifiable ROI", "Lighting and view-change check", "Prior agreement on video storage and retention"], "ar": ["موضع كاميرا ثابت", "ROI قابل للتحقق", "فحص الإضاءة وتغير زاوية الرؤية", "اتفاق مسبق على حفظ الفيديو وفترة الاحتفاظ"]},
        "kpis": {"ko": ["자동 측정 커버리지", "수기 기록 시간", "사이클 변동 폭", "검토가 필요한 이상 이벤트 수"], "en": ["Automatic measurement coverage", "Manual recording time", "Cycle variation range", "Abnormal events requiring review"], "ar": ["تغطية القياس التلقائي", "وقت التسجيل اليدوي", "نطاق تغير الدورة", "الأحداث غير الطبيعية التي تحتاج مراجعة"]},
        "pilot_scope": {"ko": "한 개 작업 위치 또는 설비 · 반복 공정 한 종류", "en": "One work position or machine · one repeated process", "ar": "موقع عمل أو معدة واحدة · عملية متكررة واحدة"},
        "related": ["work-standard"],
    },
    "work-standard": {
        "name": "Flowmatic Work Standard",
        "class": "flowmatic-work",
        "status": "preview",
        "title": {"ko": "Flowmatic Work Standard | 작업자 단계별 안내", "en": "Flowmatic Work Standard | Operator Guidance", "ar": "Flowmatic Work Standard | إرشادات عمل خطوة بخطوة"},
        "description": {"ko": "공정 지식과 공구, 자세, 확인 항목을 작업자 시점의 단계별 안내로 제공합니다.", "en": "Turn process knowledge, tools, posture, and checks into step-by-step guidance from the operator's point of view.", "ar": "حوّل معرفة العملية والأدوات والوضعية والفحوصات إلى إرشادات خطوة بخطوة من منظور المشغّل."},
        "outcome": {"ko": "작업자 단계별 안내", "en": "Step-by-step operator guidance", "ar": "إرشادات عمل خطوة بخطوة"},
        "card_desc": {"ko": "공정 지식을 작업자가 바로 쓰는 단계별 안내로 바꿉니다.", "en": "Turn process knowledge into a clear, step-by-step operator view.", "ar": "حوّل معرفة العملية إلى عرض واضح للمشغّل خطوة بخطوة."},
        "cta": {"ko": "작동 방식 보기", "en": "See how it works", "ar": "شاهد طريقة العمل"},
        "hero": {"ko": "공정 지식의|작업자 표준화", "en": "Turn process knowledge|into clear guidance.", "ar": "حوّل معرفة العملية|إلى إرشاد واضح."},
        "hero_body": {"ko": "공구·경로·자세·확인 항목을 실제 작업 순서에 맞춘 단계별 안내로 제공합니다.", "en": "Show the right tool, path, posture, and next step. Keep the view aligned with the operator.", "ar": "اعرض الأداة والمسار والوضعية والخطوة التالية الصحيحة. واجعل العرض متوافقًا مع المشغّل."},
        "steps": {
            "ko": [("01", "공정 정보 구조화", "공구·경로·자세·작업 순서를 단계별로 정리합니다."), ("02", "작업자 시점 구성", "실제 작업 순서와 시야에 맞춰 정보를 배치합니다."), ("03", "후속 작업 안내", "필수 확인 항목과 다음 행동을 작업 시점에 제공합니다.")],
            "en": [("01", "Gather the process context.", "Bring tools, paths, posture, and sequence into one scene."), ("02", "Reframe it for the operator.", "Present the information in the order the work is performed."), ("03", "Guide the next step.", "Show the next check and action at the right moment.")],
            "ar": [("01", "اجمع سياق العملية.", "اجمع الأدوات والمسارات والوضعية والتسلسل في مشهد واحد."), ("02", "أعد صياغته للمشغّل.", "اعرض المعلومات حسب ترتيب تنفيذ العمل."), ("03", "وجّه الخطوة التالية.", "اعرض الفحص والإجراء التالي في اللحظة المناسبة.")],
        },
        "audiences": {"ko": ["작업자", "현장 리더", "교육·표준작업 담당자"], "en": ["Operators", "Field leaders", "Training and standard-work owners"], "ar": ["المشغّلون", "قادة الميدان", "مسؤولو التدريب والعمل القياسي"]},
        "inputs": {"ko": ["공정 단계", "공구 정보", "이미지 또는 영상 자료", "단계별 확인 규칙"], "en": ["Process steps", "Tool information", "Image or video material", "Step confirmation rules"], "ar": ["خطوات العملية", "معلومات الأداة", "مواد صور أو فيديو", "قواعد تأكيد كل خطوة"]},
        "events": {"ko": ["단계 시작", "확인 필요", "작업 완료", "예외 보고"], "en": ["Step start", "Confirmation needed", "Work complete", "Exception report"], "ar": ["بداية الخطوة", "تأكيد مطلوب", "اكتمال العمل", "تقرير استثناء"]},
        "outputs": {"ko": ["작업자 시점의 단계별 안내", "필요한 공구와 확인 항목", "단계 확인 기록"], "en": ["Step-by-step guidance from the operator view", "Required tools and checks", "Step confirmation record"], "ar": ["إرشاد خطوة بخطوة من منظور المشغّل", "الأدوات والفحوصات المطلوبة", "سجل تأكيد الخطوات"]},
        "conditions": {"ko": ["안내를 볼 기기와 작업 위치 정의", "표준작업 콘텐츠 책임자 지정", "변경 승인과 업데이트 절차 정의"], "en": ["Define device and work position for guidance", "Assign standard-work content owner", "Define change approval and update procedure"], "ar": ["تحديد الجهاز وموقع العمل لعرض الإرشاد", "تعيين مالك محتوى العمل القياسي", "تحديد الموافقة على التغيير وإجراء التحديث"]},
        "kpis": {"ko": ["신규 작업자 교육 시간", "누락 단계 수", "표준 준수율", "작업 중 문의 횟수"], "en": ["New-operator training time", "Missed steps", "Standard adherence", "Questions during work"], "ar": ["وقت تدريب المشغّل الجديد", "عدد الخطوات المفقودة", "نسبة الالتزام بالمعيار", "عدد الأسئلة أثناء العمل"]},
        "pilot_scope": {"ko": "반복 작업 한 종류 · 대표 작업자 그룹 · 단일 작업 화면", "en": "One repeated task · representative operator group · single work screen", "ar": "مهمة متكررة واحدة · مجموعة مشغّلين ممثلة · شاشة عمل واحدة"},
        "related": ["ct", "nc"],
    },
    "tms": {
        "name": "Flowmatic TMS",
        "display": {"ko": "Flowmatic TMS — 공구 관리", "en": "Flowmatic TMS — Tool Management", "ar": "Flowmatic TMS — إدارة الأدوات"},
        "class": "flowmatic-tms",
        "status": "preview",
        "title": {"ko": "Flowmatic TMS | 공구 수명·재고·위치 관리", "en": "Flowmatic TMS | Tool Management", "ar": "Flowmatic TMS | إدارة عمر الأدوات والمخزون والموقع"},
        "description": {"ko": "실물 공구를 공정 기록과 연결하고 수명, 재고, 위치, 사용 상태를 함께 관리합니다.", "en": "Connect physical tools to process records and keep life, stock, location, and usage status aligned.", "ar": "اربط الأدوات الفعلية بسجلات العملية وحافظ على توافق العمر والمخزون والموقع وحالة الاستخدام."},
        "outcome": {"ko": "공구 수명·재고·위치 관리", "en": "Tool life, stock, and location management", "ar": "إدارة عمر الأدوات والمخزون والموقع"},
        "card_desc": {"ko": "공구 식별, 수명, 재고, 위치를 하나의 운영 정보로 묶습니다.", "en": "Keep tool identity, life, stock, and location in one operating record.", "ar": "اجمع هوية الأداة وعمرها ومخزونها وموقعها في سجل تشغيلي واحد."},
        "cta": {"ko": "작동 방식 보기", "en": "See how it works", "ar": "شاهد طريقة العمل"},
        "hero": {"ko": "공구 식별·공정 매핑·|수명 관리", "en": "Connect every tool|to its process.", "ar": "اربط كل أداة|بعمليتها."},
        "hero_body": {"ko": "실물 공구의 식별 정보와 공정·수명·재고·위치·사용 상태를 단일 운영 기록으로 관리합니다.", "en": "Identify the physical tool and match the process. Keep life, stock, and location information aligned.", "ar": "عرّف الأداة الفعلية وطابقها مع العملية. حافظ على توافق العمر والمخزون والموقع."},
        "steps": {
            "ko": [("01", "공구 식별", "라벨·사진에서 공구 ID를 추출합니다."), ("02", "공정 매핑", "공구와 공정 기록의 대응 관계를 확인합니다."), ("03", "운영 정보 갱신", "수명·재고·위치·사용 상태를 갱신합니다.")],
            "en": [("01", "Identify the physical tool.", "Read the tool identity from a label or photo."), ("02", "Match it to the process.", "Find and confirm the corresponding process record."), ("03", "Keep the record current.", "Update life, stock, location, and usage together.")],
            "ar": [("01", "عرّف الأداة الفعلية.", "اقرأ هوية الأداة من ملصق أو صورة."), ("02", "طابقها مع العملية.", "اعثر على سجل العملية المقابل وأكده."), ("03", "حافظ على السجل محدثًا.", "حدّث العمر والمخزون والموقع والاستخدام معًا.")],
        },
        "audiences": {"ko": ["공구 관리자", "생산기술 엔지니어", "공구 준비실 또는 창고 담당자"], "en": ["Tool managers", "Manufacturing engineers", "Tool room or warehouse staff"], "ar": ["مديرو الأدوات", "مهندسو الإنتاج", "مسؤولو غرفة الأدوات أو المخزن"]},
        "inputs": {"ko": ["공구 라벨 또는 사진", "공구 마스터", "공정 매핑", "수명, 재고, 위치 정보"], "en": ["Tool label or photo", "Tool master", "Process mapping", "Life, stock, and location data"], "ar": ["ملصق الأداة أو صورتها", "بيانات الأداة الرئيسية", "ربط العملية", "بيانات العمر والمخزون والموقع"]},
        "events": {"ko": ["공구 식별", "공정 매칭", "수명 임계치", "재고 부족", "위치 변경"], "en": ["Tool identification", "Process matching", "Life threshold", "Stock low", "Location change"], "ar": ["تعريف الأداة", "مطابقة العملية", "حد العمر", "نقص المخزون", "تغير الموقع"]},
        "outputs": {"ko": ["공구와 공정의 연결 기록", "현재 수명", "재고", "위치", "사용 상태"], "en": ["Tool-process link record", "Current life", "Stock", "Location", "Usage status"], "ar": ["سجل ربط الأداة بالعملية", "العمر الحالي", "المخزون", "الموقع", "حالة الاستخدام"]},
        "conditions": {"ko": ["공구 식별 방식 정의", "기준 데이터의 원본 시스템 정의", "갱신 권한과 연동 범위 확인"], "en": ["Define tool identification method", "Define source system for reference data", "Confirm update authority and integration scope"], "ar": ["تحديد طريقة تعريف الأداة", "تحديد النظام المصدر للبيانات المرجعية", "تأكيد صلاحيات التحديث ونطاق التكامل"]},
        "kpis": {"ko": ["공구 검색 시간", "재고 정확도", "공구 부족 발생 수", "공구 수명 활용률"], "en": ["Tool search time", "Stock accuracy", "Tool shortage incidents", "Tool-life utilization"], "ar": ["وقت البحث عن الأداة", "دقة المخزون", "عدد حالات نقص الأدوات", "نسبة استخدام عمر الأداة"]},
        "pilot_scope": {"ko": "공구군 한 종류 · 공정 한 종류 · 기준 데이터 한 세트", "en": "One tool family · one process · one reference-data set", "ar": "عائلة أدوات واحدة · عملية واحدة · مجموعة بيانات مرجعية واحدة"},
        "related": ["nc", "work-standard"],
    },
    "amr": {
        "name": "Flowmatic AMR",
        "display": {"ko": "Flowmatic Fleet + Material Flow", "en": "Flowmatic Fleet + Material Flow", "ar": "Flowmatic Fleet + Material Flow"},
        "class": "flowmatic-amr",
        "status": "preview",
        "title": {"ko": "Flowmatic AMR | Fleet와 라스트미터 자재 흐름", "en": "Flowmatic AMR | Fleet and Last-meter Material Flow", "ar": "Flowmatic AMR | الأسطول وتدفق المواد في آخر أمتار"},
        "description": {"ko": "자재 요구를 Fleet 배정, 보급 이동, 라인사이드 투입 확인으로 연결하고 보급 완료까지 이벤트 상태를 추적합니다.", "en": "Connect material demand to fleet assignment, replenishment movement, and line-side input confirmation, then track the event through completion.", "ar": "اربط طلب المواد بتوزيع الأسطول وحركة التزويد وتأكيد الإدخال بجانب الخط، ثم تتبع الحدث حتى اكتماله."},
        "outcome": {"ko": "Fleet와 라스트미터 실행", "en": "Fleet and last-meter execution", "ar": "تنفيذ الأسطول وآخر أمتار"},
        "card_desc": {"ko": "자재 요구를 Fleet 배정, 보급 이동, 라인사이드 투입 확인으로 연결합니다.", "en": "Connect material demand to fleet assignment, replenishment movement, and line-side input confirmation.", "ar": "اربط طلب المواد بتوزيع الأسطول وحركة التزويد وتأكيد الإدخال بجانب الخط."},
        "cta": {"ko": "작동 방식 보기", "en": "See how it works", "ar": "شاهد طريقة العمل"},
        "hero": {"ko": "자재 요구부터|라인 투입 확인까지", "en": "Move material|before the line waits.", "ar": "حرّك المواد|قبل أن ينتظر الخط."},
        "hero_body": {"ko": "자재 부족 감지, 실행자 배정, 보급 이동, 도킹, 라인사이드 투입 확인을 단일 Event로 추적합니다.", "en": "Detect demand and connect it to operators and the fleet. Close replenishment, docking, and input confirmation before shortage becomes downtime.", "ar": "اكتشف الطلب واربطه بالمشغّلين والأسطول. أغلق التزويد والإرساء وتأكيد الإدخال قبل أن يتحول النقص إلى توقف."},
        "steps": {
            "ko": [("01", "자재 요구 Event 생성", "잔량·CT·소비속도·재고 위치를 자재 요구 Event로 변환합니다."), ("02", "실행자 배정", "사람·AMR·지게차·드론 상태를 기준으로 실행 경로를 선정합니다."), ("03", "라스트미터 종결", "도착·도킹·투입 확인·빈 용기 회수까지 Event 상태를 추적합니다.")],
            "en": [("01", "Detect demand.", "Turn level, CT, consumption speed, and material location into a material-demand event."), ("02", "Assign the agent.", "Use operator, AMR, forklift, and drone state to choose the lower-loss execution path."), ("03", "Close the last meter.", "Track arrival, docking, input confirmation, and empty-container return until the event closes.")],
            "ar": [("01", "اكتشف الطلب.", "حوّل المستوى وزمن الدورة وسرعة الاستهلاك وموقع المادة إلى حدث طلب مواد."), ("02", "وزّع الوكيل.", "استخدم حالة المشغّل وAMR والرافعة والطائرة المسيّرة لاختيار مسار تنفيذ أقل خسارة."), ("03", "أغلق آخر أمتار.", "تتبع الوصول والإرساء وتأكيد الإدخال وإرجاع الحاوية الفارغة حتى إغلاق الحدث.")],
        },
        "audiences": {"ko": ["라인 작업자", "물류 운영자", "Fleet 관제 담당자"], "en": ["Line operators", "Logistics operators", "Fleet control staff"], "ar": ["مشغّلو الخط", "مشغّلو اللوجستيات", "مسؤولو مراقبة الأسطول"]},
        "inputs": {"ko": ["CT와 소비속도", "자재 위치와 보급소 매핑", "AMR, 지게차, 드론 상태 또는 연동 인터페이스"], "en": ["CT and consumption speed", "Material location and depot mapping", "AMR, forklift, drone status or integration interface"], "ar": ["زمن الدورة وسرعة الاستهلاك", "موقع المادة وربط المستودع", "حالة AMR والرافعة والطائرة المسيّرة أو واجهة التكامل"]},
        "events": {"ko": ["Shortage_Risk", "Replenishment_Task", "AMR_Dispatched", "AMR_Arrived", "Docking_Complete", "Material_Input_Confirmed", "AMR_Released"], "en": ["Shortage_Risk", "Replenishment_Task", "AMR_Dispatched", "AMR_Arrived", "Docking_Complete", "Material_Input_Confirmed", "AMR_Released"], "ar": ["Shortage_Risk", "Replenishment_Task", "AMR_Dispatched", "AMR_Arrived", "Docking_Complete", "Material_Input_Confirmed", "AMR_Released"]},
        "outputs": {"ko": ["대상 작업자 알림", "Agent 배정 상태", "보급 진행 상태", "라인사이드 투입 확인", "Fleet 해제"], "en": ["Target operator alert", "Agent assignment state", "Replenishment progress state", "Line-side input confirmation", "Fleet release"], "ar": ["تنبيه المشغّل المستهدف", "حالة توزيع الوكيل", "حالة تقدم التزويد", "تأكيد الإدخال بجانب الخط", "تحرير الأسطول"]},
        "conditions": {"ko": ["Fleet 인터페이스와 호출 권한 확인", "안전 규칙과 예외 처리 기준 확인", "초기 파일럿은 사람 승인 후 배차를 기본값으로 사용", "라스트미터 투입 확인 방식 사전 합의"], "en": ["Confirm fleet interface and call authority", "Confirm safety rules and exception criteria", "Use human-approved dispatch as the default first pilot mode", "Agree on last-meter input confirmation method"], "ar": ["تأكيد واجهة الأسطول وصلاحية الطلب", "تأكيد قواعد السلامة ومعايير الاستثناء", "اعتماد موافقة الإنسان قبل الإرسال كإعداد أولي", "الاتفاق على طريقة تأكيد الإدخال في آخر أمتار"]},
        "kpis": {"ko": ["자재 대기시간", "부족 예측부터 Agent 배정까지의 시간", "배정부터 투입 확인까지의 시간", "자재 부족으로 인한 라인 정지 횟수"], "en": ["Material waiting time", "Shortage-risk-to-agent-assignment time", "Assignment-to-input-confirmation time", "Line stops caused by material shortage"], "ar": ["وقت انتظار المواد", "الوقت من خطر النقص إلى توزيع الوكيل", "الوقت من التوزيع إلى تأكيد الإدخال", "عدد توقفات الخط بسبب نقص المواد"]},
        "pilot_scope": {"ko": "라인 한 곳 · 보급소 한 곳 · 대표 자재 경로 한 개 · 라스트미터 확인 한 종류", "en": "One line · one depot · one representative material route · one last-meter confirmation method", "ar": "خط واحد · نقطة تزويد واحدة · مسار مواد ممثل واحد · طريقة تأكيد واحدة لآخر أمتار"},
        "related": ["ct", "work-standard"],
    },
    "quality": {
        "name": "Flowmatic Quality",
        "class": "flowmatic-quality",
        "status": "working",
        "status_badges": {
            "ko": [("is-working", "작동 프로토타입"), ("is-progress", "Inspection–Dashboard 연동 진행 중")],
            "en": [("is-working", "Working prototype"), ("is-progress", "Inspection–Dashboard integration in progress")],
            "ar": [("is-working", "نموذج أولي عامل"), ("is-progress", "تكامل Inspection–Dashboard قيد التنفيذ")],
        },
        "title": {
            "ko": "Flowmatic Quality | 검사 증빙과 운영 데이터 연결",
            "en": "Flowmatic Quality | Inspection Evidence and Operating Data",
            "ar": "Flowmatic Quality | ربط أدلة الفحص ببيانات التشغيل",
        },
        "description": {
            "ko": "멀티카메라 촬영, 양품·불량 판정, 증빙 이미지와 생산수량을 하나의 검사 이벤트로 연결합니다.",
            "en": "Connect multi-camera capture, OK/NG decisions, inspection evidence, and production counts as one inspection event.",
            "ar": "اربط الالتقاط متعدد الكاميرات وقرارات OK/NG وأدلة الفحص وكميات الإنتاج في حدث فحص واحد.",
        },
        "outcome": {
            "ko": "검사 결과를 증거와|운영 데이터로 연결합니다.",
            "en": "Connect every inspection result|to evidence and operating data.",
            "ar": "اربط كل نتيجة فحص|بالأدلة وبيانات التشغيل.",
        },
        "card_desc": {
            "ko": "멀티카메라 촬영, 양품·불량 판정, 증빙 이미지와 생산수량을 하나의 검사 이벤트로 연결합니다.",
            "en": "Connect multi-camera capture, OK/NG decisions, inspection evidence, and production counts as one inspection event.",
            "ar": "اربط الالتقاط متعدد الكاميرات وقرارات OK/NG وأدلة الفحص وكميات الإنتاج في حدث فحص واحد.",
        },
        "cta": {"ko": "Quality 작동 방식 보기", "en": "Explore Flowmatic Quality", "ar": "استكشف Flowmatic Quality"},
        "hero": {"ko": "검사 결과의|운영 Event화", "en": "Close every inspection|as an operating event.", "ar": "أغلق كل فحص|كحدث تشغيلي."},
        "hero_body": {
            "ko": "품목, LOT, 작업장, 증빙, 판정과 수량을 하나의 검사 이력으로 연결합니다.",
            "en": "Connect item, LOT, workplace, evidence, verdict, and counts in one inspection history.",
            "ar": "اربط الصنف وLOT وموقع العمل والأدلة والحكم والكميات في سجل فحص واحد.",
        },
        "steps": {
            "ko": [("01", "검사 증빙 생성", "멀티카메라 촬영과 LOT·촬영 일시를 증빙 이미지에 연결합니다."), ("02", "OK/NG 판정 기록", "수동 판정을 공통 verdict 구조로 저장하고 지능형 판정 연동 기반을 구성합니다."), ("03", "Dashboard 집계", "총수량·양품·불량·모듈별 현황을 Quality Dashboard로 전달합니다."), ("04", "검사 Event 종결", "품목·LOT·작업장·증빙·결과를 단일 Event 이력으로 저장합니다.")],
            "en": [("01", "Capture and create evidence.", "Connect multi-camera capture with LOT and capture time in the evidence record."), ("02", "Record the OK/NG verdict.", "Store manual decisions through a common verdict structure ready for future intelligent modules."), ("03", "Reconcile dashboard counts.", "Aggregate total, OK, NG, and module-level status for the Quality Dashboard."), ("04", "Close the inspection event.", "Close item, LOT, workplace, evidence, and result as one event history.")],
            "ar": [("01", "التقاط وإنشاء الدليل.", "اربط الالتقاط متعدد الكاميرات مع LOT ووقت الالتقاط في سجل الأدلة."), ("02", "تسجيل حكم OK/NG.", "احفظ القرار اليدوي عبر بنية verdict مشتركة جاهزة للوحدات الذكية مستقبلًا."), ("03", "مطابقة كميات Dashboard.", "اجمع الإجمالي وOK وNG وحالة كل وحدة لإرسالها إلى Quality Dashboard."), ("04", "إغلاق حدث الفحص.", "أغلق الصنف وLOT وموقع العمل والأدلة والنتيجة كسجل حدث واحد.")],
        },
        "audiences": {
            "ko": ["품질 검사 담당자", "생산 현장 관리자", "품질 데이터 분석 담당자"],
            "en": ["Quality inspectors", "Production supervisors", "Quality-data analysts"],
            "ar": ["مفتشو الجودة", "مشرفو الإنتاج", "محللو بيانات الجودة"],
        },
        "inputs": {
            "ko": ["멀티카메라 이미지", "품목·LOT·작업장 정보", "수동 OK/NG 판정", "생산수량과 Inspection 모듈 결과"],
            "en": ["Multi-camera images", "Item, LOT, and workplace data", "Manual OK/NG verdict", "Production counts and Inspection-module results"],
            "ar": ["صور متعددة الكاميرات", "بيانات الصنف وLOT وموقع العمل", "حكم OK/NG يدوي", "كميات الإنتاج ونتائج وحدات Inspection"],
        },
        "events": {
            "ko": ["Inspection_Started", "Capture_Completed", "Inspection_OK", "Inspection_NG", "Defect_Recorded", "Evidence_Saved"],
            "en": ["Inspection_Started", "Capture_Completed", "Inspection_OK", "Inspection_NG", "Defect_Recorded", "Evidence_Saved"],
            "ar": ["Inspection_Started", "Capture_Completed", "Inspection_OK", "Inspection_NG", "Defect_Recorded", "Evidence_Saved"],
        },
        "outputs": {
            "ko": ["총 검사수량", "양품수량", "불량수량과 불량률", "증빙 이미지", "모듈별 현황", "품목 그룹 통합 현황"],
            "en": ["Total inspected", "OK count", "NG count and defect rate", "Evidence images", "Status by module", "Consolidated item-group status"],
            "ar": ["إجمالي الفحوص", "عدد OK", "عدد NG ونسبة العيوب", "صور الأدلة", "حالة كل وحدة", "حالة مجموعة الأصناف المجمعة"],
        },
        "conditions": {
            "ko": ["카메라와 촬영 순서의 현장 검증", "품목·LOT 식별 규칙 확정", "수동 판정 책임과 수정 권한 정의", "Dashboard 전송 규격과 재처리 기준 합의"],
            "en": ["Validate cameras and capture order on site", "Confirm item and LOT identification rules", "Define manual-verdict responsibility and edit authority", "Agree dashboard-transfer schema and retry criteria"],
            "ar": ["التحقق ميدانيًا من الكاميرات وترتيب الالتقاط", "تأكيد قواعد تعريف الصنف وLOT", "تحديد مسؤولية الحكم اليدوي وصلاحية التعديل", "الاتفاق على مخطط نقل Dashboard ومعايير إعادة المعالجة"],
        },
        "kpis": {
            "ko": ["검사 기록 시간", "증빙 누락률", "수량 집계 시간", "Inspection–Dashboard 데이터 불일치율", "불량 발생부터 Dashboard 반영까지의 시간", "수작업 보고서 작성시간"],
            "en": ["Inspection recording time", "Missing-evidence rate", "Count aggregation time", "Inspection–Dashboard data mismatch rate", "Time from defect to dashboard update", "Manual report preparation time"],
            "ar": ["وقت تسجيل الفحص", "نسبة الأدلة المفقودة", "وقت تجميع الكميات", "نسبة عدم تطابق بيانات Inspection–Dashboard", "الوقت من العيب إلى تحديث Dashboard", "وقت إعداد التقرير يدويًا"],
        },
        "pilot_scope": {
            "ko": "품목 그룹 한 개 · Inspection 모듈 한 개 · 대표 카메라 구성 · Dashboard 집계 한 흐름",
            "en": "One item group · one Inspection module · representative camera setup · one dashboard aggregation flow",
            "ar": "مجموعة أصناف واحدة · وحدة Inspection واحدة · إعداد كاميرات ممثل · تدفق تجميع Dashboard واحد",
        },
        "related": ["ct", "nc"],
    },
}


PRODUCTS = {slug: PRODUCTS[slug] for slug in ("ct", "quality", "nc", "work-standard", "tms", "amr")}

PRODUCTS["ct"]["status_badges"] = {
    "ko": [("is-demo", "Functional prototype · 현장 검증 중")],
    "en": [("is-demo", "Functional prototype · field validation ongoing")],
    "ar": [("is-demo", "نموذج وظيفي · التحقق الميداني مستمر")],
}
PRODUCTS["nc"]["status_badges"] = {
    "ko": [("is-demo", "Public browser demo"), ("is-progress", "Desktop functional prototype")],
    "en": [("is-demo", "Public browser demo"), ("is-progress", "Desktop functional prototype")],
    "ar": [("is-demo", "عرض متصفح عام"), ("is-progress", "نموذج مكتبي وظيفي")],
}
PRODUCTS["nc"].update({
    "name": "G-code Intelligence",
    "display": {
        "ko": "G-code Intelligence · 구 Flowmatic NC",
        "en": "G-code Intelligence · formerly Flowmatic NC",
        "ar": "G-code Intelligence · المعروف سابقًا باسم Flowmatic NC",
    },
    "title": {
        "ko": "G-code Intelligence | Machining Intelligence 구성요소",
        "en": "G-code Intelligence | A Machining Intelligence Component",
        "ar": "G-code Intelligence | مكوّن ضمن Machining Intelligence",
    },
})
PRODUCTS["quality"]["status_badges"] = {
    "ko": [("is-demo", "Working prototype"), ("is-progress", "Inspection = 증거 입력 계층")],
    "en": [("is-demo", "Working prototype"), ("is-progress", "Inspection = evidence input layer")],
    "ar": [("is-demo", "نموذج عامل"), ("is-progress", "Inspection = طبقة إدخال الأدلة")],
}
PRODUCTS["quality"].update({
    "name": "Quality Intelligence",
    "title": {
        "ko": "Quality Intelligence | 불량에서 손실·개선업무·재발까지",
        "en": "Quality Intelligence | From Defect to Loss, Work, and Recurrence",
        "ar": "Quality Intelligence | من العيب إلى الخسارة والعمل والتكرار",
    },
    "description": {
        "ko": "불량 데이터를 실제 손실과 개선업무로 연결하고 효과와 재발을 다시 확인합니다.",
        "en": "Connect defect data to actual loss and improvement work, then verify effect and recurrence.",
        "ar": "اربط بيانات العيوب بالخسارة الفعلية وعمل التحسين، ثم تحقق من الأثر والتكرار.",
    },
    "outcome": {
        "ko": "불량 데이터에서|개선업무와 재발 확인까지",
        "en": "From defect data|to improvement work and recurrence",
        "ar": "من بيانات العيوب|إلى عمل التحسين والتكرار",
    },
    "card_desc": {
        "ko": "불량을 손실순 개선업무로 바꾸고 효과와 재발을 확인합니다.",
        "en": "Turn defects into loss-ranked improvement work and verify effect and recurrence.",
        "ar": "حوّل العيوب إلى أعمال تحسين مرتبة حسب الخسارة وتحقق من الأثر والتكرار.",
    },
    "hero": {
        "ko": "불량 데이터를|실제 손실과 개선업무로 연결합니다.",
        "en": "Connect defect data|to actual loss and improvement work.",
        "ar": "اربط بيانات العيوب|بالخسارة الفعلية وعمل التحسين.",
    },
    "hero_body": {
        "ko": "품번·원인별 손실을 기준으로 우선순위를 정하고, 분석 결과에서 개선업무로 이동한 뒤 효과와 재발을 다시 확인합니다. Inspection은 증거를 제공하는 입력 계층입니다.",
        "en": "Rank priority by actual loss for each item and cause, move from analysis into owned improvement work, then verify effect and recurrence. Inspection supplies evidence as the input layer.",
        "ar": "رتّب الأولوية حسب الخسارة الفعلية لكل صنف وسبب، وانقل التحليل إلى عمل تحسين مسؤول، ثم تحقق من الأثر والتكرار. توفر Inspection الأدلة كطبقة إدخال.",
    },
    "steps": {
        "ko": [("01", "불량과 손실 연결", "불량수량·원인·기준단가를 실제 손실 문맥으로 묶습니다."), ("02", "우선순위 결정", "품번·원인별 손실을 기준으로 개선 순서를 정합니다."), ("03", "개선업무 실행", "분석 결과를 담당자·상태·다음 확인이 있는 Worklist로 전환합니다."), ("04", "효과와 재발 확인", "조치 전후의 효과를 확인하고 재발 여부를 다시 추적합니다.")],
        "en": [("01", "Connect defect and loss", "Link quantity, cause, and reference price to actual loss context."), ("02", "Set priority", "Rank improvement by loss for each item and cause."), ("03", "Execute improvement work", "Move analysis into a worklist with owner, status, and next check."), ("04", "Verify effect and recurrence", "Compare before and after, then continue recurrence monitoring.")],
        "ar": [("01", "ربط العيب بالخسارة", "اربط الكمية والسبب والسعر المرجعي بسياق الخسارة الفعلية."), ("02", "تحديد الأولوية", "رتّب التحسين حسب خسارة كل صنف وسبب."), ("03", "تنفيذ عمل التحسين", "حوّل التحليل إلى قائمة عمل لها مسؤول وحالة وفحص تالٍ."), ("04", "التحقق من الأثر والتكرار", "قارن ما قبل الإجراء وما بعده ثم تابع التكرار.")],
    },
})
PRODUCTS["work-standard"]["status_badges"] = {
    lang: [("is-preview", label)] for lang, label in {
        "ko": "Symbolic prototype", "en": "Symbolic prototype", "ar": "نموذج رمزي"
    }.items()
}
PRODUCTS["tms"]["status_badges"] = {
    lang: [("is-preview", label)] for lang, label in {
        "ko": "Tool engineering context · development preview",
        "en": "Tool engineering context · development preview",
        "ar": "سياق هندسة الأداة · معاينة تطوير",
    }.items()
}
PRODUCTS["amr"]["display"] = {
    "ko": "Logistics Intelligence / Fleet + Material Flow",
    "en": "Logistics Intelligence / Fleet + Material Flow",
    "ar": "ذكاء اللوجستيات / الأسطول وتدفق المواد",
}
PRODUCTS["amr"]["status_badges"] = {
    lang: [("is-preview", label)] for lang, label in {
        "ko": "AMR = execution actor · safety integration pending",
        "en": "AMR = execution actor · safety integration pending",
        "ar": "AMR منفذ · تكامل السلامة قيد التحقق",
    }.items()
}


QUALITY_STATUS = {
    "ko": [
        ("Working prototype", ["불량·손실·우선순위 구조", "개선 Worklist", "효과 확인과 재발 상태"]),
        ("Evidence / input layer", ["Inspection 증빙", "품목·LOT·원인·기간 문맥"]),
        ("Integration in progress", ["Inspection 결과 연동", "현장 데이터와 기준단가 provenance 확인"]),
    ],
    "en": [
        ("Working prototype", ["Defect, loss, and priority structure", "Improvement worklist", "Effect verification and recurrence state"]),
        ("Evidence / input layer", ["Inspection evidence", "Item, LOT, cause, and period context"]),
        ("Integration in progress", ["Inspection-result integration", "Field data and reference-price provenance checks"]),
    ],
    "ar": [
        ("نموذج عامل", ["بنية العيب والخسارة والأولوية", "قائمة أعمال التحسين", "التحقق من الأثر وحالة التكرار"]),
        ("طبقة الأدلة والإدخال", ["أدلة Inspection", "سياق الصنف وLOT والسبب والفترة"]),
        ("التكامل قيد التنفيذ", ["تكامل نتائج Inspection", "فحص بيانات الميدان ومصدر السعر المرجعي"]),
    ],
}


def e(value: str) -> str:
    return escape(str(value), quote=True)


def lines(text: str) -> str:
    return '<span class="copy-lines">' + "".join(f'<span class="copy-line">{e(part.strip())}</span>' for part in text.split("|")) + "</span>"


def ul(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{e(item)}</li>" for item in items) + "</ul>"


def page_path(lang: str, slug: str = "home", compat: bool = False) -> str:
    if compat and lang == "ko":
        return "/" if slug == "home" else f"/{slug}.html"
    return f"/{lang}/" if slug == "home" else f"/{lang}/{slug}/"


def transformation_blocks(lang: str, canonical_path: str) -> tuple[str, str, str]:
    """Carry the approved closed-loop story through generator-based rebuilds."""
    source = Path("index.html") if canonical_path == "/" else Path(lang) / "index.html"
    if not source.exists():
        return "", "", ""
    existing = source.read_text(encoding="utf-8")
    patterns = (
        r'<style id="flowmatic-transformation-style">.*?</style>',
        r'<section class="transformation".*?</section>',
        r'<script id="flowmatic-transformation-script">.*?</script>',
    )
    blocks = []
    for pattern in patterns:
        match = re.search(pattern, existing, flags=re.DOTALL)
        blocks.append(match.group(0) if match else "")
    return tuple(blocks)


def abs_url(path: str) -> str:
    return f"{BASE_URL}{path}"


def product_name(product: dict, lang: str) -> str:
    return product.get("display", {}).get(lang) or product["name"]


def status_badges(product: dict, lang: str) -> str:
    custom = product.get("status_badges", {}).get(lang)
    if custom:
        return '<span class="status-badge-list">' + "".join(
            f'<span class="status-badge {e(css_class)}">{e(label)}</span>' for css_class, label in custom
        ) + "</span>"
    if product["status"] == "demo":
        return f'<span class="status-badge is-demo">{e(LANGS[lang]["demo_available"])}</span>'
    return f'<span class="status-badge is-preview">{e(LANGS[lang]["development_preview"])}</span>'


def hreflang_links(slug: str, canonical_path: str) -> str:
    links = [f'<link rel="canonical" href="{abs_url(canonical_path)}">']
    for lang in LANGS:
        links.append(f'<link rel="alternate" hreflang="{lang}" href="{abs_url(page_path(lang, slug))}">')
    links.append(f'<link rel="alternate" hreflang="x-default" href="{abs_url(page_path("ko", slug))}">')
    return "\n".join(links)


def meta_head(lang: str, slug: str, title: str, description: str, canonical_path: str) -> str:
    schema = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "name": "Flowmatic", "url": f"{BASE_URL}/", "email": CONTACT_EMAIL, "logo": f"{BASE_URL}{BRAND_PATH}/flowmatic-logo-mark.png", "image": OG_IMAGE},
            {"@type": "WebPage", "name": title, "description": description, "url": abs_url(canonical_path), "inLanguage": lang},
        ],
    }, ensure_ascii=False)
    return f"""<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta name="theme-color" content="#FFFFFF">
{hreflang_links(slug, canonical_path)}
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{abs_url(canonical_path)}">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{OG_IMAGE}">
<script type="application/ld+json">{schema}</script>
<link rel="icon" href="{BRAND_MARK}?v={BRAND_VERSION}" sizes="any" type="image/svg+xml">
<link rel="icon" href="/favicon.ico?v={BRAND_VERSION}" sizes="16x16 32x32 48x48" type="image/x-icon">
<link rel="shortcut icon" href="/favicon.ico?v={BRAND_VERSION}" type="image/x-icon">
<link rel="apple-touch-icon" sizes="180x180" href="{BRAND_PATH}/apple-touch-icon.png?v={BRAND_VERSION}">
<link rel="mask-icon" href="{BRAND_MARK}?v={BRAND_VERSION}" color="#111111">
<link rel="manifest" href="/site.webmanifest?v={BRAND_VERSION}">
<link rel="stylesheet" href="{CSS_HREF}">
</head>"""


def header(lang: str, slug: str) -> str:
    t = LANGS[lang]
    home = page_path(lang)
    nav = t["nav"]
    anchors = [
        ("approach", nav["approach"]),
        ("flow", nav["flow"]),
        ("products", nav["products"]),
        ("contact", nav["contact"]),
    ]
    nav_html = "".join(f'<a href="{home}#{key}">{e(label)}</a>' for key, label in anchors)
    lang_html = "".join(
        f'<a class="lang-button{" is-active" if code == lang else ""}" data-lang-button="{code}" data-lang-link="{code}" hreflang="{code}" lang="{code}" href="{page_path(code, slug)}">{e(meta["label"])}</a>'
        for code, meta in LANGS.items()
    )
    return f"""<a class="skip-link" href="#main">{e(t["skip"])}</a>
<header class="site-header" data-header>
<a aria-label="Flowmatic home" class="brand" href="{home}#hero"><img alt="" aria-hidden="true" class="brand-mark" height="30" src="{BRAND_MARK}" width="30"><span>Flowmatic</span></a>
<div class="header-actions">
<nav class="site-nav" data-nav id="site-nav">{nav_html}</nav>
<div aria-label="Language switcher" class="lang-switcher">{lang_html}</div>
<button aria-controls="site-nav" aria-expanded="false" class="nav-toggle" data-nav-toggle type="button"><span class="sr-only">{e(t["open"])}</span><span aria-hidden="true"></span><span aria-hidden="true"></span></button>
</div>
</header>"""


def footer(lang: str) -> str:
    h = HOME[lang]
    return f"""<footer class="site-footer">
<a aria-label="Flowmatic home" class="footer-brand" href="{page_path(lang)}#hero"><img alt="" aria-hidden="true" class="brand-mark" height="34" src="{BRAND_MARK}" width="34"><strong>Flowmatic</strong></a>
<p>{e(h["support"])}</p>
<div class="footer-links"><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><a href="{page_path(lang)}#hero">{e(LANGS[lang]["home"])}</a></div>
<small>© 2026 Flowmatic</small>
</footer>"""


def field_story(lang: str) -> str:
    labels = {
        "ko": ["현장 읽기", "이벤트 생성", "다음 행동 선택", "응답 확인", "카메라", "NC 코드", "작업자", "현장 데이터", "데이터 입력", "이벤트", "이벤트 입력", "행동", "행동 입력", "종결", "안내", "알림", "호출", "작업자<br><b>확인</b>", "보급소", "라인", "이벤트 종결", "사이클 완료", "자재 부족", "경로 위험"],
        "en": ["READ THE FIELD", "CREATE AN EVENT", "SELECT THE NEXT ACTION", "CONFIRM THE RESPONSE", "CAMERA", "NC CODE", "OPERATOR", "FIELD DATA", "DATA IN", "EVENT", "EVENT IN", "ACTION", "ACTION IN", "CLOSED", "GUIDE", "ALERT", "CALL", "OPERATOR<br><b>ACK</b>", "DEPOT", "LINE", "EVENT CLOSED", "CYCLE COMPLETE", "MATERIAL LOW", "PATH RISK"],
        "ar": ["قراءة الميدان", "إنشاء حدث", "اختيار الإجراء التالي", "تأكيد الاستجابة", "كاميرا", "كود NC", "المشغّل", "بيانات الميدان", "إدخال البيانات", "حدث", "الحدث وارد", "إجراء", "الإجراء وارد", "مغلق", "إرشاد", "تنبيه", "طلب", "المشغّل<br><b>أكد</b>", "المستودع", "الخط", "إغلاق الحدث", "اكتملت الدورة", "نقص المواد", "خطر المسار"],
    }[lang]
    return f"""<div aria-label="Flowmatic operational flow animation" class="field-story" data-field-story>
<div aria-hidden="true" class="story-rail"></div>
<section class="story-stage stage-read" data-story-stage="read"><span class="stage-number">01</span><p class="stage-label">{labels[0]}</p><div class="factory-machine"><span class="machine-door"></span><span class="machine-part"></span><span class="machine-arm"></span></div><div class="camera-unit"><span></span></div><div class="camera-cone"></div><span class="signal-chip chip-camera">{labels[4]}</span><span class="signal-chip chip-code">{labels[5]}</span><span class="signal-chip chip-operator">{labels[6]}</span><span class="phase-box read-collector">{labels[7]}</span></section>
<section class="story-stage stage-event" data-story-stage="event"><span class="stage-number">02</span><p class="stage-label">{labels[1]}</p><span class="phase-box stage-intake intake-blue">{labels[8]}</span><span class="phase-box stage-output event-output">{labels[9]}</span><div class="event-engine"><span class="event-scan-line"></span><span class="event-name event-cycle">{labels[21]}</span><span class="event-name event-material">{labels[22]}</span><span class="event-name event-risk">{labels[23]}</span></div></section>
<section class="story-stage stage-action" data-story-stage="action"><span class="stage-number">03</span><p class="stage-label">{labels[2]}</p><span class="phase-box stage-intake intake-red">{labels[10]}</span><span class="phase-box stage-output action-output">{labels[11]}</span><div class="action-router"><span class="router-core">FLOWMATIC</span><span class="action-node node-guide">{labels[14]}</span><span class="action-node node-alert">{labels[15]}</span><span class="action-node node-call">{labels[16]}</span></div></section>
<section class="story-stage stage-confirm" data-story-stage="confirm"><span class="stage-number">04</span><p class="stage-label">{labels[3]}</p><span class="phase-box stage-intake intake-yellow">{labels[12]}</span><span class="phase-box stage-output confirm-output">{labels[13]}</span><div class="response-scene"><span class="operator-screen">{labels[17]}</span><span class="mini-depot">{labels[18]}</span><span class="mini-line">{labels[19]}</span><span class="mini-amr"></span><span class="closed-state">{labels[20]}</span></div></section>
<span aria-hidden="true" class="story-packet packet-main"></span>
</div>"""


def mini_visual(slug: str, lang: str) -> str:
    if slug == "nc":
        return '<div aria-hidden="true" class="product-mini mini-nc"><svg viewBox="0 0 320 180"><path class="mini-path" d="M35 140 L35 45 L145 45 L145 92 L270 92 L270 145"></path><circle class="mini-tool" r="9"><animateMotion dur="4s" path="M35 140 L35 45 L145 45 L145 92 L270 92 L270 145" repeatCount="indefinite"></animateMotion></circle></svg></div>'
    if slug == "ct":
        return '<div aria-hidden="true" class="product-mini mini-ct"><span class="mini-roi"></span><span class="mini-object"></span><span class="mini-timer">00:12.4</span><span class="mini-cycle-bar"></span></div>'
    if slug == "quality":
        labels = {"ko": ["촬영", "판정", "집계"], "en": ["CAPTURE", "VERDICT", "COUNT"], "ar": ["التقاط", "حكم", "تجميع"]}[lang]
        return f'<div aria-hidden="true" class="product-mini mini-quality"><span>{e(labels[0])}</span><i>→</i><span>OK / NG</span><i>→</i><span>{e(labels[2])}</span></div>'
    if slug == "work-standard":
        return '<div aria-hidden="true" class="product-mini mini-work"><span class="mini-hand"></span><span class="mini-work-step s1">01</span><span class="mini-work-step s2">02</span><span class="mini-work-step s3">03</span></div>'
    if slug == "tms":
        life = {"ko": "수명", "en": "LIFE", "ar": "العمر"}[lang]
        stock = {"ko": "재고", "en": "STOCK", "ar": "المخزون"}[lang]
        return f'<div aria-hidden="true" class="product-mini mini-tms"><span>T12</span><span>D12</span><span>{e(life)}</span><span>{e(stock)}</span></div>'
    material = {"ko": "자재 부족", "en": "MATERIAL LOW", "ar": "نقص المواد"}[lang]
    depot = {"ko": "보급소", "en": "DEPOT", "ar": "المستودع"}[lang]
    line = {"ko": "A 라인", "en": "LINE A", "ar": "الخط A"}[lang]
    return f'<div aria-hidden="true" class="product-mini mini-amr-card"><span class="mini-alert">{e(material)}</span><span class="mini-amr-depot">{e(depot)}</span><span class="mini-amr-line">{e(line)}</span><span class="mini-amr-cart"></span></div>'


def product_cards(lang: str) -> str:
    cards = []
    for i, (slug, product) in enumerate(PRODUCTS.items(), start=1):
        cards.append(f"""<article class="cell product-card span-4 reveal delay-{((i - 1) % 3) + 1}">
{mini_visual(slug, lang)}
<p class="eyebrow">{e(product_name(product, lang))}</p>
<h3 class="semantic-copy card-title-fit" data-fit-min="22" data-fit-text>{lines(product["outcome"][lang])}</h3>
<p>{e(product["card_desc"][lang])}</p>
{status_badges(product, lang)}
<a class="product-link" href="{page_path(lang, slug)}"><span class="product-link-label">{e(product["cta"][lang])}</span><span aria-hidden="true">→</span></a>
</article>""")
    return "\n".join(cards)


def factory_asset(src: str, alt: str) -> str:
    png = src[:-4] + ".png" if src.endswith(".svg") else src
    return f'<figure class="factory-asset"><picture><source srcset="{e(src)}" type="image/svg+xml"><img alt="{e(alt)}" decoding="async" height="720" loading="lazy" src="{e(png)}" width="1200"></picture></figure>'


def before_after_section(lang: str) -> str:
    data = BEFORE_AFTER[lang]
    before_items = "".join(f"<li>{e(item)}</li>" for item in data["before_items"])
    after_flow = "".join(f"<span>{e(item)}</span>" for item in BEFORE_AFTER["flow"])
    labels = {
        "ko": ("BEFORE", "AFTER", "사람의 반복 연결", "같은 운영 문맥"),
        "en": ("BEFORE", "AFTER", "Repeated manual handoffs", "One operating context"),
        "ar": ("قبل", "بعد", "تسليم يدوي متكرر", "سياق تشغيل واحد"),
    }[lang]
    return f"""<section aria-labelledby="before-after-title" class="before-after section-grid" id="before-after">
<div class="cell span-12 reveal"><p class="eyebrow">What changes first</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="before-after-title">{lines(data["title"])}</h2><p class="body-large">{e(data["body"])}</p></div>
<article class="cell span-5 outcome-before reveal"><p class="eyebrow">{e(labels[0])} · {e(labels[2])}</p><h3>{e(data["before"])}</h3><ul>{before_items}</ul></article>
<div class="cell span-2 before-after-arrow reveal delay-1" aria-hidden="true">→</div>
<article class="cell span-5 outcome-after reveal delay-2"><p class="eyebrow">{e(labels[1])} · {e(labels[3])}</p><h3>{e(data["after"])}</h3><div class="context-flow">{after_flow}</div></article>
</section>"""


def outcomes_section(lang: str) -> str:
    data = OUTCOMES[lang]
    head = "".join(f"<span>{e(item)}</span>" for item in data["labels"])
    rows = "".join(
        f'<div class="outcome-row"><strong>{e(domain)}</strong><span>{e(before)}</span><span>{e(after)}</span></div>'
        for domain, before, after in data["rows"]
    )
    return f"""<section aria-labelledby="outcomes-title" class="what-changes section-grid" id="what-changes">
<div class="cell span-7 reveal"><p class="eyebrow">Four Intelligence outcomes</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="outcomes-title">{lines(data["title"])}</h2><p class="body-large">{e(data["body"])}</p></div>
<div class="cell span-12 outcome-table reveal delay-1" role="table"><div class="outcome-row outcome-head" role="row">{head}</div>{rows}</div>
</section>"""


def machining_vnext_diagrams(lang: str, data: dict) -> str:
    hierarchy = "".join(f'<span class="recipe-node">{e(item)}</span>' for item in data["hierarchy"])
    setup = "".join(f"<span>{e(item)}</span>" for item in data["setup_context"])
    labels = {
        "ko": {
            "context_title": "여러 파일을 하나의 공정으로 묶는|제조 문맥의 중심축",
            "context_body": "Machine Setup은 좌표계와 공구만이 아니라 치구·기준핀·세팅 기준까지 같은 공정의 문맥으로 묶습니다.",
            "assembly_title": "Feature에서 단위공정으로.|검사 후 최종 NC로.",
            "connected": "CONNECTED ENVIRONMENT", "air": "AIR-GAPPED ENVIRONMENT",
            "sync_title": "네트워크가 없는 설비도|같은 기준으로",
            "sync_body": "패키지의 revision·hash·manifest·출처를 확인하고, 분기된 수정은 조용히 덮어쓰지 않고 Conflict review로 보냅니다.",
        },
        "en": {
            "context_title": "The manufacturing context|that makes separate files one process",
            "context_body": "Machine Setup connects coordinates and tools with fixtures, reference pins, and setup references in the same process context.",
            "assembly_title": "From feature to unit process.|From checked blocks to final NC.",
            "connected": "CONNECTED ENVIRONMENT", "air": "AIR-GAPPED ENVIRONMENT",
            "sync_title": "One operating baseline|without a connected factory",
            "sync_body": "Verify revision, hash, manifest, and source. Divergent changes are never overwritten silently; they move to conflict review.",
        },
        "ar": {
            "context_title": "سياق التصنيع|الذي يجعل الملفات المنفصلة عملية واحدة",
            "context_body": "يربط Machine Setup الإحداثيات والأدوات مع المثبتات ودبابيس المرجع ومراجع الإعداد في سياق عملية واحدة.",
            "assembly_title": "من الميزة إلى وحدة العملية.|ومن الكتل المفحوصة إلى NC النهائي.",
            "connected": "بيئة متصلة", "air": "بيئة معزولة عن الشبكة",
            "sync_title": "معيار تشغيل واحد|من دون مصنع متصل",
            "sync_body": "تحقق من revision وhash وmanifest والمصدر. لا تُستبدل التغييرات المتفرعة بصمت، بل تنتقل إلى مراجعة التعارض.",
        },
    }[lang]
    return f"""<section aria-labelledby="recipe-context-title" class="machining-context section-grid">
<div class="cell span-5 reveal"><p class="eyebrow">Manufacturing Recipe context</p><h2 class="section-title semantic-copy" data-fit-min="32" data-fit-text id="recipe-context-title">{lines(labels["context_title"])}</h2><p class="body-large">{e(labels["context_body"])}</p><div class="setup-context">{setup}</div></div>
<div class="cell span-7 recipe-hierarchy reveal delay-1">{hierarchy}</div>
</section>
<section aria-labelledby="assembly-title" class="machining-assembly section-grid"><div class="cell span-12 reveal"><p class="eyebrow">Generate · Safety Contract · Assemble</p><h2 class="section-title semantic-copy" data-fit-min="32" data-fit-text id="assembly-title">{lines(labels["assembly_title"])}</h2></div>
<div class="cell span-12 assembly-flow reveal delay-1"><span>HOLE GROUP<br>Drill → Tap</span><span>FACE A<br>Milling</span><span>BORE B<br>Rough → Finish</span><b>OP20</b><strong>BOUNDARY CHECK<br>PASS / BLOCK</strong><b>FINAL NC</b></div></section>
<section aria-labelledby="airgap-title" class="airgap section-grid"><div class="cell span-6 reveal"><p class="eyebrow">Air-gapped / USB operation</p><h2 class="section-title semantic-copy" data-fit-min="32" data-fit-text id="airgap-title">{lines(labels["sync_title"])}</h2><p class="body-large">{e(labels["sync_body"])}</p></div>
<div class="cell span-6 airgap-flow reveal delay-1"><div><strong>{e(labels["connected"])}</strong><span>Engineering / Reference</span><span>NAS / Shared Folder</span><span>Local Machining Intelligence</span></div><div><strong>{e(labels["air"])}</strong><span>Versioned Transfer Package</span><span>USB · Verify revision / hash</span><span>Isolated Local PC</span><span>CNC / Local Operation</span></div><p>Same → No update · Newer → Safe update · Divergent → Conflict review</p></div></section>"""


def certified_core_section(lang: str) -> str:
    cards = "".join(
        f'<article class="cell certified-core-card span-3 reveal delay-{i + 1}"><h3>{e(title)}</h3><p>{e(body[lang])}</p></article>'
        for i, (title, body) in enumerate(CERTIFIED_CORE["cards"])
    )
    return f"""<section aria-labelledby="certified-core-title" class="certified-core section-grid" id="certified-core">
<div class="cell span-8 reveal"><p class="eyebrow">Certified core boundary</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="certified-core-title">{lines(CERTIFIED_CORE["title"][lang])}</h2><p class="body-large">{e(CERTIFIED_CORE["body"][lang])}</p></div>
<div class="cell span-4 reveal delay-1">{factory_asset(f"{FACTORY_OS_ASSET_PATH}/03_certified_core_boundary.svg", "Flowmatic certified core boundary")}</div>{cards}</section>"""


def intelligence_domains_section(lang: str) -> str:
    cards = []
    for i, domain in enumerate(DOMAINS):
        component_list = "".join(f"<li>{e(item)}</li>" for item in domain["components"])
        cards.append(f"""<article class="cell domain-card span-6 reveal delay-{(i % 2) + 1}">
<div class="domain-card-head"><p class="eyebrow">{e(domain["status"][lang])}</p><span>{i + 1:02}</span></div><h3>{e(domain["name"])}</h3><p>{e(domain["body"][lang])}</p><div class="intelligence-flow compact">{e(domain["flow"])}</div><ul class="domain-components">{component_list}</ul><a class="product-link" href="{page_path(lang, domain["slug"])}"><span>{e({"ko":"자세히 보기","en":"Explore domain","ar":"استكشف المجال"}[lang])}</span><span aria-hidden="true">→</span></a></article>""")
    title = {"ko":"네 개의 전문 지능.|하나의 공장 운영 언어.","en":"Four specialized intelligence domains.|One factory operating language.","ar":"أربعة مجالات ذكاء متخصصة.|لغة تشغيل واحدة للمصنع."}[lang]
    body = {"ko":"Quality · Machining · Operations · Logistics Intelligence를 공통 Manufacturing Context와 Event 체계로 통합합니다.","en":"Quality, Machining, Operations, and Logistics Intelligence share Manufacturing Context and an Event language.","ar":"تشترك مجالات ذكاء الجودة والتشغيل والعمليات واللوجستيات في سياق التصنيع ولغة الأحداث."}[lang]
    return f"""<section aria-labelledby="products-title" class="intelligence-domains section-grid" id="products">
<div class="cell span-7 reveal"><p class="eyebrow">Factory Operating Intelligence</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="products-title">{lines(title)}</h2><p class="body-large">{e(body)}</p></div>
<div class="cell span-5 reveal delay-1">{factory_asset(f"{FACTORY_OS_ASSET_PATH}/00_factory_os_four_axes.svg", "Four Flowmatic intelligence domains connected to shared manufacturing context")}</div>{''.join(cards)}</section>"""


def platform_architecture_section(lang: str) -> str:
    layers = "".join(
        f'<article class="platform-layer reveal delay-{(i % 4) + 1}"><div><p class="eyebrow">{e(status[lang])}</p><h3>{e(name)}</h3></div><p>{e(body[lang])}</p></article>'
        for i, (name, status, body) in enumerate(PLATFORM["layers"])
    )
    entities = "".join(f"<span>{e(item)}</span>" for item in PLATFORM["entities"])
    return f"""<section aria-labelledby="platform-title" class="platform-architecture section-grid" id="system">
<div class="cell span-7 reveal"><p class="eyebrow">Shared context → Event Core → Control Tower</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="platform-title">{lines(PLATFORM["title"][lang])}</h2><p class="body-large">{e(PLATFORM["body"][lang])}</p><a class="fm-button primary" href="{page_path(lang, 'platform')}">{e({"ko":"플랫폼 아키텍처 보기","en":"Explore the platform architecture","ar":"استكشف بنية المنصة"}[lang])}</a></div>
<div class="cell span-5 platform-entities reveal delay-1"><p class="eyebrow">Manufacturing Context</p>{entities}</div><div class="cell span-12 platform-stack">{layers}</div></section>"""


def component_hierarchy_section(lang: str) -> str:
    groups = [
        ("Quality Intelligence", [("Inspection · evidence/input", "quality"), ("Loss · Priority · Work · Verify · Recurrence", "quality")]),
        ("Machining Intelligence", [("G-code Intelligence", "nc"), ("Measurement / Compensation", "machining-intelligence"), ("Work Standard", "work-standard"), ("Machine / Tool Context", "tms")]),
        ("Operations Intelligence", [("Procurement · Consumables · Tool Economics", "operations-intelligence"), ("Labor · Operational Cost · Anomaly", "operations-intelligence")]),
        ("Logistics Intelligence", [("Operator · Dispatch / Fleet", "logistics-intelligence"), ("Worker · Forklift · AMR actors", "amr"), ("Last-meter Confirmation", "logistics-intelligence")]),
    ]
    cards = "".join(
        f'<article class="cell component-group span-3 reveal delay-{i + 1}"><h3>{e(title)}</h3><ul>{"".join(f"<li><a href=\"{page_path(lang, slug)}\">{e(label)}</a></li>" for label, slug in items)}</ul></article>'
        for i, (title, items) in enumerate(groups)
    )
    title = {"ko":"기존 제품 유지.|지능 도메인별 역할 구분.","en":"Existing products remain.|Their role is clearer within each intelligence domain.","ar":"تبقى المنتجات الحالية.|ويصبح دورها أوضح داخل كل مجال ذكاء."}[lang]
    return f'<section aria-labelledby="components-title" class="component-hierarchy section-grid"><div class="cell span-12 reveal"><p class="eyebrow">Component hierarchy</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="components-title">{lines(title)}</h2></div>{cards}</section>'


def built_evidence_section(lang: str) -> str:
    cards = "".join(
        f'<article class="cell evidence-card span-3 reveal delay-{i + 1}"><p class="eyebrow">{e(status[lang])}</p><h3>{e(name)}</h3><p>{e(body[lang])}</p><a class="product-link" href="{page_path(lang, slug)}"><span>{e({"ko":"확인하기","en":"Inspect","ar":"فحص"}[lang])}</span><span aria-hidden="true">→</span></a></article>'
        for i, (name, status, body, slug) in enumerate(EVIDENCE)
    )
    title = {"ko":"구현 증거와|후속 통합 범위.","en":"Separate built evidence|from the next integration.","ar":"نفصل الدليل المبني|عن التكامل التالي."}[lang]
    body = {"ko":"공개 데모·작동 프로토타입·내부 검증 MVP를 상태별로 구분합니다.","en":"Public demos, working prototypes, and internally validated MVPs are labeled as they are.","ar":"تُعرض حالة العروض العامة والنماذج العاملة وMVP الخاضع للتحقق الداخلي كما هي."}[lang]
    return f'<section aria-labelledby="evidence-title" class="built-evidence section-grid" id="demo-workflows"><div class="cell span-12 reveal"><p class="eyebrow">Built evidence</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="evidence-title">{lines(title)}</h2><p class="body-large">{e(body)}</p></div>{cards}</section>'


def deployment_modes_section(lang: str) -> str:
    cards = "".join(
        f'<article class="cell deployment-mode span-6 reveal delay-{i + 1}"><p class="eyebrow">{e(status[lang])}</p><h3>{e(name)}</h3><p>{e(body[lang])}</p></article>'
        for i, (name, body, status) in enumerate(DEPLOYMENT_MODES)
    )
    title = {"ko":"Brownfield 우선.|Greenfield 확장.","en":"Start from the existing factory.|Extend toward future Event-model design.","ar":"ابدأ من المصنع القائم.|وامتد نحو تصميم نموذج أحداث المستقبل."}[lang]
    return f'<section aria-labelledby="deployment-title" class="deployment-modes section-grid"><div class="cell span-12 reveal"><p class="eyebrow">Deployment modes</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="deployment-title">{lines(title)}</h2></div>{cards}</section>'


def component_context_section(lang: str, slug: str) -> str:
    parent, copy = COMPONENT_CONTEXT[slug]
    label = "Quality Intelligence" if parent == "quality" else FACTORY_OS_PAGES[parent]["label"]
    return f'<section aria-label="Component context" class="component-context section-grid"><div class="cell yellow span-12 reveal"><p class="eyebrow">Component context</p><p class="body-large">{e(copy[lang])}</p><a class="product-link" href="{page_path(lang, parent)}"><span>{e(label)}</span><span aria-hidden="true">→</span></a></div></section>'


def quality_current_section(lang: str) -> str:
    cards = "".join(
        f'<article class="cell quality-current-card span-3 reveal delay-{i + 1}"><h3>{e(title)}</h3><p>{e(body[lang])}</p></article>'
        for i, (title, body) in enumerate(QUALITY_CURRENT["cards"])
    )
    flow = "".join(f"<span>{e(step)}</span>" for step in QUALITY_CURRENT["flow"])
    return f"""<section aria-labelledby="quality-current-title" class="quality-current section-grid">
<div class="cell span-7 reveal"><p class="eyebrow">Quality Intelligence · Working prototype</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="quality-current-title">{lines(QUALITY_CURRENT["title"][lang])}</h2><p class="body-large">{e(QUALITY_CURRENT["body"][lang])}</p><div class="intelligence-flow">{flow}</div></div>
<div class="cell span-5 reveal delay-1"><figure class="factory-asset"><img alt="Quality Intelligence workflow from defect to recurrence" decoding="async" height="720" loading="lazy" src="{FACTORY_OS_ASSET_PATH}/quality_intelligence_workflow.svg" width="1200"></figure></div>{cards}</section>"""


def intelligence_page(lang: str, slug: str, canonical_path: str) -> str:
    data = FACTORY_OS_PAGES[slug]
    flow = "".join(f"<span>{e(step)}</span>" for step in data["flow"])
    sections = "".join(
        f'<article class="cell intelligence-section-card span-6 reveal delay-{(i % 2) + 1}"><p class="eyebrow">{e(status[lang])}</p><h2>{e(title)}</h2><p>{e(body[lang])}</p>{ul(items)}</article>'
        for i, (title, status, body, items) in enumerate(data["sections"])
    )
    asset_alt = f'{data["label"]} architecture'
    asset = f'<div class="cell span-12 reveal">{factory_asset(data["asset"], asset_alt)}</div>' if data.get("asset") else ""
    guardrail = {"ko":"공개 범위 경계","en":"Public scope boundary","ar":"حدود النطاق العام"}[lang]
    back = {"ko":"전체 지능축 보기","en":"View all intelligence domains","ar":"عرض جميع مجالات الذكاء"}[lang]
    contact = {"ko":"파일럿 상담","en":"Discuss a pilot","ar":"ناقش مشروعًا تجريبيًا"}[lang]
    vnext_diagrams = machining_vnext_diagrams(lang, data) if slug == "machining-intelligence" else ""
    return f"""<!doctype html>
<html lang="{lang}" dir="{LANGS[lang]["dir"]}">
{meta_head(lang, slug, data["title"][lang], data["description"][lang], canonical_path)}
<body class="intelligence-page" data-lang="{lang}" data-static-lang="true">{header(lang, slug)}<main id="main">
<section aria-labelledby="intelligence-title" class="intelligence-hero section-grid"><div class="cell span-7 reveal"><p class="eyebrow">{e(data["status"][lang])}</p><h1 class="hero-title semantic-copy" data-fit-min="34" data-fit-text id="intelligence-title">{lines(data["hero"][lang])}</h1><p class="body-large">{e(data["body"][lang])}</p><a class="detail-inline-back" href="{page_path(lang)}#products">← {e(back)}</a></div><div class="cell blue span-5 reveal delay-1"><p class="kicker">{e(data["label"])}</p><div class="intelligence-flow vertical">{flow}</div></div>{asset}</section>
{vnext_diagrams}
<section aria-label="Architecture details" class="intelligence-details section-grid">{sections}<div class="cell red span-12 guardrail-panel reveal"><p class="eyebrow">{e(guardrail)}</p><p class="body-large">{e(data["guardrail"][lang])}</p></div></section>
<section class="section-grid"><div class="cell yellow span-12 cta-actions"><a class="fm-button primary" href="{page_path(lang)}?interest={slug}#contact">{e(contact)}</a><a class="fm-button" href="{page_path(lang, 'platform')}">Flowmatic Platform / Factory OS</a></div></section>
</main>{footer(lang)}<script src="{SCRIPT_SRC}"></script></body></html>"""


def progression_section(lang: str) -> str:
    data = STRATEGIC_NARRATIVE[lang]
    axis = AXIS_NARRATIVE[lang]
    steps = "".join(
        f'<span class="progression-step {"is-core" if i in (0, 1, 6) else ""}">{e(step)}</span>'
        for i, step in enumerate(data["steps"])
    )
    return f"""<section aria-labelledby="progression-title" class="vision-progress section-grid" id="system">
<div class="cell span-5 reveal"><p class="eyebrow">Strategic wedge</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="progression-title">{lines(data["title"])}</h2><p class="body-large">{e(data["body"])}</p></div>
<div class="cell blue span-7 reveal delay-1"><p class="body-large">{e(data["support"])}</p><div class="progression-chain">{steps}</div></div>
<div class="cell span-12 axis-narrative reveal delay-2"><p class="body-large">{e(axis["copy"])}</p><div class="quality-axis-diagram" role="group" aria-label="CT and Quality axes connected by Event DB"><div class="axis-node axis-ct"><strong>Flowmatic CT</strong><span>{e(axis["ct"])}</span></div><span class="axis-arrow axis-arrow-down" aria-label="{e(axis["down"])}">↓</span><div class="axis-node axis-event"><strong>Event DB</strong></div><span class="axis-arrow axis-arrow-up" aria-label="{e(axis["up"])}">↑</span><div class="axis-node axis-quality"><strong>Flowmatic Quality</strong><span>{e(axis["quality"])}</span></div></div></div>
</section>"""


def material_flow_section(lang: str) -> str:
    data = MATERIAL_FLOW[lang]
    flow = "".join(f'<span>{e(item)}</span>' for item in data["flow"])
    cards = "\n".join(
        f"""<article class="cell material-card span-4 reveal delay-{i+1}"><p class="eyebrow">Material Flow</p><h3>{e(title)}</h3><p>{e(body)}</p>{ul(events)}</article>"""
        for i, (title, body, events) in enumerate(data["cards"])
    )
    return f"""<section aria-labelledby="material-title" class="material-flow section-grid" id="material-flow">
<div class="cell span-7 reveal"><p class="eyebrow">Material Flow Intelligence</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="material-title">{lines(data["title"])}</h2><p class="body-large">{e(data["body"])}</p></div>
<div class="cell yellow span-5 reveal delay-1"><h3 class="block-statement">{lines(data["statement"])}</h3><p>{e(data["support"])}</p></div>
<div class="cell span-12 reveal delay-2"><div class="mondrian-flow">{flow}</div></div>
{cards}
</section>"""


def mobile_automation_section(lang: str) -> str:
    data = MOBILE_AUTOMATION[lang]
    levels = "\n".join(
        f"""<article class="automation-level reveal delay-{(i % 3) + 1}"><span>{e(level)}</span><h3>{e(title)}</h3><p>{e(body)}</p></article>"""
        for i, (level, title, body) in enumerate(data["levels"])
    )
    return f"""<section aria-labelledby="automation-title" class="mobile-automation section-grid" id="mobile-automation">
<div class="cell span-8 reveal"><p class="eyebrow">Mobile Automation</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="automation-title">{lines(data["title"])}</h2><p class="body-large">{e(data["body"])}</p><p class="body-large">{e(data["support"])}</p></div>
<div class="cell red span-4 reveal delay-1"><h3 class="block-statement">{e(data["highlight"])}</h3></div>
<div class="cell span-12 automation-ladder">{levels}</div>
<div class="cell blue span-12 reveal"><p class="body-large">{e(data["safety"])}</p></div>
</section>"""


def orchestrator_section(lang: str) -> str:
    data = ORCHESTRATOR[lang]
    agents = "".join(f"<span>{e(agent)}</span>" for agent in data["agents"])
    cost = " + ".join(data["cost"])
    notes = "".join(f"<li>{e(note)}</li>" for note in data["notes"])
    return f"""<section aria-labelledby="orchestrator-title" class="orchestrator section-grid" id="orchestrator">
<div class="cell span-7 reveal"><p class="eyebrow">Orchestrator</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="orchestrator-title">{lines(data["title"])}</h2><p class="body-large">{e(data["body"])}</p></div>
<div class="cell yellow span-5 reveal delay-1"><p class="eyebrow">Total Cost</p><code class="cost-function">Total Cost = {e(cost)}</code></div>
<div class="cell span-12 reveal delay-2"><div class="agent-cloud">{agents}</div></div>
<div class="cell gray span-12 reveal"><ul class="related-list">{notes}</ul></div>
</section>"""


def brownfield_section(lang: str) -> str:
    data = BROWNFIELD[lang]
    cards = "".join(
        f'<span class="brownfield-card {"is-result" if i == len(data["cards"]) - 1 else ""}">{e(item)}</span>'
        for i, item in enumerate(data["cards"])
    )
    return f"""<section aria-labelledby="brownfield-title" class="brownfield section-grid" id="brownfield">
<div class="cell span-6 reveal"><p class="eyebrow">Brownfield strategy</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="brownfield-title">{lines(data["title"])}</h2><p class="body-large">{e(data["body"])}</p></div>
<div class="cell blue span-6 reveal delay-1"><div class="brownfield-equation">{cards}</div></div>
<div class="cell yellow span-12 reveal delay-2">{ul(data["points"])}</div>
</section>"""


def roadmap_section(lang: str) -> str:
    rows = "\n".join(
        f"""<article class="roadmap-item reveal delay-{(i % 4) + 1}"><span>{e(phase)}</span><h3>{e(title)}</h3><p>{e(body)}</p></article>"""
        for i, (phase, title, copy) in enumerate(FACTORY_OS_ROADMAP)
        for body in (copy[lang],)
    )
    title = {"ko": "5단계 통합 로드맵", "en": "Five-stage integration roadmap", "ar": "خارطة تكامل من خمس مراحل"}[lang]
    subtitle = {"ko": "전문 지능에서|배포 템플릿까지", "en": "From specialized intelligence|to deployment templates", "ar": "من الذكاء المتخصص|إلى قوالب النشر"}[lang]
    return f"""<section aria-labelledby="roadmap-title" class="roadmap section-grid" id="roadmap">
<div class="cell span-12 reveal"><p class="eyebrow">{e(title)}</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="roadmap-title">{lines(subtitle)}</h2></div>
<div class="cell span-12 roadmap-grid">{rows}</div>
</section>"""


def final_vision_section(lang: str) -> str:
    data = FINAL_VISION[lang]
    items = "".join(f"<li>{e(item)}</li>" for item in data["lines"])
    return f"""<section aria-labelledby="final-vision-title" class="final-vision section-grid" id="vision">
<div class="cell blue span-7 reveal"><p class="eyebrow">Final vision</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="final-vision-title">{lines(data["title"])}</h2><p class="body-large">{e(data["body"])}</p></div>
<div class="cell span-5 reveal delay-1"><ul class="vision-list">{items}</ul></div>
<div class="cell yellow span-12 reveal delay-2"><h3 class="block-statement">{e(data["close"])}</h3></div>
</section>"""


def tech_visual(slug: str, lang: str) -> str:
    if slug == "nc":
        label = {"ko": ["1 · 코드 읽기", "2 · 움직임 재구성", "3 · 가공 전 검토", "급속 이동 확인", "공구", "검토"], "en": ["1 · READ THE CODE", "2 · REBUILD THE MOTION", "3 · REVIEW BEFORE CUTTING", "CHECK RAPID MOVE", "TOOLS", "REVIEW"], "ar": ["1 · قراءة الكود", "2 · إعادة بناء الحركة", "3 · المراجعة قبل التشغيل", "تحقق من الحركة السريعة", "الأدوات", "مراجعة"]}[lang]
        return f"""<div aria-label="NC code becomes a visual toolpath and review result" class="tech-visual nc-explainer" data-tech-animation="nc">
<div class="visual-label label-input">{label[0]}</div><div class="nc-code-panel"><span class="code-line active">N120 G01 X20. Y40. F800</span><span class="code-line">N130 G02 X60. Y40. R20.</span><span class="code-line risk-line">N140 G00 Z-4.0</span><span class="code-line">N150 M81 INDEX</span></div><div class="visual-arrow arrow-a">→</div>
<div class="visual-label label-process">{label[1]}</div><div class="nc-path-stage"><svg aria-hidden="true" viewBox="0 0 420 270"><path class="nc-route" d="M40 220 L40 55 L180 55 Q230 55 230 110 L230 165 L365 165 L365 225"></path><circle class="nc-moving-tool" r="11"><animateMotion dur="6s" path="M40 220 L40 55 L180 55 Q230 55 230 110 L230 165 L365 165 L365 225" repeatCount="indefinite"></animateMotion></circle><circle class="nc-risk-zone" cx="230" cy="150" r="24"></circle></svg><span class="risk-caption">{label[3]}</span></div><div class="visual-arrow arrow-b">→</div>
<div class="visual-label label-output">{label[2]}</div><div class="nc-result-panel"><span><b>CT</b> 213.4 s</span><span><b>{label[4]}</b> 12</span><span class="result-alert"><b>{label[5]}</b> 1 path</span></div></div>"""
    if slug == "ct":
        label = {"ko": ["1 · 기준 영역 관찰", "2 · 시작·종료 감지", "3 · 타임라인 생성", "기준 ROI", "시작", "종료", "시간"], "en": ["1 · WATCH THE REFERENCE AREA", "2 · DETECT START / END", "3 · BUILD THE TIMELINE", "HOME ROI", "START", "END", "TIME"], "ar": ["1 · مراقبة منطقة المرجع", "2 · اكتشاف البداية / النهاية", "3 · بناء الخط الزمني", "منطقة ROI", "البداية", "النهاية", "الوقت"]}[lang]
        return f"""<div aria-label="Camera motion becomes cycle time events" class="tech-visual ct-explainer" data-tech-animation="ct">
<div class="visual-label label-input">{label[0]}</div><div class="ct-camera-frame"><span class="ct-camera-tag">CAMERA</span><span class="ct-roi">{label[3]}</span><span class="ct-robot-arm"></span><span class="ct-machine-door"></span></div><div class="visual-arrow arrow-a">→</div>
<div class="visual-label label-process">{label[1]}</div><div class="ct-event-panel"><strong class="ct-state" data-ct-state>HOME</strong><span class="ct-event start-event">{label[4]}</span><span class="ct-event end-event">{label[5]}</span><span class="ct-live-timer" data-ct-timer>00:00.0</span></div><div class="visual-arrow arrow-b">→</div>
<div class="visual-label label-output">{label[2]}</div><div class="ct-timeline"><span class="ct-segment load">LOAD</span><span class="ct-segment machine">MACHINE</span><span class="ct-segment unload">UNLOAD</span><span class="ct-playhead"></span><span class="ct-result"><b>{label[6]}</b><span data-ct-result>12.4 s</span></span></div></div>"""
    if slug == "quality":
        label = {
            "ko": ["1 · 촬영 및 증빙", "2 · OK / NG 판정", "3 · Dashboard 집계", "LOT · 촬영 일시", "수동 verdict", "총수량", "양품", "불량"],
            "en": ["1 · CAPTURE + EVIDENCE", "2 · OK / NG VERDICT", "3 · DASHBOARD COUNTS", "LOT · CAPTURE TIME", "MANUAL VERDICT", "TOTAL", "OK", "NG"],
            "ar": ["1 · الالتقاط والأدلة", "2 · حكم OK / NG", "3 · تجميع Dashboard", "LOT · وقت الالتقاط", "حكم يدوي", "الإجمالي", "OK", "NG"],
        }[lang]
        return f"""<div aria-label="Inspection capture becomes a verdict and dashboard count" class="tech-visual quality-explainer" data-tech-animation="quality">
<div class="visual-label label-input">{label[0]}</div><div class="quality-capture"><span class="quality-camera q1"></span><span class="quality-camera q2"></span><span class="quality-evidence">{label[3]}</span></div><div class="visual-arrow arrow-a">→</div>
<div class="visual-label label-process">{label[1]}</div><div class="quality-verdict"><span>{label[4]}</span><strong class="quality-ok">OK</strong><strong class="quality-ng">NG</strong></div><div class="visual-arrow arrow-b">→</div>
<div class="visual-label label-output">{label[2]}</div><div class="quality-counts"><span><b>{label[5]}</b> 240</span><span><b>{label[6]}</b> 236</span><span><b>{label[7]}</b> 4</span></div></div>"""
    if slug == "work-standard":
        label = {"ko": ["1 · 공정·공구 데이터", "2 · 작업자 시점", "3 · 단계별 안내", "공구", "경로", "자세", "01 · 공구 장착", "02 · 표면 확인", "03 · 결과 확인"], "en": ["1 · PROCESS + TOOL DATA", "2 · OPERATOR VIEW", "3 · STEP-BY-STEP GUIDE", "TOOL", "PATH", "POSTURE", "01 · LOAD TOOL", "02 · CHECK SURFACE", "03 · CONFIRM RESULT"], "ar": ["1 · بيانات العملية والأداة", "2 · عرض المشغّل", "3 · دليل خطوة بخطوة", "الأداة", "المسار", "الوضعية", "01 · تحميل الأداة", "02 · فحص السطح", "03 · تأكيد النتيجة"]}[lang]
        return f"""<div aria-label="Process data becomes operator guidance" class="tech-visual work-explainer" data-tech-animation="work">
<div class="visual-label label-input">{label[0]}</div><div class="work-inputs"><span>{label[3]}</span><span>{label[4]}</span><span>{label[5]}</span></div><div class="visual-arrow arrow-a">→</div>
<div class="visual-label label-process">{label[1]}</div><div class="work-board"><span class="work-part"></span><span class="work-path path-face"></span><span class="work-path path-hole"></span><span class="work-cursor"></span></div><div class="visual-arrow arrow-b">→</div>
<div class="visual-label label-output">{label[2]}</div><div class="work-guide-list"><span class="guide-active">{label[6]}</span><span>{label[7]}</span><span>{label[8]}</span></div></div>"""
    if slug == "tms":
        label = {"ko": ["1 · 공구 식별", "2 · 공정 매칭", "3 · 정보 갱신", "공정 · OP20", "공구 · 엔드밀", "매칭 완료", "수명", "재고", "위치"], "en": ["1 · IDENTIFY THE TOOL", "2 · MATCH THE PROCESS", "3 · UPDATE THE RECORD", "PROCESS · OP20", "TOOL · END MILL", "MATCHED", "LIFE", "STOCK", "LOCATION"], "ar": ["1 · تعريف الأداة", "2 · مطابقة العملية", "3 · تحديث السجل", "العملية · OP20", "الأداة · قاطع نهائي", "مطابق", "العمر", "المخزون", "الموقع"]}[lang]
        return f"""<div aria-label="A physical tool label is mapped to process, life and stock" class="tech-visual tms-explainer" data-tech-animation="tms">
<div class="visual-label label-input">{label[0]}</div><div class="tms-photo"><span class="scan-corner c1"></span><span class="scan-corner c2"></span><span class="scan-corner c3"></span><span class="scan-corner c4"></span><strong>T12 / D12</strong></div><div class="visual-arrow arrow-a">→</div>
<div class="visual-label label-process">{label[1]}</div><div class="tms-match"><span>{label[3]}</span><span>{label[4]}</span><strong>{label[5]}</strong></div><div class="visual-arrow arrow-b">→</div>
<div class="visual-label label-output">{label[2]}</div><div class="tms-output"><span><b>{label[6]}</b> 72%</span><span><b>{label[7]}</b> 08</span><span><b>{label[8]}</b> A-12</span></div></div>"""
    label = {"ko": ["1 · 자재 부족 감지", "2 · Agent 배정", "3 · 라스트미터 실행", "A 라인", "자재 부족", "FLOWMATIC OPERATOR", "확인", "보급소", "투입 확인"], "en": ["1 · MATERIAL RUNS LOW", "2 · ASSIGN THE AGENT", "3 · LAST-METER EXECUTION", "LINE A", "MATERIAL LOW", "FLOWMATIC OPERATOR", "ACKNOWLEDGE", "DEPOT", "INPUT CONFIRMED"], "ar": ["1 · انخفاض المواد", "2 · توزيع الوكيل", "3 · تنفيذ آخر أمتار", "الخط A", "نقص المواد", "FLOWMATIC OPERATOR", "تأكيد", "المستودع", "تأكيد الإدخال"]}[lang]
    return f"""<div aria-label="Material low event becomes fleet assignment and last-meter execution" class="tech-visual amr-explainer" data-tech-animation="amr">
<div class="visual-label label-input">{label[0]}</div><div class="amr-line-box"><span>{label[3]}</span><div class="material-gauge"><i></i></div><strong>{label[4]}</strong></div><div class="visual-arrow arrow-a">→</div>
<div class="visual-label label-process">{label[1]}</div><div class="operator-alert"><span>{label[5]}</span><strong data-amr-message>CALL REQUEST</strong><button tabindex="-1" type="button">{label[6]}</button></div><div class="visual-arrow arrow-b">→</div>
<div class="visual-label label-output">{label[2]}</div><div class="amr-route-scene"><span class="route-depot">{label[7]}</span><span class="route-line">{label[3]}</span><span class="route-track"></span><span class="amr-cart-large"></span><span class="amr-complete">{label[8]}</span></div></div>"""


def qr_contact_signature(qr_alt: str) -> str:
    """Render the reusable official QR contact signature component."""
    return f'<figure class="qr-contact-signature"><a aria-label="{e(qr_alt)}" href="{BASE_URL}/"><img alt="{e(qr_alt)}" decoding="async" height="1400" loading="lazy" src="{QR_SIGNATURE}" width="1200"></a></figure>'


def contact_section(lang: str) -> str:
    h = HOME[lang]
    t = CONTACT_FORM[lang]
    all_label = {"ko": "전체 / 미정", "en": "All / undecided", "ar": "الكل / غير محدد"}[lang]
    options = "".join(
        f'<option value="{e(value)}">{e(all_label if value == "all" else label)}</option>'
        for value, label in CONTACT_PRODUCT_OPTIONS
    )
    controls = [
        f'<div class="contact-field"><label for="contact-organization">{e(t["organization"])}</label><input id="contact-organization" name="organization" type="text" autocomplete="organization" required aria-required="true"></div>',
        f'<div class="contact-field"><label for="contact-name">{e(t["name"])}</label><input id="contact-name" name="name" type="text" autocomplete="name" required aria-required="true"></div>',
        f'<div class="contact-field contact-field-wide"><label for="contact-product">{e(t["product"])}</label><select id="contact-product" name="product" data-contact-product>{options}</select></div>',
        f'<div class="contact-field contact-field-wide"><label for="contact-brief">{e(t["brief"])}</label><textarea id="contact-brief" name="brief" rows="8" required aria-required="true">{e(t["brief_template"])}</textarea></div>',
        f'<div class="contact-field contact-field-wide"><label for="contact-reply">{e(t["contact"])}</label><input id="contact-reply" name="reply" type="text" autocomplete="email" required aria-required="true"></div>',
    ]
    qr_alt = {
        "ko": "Flowmatic 공식 QR 연락 시그니처. 스캔하면 flowmatic-os.com을 엽니다.",
        "en": "Flowmatic official QR contact signature. Scan to open flowmatic-os.com.",
        "ar": "توقيع اتصال QR الرسمي لـ Flowmatic. امسح الرمز لفتح flowmatic-os.com.",
    }[lang]
    return f"""<section aria-labelledby="contact-title" class="cta contact-section section-grid" id="contact">
<div class="cell span-5 contact-intro reveal"><p class="eyebrow">{e(LANGS[lang]["contact"])}</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="contact-title">{lines(h["contact_title"])}</h2><p class="body-large">{e(h["contact_body"])}</p><div class="contact-email-panel"><a class="contact-email" data-contact-email href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a><div class="contact-email-actions"><button class="fm-button" data-copy-email data-copy-success="{e(t["copied"])}" data-copy-failed="{e(t["copy_failed"])}" type="button">{e(t["copy"])}</button></div><p class="contact-copy-status" data-copy-status aria-live="polite"></p></div>{qr_contact_signature(qr_alt)}</div>
<div class="cell yellow span-7 contact-form-cell reveal delay-1"><form action="{CONTACT_ENDPOINT}" data-contact-form data-required-message="{e(t["required"])}" data-sending-message="{e(t["sending"])}" data-success-message="{e(t["sent"])}" data-failed-message="{e(t["failed"])}" data-unavailable-message="{e(t["unavailable"])}" method="post" novalidate><input name="_subject" type="hidden" value="Flowmatic website inquiry"><input name="language" type="hidden" value="{e(lang)}"><div aria-hidden="true" class="contact-honeypot"><label for="contact-company-website">Website</label><input id="contact-company-website" name="_gotcha" tabindex="-1" type="text" autocomplete="off"></div><div class="contact-form-grid">{"".join(controls)}</div><button class="fm-button primary contact-submit" type="submit">{e(t["submit"])}</button><p class="contact-form-status" data-contact-form-status aria-live="polite"></p></form></div>
</section>"""


def home_page(lang: str, canonical_path: str) -> str:
    h = HOME[lang]
    transformation_style, transformation_section, transformation_script = transformation_blocks(lang, canonical_path)
    logic_cards = "".join(f'<li><strong>{e(title)}</strong><span>{e(body)}</span></li>' for title, body in FLOW_STEPS[lang])
    problem = "\n".join(f'<article class="cell {"red" if i < 2 else "gray"} problem-card span-3 reveal delay-{i+1}"><span>{num}</span><h3 class="semantic-copy card-title-fit" data-fit-min="20" data-fit-text>{lines(title)}</h3><p>{e(body)}</p></article>' for i, (num, title, body) in enumerate(PROBLEM_CARDS[lang]))
    principles = "\n".join(f'<article class="cell {"yellow" if i == 1 else "blue" if i == 3 else "gray"} strategy-card span-3 reveal delay-{i+1}"><span>{num}</span><h3 class="semantic-copy card-title-fit" data-fit-min="20" data-fit-text>{lines(title)}</h3><p>{e(body)}</p></article>' for i, (num, title, body) in enumerate(PRINCIPLES[lang]))
    pilot = "\n".join(f'<article class="cell pilot-step span-3 reveal delay-{i+1}"><span>{num}</span><h3>{e(title)}</h3><p>{e(body)}</p></article>' for i, (num, title, body) in enumerate(PILOT_STEPS[lang]))
    workflow_nc = {"ko": "NC 프로그램 → 공구 경로 재구성 → 가공 전 검토", "en": "NC program → Toolpath reconstruction → Review point", "ar": "برنامج NC → إعادة بناء مسار الأداة → نقطة مراجعة"}[lang]
    workflow_ct = {"ko": "고정 카메라 ROI → 시작·종료 이벤트 → 사이클 타임라인", "en": "Fixed camera ROI → Start/end event → Cycle timeline", "ar": "ROI لكاميرا ثابتة → حدث بداية/نهاية → خط زمني للدورة"}[lang]
    html = f"""<!doctype html>
<html lang="{lang}" dir="{LANGS[lang]["dir"]}">
{meta_head(lang, "home", h["title"], h["description"], canonical_path).replace("</head>", transformation_style + "\n</head>")}
<body data-lang="{lang}" data-static-lang="true">
{header(lang, "home")}
<main id="main">
<section aria-labelledby="hero-title" class="hero section-grid" id="hero">
<div class="cell hero-copy span-7 reveal"><p class="eyebrow">{e(h["eyebrow"])}</p><h1 class="hero-title semantic-copy brand-hero-title" data-fit-min="40" data-fit-text id="hero-title">{lines(h["h1"])}</h1><p class="body-large">{e(h["brand_subcopy"])}</p><p>{e(h["body"])}</p><div class="hero-actions"><a class="fm-button primary" href="#system">{e(h["primary"])}</a><a class="fm-button" href="#roadmap">{e(h["secondary"])}</a></div></div>
<div class="cell blue hero-layer span-5 reveal delay-1"><p class="kicker">Engineering Intelligence OS</p><h2 class="semantic-copy" data-fit-min="27" data-fit-text>{lines({"ko":"Motion → Event →|Decision → Action","en":"Motion → Event →|Decision → Action","ar":"Motion → Event →|Decision → Action"}[lang])}</h2><p class="semantic-copy copy-body" data-fit-min="17" data-fit-text>{lines(h["support"])}</p></div>
<div class="cell yellow hero-note span-4 reveal delay-2"><strong>{e(FLOW_STEPS[lang][0][0])}</strong><span>{e(FLOW_STEPS[lang][0][1])}</span></div>
<div class="cell red hero-note span-3 reveal delay-3"><strong>{e(FLOW_STEPS[lang][1][0])}</strong><span>{e(FLOW_STEPS[lang][1][1])}</span></div>
<div class="cell hero-scroll span-5 reveal delay-4"><span>{e(h["primary"])}</span><span aria-hidden="true" class="scroll-line"></span></div>
</section>
{transformation_section}
{before_after_section(lang)}
{intelligence_domains_section(lang)}
{outcomes_section(lang)}
<section aria-labelledby="strategy-title" class="strategy section-grid" id="approach">
<div class="cell span-8 reveal"><p class="eyebrow">{e({"ko":"현장 중심 설계","en":"Field-first design","ar":"تصميم يبدأ من الميدان"}[lang])}</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="strategy-title">{lines(h["strategy_title"])}</h2><p class="body-large">{e(h["strategy_body"])}</p></div>
<div class="cell blue span-4 reveal delay-1 strategy-core"><p class="kicker">Minimal intervention / Maximum clarity</p><h3>{e({"ko":"현장 제약 기반 설계","en":"Intelligence should fit the field.","ar":"يجب أن يناسب الذكاء أرض الواقع."}[lang])}</h3><p>{e(h["support"])}</p></div>{principles}</section>
<section aria-labelledby="flow-title" class="field-flow section-grid" id="flow">
<div class="cell span-5 flow-copy reveal"><p class="eyebrow">{e({"ko":"Flowmatic 작동 방식","en":"How Flowmatic works","ar":"كيف يعمل Flowmatic"}[lang])}</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="flow-title">{lines(h["flow_title"])}</h2><p class="body-large">{e(h["flow_body"])}</p><ol class="flow-explanation">{logic_cards}</ol></div>
<div class="cell span-7 flow-visual-cell reveal delay-1">{field_story(lang)}</div>
</section>
{built_evidence_section(lang)}
{platform_architecture_section(lang)}
{component_hierarchy_section(lang)}
{certified_core_section(lang)}
{deployment_modes_section(lang)}
{roadmap_section(lang)}
<section aria-labelledby="pilot-title" class="pilot section-grid" id="pilot">
<div class="cell span-12 reveal"><p class="eyebrow">{e({"ko":"파일럿 진행 방식","en":"Pilot approach","ar":"نهج المشروع التجريبي"}[lang])}</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="pilot-title">{lines(h["pilot_title"])}</h2></div>{pilot}<div class="cell yellow span-12 pilot-note reveal"><p class="body-large">{e(h["deploy_note"])}</p></div></section>
{contact_section(lang)}
</main>{footer(lang)}{transformation_script}<script src="{SCRIPT_SRC}"></script></body></html>"""
    return html


def demo_panel(product: dict, slug: str, lang: str) -> str:
    if product["status"] == "demo":
        title = {"ko": f"{product['name']} 실제 데모", "en": f"{product['name']} working demo", "ar": f"عرض {product['name']} العملي"}[lang]
        summary = product["description"][lang]
        return f"""<div class="cell span-4 demo-copy reveal"><p class="eyebrow">{e(LANGS[lang]["product_demo"])}</p><h2 class="section-title semantic-copy" data-fit-min="28" data-fit-text id="demo-title">{lines(title)}</h2><p class="body-large">{e(summary)}</p></div>
<div class="cell span-8 demo-cell reveal delay-1"><div class="demo-player" data-demo-video data-video-base="{e(product["video"])}" data-video-title="{e(product["name"])} demo"><video aria-label="{e(product["name"])} demo" controls hidden playsinline preload="metadata" poster="{BRAND_PATH}/flowmatic-og.svg" width="1920" height="1080"></video><div class="video-placeholder" data-video-placeholder><span aria-hidden="true" class="video-icon">▶</span><p><strong>{e(LANGS[lang]["video_unavailable"])}</strong></p></div></div><p class="video-summary">{e(summary)}</p></div>"""
    scope = {"ko": "작동 개념과 현재 연동 범위", "en": "Operating concept and current integration scope", "ar": "مفهوم التشغيل ونطاق التكامل الحالي"}[lang]
    eyebrow = product.get("status_badges", {}).get(lang, [("", LANGS[lang]["development_preview"])])[0][1]
    return f"""<div class="cell span-4 demo-copy reveal"><p class="eyebrow">{e(eyebrow)}</p><h2 class="section-title semantic-copy" data-fit-min="28" data-fit-text id="demo-title">{lines(product["outcome"][lang])}</h2><p class="body-large">{e(product["description"][lang])}</p></div>
<div class="cell span-8 demo-cell reveal delay-1"><div class="development-panel">{status_badges(product, lang)}<h3>{e(product_name(product, lang))}</h3><ul><li><strong>{e(LANGS[lang]["current_scope"])}:</strong> {e(scope)}</li><li><strong>{e(LANGS[lang]["pilot_input"])}:</strong> {e(product["inputs"][lang][0])}</li><li><strong>{e(LANGS[lang]["pilot_result"])}:</strong> {e(product["outputs"][lang][0])}</li></ul><a class="fm-button primary" href="{page_path(lang)}?interest={slug}#contact">{e(LANGS[lang]["pilot"])}</a></div></div>"""


def quality_status_section(lang: str) -> str:
    cards = []
    classes = ["is-implemented", "is-progress", "is-target"]
    for i, (status, items) in enumerate(QUALITY_STATUS[lang]):
        cards.append(f'<article class="cell quality-status-card span-4 {classes[i]} reveal delay-{i+1}"><p class="eyebrow">{e(status)}</p>{ul(items)}</article>')
    title = {"ko": "구현·연동·목표|범위 구분", "en": "Implementation status|is explicit.", "ar": "حالة التنفيذ|واضحة ومحددة."}[lang]
    body = {"ko": "현재 구현, 연동 진행, 목표 아키텍처를 단계별로 구분합니다.", "en": "Working scope, integration work, and architecture targets are shown separately.", "ar": "يتم عرض النطاق العامل وأعمال التكامل وأهداف البنية بشكل منفصل."}[lang]
    return f'<section aria-labelledby="quality-status-title" class="quality-status section-grid"><div class="cell span-12 reveal"><p class="eyebrow">Flowmatic Quality status</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="quality-status-title">{lines(title)}</h2><p class="body-large">{e(body)}</p></div>{"".join(cards)}</section>'


NC_BROWSER_DEMO = {
    "ko": {
        "eyebrow": "TRY FLOWMATIC NC",
        "title": "NC 프로그램의|시간 구조 분석",
        "body": "G-code의 절삭·급속이송·공구교환을 분석해 이론상 프로그램 시간을 산출합니다.",
        "privacy": "파일은 이 브라우저 안에서만 분석되며 서버로 전송되지 않습니다.",
        "drop": "NC, CNC, TAP 또는 TXT 파일을 여기에 놓으세요.",
        "open": "NC 파일 열기",
        "sample": "샘플 실행",
        "reset": "초기화",
        "recalculate": "다시 계산",
        "settings": "계산 설정",
        "rapid_feed": "Rapid Feed",
        "default_feed": "Default Cutting Feed",
        "tool_change": "Tool Change Time",
        "file": "파일",
        "size": "크기",
        "lines": "전체 행 수",
        "motions": "계산 가능한 이동",
        "excluded": "제외된 명령",
        "result": "이론상 프로그램 예상시간",
        "condition": "프로그램에 기록된 좌표와 이송속도를 기준으로 계산한 이론값입니다.",
        "disclaimer": "실제 설비 시간은 가감속, 공구교환 동작, 스핀들 응답, PLC 대기, 클램핑, 매크로, 서브프로그램 및 설비 고유 동작에 따라 달라질 수 있습니다.",
        "status": "Analysis Status",
        "empty": "샘플을 실행하거나 로컬 NC 파일을 선택하세요.",
        "cutting": "Cutting",
        "rapid": "Rapid",
        "tool_change_label": "Tool Change",
        "tools": "Tools",
        "motion_blocks": "Motion Blocks",
        "excluded_blocks": "Excluded Blocks",
        "warnings": "경고 및 계산 제외 항목",
        "show_all": "전체 경고 보기",
        "tool_results": "공구별 시간",
        "preview": "G-code 미리보기",
    },
    "en": {
        "eyebrow": "TRY FLOWMATIC NC",
        "title": "Open the program.|See where the time goes.",
        "body": "Analyze basic G-code movements directly in your browser and review the theoretical time structure.",
        "privacy": "Your file is analyzed locally in this browser and is not uploaded.",
        "drop": "Drop an NC, CNC, TAP, TXT, or MIN file here.",
        "open": "Open NC file",
        "sample": "Run sample",
        "reset": "Reset",
        "recalculate": "Recalculate",
        "settings": "Calculation settings",
        "rapid_feed": "Rapid Feed",
        "default_feed": "Default Cutting Feed",
        "tool_change": "Tool Change Time",
        "file": "File",
        "size": "Size",
        "lines": "Lines",
        "motions": "Calculated moves",
        "excluded": "Excluded blocks",
        "result": "Theoretical Program Time",
        "condition": "Calculated from programmed coordinates and feed rates.",
        "disclaimer": "Actual machine time can vary with acceleration, tool-change motion, spindle response, PLC waiting, clamping, macros, subprograms, and machine-specific behavior.",
        "status": "Analysis Status",
        "empty": "Run the sample or choose a local NC file.",
        "cutting": "Cutting",
        "rapid": "Rapid",
        "tool_change_label": "Tool Change",
        "tools": "Tools",
        "motion_blocks": "Motion Blocks",
        "excluded_blocks": "Excluded Blocks",
        "warnings": "Warnings and excluded items",
        "show_all": "Show all warnings",
        "tool_results": "Time by tool",
        "preview": "G-code preview",
    },
    "ar": {
        "eyebrow": "TRY FLOWMATIC NC",
        "title": "افتح البرنامج.|واكتشف أين يذهب الوقت.",
        "body": "حلّل حركات G-code الأساسية مباشرة داخل المتصفح وراجع بنية الوقت النظرية.",
        "privacy": "يتم تحليل ملفك محليًا داخل هذا المتصفح ولا يتم رفعه إلى الخادم.",
        "drop": "ضع ملف NC أو CNC أو TAP أو TXT أو MIN هنا.",
        "open": "فتح ملف NC",
        "sample": "تشغيل العينة",
        "reset": "إعادة ضبط",
        "recalculate": "إعادة الحساب",
        "settings": "إعدادات الحساب",
        "rapid_feed": "Rapid Feed",
        "default_feed": "Default Cutting Feed",
        "tool_change": "Tool Change Time",
        "file": "الملف",
        "size": "الحجم",
        "lines": "عدد الأسطر",
        "motions": "الحركات المحسوبة",
        "excluded": "الأوامر المستبعدة",
        "result": "Theoretical Program Time",
        "condition": "محسوب من الإحداثيات وسرعات التغذية المكتوبة في البرنامج.",
        "disclaimer": "قد يختلف وقت الماكينة الفعلي بسبب التسارع، وحركة تغيير الأداة، واستجابة المغزل، وانتظار PLC، والتثبيت، والماكرو، والبرامج الفرعية، وسلوك المعدة الخاص.",
        "status": "Analysis Status",
        "empty": "شغّل العينة أو اختر ملف NC محليًا.",
        "cutting": "Cutting",
        "rapid": "Rapid",
        "tool_change_label": "Tool Change",
        "tools": "Tools",
        "motion_blocks": "Motion Blocks",
        "excluded_blocks": "Excluded Blocks",
        "warnings": "التحذيرات والعناصر المستبعدة",
        "show_all": "عرض كل التحذيرات",
        "tool_results": "الوقت حسب الأداة",
        "preview": "معاينة G-code",
    },
}


def nc_browser_demo_section(lang: str) -> str:
    t = NC_BROWSER_DEMO[lang]
    return f"""<section aria-labelledby="nc-browser-demo-title" class="nc-browser-demo-lite section-grid" data-nc-demo-lite>
<div class="cell span-12 nc-demo-title-cell reveal"><p class="eyebrow">{e(t["eyebrow"])}</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="nc-browser-demo-title">{lines(t["title"])}</h2><p class="body-large">{e(t["body"])}</p></div>
<div class="cell span-5 nc-demo-input-cell reveal delay-1">
<div class="nc-demo-dropzone" data-nc-dropzone tabindex="0" role="button" aria-controls="nc-demo-file"><strong>{e(t["drop"])}</strong><span>{e(t["privacy"])}</span></div>
<input accept=".nc,.cnc,.tap,.txt,.min" class="sr-only" data-nc-file id="nc-demo-file" type="file">
<div class="nc-demo-actions"><label class="fm-button primary" for="nc-demo-file">{e(t["open"])}</label><button class="fm-button" data-nc-sample type="button">{e(t["sample"])}</button><button class="fm-button" data-nc-reset type="button">{e(t["reset"])}</button></div>
<p class="nc-demo-privacy">{e(t["privacy"])}</p>
<dl class="nc-demo-file-meta"><div><dt>{e(t["file"])}</dt><dd data-nc-meta="file">—</dd></div><div><dt>{e(t["size"])}</dt><dd data-nc-meta="size">—</dd></div><div><dt>{e(t["lines"])}</dt><dd data-nc-meta="lines">—</dd></div><div><dt>{e(t["motions"])}</dt><dd data-nc-meta="motions">—</dd></div><div><dt>{e(t["excluded"])}</dt><dd data-nc-meta="excluded">—</dd></div></dl>
<details class="nc-demo-settings"><summary>{e(t["settings"])}</summary><div class="nc-demo-setting-grid"><label>{e(t["rapid_feed"])}<input data-nc-setting="rapidFeed" inputmode="decimal" min="1" step="100" type="number" value="20000"><span>mm/min</span></label><label>{e(t["default_feed"])}<input data-nc-setting="defaultFeed" inputmode="decimal" min="1" step="10" type="number" value="1000"><span>mm/min</span></label><label>{e(t["tool_change"])}<input data-nc-setting="toolChange" inputmode="decimal" min="0" step="0.1" type="number" value="6.0"><span>sec/change</span></label></div><button class="fm-button primary" data-nc-recalculate type="button">{e(t["recalculate"])}</button></details>
</div>
<div class="cell span-7 nc-demo-result-cell reveal delay-2" aria-live="polite">
<p class="eyebrow">{e(t["result"])}</p><strong class="nc-demo-total" data-nc-result="total">—</strong><p class="nc-demo-condition">{e(t["condition"])}</p>
<div class="nc-demo-status"><span>{e(t["status"])}</span><strong data-nc-result="status">{e(t["empty"])}</strong></div>
<div class="nc-demo-kpi-grid"><article><span>{e(t["cutting"])}</span><strong data-nc-result="cutting">—</strong></article><article><span>{e(t["rapid"])}</span><strong data-nc-result="rapid">—</strong></article><article><span>{e(t["tool_change_label"])}</span><strong data-nc-result="toolChange">—</strong></article><article><span>{e(t["tools"])}</span><strong data-nc-result="tools">—</strong></article><article><span>{e(t["motion_blocks"])}</span><strong data-nc-result="motionBlocks">—</strong></article><article><span>{e(t["excluded_blocks"])}</span><strong data-nc-result="excludedBlocks">—</strong></article></div>
<div class="nc-demo-timebar" aria-label="{e(t["result"])}"><span data-nc-bar="cutting"></span><span data-nc-bar="rapid"></span><span data-nc-bar="toolChange"></span></div>
<div class="nc-demo-legend"><span>{e(t["cutting"])}</span><span>{e(t["rapid"])}</span><span>{e(t["tool_change_label"])}</span></div>
<p class="nc-demo-disclaimer">{e(t["disclaimer"])}</p>
</div>
<div class="cell span-6 nc-demo-warning-cell reveal"><h3>{e(t["warnings"])}</h3><div data-nc-alert role="alert" hidden></div><ul data-nc-warnings></ul><button class="fm-button" data-nc-show-warnings type="button" hidden>{e(t["show_all"])}</button></div>
<div class="cell span-6 nc-demo-tool-cell reveal delay-1"><h3>{e(t["tool_results"])}</h3><div class="nc-demo-tool-list" data-nc-tools role="table" aria-label="{e(t["tool_results"])}"></div></div>
<div class="cell span-12 nc-demo-preview-cell reveal"><h3>{e(t["preview"])}</h3><div class="nc-demo-preview" data-nc-preview aria-label="{e(t["preview"])}"></div></div>
</section>"""


def product_page(lang: str, slug: str, canonical_path: str) -> str:
    product = PRODUCTS[slug]
    title = product["title"][lang]
    description = product["description"][lang]
    step_span = 3 if slug == "quality" else 4
    steps = "\n".join(f'<article class="cell span-{step_span} detail-feature reveal delay-{(i % 4) + 1}"><span>{num}</span><h3 class="semantic-copy card-title-fit" data-fit-min="19" data-fit-text>{lines(head)}</h3><p>{e(body)}</p></article>' for i, (num, head, body) in enumerate(product["steps"][lang]))
    spec_cards = [
        ("대상 사용자" if lang == "ko" else "Target users" if lang == "en" else "المستخدمون المستهدفون", product["audiences"][lang]),
        ("입력" if lang == "ko" else "Inputs" if lang == "en" else "المدخلات", product["inputs"][lang]),
        ("운영 이벤트" if lang == "ko" else "Operational events" if lang == "en" else "الأحداث التشغيلية", product["events"][lang]),
        ("결과" if lang == "ko" else "Outputs" if lang == "en" else "النتائج", product["outputs"][lang]),
        ("파일럿 적용 조건" if lang == "ko" else "Pilot conditions" if lang == "en" else "شروط التطبيق التجريبي", product["conditions"][lang]),
        ("측정 KPI" if lang == "ko" else "KPI candidates" if lang == "en" else "مؤشرات KPI المرشحة", product["kpis"][lang]),
    ]
    specs = "\n".join(f'<article class="cell spec-card span-4 reveal delay-{(i % 3) + 1}"><span>{i+1:02}</span><h3>{e(head)}</h3>{ul(items)}</article>' for i, (head, items) in enumerate(spec_cards))
    related_items = "".join(f'<li><a href="{page_path(lang, rel)}">{e(product_name(PRODUCTS[rel], lang))}</a> — {e(PRODUCTS[rel]["outcome"][lang])}</li>' for rel in product["related"])
    nc_demo = f"\n{nc_browser_demo_section(lang)}" if slug == "nc" else ""
    quality_status = f"\n{quality_status_section(lang)}" if slug == "quality" else ""
    extra_script = f'<script src="{NC_DEMO_SRC}"></script>' if slug == "nc" else ""
    html = f"""<!doctype html>
<html lang="{lang}" dir="{LANGS[lang]["dir"]}">
{meta_head(lang, slug, title, description, canonical_path)}
<body class="technology-page {product["class"]}" data-lang="{lang}" data-static-lang="true">
{header(lang, slug)}
<main id="main">
<section aria-labelledby="tech-title" class="detail-overview section-grid">
<div class="cell span-5 detail-hero-copy reveal"><p class="eyebrow">{e(product_name(product, lang))}</p><h1 class="hero-title semantic-copy" data-fit-min="30" data-fit-text id="tech-title">{lines(product["hero"][lang])}</h1><p class="body-large">{e(product["hero_body"][lang])}</p><div class="detail-meta">{status_badges(product, lang)}<span>{e(product["pilot_scope"][lang])}</span></div><a class="detail-inline-back" href="{page_path(lang)}#products">← {e(LANGS[lang]["all_products"])}</a></div>
<div class="cell span-7 detail-animation reveal delay-1"><div class="detail-animation-head"><p class="eyebrow">{e({"ko":"현재 Operating sequence","en":"Current operating sequence","ar":"تسلسل التشغيل الحالي"}[lang])}</p></div>{tech_visual(slug, lang)}</div>{steps}</section>
{component_context_section(lang, slug)}
<section aria-labelledby="demo-title" class="detail-demo section-grid">{demo_panel(product, slug, lang)}</section>{nc_demo}{quality_status}{quality_current_section(lang) if slug == "quality" else ""}
<section aria-labelledby="spec-title" class="detail-specs section-grid"><div class="cell span-12 reveal"><p class="eyebrow">{e({"ko":"파일럿 검증 데이터","en":"Pilot validation data","ar":"بيانات التحقق التجريبي"}[lang])}</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="spec-title">{lines(product["outcome"][lang])}</h2><p class="body-large">{e(product["description"][lang])}</p></div>{specs}<div class="cell yellow span-12 reveal"><p class="body-large"><strong>{e({"ko":"파일럿 범위","en":"Pilot scope","ar":"نطاق المشروع التجريبي"}[lang])}:</strong> {e(product["pilot_scope"][lang])}</p></div></section>
<section aria-labelledby="related-title" class="related-flow section-grid"><div class="cell blue span-8 reveal"><p class="eyebrow">{e(LANGS[lang]["related"])}</p><h2 class="section-title semantic-copy" data-fit-min="30" data-fit-text id="related-title">{lines({"ko":"같은 운영 흐름에서|연결되는 모듈","en":"Modules connected|in the same operating flow","ar":"وحدات متصلة|في نفس التدفق التشغيلي"}[lang])}</h2><ul class="related-list">{related_items}</ul></div><div class="cell yellow span-4 cta-actions detail-cta-actions reveal delay-1"><a class="fm-button primary" href="{page_path(lang)}?interest={slug}#contact">{e(LANGS[lang]["pilot"])}</a><a class="fm-button" href="{page_path(lang)}#products">{e(LANGS[lang]["all_products"])}</a></div></section>
</main>{footer(lang)}<script src="{SCRIPT_SRC}"></script>{extra_script}</body></html>"""
    return html


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def sitemap() -> str:
    urls = ["/", "/ko/", "/en/", "/ar/"]
    for lang in LANGS:
        urls.extend(page_path(lang, slug) for slug in PRODUCTS)
        urls.extend(page_path(lang, slug) for slug in FACTORY_OS_PAGES)
    body = "\n".join(f"  <url><loc>{abs_url(path)}</loc></url>" for path in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n'


def notes() -> str:
    return f"""# Flowmatic Implementation Notes

- 작성일: {date.today().isoformat()}
- 기술 스택: 순수 정적 HTML/CSS/JavaScript, GitHub Pages 배포
- 배포 플랫폼: GitHub Pages + CNAME `flowmatic-os.com`
- 다국어 처리 방식: `/ko/`, `/en/`, `/ar/` 정적 HTML을 생성하며 각 HTML에는 해당 언어만 렌더링합니다. 기존 루트 URL과 `*.html` 제품 URL은 한국어 호환 페이지로 유지합니다.
- 데모 영상 파일: `flowmatic_nc_demo.mp4`, `flowmatic_ct_demo.mp4`; 두 제품 페이지의 `<video>`는 `controls`, `playsinline`, `preload="metadata"`, `poster`를 사용합니다.
- NC 공개 브라우저 데모: `/nc-demo-lite.js`, `/nc-demo-lite-worker.js`, `/demo-data/flowmatic-nc-sample.nc`; 업로드 없이 브라우저 내부에서 기본 G-code 이동시간만 계산합니다.
- Quality Intelligence: `/ko/quality/`, `/en/quality/`, `/ar/quality/` 및 한국어 호환 URL `/quality.html`; Defect → Loss → Priority → Work → Verify → Recurrence 구조를 기준으로 하며 Inspection은 Evidence / Input Layer로 표시합니다.
- Machining Intelligence: Manufacturing Recipe, 기존 G-code 문맥 추론, safe assembly, 측정/보정, managed metadata, air-gapped USB 동기화를 V.Next 구조로 설명합니다. source-level 검증과 Active development / PoC 범위를 분리합니다.
- Factory Operating Intelligence: Quality / Machining / Operations / Logistics 네 지능축과 Shared Manufacturing Context → Event Core → Manufacturing Control Shell → 계획된 Cross-domain Control Tower 구조를 `/{{lang}}/platform/`에서 설명합니다.
- 신규 정식 URL: `/{{lang}}/machining-intelligence/`, `/{{lang}}/operations-intelligence/`, `/{{lang}}/logistics-intelligence/`, `/{{lang}}/platform/`; 기존 NC/CT/Quality/Work Standard/TMS/AMR URL은 하위 컴포넌트 페이지로 유지합니다.
- Operations Intelligence: Functional MVP / internal validation 상태로 표시하며, Tracked Operational Cost를 완전 제조원가나 회계원가로 표현하지 않습니다.
- 개발 프리뷰 제품: Work Standard, TMS, AMR은 빈 비디오 플레이어 없이 개발 상태 패널, 파일럿 입력, 확인 결과, 문의 CTA를 표시합니다.
- 공식 브랜드 마크: 좌상단 파랑, 좌하단 빨강, 우측 노랑 2칸의 2×2 마크를 `/assets/branding/`에서 단일 관리합니다. 헤더·푸터·파비콘·앱 아이콘·OG 이미지가 같은 원본을 사용합니다.
- 공식 QR 연락 시그니처: `{BASE_URL}/`로 연결하며 `{CONTACT_EMAIL}`을 함께 표시합니다. Contact 영역과 외부 자료에서 재사용할 SVG/PNG를 제공합니다.
- 공식 문의 목적지: `{CONTACT_EMAIL}`. 문의 폼은 Formspree 엔드포인트를 통해 AJAX로 제출하며, 성공·실패 상태를 페이지 안에서 안내합니다.
- 문의 선택지는 네 Intelligence와 Platform / Control Tower만 노출하며 legacy component URL의 interest 값은 상위 Intelligence로 매핑합니다.
- 사용자 확인 필요: 개인정보처리방침 URL, 법인명/주소/전화번호, 아랍어 원어민 최종 감수, 실제 CNC/CMM 및 machine adapter 현장 검증 상태.
"""


def main() -> None:
    write(Path("index.html"), home_page("ko", "/"))
    for slug in PRODUCTS:
        write(Path(f"{slug}.html"), product_page("ko", slug, f"/{slug}.html"))
    for lang in LANGS:
        write(Path(lang) / "index.html", home_page(lang, page_path(lang)))
        for slug in PRODUCTS:
            write(Path(lang) / slug / "index.html", product_page(lang, slug, page_path(lang, slug)))
        for slug in FACTORY_OS_PAGES:
            write(Path(lang) / slug / "index.html", intelligence_page(lang, slug, page_path(lang, slug)))
    write(Path("robots.txt"), "User-agent: *\nAllow: /\nSitemap: https://flowmatic-os.com/sitemap.xml\n")
    write(Path("sitemap.xml"), sitemap())
    write(Path("IMPLEMENTATION_NOTES.md"), notes())


if __name__ == "__main__":
    main()
