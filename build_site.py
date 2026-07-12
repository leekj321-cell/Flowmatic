from __future__ import annotations

from datetime import date
from html import escape
from pathlib import Path


BASE_URL = "https://flowmatic-os.com"
CSS_HREF = "/style-v5.19.css"
SCRIPT_SRC = "/script.js?v=5.16"
OG_IMAGE = f"{BASE_URL}/og-flowmatic.svg"


LANGS = {
    "ko": {
        "label": "KR",
        "name": "한국어",
        "dir": "ltr",
        "skip": "본문으로 건너뛰기",
        "open": "메뉴 열기",
        "nav": {"approach": "설계 원칙", "flow": "작동 방식", "products": "제품", "contact": "파일럿 상담"},
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
        "nav": {"approach": "Approach", "flow": "How it works", "products": "Products", "contact": "Discuss a pilot"},
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
        "nav": {"approach": "النهج", "flow": "طريقة العمل", "products": "المنتجات", "contact": "ناقش مشروعًا تجريبيًا"},
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


HOME = {
    "ko": {
        "title": "Flowmatic | 제조 현장 운영 인텔리전스",
        "description": "Flowmatic은 카메라, NC 코드, 작업자 입력을 운영 이벤트로 바꾸고 알림·검토·호출·안내에 연결하는 제조 현장 운영 인텔리전스입니다.",
        "eyebrow": "제조 현장 운영 인텔리전스",
        "h1": "현장 이벤트를|다음 행동으로 연결합니다.",
        "body": "Flowmatic은 카메라, NC 코드, 작업자 입력을 사이클 손실, 경로 위험, 자재 요구, 작업 안내로 바꾸고 알림·검토·호출·안내에 연결합니다. 기존 설비와 작업 방식은 그대로 유지합니다.",
        "primary": "제품 데모 보기",
        "secondary": "파일럿 상담",
        "support": "공장에는 시스템 하나를 더 얹기보다, 끊긴 운영이 흐르도록 해야 합니다.",
        "problem_title": "생산은 계속됩니다.|판단은 뒤늦게 따라옵니다.",
        "problem_body": "현장은 멈추지 않습니다. 중요한 이벤트와 다음 행동은 뒤늦게 드러납니다.",
        "strategy_title": "현장을 바꾸기 전에|흐름을 읽습니다.",
        "strategy_body": "지금 돌아가는 라인에서 시작합니다. 가치를 만드는 설비와 작업 방식, 사람을 그대로 살립니다. 먼저 이벤트를 보이게 만들고, 다음 행동 하나를 연결한 뒤, 가치가 확인되면 자동화합니다.",
        "flow_title": "Observe → Eventize|Act → Confirm",
        "flow_body": "공식 운영 논리는 하나입니다. 신호를 읽고, 운영 이벤트로 바꾸고, 다음 행동에 연결한 뒤, 응답을 확인합니다.",
        "products_title": "제품은 상태와 검증 범위가|분명해야 합니다.",
        "products_body": "NC와 CT는 실제 데모로 확인할 수 있습니다. Work Standard, TMS, AMR은 작동 개념과 현재 개발 상태를 보여줍니다.",
        "workflow_title": "Demo workflows",
        "workflow_body": "고객 수치 대신 실제 데모로 확인 가능한 흐름만 보여줍니다.",
        "pilot_title": "기존 라인을 바꾸지 않고,|이벤트 하나부터 검증합니다.",
        "deploy_note": "배포 구조, 데이터 저장 위치, 보관 기간, 접근 권한, 기존 시스템 연동 범위는 파일럿 설계 단계에서 확인합니다.",
        "contact_title": "현재 라인을 바꾸지 않고,|이벤트 하나부터 검증하세요.",
        "contact_body": "대상 공정과 해결하려는 문제를 알려주시면 입력 신호, 다음 행동, 측정할 KPI를 기준으로 파일럿 범위를 정리합니다.",
        "contact_cta": "파일럿 상담 요청",
        "contact_fallback": "실제 문의 이메일 또는 폼 엔드포인트가 저장소에서 확인되지 않아, 모든 CTA는 이 Contact 섹션으로 안전하게 연결됩니다.",
    },
    "en": {
        "title": "Flowmatic | Operational Intelligence for Manufacturing",
        "description": "Flowmatic turns camera, NC-code, and operator signals into actionable manufacturing events, alerts, reviews, guidance, and material calls.",
        "eyebrow": "Operational Intelligence for Manufacturing",
        "h1": "Turn factory events|into the next action.",
        "body": "Flowmatic turns camera, NC-code, and operator signals into cycle loss, path risk, material demand, and work guidance—then connects each event to an alert, review, call, or guide without replacing the systems already running your factory.",
        "primary": "View product demos",
        "secondary": "Discuss a pilot",
        "support": "A factory does not need one more system. It needs operations to flow.",
        "problem_title": "Production keeps moving.|Decisions arrive late.",
        "problem_body": "The field never stops. Important events and the next action often appear too late.",
        "strategy_title": "Read the flow|before changing the field.",
        "strategy_body": "Start with the line as it is. Keep the equipment, workflow, and people already creating value. Make the event visible first, connect one next action, and automate only after the value is proven.",
        "flow_title": "Observe → Eventize|Act → Confirm",
        "flow_body": "Flowmatic uses one operating logic: observe the signal, turn it into an event, connect a next action, and confirm the response.",
        "products_title": "Product status and pilot scope|should be explicit.",
        "products_body": "NC and CT include working demos. Work Standard, TMS, and AMR show their operating concept and current development status.",
        "workflow_title": "Demo workflows",
        "workflow_body": "Without verified customer metrics, the site shows only workflows that can be inspected through actual demos.",
        "pilot_title": "Validate one event|without replacing the line.",
        "deploy_note": "Deployment architecture, data location, retention, access control, and integration scope are confirmed during pilot design.",
        "contact_title": "Validate one event|without replacing the line.",
        "contact_body": "Share the process and operational problem. We will define a pilot around the input signal, the next action, and the KPI to verify.",
        "contact_cta": "Request a pilot discussion",
        "contact_fallback": "No verified email or form endpoint was found in the repository, so every CTA safely routes to this Contact section.",
    },
    "ar": {
        "title": "Flowmatic | ذكاء تشغيلي للتصنيع",
        "description": "يحوّل Flowmatic إشارات المصنع إلى أحداث تشغيلية قابلة للتنفيذ وتنبيهات ومراجعات وإرشادات وطلبات مواد.",
        "eyebrow": "ذكاء تشغيلي للتصنيع",
        "h1": "حوّل أحداث المصنع|إلى الإجراء التالي.",
        "body": "يحوّل Flowmatic إشارات الكاميرات وبرامج NC ومدخلات المشغّلين إلى أحداث تشغيلية مثل فقدان زمن الدورة، ومخاطر مسار الأداة، وطلب المواد، وإرشادات العمل، ثم يربط كل حدث بتنبيه أو مراجعة أو طلب أو إرشاد، من دون استبدال الأنظمة القائمة في المصنع.",
        "primary": "شاهد عروض المنتجات",
        "secondary": "ناقش مشروعًا تجريبيًا",
        "support": "لا يحتاج المصنع إلى نظام إضافي، بل يحتاج إلى تدفق العمليات.",
        "problem_title": "الإنتاج يستمر بالحركة.|والقرارات تصل متأخرة.",
        "problem_body": "الميدان لا يتوقف. وغالبًا ما تظهر الأحداث المهمة والإجراء التالي بعد فوات الوقت.",
        "strategy_title": "اقرأ التدفق|قبل تغيير الميدان.",
        "strategy_body": "ابدأ من الخط كما هو. حافظ على المعدات وسير العمل والأشخاص الذين يصنعون القيمة. اجعل الحدث مرئيًا أولًا، ثم اربطه بإجراء تالٍ واحد، ولا تؤتمت إلا بعد إثبات القيمة.",
        "flow_title": "الرصد → تحويل الإشارة إلى حدث|ربط الإجراء → التأكيد",
        "flow_body": "يستخدم Flowmatic منطق تشغيل واحدًا: قراءة الإشارة، تحويلها إلى حدث، ربطها بإجراء تالٍ، ثم تأكيد الاستجابة.",
        "products_title": "يجب أن تكون حالة المنتج|ونطاق التحقق واضحين.",
        "products_body": "يتضمن NC وCT عروضًا عملية، بينما يوضح Work Standard وTMS وAMR مفهوم التشغيل وحالة التطوير الحالية.",
        "workflow_title": "تدفقات العروض",
        "workflow_body": "من دون مقاييس عملاء موثقة، يعرض الموقع فقط التدفقات التي يمكن فحصها من خلال العروض الفعلية.",
        "pilot_title": "تحقق من حدث واحد|من دون استبدال الخط.",
        "deploy_note": "يتم تأكيد بنية النشر وموقع البيانات وفترة الاحتفاظ وصلاحيات الوصول ونطاق التكامل أثناء تصميم المشروع التجريبي.",
        "contact_title": "تحقق من حدث واحد|من دون استبدال الخط.",
        "contact_body": "شارك العملية والمشكلة التشغيلية. سنحدد نطاقًا تجريبيًا حول إشارة الإدخال والإجراء التالي ومؤشر KPI المراد التحقق منه.",
        "contact_cta": "اطلب نقاشًا تجريبيًا",
        "contact_fallback": "لم يتم العثور في المستودع على بريد تواصل أو نقطة إرسال موثقة، لذلك تنتقل كل أزرار CTA بأمان إلى قسم التواصل هذا.",
    },
}


PROBLEM_CARDS = {
    "ko": [
        ("01", "사이클 손실을|바로 봅니다.", "대응할 수 있을 때 지연을 발견합니다."),
        ("02", "가공 전에|위험을 봅니다.", "코드 속 위험한 이동을 눈앞에 꺼내놓습니다."),
        ("03", "기다리기 전에|자재를 부릅니다.", "라인이 기다리기 전에 자재 요구를 알립니다."),
        ("04", "숙련자의 판단을|표준으로 남깁니다.", "숙련자의 판단을 누구나 이어받을 수 있게 만듭니다."),
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
        ("01", "잘 돌아가는 것|위에 쌓습니다.", "가치를 만드는 설비와 작업 방식, 현장 경험을 살립니다."),
        ("02", "자동화보다|먼저 관찰합니다.", "대응을 자동화하기 전에 이벤트부터 분명하게 만듭니다."),
        ("03", "하나의 다음 행동을|연결합니다.", "이벤트를 안내, 알림, 호출, 검토 중 하나의 행동으로 잇습니다."),
        ("04", "최종 판단은|사람이 맡습니다.", "반복은 자동화하되 승인과 예외 판단은 사람이 맡습니다."),
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
        ("관찰", "카메라, NC 코드, 작업자 입력 등 실제 작업에서 신호를 읽습니다."),
        ("이벤트화", "원시 신호를 지연, 위험, 수요 등 운영 이벤트로 바꿉니다."),
        ("행동 연결", "이벤트를 알림, 검토, 안내, 호출 중 하나의 다음 행동으로 연결합니다."),
        ("확인", "사람 또는 설비의 응답을 확인하고 이벤트를 종결합니다."),
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
        ("01", "이벤트 선택", "사이클 완료, 경로 위험, 작업 단계, 공구 부족, 자재 요구 중 하나를 고릅니다."),
        ("02", "입력 확인", "카메라, NC 파일, 작업자 입력, 기준 데이터, 인터페이스를 확인합니다."),
        ("03", "다음 행동 연결", "알림, 검토, 안내, 호출 중 하나를 연결합니다."),
        ("04", "KPI 확인", "사전에 합의한 KPI로 계속 적용할지 결정합니다."),
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


PRODUCTS = {
    "nc": {
        "name": "Flowmatic NC",
        "class": "flowmatic-nc",
        "status": "demo",
        "video": "/flowmatic_nc_demo",
        "title": {
            "ko": "Flowmatic NC | 가공 전 공구 경로 검토",
            "en": "Flowmatic NC | Pre-cut Toolpath Review",
            "ar": "Flowmatic NC | مراجعة مسار الأداة قبل التشغيل",
        },
        "description": {
            "ko": "NC/G-code를 공구 경로, 예상 사이클타임, 검토 지점으로 바꿔 가공 전에 확인합니다.",
            "en": "Turn NC and G-code into visible toolpaths, estimated cycle time, and review points before machining.",
            "ar": "حوّل NC وG-code إلى مسارات أداة مرئية وزمن دورة تقديري ونقاط مراجعة قبل التشغيل.",
        },
        "outcome": {"ko": "가공 전 공구 경로 검토", "en": "Pre-cut toolpath review", "ar": "مراجعة مسار الأداة قبل التشغيل"},
        "card_desc": {"ko": "G-code를 공구 움직임과 사이클타임, 검토 지점으로 바꿉니다.", "en": "Turn G-code into visible motion, cycle time, and review points.", "ar": "حوّل G-code إلى حركة مرئية وزمن دورة ونقاط مراجعة."},
        "cta": {"ko": "NC 데모 보기", "en": "View NC demo", "ar": "شاهد عرض NC"},
        "hero": {"ko": "가공 전에|공구 경로를 봅니다.", "en": "See the toolpath|before cutting.", "ar": "شاهد مسار الأداة|قبل التشغيل."},
        "hero_body": {"ko": "코드를 읽고 공구 움직임을 재구성합니다. 설비를 돌리기 전에 경로를 확인합니다.", "en": "Read the code and rebuild the motion. Review the path before the machine runs.", "ar": "اقرأ الكود وأعد بناء الحركة. راجع المسار قبل تشغيل الماكينة."},
        "steps": {
            "ko": [("01", "NC 프로그램을 해석합니다.", "공구, 이송, 좌표, 인덱스 동작을 읽어냅니다."), ("02", "공구 움직임을 재구성합니다.", "공구가 움직일 위치와 순서를 보여줍니다."), ("03", "가공 전에 검토합니다.", "설비를 돌리기 전에 사이클타임과 위험 경로를 확인합니다.")],
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
        "title": {"ko": "Flowmatic CT | 사이클 자동 측정", "en": "Flowmatic CT | Automatic Cycle Measurement", "ar": "Flowmatic CT | قياس زمن الدورة تلقائيًا"},
        "description": {"ko": "고정 카메라와 ROI로 시작·종료를 감지하고 사이클타임과 공정 타임라인을 자동 생성합니다.", "en": "Detect cycle start and end from a fixed camera ROI and build cycle time and process timelines automatically.", "ar": "اكتشف بداية الدورة ونهايتها من ROI لكاميرا ثابتة وأنشئ زمن الدورة وخط العملية تلقائيًا."},
        "outcome": {"ko": "사이클 자동 측정", "en": "Automatic cycle measurement", "ar": "قياس زمن الدورة تلقائيًا"},
        "card_desc": {"ko": "카메라 속 반복 움직임을 사이클 이벤트와 시간 데이터로 바꿉니다.", "en": "Turn repeated camera motion into cycle events and time data.", "ar": "حوّل الحركة المتكررة في الكاميرا إلى أحداث دورة وبيانات زمنية."},
        "cta": {"ko": "CT 데모 보기", "en": "View CT demo", "ar": "شاهد عرض CT"},
        "hero": {"ko": "움직임만으로|사이클을 측정합니다.", "en": "Measure the cycle|from the motion.", "ar": "قِس الدورة|من الحركة."},
        "hero_body": {"ko": "고정 카메라가 사이클 이벤트를 감지합니다. 타임라인은 자동으로 만들어집니다.", "en": "A fixed camera detects cycle events. The timeline is built automatically.", "ar": "تكتشف كاميرا ثابتة أحداث الدورة. ويتم إنشاء الخط الزمني تلقائيًا."},
        "steps": {
            "ko": [("01", "기준 영역을 관찰합니다.", "고정 카메라와 ROI로 반복 위치를 관찰합니다."), ("02", "사이클의 시작과 끝을 잡습니다.", "현장 움직임의 변화에서 시작과 종료를 잡습니다."), ("03", "시간 데이터로 정리합니다.", "검출한 이벤트를 사이클타임과 공정 타임라인으로 정리합니다.")],
            "en": [("01", "Watch a reference area.", "Observe repeated positions with a fixed camera and ROI."), ("02", "Detect the cycle boundary.", "Detect start and finish from changes in field movement."), ("03", "Build time data.", "Turn detected events into cycle time and a process timeline.")],
            "ar": [("01", "راقب منطقة مرجعية.", "راقب المواضع المتكررة بكاميرا ثابتة وROI."), ("02", "اكتشف حدود الدورة.", "اكتشف البداية والنهاية من تغيرات حركة الميدان."), ("03", "ابنِ بيانات الوقت.", "حوّل الأحداث المكتشفة إلى زمن دورة وخط زمني للعملية.")],
        },
        "audiences": {"ko": ["생산기술 엔지니어", "라인 관리자", "개선 활동 담당자"], "en": ["Manufacturing engineers", "Line managers", "Improvement teams"], "ar": ["مهندسو الإنتاج", "مديرو الخطوط", "فرق التحسين"]},
        "inputs": {"ko": ["고정 카메라 영상", "ROI", "시작·종료 기준"], "en": ["Fixed camera video", "ROI", "Start/end criteria"], "ar": ["فيديو كاميرا ثابتة", "ROI", "معايير البداية والنهاية"]},
        "events": {"ko": ["사이클 시작", "사이클 종료", "사이클 완료", "변동 검토 후보"], "en": ["Cycle start", "Cycle end", "Cycle complete", "Variation review candidate"], "ar": ["بداية الدورة", "نهاية الدورة", "اكتمال الدورة", "مرشح مراجعة التغير"]},
        "outputs": {"ko": ["사이클타임", "공정 타임라인", "반복 사이클 기록"], "en": ["Cycle time", "Process timeline", "Repeated cycle records"], "ar": ["زمن الدورة", "خط العملية", "سجلات الدورات المتكررة"]},
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
        "hero": {"ko": "공정 지식을|작업 안내로 바꿉니다.", "en": "Turn process knowledge|into clear guidance.", "ar": "حوّل معرفة العملية|إلى إرشاد واضح."},
        "hero_body": {"ko": "필요한 공구, 경로, 자세, 다음 단계를 보여줍니다. 모든 안내는 작업자 시점에 맞춥니다.", "en": "Show the right tool, path, posture, and next step. Keep the view aligned with the operator.", "ar": "اعرض الأداة والمسار والوضعية والخطوة التالية الصحيحة. واجعل العرض متوافقًا مع المشغّل."},
        "steps": {
            "ko": [("01", "공정 정보를 모읍니다.", "공구, 경로, 자세, 작업 순서를 한 장면에 모읍니다."), ("02", "작업자 시점으로 다시 보여줍니다.", "실제 작업 순서와 작업자 시야에 맞춰 다시 보여줍니다."), ("03", "다음 작업을 안내합니다.", "필요한 확인과 다음 행동을 알맞은 순간에 보여줍니다.")],
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
        "hero": {"ko": "실물 공구를|공정과 연결합니다.", "en": "Connect every tool|to its process.", "ar": "اربط كل أداة|بعمليتها."},
        "hero_body": {"ko": "실물 공구를 식별해 공정과 연결합니다. 수명과 재고, 위치 정보를 함께 맞춥니다.", "en": "Identify the physical tool and match the process. Keep life, stock, and location information aligned.", "ar": "عرّف الأداة الفعلية وطابقها مع العملية. حافظ على توافق العمر والمخزون والموقع."},
        "steps": {
            "ko": [("01", "실물 공구를 식별합니다.", "라벨이나 사진에서 공구 식별 정보를 읽습니다."), ("02", "공정과 연결합니다.", "대응하는 공정 기록을 찾아 확인합니다."), ("03", "운영 정보를 최신으로 유지합니다.", "수명, 재고, 위치, 사용 상태를 함께 갱신합니다.")],
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
        "display": {"ko": "Flowmatic AMR Calling + Operator", "en": "Flowmatic AMR Calling + Operator", "ar": "Flowmatic AMR Calling + Operator"},
        "class": "flowmatic-amr",
        "status": "preview",
        "title": {"ko": "Flowmatic AMR | 자재 호출과 AMR 배차", "en": "Flowmatic AMR | Material Calling and Dispatch", "ar": "Flowmatic AMR | طلب المواد وإرسال الروبوت المتنقل"},
        "description": {"ko": "자재 요구를 작업자 알림과 AMR 배차로 연결하고 보급 완료까지 이벤트 상태를 추적합니다.", "en": "Connect material demand to operator alerts and AMR dispatch, then track the event through supply completion.", "ar": "اربط طلب المواد بتنبيهات المشغّل وإرسال AMR، ثم تتبع الحدث حتى اكتمال التزويد."},
        "outcome": {"ko": "자재 호출과 AMR 배차", "en": "Material calls and AMR dispatch", "ar": "طلب المواد وإرسال الروبوت المتنقل"},
        "card_desc": {"ko": "자재 요구를 작업자 알림과 AMR 배차로 연결합니다.", "en": "Connect material demand to an operator alert and AMR dispatch.", "ar": "اربط طلب المواد بتنبيه المشغّل وإرسال AMR."},
        "cta": {"ko": "작동 방식 보기", "en": "See how it works", "ar": "شاهد طريقة العمل"},
        "hero": {"ko": "라인이 기다리기 전에|자재를 호출합니다.", "en": "Call material|before the line waits.", "ar": "اطلب المواد|قبل أن ينتظر الخط."},
        "hero_body": {"ko": "자재 요구를 감지해 작업자에게 알립니다. 정지로 이어지기 전에 AMR 배차 요청으로 연결합니다.", "en": "Detect demand and alert the operator. Connect the request to AMR dispatch before shortage becomes downtime.", "ar": "اكتشف الطلب ونبّه المشغّل. اربط الطلب بإرسال AMR قبل أن يتحول النقص إلى توقف."},
        "steps": {
            "ko": [("01", "자재 요구를 감지합니다.", "잔량 신호나 호출 입력을 자재 요구 이벤트로 바꿉니다."), ("02", "필요한 사람에게 알립니다.", "대상 라인과 필요한 행동을 분명하게 보여줍니다."), ("03", "배차하고 흐름을 닫습니다.", "보급 완료를 확인하고 이벤트 상태를 닫습니다.")],
            "en": [("01", "Detect demand.", "Turn stock signals or call inputs into a material-demand event."), ("02", "Alert the right person.", "Show the target line and the required action clearly."), ("03", "Dispatch and close the loop.", "Confirm supply completion and close the event state.")],
            "ar": [("01", "اكتشف الطلب.", "حوّل إشارات المخزون أو مدخلات الطلب إلى حدث طلب مواد."), ("02", "نبّه الشخص المناسب.", "اعرض الخط المستهدف والإجراء المطلوب بوضوح."), ("03", "أرسل وأغلق الحلقة.", "أكد اكتمال التزويد وأغلق حالة الحدث.")],
        },
        "audiences": {"ko": ["라인 작업자", "물류 운영자", "AMR 관제 담당자"], "en": ["Line operators", "Logistics operators", "AMR control staff"], "ar": ["مشغّلو الخط", "مشغّلو اللوجستيات", "مسؤولو مراقبة AMR"]},
        "inputs": {"ko": ["자재 잔량 신호 또는 수동 호출", "라인·보급소 매핑", "AMR 상태 또는 연동 인터페이스"], "en": ["Material level signal or manual call", "Line-depot mapping", "AMR status or integration interface"], "ar": ["إشارة كمية المواد أو طلب يدوي", "ربط الخط بموقع التزويد", "حالة AMR أو واجهة التكامل"]},
        "events": {"ko": ["자재 부족", "호출 확인", "배차 요청", "공급 완료", "예외 또는 실패"], "en": ["Material low", "Call confirmed", "Dispatch request", "Supply complete", "Exception or failure"], "ar": ["نقص المواد", "تأكيد الطلب", "طلب الإرسال", "اكتمال التزويد", "استثناء أو فشل"]},
        "outputs": {"ko": ["대상 작업자 알림", "배차 요청 상태", "공급 진행 상태", "완료 확인"], "en": ["Target operator alert", "Dispatch request status", "Supply progress state", "Completion confirmation"], "ar": ["تنبيه المشغّل المستهدف", "حالة طلب الإرسال", "حالة تقدم التزويد", "تأكيد الاكتمال"]},
        "conditions": {"ko": ["AMR 인터페이스와 호출 권한 확인", "안전 규칙과 예외 처리 기준 확인", "초기 파일럿은 사람 승인 후 배차를 기본값으로 사용"], "en": ["Confirm AMR interface and call authority", "Confirm safety rules and exception criteria", "Use human-approved dispatch as the default first pilot mode"], "ar": ["تأكيد واجهة AMR وصلاحية الطلب", "تأكيد قواعد السلامة ومعايير الاستثناء", "اعتماد موافقة الإنسان قبل الإرسال كإعداد أولي"]},
        "kpis": {"ko": ["자재 대기시간", "호출부터 배차까지의 시간", "배차부터 공급 완료까지의 시간", "자재 부족으로 인한 라인 정지 횟수"], "en": ["Material waiting time", "Call-to-dispatch time", "Dispatch-to-supply-complete time", "Line stops caused by material shortage"], "ar": ["وقت انتظار المواد", "الوقت من الطلب إلى الإرسال", "الوقت من الإرسال إلى اكتمال التزويد", "عدد توقفات الخط بسبب نقص المواد"]},
        "pilot_scope": {"ko": "라인 한 곳 · 보급소 한 곳 · 대표 자재 경로 한 개", "en": "One line · one depot · one representative material route", "ar": "خط واحد · نقطة تزويد واحدة · مسار مواد ممثل واحد"},
        "related": ["work-standard"],
    },
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


def abs_url(path: str) -> str:
    return f"{BASE_URL}{path}"


def product_name(product: dict, lang: str) -> str:
    return product.get("display", {}).get(lang) or product["name"]


def hreflang_links(slug: str, canonical_path: str) -> str:
    links = [f'<link rel="canonical" href="{abs_url(canonical_path)}">']
    for lang in LANGS:
        links.append(f'<link rel="alternate" hreflang="{lang}" href="{abs_url(page_path(lang, slug))}">')
    links.append(f'<link rel="alternate" hreflang="x-default" href="{abs_url(page_path("ko", slug))}">')
    return "\n".join(links)


def meta_head(lang: str, slug: str, title: str, description: str, canonical_path: str) -> str:
    return f"""<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta name="theme-color" content="#FAFAF7">
{hreflang_links(slug, canonical_path)}
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(description)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{abs_url(canonical_path)}">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
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
        f'<a class="lang-button{" is-active" if code == lang else ""}" data-lang-link="{code}" hreflang="{code}" lang="{code}" href="{page_path(code, slug)}">{e(meta["label"])}</a>'
        for code, meta in LANGS.items()
    )
    return f"""<a class="skip-link" href="#main">{e(t["skip"])}</a>
<header class="site-header" data-header>
<a aria-label="Flowmatic home" class="brand" href="{home}#hero"><span aria-hidden="true" class="brand-mark"></span><span>Flowmatic</span></a>
<div class="header-actions">
<nav class="site-nav" data-nav id="site-nav">{nav_html}</nav>
<div aria-label="Language switcher" class="lang-switcher">{lang_html}</div>
<button aria-controls="site-nav" aria-expanded="false" class="nav-toggle" data-nav-toggle type="button"><span class="sr-only">{e(t["open"])}</span><span aria-hidden="true"></span><span aria-hidden="true"></span></button>
</div>
</header>"""


def footer(lang: str) -> str:
    h = HOME[lang]
    return f"""<footer class="site-footer">
<strong>Flowmatic</strong>
<p>{e(h["support"])}</p>
<a href="{page_path(lang)}#hero">{e(LANGS[lang]["home"])}</a>
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
        status_class = "is-demo" if product["status"] == "demo" else "is-preview"
        status_label = LANGS[lang]["demo_available"] if product["status"] == "demo" else LANGS[lang]["development_preview"]
        cards.append(f"""<article class="cell product-card span-4 reveal delay-{((i - 1) % 3) + 1}">
{mini_visual(slug, lang)}
<p class="eyebrow">{e(product_name(product, lang))}</p>
<h3 class="semantic-copy card-title-fit" data-fit-min="22" data-fit-text>{lines(product["outcome"][lang])}</h3>
<p>{e(product["card_desc"][lang])}</p>
<span class="status-badge {status_class}">{e(status_label)}</span>
<a class="product-link" href="{page_path(lang, slug)}"><span class="product-link-label">{e(product["cta"][lang])}</span><span aria-hidden="true">→</span></a>
</article>""")
    return "\n".join(cards)


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
    label = {"ko": ["1 · 자재 부족 감지", "2 · 작업자 알림", "3 · AMR 배차", "A 라인", "자재 부족", "FLOWMATIC OPERATOR", "확인", "보급소", "보급 완료"], "en": ["1 · MATERIAL RUNS LOW", "2 · ALERT THE OPERATOR", "3 · DISPATCH THE AMR", "LINE A", "MATERIAL LOW", "FLOWMATIC OPERATOR", "ACKNOWLEDGE", "DEPOT", "SUPPLY COMPLETE"], "ar": ["1 · انخفاض المواد", "2 · تنبيه المشغّل", "3 · إرسال AMR", "الخط A", "نقص المواد", "FLOWMATIC OPERATOR", "تأكيد", "المستودع", "اكتمل التزويد"]}[lang]
    return f"""<div aria-label="Material low event becomes operator alert and AMR dispatch" class="tech-visual amr-explainer" data-tech-animation="amr">
<div class="visual-label label-input">{label[0]}</div><div class="amr-line-box"><span>{label[3]}</span><div class="material-gauge"><i></i></div><strong>{label[4]}</strong></div><div class="visual-arrow arrow-a">→</div>
<div class="visual-label label-process">{label[1]}</div><div class="operator-alert"><span>{label[5]}</span><strong data-amr-message>CALL REQUEST</strong><button tabindex="-1" type="button">{label[6]}</button></div><div class="visual-arrow arrow-b">→</div>
<div class="visual-label label-output">{label[2]}</div><div class="amr-route-scene"><span class="route-depot">{label[7]}</span><span class="route-line">{label[3]}</span><span class="route-track"></span><span class="amr-cart-large"></span><span class="amr-complete">{label[8]}</span></div></div>"""


def home_page(lang: str, canonical_path: str) -> str:
    h = HOME[lang]
    logic_cards = "".join(f'<li><strong>{e(title)}</strong><span>{e(body)}</span></li>' for title, body in FLOW_STEPS[lang])
    problem = "\n".join(f'<article class="cell {"red" if i < 2 else "gray"} problem-card span-3 reveal delay-{i+1}"><span>{num}</span><h3 class="semantic-copy card-title-fit" data-fit-min="20" data-fit-text>{lines(title)}</h3><p>{e(body)}</p></article>' for i, (num, title, body) in enumerate(PROBLEM_CARDS[lang]))
    principles = "\n".join(f'<article class="cell {"yellow" if i == 1 else "blue" if i == 3 else "gray"} strategy-card span-3 reveal delay-{i+1}"><span>{num}</span><h3 class="semantic-copy card-title-fit" data-fit-min="20" data-fit-text>{lines(title)}</h3><p>{e(body)}</p></article>' for i, (num, title, body) in enumerate(PRINCIPLES[lang]))
    pilot = "\n".join(f'<article class="cell pilot-step span-3 reveal delay-{i+1}"><span>{num}</span><h3>{e(title)}</h3><p>{e(body)}</p></article>' for i, (num, title, body) in enumerate(PILOT_STEPS[lang]))
    workflow_nc = {"ko": "NC 프로그램 → 공구 경로 재구성 → 가공 전 검토", "en": "NC program → Toolpath reconstruction → Review point", "ar": "برنامج NC → إعادة بناء مسار الأداة → نقطة مراجعة"}[lang]
    workflow_ct = {"ko": "고정 카메라 ROI → 시작·종료 이벤트 → 사이클 타임라인", "en": "Fixed camera ROI → Start/end event → Cycle timeline", "ar": "ROI لكاميرا ثابتة → حدث بداية/نهاية → خط زمني للدورة"}[lang]
    html = f"""<!doctype html>
<html lang="{lang}" dir="{LANGS[lang]["dir"]}">
{meta_head(lang, "home", h["title"], h["description"], canonical_path)}
<body data-lang="{lang}" data-static-lang="true">
{header(lang, "home")}
<main id="main">
<section aria-labelledby="hero-title" class="hero section-grid" id="hero">
<div class="cell hero-copy span-7 reveal"><p class="eyebrow">{e(h["eyebrow"])}</p><h1 class="hero-title semantic-copy" data-fit-min="40" data-fit-text id="hero-title">{lines(h["h1"])}</h1><p class="body-large">{e(h["body"])}</p><div class="hero-actions"><a class="fm-button primary" href="#demo-workflows">{e(h["primary"])}</a><a class="fm-button" href="#contact">{e(h["secondary"])}</a></div><p class="hero-support">{e(h["support"])}</p></div>
<div class="cell blue hero-layer span-5 reveal delay-1"><p class="kicker">Flowmatic</p><h2 class="semantic-copy" data-fit-min="27" data-fit-text>{lines(h["eyebrow"])}</h2><p class="semantic-copy copy-body" data-fit-min="17" data-fit-text>{lines(h["support"])}</p></div>
<div class="cell yellow hero-note span-4 reveal delay-2"><strong>{e(FLOW_STEPS[lang][0][0])}</strong><span>{e(FLOW_STEPS[lang][0][1])}</span></div>
<div class="cell red hero-note span-3 reveal delay-3"><strong>{e(FLOW_STEPS[lang][1][0])}</strong><span>{e(FLOW_STEPS[lang][1][1])}</span></div>
<div class="cell hero-scroll span-5 reveal delay-4"><span>{e(h["primary"])}</span><span aria-hidden="true" class="scroll-line"></span></div>
</section>
<section aria-labelledby="problem-title" class="problem section-grid">
<div class="cell span-12 reveal"><p class="eyebrow">{e({"ko":"해결하는 운영 문제","en":"Operational gaps","ar":"فجوات التشغيل"}[lang])}</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="problem-title">{lines(h["problem_title"])}</h2><p class="body-large">{e(h["problem_body"])}</p></div>{problem}</section>
<section aria-labelledby="strategy-title" class="strategy section-grid" id="approach">
<div class="cell span-8 reveal"><p class="eyebrow">{e({"ko":"현장 중심 설계","en":"Field-first design","ar":"تصميم يبدأ من الميدان"}[lang])}</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="strategy-title">{lines(h["strategy_title"])}</h2><p class="body-large">{e(h["strategy_body"])}</p></div>
<div class="cell blue span-4 reveal delay-1 strategy-core"><p class="kicker">Minimal intervention / Maximum clarity</p><h3>{e({"ko":"지능은 현장에 맞아야 합니다.","en":"Intelligence should fit the field.","ar":"يجب أن يناسب الذكاء أرض الواقع."}[lang])}</h3><p>{e(h["support"])}</p></div>{principles}</section>
<section aria-labelledby="flow-title" class="field-flow section-grid" id="flow">
<div class="cell span-5 flow-copy reveal"><p class="eyebrow">{e({"ko":"Flowmatic 작동 방식","en":"How Flowmatic works","ar":"كيف يعمل Flowmatic"}[lang])}</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="flow-title">{lines(h["flow_title"])}</h2><p class="body-large">{e(h["flow_body"])}</p><ol class="flow-explanation">{logic_cards}</ol></div>
<div class="cell span-7 flow-visual-cell reveal delay-1">{field_story(lang)}</div>
</section>
<section aria-labelledby="products-title" class="product-index section-grid" id="products">
<div class="cell span-12 reveal"><p class="eyebrow">Flowmatic Products</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="products-title">{lines(h["products_title"])}</h2><p class="body-large">{e(h["products_body"])}</p></div>{product_cards(lang)}</section>
<section aria-labelledby="workflow-title" class="demo-workflows section-grid" id="demo-workflows">
<div class="cell span-12 reveal"><p class="eyebrow">Demo workflows</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="workflow-title">{lines(h["workflow_title"])}</h2><p class="body-large">{e(h["workflow_body"])}</p></div>
<article class="cell workflow-card span-6 reveal delay-1"><p class="eyebrow">{e(LANGS[lang]["product_demo"])}</p><h3>Flowmatic NC</h3><div class="workflow-flow">{e(workflow_nc)}</div><a class="fm-button primary" href="{page_path(lang, "nc")}">{e(PRODUCTS["nc"]["cta"][lang])}</a></article>
<article class="cell workflow-card blue span-6 reveal delay-2"><p class="eyebrow">{e(LANGS[lang]["product_demo"])}</p><h3>Flowmatic CT</h3><div class="workflow-flow">{e(workflow_ct)}</div><a class="fm-button primary" href="{page_path(lang, "ct")}">{e(PRODUCTS["ct"]["cta"][lang])}</a></article>
</section>
<section aria-labelledby="pilot-title" class="pilot section-grid" id="pilot">
<div class="cell span-12 reveal"><p class="eyebrow">{e({"ko":"파일럿 진행 방식","en":"Pilot approach","ar":"نهج المشروع التجريبي"}[lang])}</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="pilot-title">{lines(h["pilot_title"])}</h2></div>{pilot}<div class="cell yellow span-12 pilot-note reveal"><p class="body-large">{e(h["deploy_note"])}</p></div></section>
<section aria-labelledby="contact-title" class="cta section-grid" id="contact">
<div class="cell span-8 reveal"><p class="eyebrow">{e(LANGS[lang]["contact"])}</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="contact-title">{lines(h["contact_title"])}</h2><p class="body-large">{e(h["contact_body"])}</p><p class="contact-interest"><span>{e(LANGS[lang]["selected_interest"])}</span><strong data-interest-label>All / undecided</strong></p></div>
<div class="cell yellow span-4 contact-note reveal delay-1"><p><strong>{e(h["contact_cta"])}</strong></p><p>{e(h["contact_fallback"])}</p><ul><li>{e({"ko":"대상 공정","en":"Target process","ar":"العملية المستهدفة"}[lang])}</li><li>{e({"ko":"해결하려는 운영 문제","en":"Operational problem to solve","ar":"المشكلة التشغيلية المراد حلها"}[lang])}</li><li>{e({"ko":"확인할 입력 신호와 KPI","en":"Input signal and KPI to verify","ar":"إشارة الإدخال ومؤشر KPI للتحقق"}[lang])}</li></ul></div>
</section>
</main>{footer(lang)}<script src="{SCRIPT_SRC}"></script></body></html>"""
    return html


def demo_panel(product: dict, slug: str, lang: str) -> str:
    if product["status"] == "demo":
        title = {"ko": f"{product['name']} 실제 데모", "en": f"{product['name']} working demo", "ar": f"عرض {product['name']} العملي"}[lang]
        summary = product["description"][lang]
        return f"""<div class="cell span-4 demo-copy reveal"><p class="eyebrow">{e(LANGS[lang]["product_demo"])}</p><h2 class="section-title semantic-copy" data-fit-min="28" data-fit-text id="demo-title">{lines(title)}</h2><p class="body-large">{e(summary)}</p></div>
<div class="cell span-8 demo-cell reveal delay-1"><div class="demo-player" data-demo-video data-video-base="{e(product["video"])}" data-video-title="{e(product["name"])} demo"><video aria-label="{e(product["name"])} demo" controls hidden playsinline preload="metadata" poster="/og-flowmatic.svg" width="1920" height="1080"></video><div class="video-placeholder" data-video-placeholder><span aria-hidden="true" class="video-icon">▶</span><p><strong>{e(LANGS[lang]["video_unavailable"])}</strong></p></div></div><p class="video-summary">{e(summary)}</p></div>"""
    scope = {"ko": "작동 개념", "en": "Operating concept", "ar": "مفهوم التشغيل"}[lang]
    return f"""<div class="cell span-4 demo-copy reveal"><p class="eyebrow">{e(LANGS[lang]["development_preview"])}</p><h2 class="section-title semantic-copy" data-fit-min="28" data-fit-text id="demo-title">{lines(product["outcome"][lang])}</h2><p class="body-large">{e(product["description"][lang])}</p></div>
<div class="cell span-8 demo-cell reveal delay-1"><div class="development-panel"><span class="status-badge is-preview">{e(LANGS[lang]["development_preview"])}</span><h3>{e(product["name"])}</h3><ul><li><strong>{e(LANGS[lang]["current_scope"])}:</strong> {e(scope)}</li><li><strong>{e(LANGS[lang]["pilot_input"])}:</strong> {e(product["inputs"][lang][0])}</li><li><strong>{e(LANGS[lang]["pilot_result"])}:</strong> {e(product["outputs"][lang][0])}</li></ul><a class="fm-button primary" href="{page_path(lang)}?interest={slug}#contact">{e(LANGS[lang]["pilot"])}</a></div></div>"""


def product_page(lang: str, slug: str, canonical_path: str) -> str:
    product = PRODUCTS[slug]
    title = product["title"][lang]
    description = product["description"][lang]
    status_label = LANGS[lang]["demo_available"] if product["status"] == "demo" else LANGS[lang]["development_preview"]
    status_class = "is-demo" if product["status"] == "demo" else "is-preview"
    steps = "\n".join(f'<article class="cell span-4 detail-feature reveal delay-{i+1}"><span>{num}</span><h3 class="semantic-copy card-title-fit" data-fit-min="19" data-fit-text>{lines(head)}</h3><p>{e(body)}</p></article>' for i, (num, head, body) in enumerate(product["steps"][lang]))
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
    html = f"""<!doctype html>
<html lang="{lang}" dir="{LANGS[lang]["dir"]}">
{meta_head(lang, slug, title, description, canonical_path)}
<body class="technology-page {product["class"]}" data-lang="{lang}" data-static-lang="true">
{header(lang, slug)}
<main id="main">
<section aria-labelledby="tech-title" class="detail-overview section-grid">
<div class="cell span-5 detail-hero-copy reveal"><p class="eyebrow">{e(product_name(product, lang))}</p><h1 class="hero-title semantic-copy" data-fit-min="30" data-fit-text id="tech-title">{lines(product["hero"][lang])}</h1><p class="body-large">{e(product["hero_body"][lang])}</p><div class="detail-meta"><span class="status-badge {status_class}">{e(status_label)}</span><span>{e(product["pilot_scope"][lang])}</span></div><a class="detail-inline-back" href="{page_path(lang)}#products">← {e(LANGS[lang]["all_products"])}</a></div>
<div class="cell span-7 detail-animation reveal delay-1"><div class="detail-animation-head"><p class="eyebrow">{e({"ko":"현재 Operating sequence","en":"Current operating sequence","ar":"تسلسل التشغيل الحالي"}[lang])}</p></div>{tech_visual(slug, lang)}</div>{steps}</section>
<section aria-labelledby="demo-title" class="detail-demo section-grid">{demo_panel(product, slug, lang)}</section>
<section aria-labelledby="spec-title" class="detail-specs section-grid"><div class="cell span-12 reveal"><p class="eyebrow">{e({"ko":"파일럿 검증 데이터","en":"Pilot validation data","ar":"بيانات التحقق التجريبي"}[lang])}</p><h2 class="section-title semantic-copy" data-fit-min="34" data-fit-text id="spec-title">{lines(product["outcome"][lang])}</h2><p class="body-large">{e(product["description"][lang])}</p></div>{specs}<div class="cell yellow span-12 reveal"><p class="body-large"><strong>{e({"ko":"파일럿 범위","en":"Pilot scope","ar":"نطاق المشروع التجريبي"}[lang])}:</strong> {e(product["pilot_scope"][lang])}</p></div></section>
<section aria-labelledby="related-title" class="related-flow section-grid"><div class="cell blue span-8 reveal"><p class="eyebrow">{e(LANGS[lang]["related"])}</p><h2 class="section-title semantic-copy" data-fit-min="30" data-fit-text id="related-title">{lines({"ko":"같은 운영 흐름에서|연결되는 모듈","en":"Modules connected|in the same operating flow","ar":"وحدات متصلة|في نفس التدفق التشغيلي"}[lang])}</h2><ul class="related-list">{related_items}</ul></div><div class="cell yellow span-4 cta-actions detail-cta-actions reveal delay-1"><a class="fm-button primary" href="{page_path(lang)}?interest={slug}#contact">{e(LANGS[lang]["pilot"])}</a><a class="fm-button" href="{page_path(lang)}#products">{e(LANGS[lang]["all_products"])}</a></div></section>
</main>{footer(lang)}<script src="{SCRIPT_SRC}"></script></body></html>"""
    return html


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def sitemap() -> str:
    urls = ["/", "/ko/", "/en/", "/ar/"]
    for lang in LANGS:
        urls.extend(page_path(lang, slug) for slug in PRODUCTS)
    body = "\n".join(f"  <url><loc>{abs_url(path)}</loc></url>" for path in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n'


def notes() -> str:
    return f"""# Flowmatic Implementation Notes

- 작성일: {date.today().isoformat()}
- 기술 스택: 순수 정적 HTML/CSS/JavaScript, GitHub Pages 배포
- 배포 플랫폼: GitHub Pages + CNAME `flowmatic-os.com`
- 다국어 처리 방식: `/ko/`, `/en/`, `/ar/` 정적 HTML을 생성하며 각 HTML에는 해당 언어만 렌더링합니다. 기존 루트 URL과 `*.html` 제품 URL은 한국어 호환 페이지로 유지합니다.
- 데모 영상 파일: `flowmatic_nc_demo.mp4`, `flowmatic_ct_demo.mp4`; 두 제품 페이지의 `<video>`는 `controls`, `playsinline`, `preload="metadata"`, `poster`를 사용합니다.
- 개발 프리뷰 제품: Work Standard, TMS, AMR은 빈 비디오 플레이어 없이 개발 상태 패널, 파일럿 입력, 확인 결과, 문의 CTA를 표시합니다.
- 실제 문의 목적지: 저장소에서 검증된 이메일, 폼 엔드포인트, 예약 링크를 찾지 못했습니다. 안전한 폴백으로 모든 CTA를 Contact 섹션과 `interest` query parameter로 연결했습니다.
- 적용한 안전한 폴백: 고객사, 성과 수치, 보안 인증, 배포 방식, 지원 컨트롤러, 회사 주소, 전화번호, 이메일은 추측해 표시하지 않았습니다.
- 사용자 확인 필요: 실제 문의 이메일 또는 폼 엔드포인트, 개인정보처리방침 URL, 법인명/주소/전화번호, 아랍어 최종 감수, Work Standard/TMS/AMR의 출시 상태.
"""


def main() -> None:
    write(Path("index.html"), home_page("ko", "/"))
    for slug in PRODUCTS:
        write(Path(f"{slug}.html"), product_page("ko", slug, f"/{slug}.html"))
    for lang in LANGS:
        write(Path(lang) / "index.html", home_page(lang, page_path(lang)))
        for slug in PRODUCTS:
            write(Path(lang) / slug / "index.html", product_page(lang, slug, page_path(lang, slug)))
    write(Path("robots.txt"), "User-agent: *\nAllow: /\nSitemap: https://flowmatic-os.com/sitemap.xml\n")
    write(Path("sitemap.xml"), sitemap())
    write(Path("IMPLEMENTATION_NOTES.md"), notes())


if __name__ == "__main__":
    main()
