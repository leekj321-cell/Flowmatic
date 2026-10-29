"""Concise internal-review scope for collapsed product technical details."""

from html import escape as e


COPY = {
    "ko": {
        "label": "내부 검토",
        "machining": {
            "title": "설계 조건과 가공계획 검토",
            "body": (
                "표준 부품·공통 치구 몸체와 설계 BOM을 검토합니다. "
                "치구 제약에 따른 NC 후보·전체 공정시간을 비교하고, "
                "채택한 설계 기준으로 정적 생산능력을 추정합니다."
            ),
            "scope": (
                "각 기능은 별도의 내부 설계·계획 시험 범위이며, "
                "실제 절삭·충돌 검증은 포함하지 않습니다."
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
                "Standard components, shared fixture bodies and design bills of "
                "materials are reviewed. Candidate NC programs and total process "
                "times are compared under fixture constraints, while adopted "
                "design criteria support static production capacity estimates."
            ),
            "scope": (
                "These are separate internal design and planning tests, without "
                "validation of cutting or collision clearance."
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
                "تُراجع المكونات القياسية وأجسام التثبيت المشتركة وقوائم مواد التصميم. "
                "تُقارن برامج NC المرشحة وأزمنة العملية الكلية وفق قيود التثبيت، "
                "وتُستخدم معايير التصميم المعتمد لتقدير حسابي غير ديناميكي للطاقة الإنتاجية."
            ),
            "scope": (
                "تستند هذه الوظائف إلى اختبارات داخلية منفصلة للتصميم والتخطيط، "
                "ولا تشمل التحقق من أداء القطع أو خلو المسارات من التصادم."
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
