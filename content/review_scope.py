"""Concise internal-review scope for collapsed product technical details."""

from html import escape as e


COPY = {
    "ko": {
        "label": "내부 검토",
        "machining": {
            "title": "설계 조건과 가공계획 검토",
            "body": (
                "지원 형상의 공정·NC·공구 정보와 3D 치구·설계 BOM을 "
                "데스크톱 제품 시연의 연결된 작업 흐름에서 검토합니다. "
                "공정시간 비교를 생산능력 계획에 사용합니다."
            ),
            "scope": (
                "제품 시연에서 확인한 지원 형상의 소프트웨어 검토 범위입니다. "
                "실제 제작에 사용할 치구·공구의 최종 선정과 제작도면 검토, "
                "현장 절삭시험·충돌 검증은 별도로 필요합니다."
            ),
        },
        "quality": {
            "title": "설계·품질 요구사항 매핑",
            "body": (
                "설계 객체와 품질 요구사항·특성의 연결 기준을 "
                "APQP 초안에 기록하고 검토합니다."
            ),
            "scope": (
                "초안 매핑 검토 범위이며, 완성된 검사계획이나 "
                "자동 개정 동기화를 포함하지 않습니다."
            ),
        },
        "logistics": {
            "title": "설비·운반 상태 시뮬레이션",
            "body": (
                "시뮬레이션에서 설비별 가공·막힘·투입 대기와 "
                "가상 운반기의 작업·빈 이동을 구분합니다. "
                "각 상태를 비교해 병목 후보를 검토합니다."
            ),
            "scope": (
                "합성 데이터 기반의 내부 검토이며, "
                "현장 OEE 측정이나 실제 운반 제어를 의미하지 않습니다."
            ),
        },
    },
    "en": {
        "label": "Internal review",
        "machining": {
            "title": "Design and machining plan review",
            "body": (
                "For supported geometry, the desktop product demonstration links "
                "process and NC review with tool information, 3D fixtures and "
                "design bills of materials. Process-time comparisons support "
                "production-capacity planning."
            ),
            "scope": (
                "This covers software review of the supported geometry shown in "
                "the product demonstration. Final fixture and tool selection and "
                "fabrication drawings for physical use require separate engineering "
                "review, cutting trials and collision validation."
            ),
        },
        "quality": {
            "title": "Design and quality requirement mapping",
            "body": (
                "Mappings between design objects, quality requirements and "
                "characteristics are recorded and reviewed in an APQP draft."
            ),
            "scope": (
                "Scope is draft mapping review; completed inspection plans and "
                "automatic revision synchronization remain outside this scope."
            ),
        },
        "logistics": {
            "title": "Simulation of equipment and handling states",
            "body": (
                "Simulation distinguishes unit processing, blocking and input "
                "waiting, together with virtual handling activity and empty "
                "movement. These states support review of potential bottlenecks."
            ),
            "scope": (
                "This is an internal review using synthetic data, not field OEE "
                "measurement or control of physical handling equipment."
            ),
        },
    },
    "ar": {
        "label": "مراجعة داخلية",
        "machining": {
            "title": "مراجعة التصميم وخطة التشغيل",
            "body": (
                "يعرض المنتج المكتبي، للأشكال المدعومة، مراجعة مترابطة للعمليات "
                "وبرامج NC ومعلومات الأدوات ونماذج المثبتات ثلاثية الأبعاد "
                "وقوائم مواد التصميم. تدعم مقارنة أزمنة العمليات تخطيط الطاقة الإنتاجية."
            ),
            "scope": (
                "يشمل ذلك مراجعة برمجية للأشكال المدعومة المعروضة في العرض التوضيحي. "
                "يتطلب الاختيار النهائي للمثبتات والأدوات ورسومات التصنيع للاستخدام الفعلي "
                "مراجعة هندسية منفصلة، كما يلزم التحقق الميداني من أداء القطع وخلو المسارات من التصادم."
            ),
        },
        "quality": {
            "title": "ربط التصميم بمتطلبات الجودة",
            "body": (
                "تُسجّل الروابط بين عناصر التصميم ومتطلبات الجودة وخصائص الجودة "
                "وتُراجع ضمن مسودة APQP."
            ),
            "scope": (
                "يقتصر النطاق على مراجعة روابط المسودة، ولا يشمل خطة فحص مكتملة "
                "أو مزامنة التعديلات تلقائيًا."
            ),
        },
        "logistics": {
            "title": "محاكاة حالات المعدات والمناولة",
            "body": (
                "تميّز المحاكاة بين حالات المعالجة والتوقف بسبب عائق في التدفق "
                "وانتظار التغذية لكل وحدة، إلى جانب عمل المناولة الافتراضية وحركتها "
                "دون حمولة. تُقارن هذه الحالات لمراجعة مواضع الاختناق المحتملة."
            ),
            "scope": (
                "هذه مراجعة داخلية ببيانات اصطناعية، وليست قياسًا ميدانيًا لـOEE "
                "أو تحكمًا في معدات مناولة فعلية."
            ),
        },
    },
}


def render_review_scope(lang, kind):
    """Render one bounded review note; unknown locales or kinds fail closed."""
    locale = COPY[lang]
    copy = locale[kind]
    identifier = f"review-{kind}"
    return (
        f'<div class="review-scope" id="{e(identifier)}">'
        f'<article class="wr-card" aria-labelledby="{e(identifier)}-title">'
        f'<p class="wr-label">{e(locale["label"])}</p>'
        f'<h3 id="{e(identifier)}-title">{e(copy["title"])}</h3>'
        f'<p>{e(copy["body"])}</p>'
        f'<p class="wr-footnote">{e(copy["scope"])}</p>'
        '</article></div>'
    )
