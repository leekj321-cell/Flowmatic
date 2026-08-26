"""Public-safe multilingual content for the Factory OS v2 information architecture."""


def l(ko, en, ar):
    return {"ko": ko, "en": en, "ar": ar}


ASSET_PATH = "/assets/factory-os"

HOME_OVERRIDES = {
    "ko": {
        "title": "Flowmatic | Factory Operating Intelligence",
        "description": "Flowmatic은 기존 공장을 유지하면서 품질·가공·운영·물류에서 사람이 메우던 판단과 전달의 간극을 구조화하는 Factory Operating Intelligence입니다.",
        "body": "기존 공장은 그대로 두고, 사람이 시스템 사이에서 메우던 운영의 간극을 읽고 판단해 다음 행동으로 연결합니다.",
        "products_title": "네 개의 전문 지능.|하나의 공장 운영 언어.",
        "products_body": "각 도메인은 독립적으로 도입되며 공통 Manufacturing Context와 Event 체계를 공유합니다.",
        "workflow_title": "구현 증거와|후속 통합 범위.",
        "workflow_body": "구현됨·개발 중·계획을 분리해 현재 제품 상태와 다음 통합 범위를 정확히 보여줍니다.",
    },
    "en": {
        "title": "Flowmatic | Factory Operating Intelligence",
        "description": "Flowmatic keeps the factory that already works and structures the judgment and handoff gaps people bridge across quality, machining, operations, and logistics.",
        "body": "Keep the factory that already works. Connect the operational gaps people bridge between systems, from signal and context to the next accountable action.",
        "products_title": "Four specialized intelligence domains.|One factory operating language.",
        "products_body": "Each domain can start independently while using the same Manufacturing Context and Event language by design.",
        "workflow_title": "Separate built evidence|from the next integration.",
        "workflow_body": "Inspect real demos and working prototypes while Event Core and Control Tower remain clearly labeled as the next integration stages.",
    },
    "ar": {
        "title": "Flowmatic | ذكاء تشغيل المصنع",
        "description": "يحافظ Flowmatic على المصنع القائم وينظم فجوات القرار والتسليم التي يعالجها الأشخاص بين الجودة والتشغيل والعمليات واللوجستيات.",
        "body": "حافظ على المصنع الذي يعمل بالفعل، واربط فجوات التشغيل بين الأنظمة من الإشارة والسياق إلى الإجراء التالي ومسؤوله.",
        "products_title": "أربعة مجالات ذكاء متخصصة.|لغة تشغيل واحدة للمصنع.",
        "products_body": "يمكن لكل مجال أن يبدأ مستقلًا، مع تصميمه لاستخدام سياق التصنيع ولغة الأحداث نفسيهما.",
        "workflow_title": "نفصل الدليل المبني|عن التكامل التالي.",
        "workflow_body": "يمكن فحص العروض الفعلية والنماذج العاملة، بينما يبقى Event Core وControl Tower مرحلتي التكامل التاليتين بوضوح.",
    },
}

DOMAINS = [
    {
        "slug": "quality",
        "name": "Quality Intelligence",
        "status": l("Working prototype", "Working prototype", "نموذج أولي عامل"),
        "flow": "Defect → Loss → Priority → Work → Verify → Recurrence",
        "body": l(
            "불량을 집계하는 데서 끝내지 않습니다. 실제 손실을 기준으로 개선 우선순위를 정하고 업무·효과·재발까지 연결합니다.",
            "Go beyond defect counts. Rank improvement work by actual loss, then connect ownership, effect verification, and recurrence.",
            "لا يتوقف عند عدّ العيوب، بل يرتب أعمال التحسين حسب الخسارة الفعلية ويربط المسؤولية والتحقق من الأثر والتكرار.",
        ),
        "components": ["Inspection — Evidence / Input Layer", "Loss / Priority", "Worklist", "Effect Verification", "Recurrence"],
    },
    {
        "slug": "machining-intelligence",
        "name": "Machining Intelligence",
        "status": l("Active development / PoC", "Active development / PoC", "تطوير نشط / نطاق PoC"),
        "flow": "Understand → Build Recipe → Generate → Measure → Correct → Standardize",
        "body": l(
            "제품·공정·Feature·NC·측정·보정을 하나의 Manufacturing Recipe로 연결합니다. 기존 G-code의 공정 문맥을 복원하고 새로운 NC에는 그 문맥을 다시 담습니다.",
            "Connect product, process, feature, NC, measurement, and correction in one Manufacturing Recipe. Recover process context from existing G-code and carry it into newly generated NC.",
            "يربط المنتج والعملية والميزة وNC والقياس والتصحيح في Manufacturing Recipe واحدة، ويستعيد سياق G-code القائم ويحمله إلى NC الجديد.",
        ),
        "components": ["G-code Intelligence", "Manufacturing Recipe", "Generator / Safe Assembly", "Measurement / Compensation", "Work Standard", "Machine / Tool Context"],
    },
    {
        "slug": "operations-intelligence",
        "name": "Operations Intelligence",
        "status": l("Functional MVP / internal validation", "Functional MVP / internal validation", "MVP وظيفي / تحقق داخلي"),
        "flow": "Intake → Allocate → Track → Normalize → Detect",
        "body": l(
            "메일·메신저·현장 요청을 품목과 수량으로 구조화하고, 구매·소모품·공구·인력 사용량을 생산문맥과 연결해 비용과 이상징후를 찾습니다.",
            "Structure requests from email, chat, and the shop floor into items and quantities, then connect purchasing, consumables, tools, and labor to production context to surface cost and anomaly signals.",
            "ينظم طلبات البريد والمحادثة والميدان إلى أصناف وكميات، ثم يربط المشتريات والمواد المستهلكة والأدوات والعمل بسياق الإنتاج لإظهار التكلفة وإشارات الشذوذ.",
        ),
        "components": ["Procurement", "Consumables", "Tool Economics", "Labor", "Tracked Operational Cost", "Anomaly"],
    },
    {
        "slug": "logistics-intelligence",
        "name": "Logistics Intelligence",
        "status": l("Prototype integration", "Prototype integration", "تكامل نموذجي أولي"),
        "flow": "Demand → Prioritize → Assign → Dispatch → Confirm",
        "body": l(
            "자재 요청을 작업으로 바꾸고 사람·지게차·AMR 가운데 실행 주체를 배정한 뒤 실제 투입 완료까지 확인합니다.",
            "Turn material demand into work, assign the right person, forklift, or AMR, and confirm that the material was actually put into use.",
            "يحوّل طلب المواد إلى عمل، ويعيّن الشخص أو الرافعة أو AMR المناسب، ثم يؤكد إدخال المادة فعليًا.",
        ),
        "components": ["Operator", "Fleet / Dispatch", "AMR / Forklift / Worker", "Last-meter confirmation"],
    },
]

CERTIFIED_CORE = {
    "title": l(
        "인증 핵심 유지.|수작업 간극 자동화.",
        "Keep the certified core.|Automate the manual gap.",
        "نُبقي النواة المعتمدة.|ونؤتمت الفجوة اليدوية.",
    ),
    "body": l(
        "기존 안전제어·전문 CAM·정밀측정·기준정보 시스템은 유지합니다. Flowmatic은 시스템 사이의 관찰·문맥·우선순위·업무·증빙·확인을 연결합니다.",
        "Flowmatic does not force-replace safety control, specialist CAM, precision metrology, or systems of record. It connects observation, context, priority, workflow, evidence, and confirmation between them.",
        "لا يستبدل Flowmatic قسرًا التحكم الآمن أو CAM المتخصص أو القياس الدقيق أو أنظمة السجل. بل يربط الرصد والسياق والأولوية وسير العمل والدليل والتأكيد بينها.",
    ),
    "cards": [
        ("PLC / Safety", l("비상정지·인터록·인증 안전제어는 기존 제어계층에서 유지합니다.", "Keep E-stop, interlocks, and certified safety control in the existing layer.", "تبقى أنظمة الإيقاف الطارئ والتشابك والتحكم الآمن المعتمد في طبقتها الحالية.")),
        ("CAM", l("복잡한 Toolpath 생성은 전문 CAM에서 수행하며 Flowmatic은 현장 검토 workflow를 연결합니다.", "Keep complex toolpath generation in specialist CAM and connect the field review workflow.", "يبقى توليد مسار الأداة المعقد في CAM المتخصص، مع ربط سير مراجعة الميدان.")),
        ("Precision Metrology", l("µm급 판정은 전용 측정기가 담당하며 Vision은 screening과 triage를 지원합니다.", "Keep micron-level acceptance in dedicated metrology; Vision supports screening and triage.", "يبقى حكم القبول بمستوى الميكرون لأجهزة القياس المخصصة، وتدعم الرؤية الفحص والفرز.")),
        ("ERP / MES / WMS", l("System of Record는 유지하며 필요한 Adapter와 Event layer만 연결합니다.", "Keep the system of record and connect only the adapters and Event layer required.", "نُبقي نظام السجل ونربط فقط المحولات وطبقة الأحداث المطلوبة.")),
    ],
}

PLATFORM = {
    "title": l(
        "도메인별 전문 지능.|공통 ID와 Event 체계.",
        "Different domains.|One identity and Event language for the factory.",
        "تختلف المجالات.|لكن هوية المصنع ولغة الأحداث واحدة.",
    ),
    "body": l(
        "네 지능축은 Shared Manufacturing Context와 Event Core를 공유합니다. Control Tower는 후속 통합 감독 계층입니다.",
        "The four domains first align on Shared Manufacturing Context, then connect through Event Core. Control Tower is the planned integrated supervision layer above that foundation.",
        "تتوافق المجالات الأربعة أولًا على سياق تصنيع مشترك، ثم تتصل عبر Event Core. أما Control Tower فهي طبقة إشراف متكاملة مخطط لها فوق هذا الأساس.",
    ),
    "entities": ["Factory", "Area", "Line", "Equipment", "Product", "LOT", "Process Group", "Operation", "Feature", "Recipe / Revision", "Tool", "Worker", "Task", "Material", "Time"],
    "layers": [
        ("Shared Manufacturing Context", l("Integration foundation", "Integration foundation", "أساس التكامل"), l("공장·설비·제품·LOT의 공통 ID를 유지하며 Machining 문맥은 공정·Operation·Feature·Recipe revision까지 연결 가능하도록 확장합니다.", "Maintain shared factory, equipment, product, and LOT identity while extending machining context down to process, operation, feature, and recipe revision.", "حافظ على هوية المصنع والمعدة والمنتج وLOT مع توسيع سياق التشغيل إلى العملية وOperation والميزة ومراجعة Recipe.")),
        ("Event Core", l("Next integration layer", "Next integration layer", "طبقة التكامل التالية"), l("도메인 신호를 공통 Event·State·Context·Linkage로 정규화하는 다음 계층입니다.", "The next layer that normalizes domain signals into common Event, State, Context, and Linkage.", "الطبقة التالية التي توحّد إشارات المجالات إلى Event وState وContext وLinkage مشتركة.")),
        ("Manufacturing Control Shell", l("Prototype", "Prototype", "نموذج أولي"), l("공통 Factory·Group·Period 문맥과 모듈 실행·집계를 제공하는 현재 상위 Shell입니다.", "The current upper shell for shared Factory, Group, and Period context plus module launch and aggregation.", "الغلاف العلوي الحالي لسياق Factory وGroup وPeriod المشترك وتشغيل الوحدات وتجميعها.")),
        ("Cross-domain Control Tower", l("Planned integrated supervision", "Planned integrated supervision", "إشراف متكامل مخطط"), l("손실·위험·우선순위·다음 행동을 도메인 간에 종합하는 계획 단계입니다.", "The planned layer for cross-domain loss, risk, priority, and next-action supervision.", "الطبقة المخطط لها للإشراف عبر المجالات على الخسارة والمخاطر والأولوية والإجراء التالي.")),
    ],
}

EVIDENCE = [
    ("Machining · Recipe", l("Source-level validated", "Source-level validated", "متحقق على مستوى المصدر"), l("Manufacturing Recipe persistence, Product→Process Group→Operation scope, stored Code Blocks, final order와 assembled G-code를 deterministic source test로 확인했습니다.", "Deterministic source tests cover Manufacturing Recipe persistence, Product→Process Group→Operation scope, stored Code Blocks, final order, and assembled G-code.", "تغطي اختبارات المصدر الحتمية حفظ Manufacturing Recipe ونطاق Product→Process Group→Operation وكتل الكود وترتيبها وG-code المجمّع."), "machining-intelligence"),
    ("Machining · Safety Contract", l("Source-level validated", "Source-level validated", "متحقق على مستوى المصدر"), l("Block Boundary Safety Contract와 fail-closed assembly logic을 source level에서 검증했습니다.", "Block Boundary Safety Contract and fail-closed assembly logic are validated at source level.", "تم التحقق على مستوى المصدر من Block Boundary Safety Contract ومنطق التجميع fail-closed."), "machining-intelligence"),
    ("Machining · V.Next scope", l("Active development / PoC", "Active development / PoC", "تطوير نشط / نطاق PoC"), l("Unmanaged G-code inference, managed metadata, USB sync, CNC/CMM 연결과 설비측 보정은 개발·PoC 범위입니다.", "Unmanaged G-code inference, managed metadata, USB sync, CNC/CMM integration, and machine-side correction remain development and PoC scope.", "يبقى استدلال G-code غير المدار والبيانات الوصفية والمزامنة عبر USB وتكامل CNC/CMM والتصحيح على الماكينة ضمن التطوير وPoC."), "machining-intelligence"),
    ("Quality", l("Working prototype", "Working prototype", "نموذج عامل"), l("불량→손실→우선순위→업무→효과확인→재발 구조를 구현하며 Inspection은 증거 입력 계층으로 둡니다.", "The working structure connects defect, loss, priority, work, effect verification, and recurrence; Inspection remains the evidence input layer.", "يربط الهيكل العامل العيب والخسارة والأولوية والعمل والتحقق من الأثر والتكرار، بينما تبقى Inspection طبقة إدخال الأدلة."), "quality"),
    ("Operations", l("Functional MVP / internal validation", "Functional MVP / internal validation", "MVP وظيفي / تحقق داخلي"), l("요청 구조화와 생산량 기준 자원사용·비용·이상 후보를 내부 검증 중입니다.", "Request structuring and production-normalized resource, cost, and anomaly candidates are under internal validation.", "يخضع تنظيم الطلبات وتطبيع الموارد والتكلفة ومؤشرات الشذوذ حسب الإنتاج للتحقق الداخلي."), "operations-intelligence"),
    ("Logistics", l("Prototype integration", "Prototype integration", "تكامل نموذج أولي"), l("요청·우선순위·실행자 배정·배차·투입 확인을 연결하는 prototype integration 범위입니다.", "Prototype integration connects demand, priority, actor assignment, dispatch, and input confirmation.", "يربط تكامل النموذج الأولي الطلب والأولوية وتعيين المنفذ والإرسال وتأكيد الإدخال."), "logistics-intelligence"),
]

DEPLOYMENT_MODES = [
    ("Brownfield — Factory → Model", l("현장 움직임·문서·NC·작업방식에서 운영모델을 구성합니다.", "Read the existing factory's motion, documents, NC, and work methods to reconstruct an operating model.", "نقرأ حركة المصنع القائم ووثائقه وNC وأساليب العمل لإعادة بناء نموذج التشغيل."), l("Field-first deployment", "Field-first deployment", "نشر يبدأ من الميدان")),
    ("Greenfield — Model → Factory", l("안정화 전부터 Process·Quality·Material·Work·Control Event model을 설계하는 미래 확장 아키텍처입니다.", "A future-expansion architecture that designs Process, Quality, Material, Work, and Control Event models before stabilization.", "بنية توسع مستقبلية تصمم نماذج أحداث العملية والجودة والمواد والعمل والتحكم قبل الاستقرار."), l("Deployment architecture / future expansion", "Deployment architecture / future expansion", "بنية نشر / توسع مستقبلي")),
]

ROADMAP = [
    ("01", "Specialized Intelligence", l("Quality·NC·CT·Operations·Operator·Fleet 프로토타입을 도메인별로 검증합니다.", "Validate Quality, NC, CT, Operations, Operator, and Fleet prototypes within each domain.", "التحقق من نماذج Quality وNC وCT وOperations وOperator وFleet داخل كل مجال.")),
    ("02", "Domain Integration", l("Machining·Operations·Logistics의 내부 문맥과 workflow를 통합합니다.", "Close the internal context and workflows of Machining, Operations, and Logistics intelligence.", "استكمال السياق الداخلي وسير العمل لذكاء التشغيل والعمليات واللوجستيات.")),
    ("03", "Shared Context + Event Core", l("공통 ID·Event schema·도메인 간 linkage를 구축합니다.", "Connect common identity, Event schema, and cross-domain linkage.", "ربط الهوية المشتركة ومخطط الأحداث والعلاقات بين المجالات.")),
    ("04", "Control Tower", l("도메인 간 손실·위험·우선순위·후속 행동을 통합 감독합니다.", "Integrate cross-domain loss, risk, priority, and next-action supervision.", "دمج الإشراف عبر المجالات على الخسارة والمخاطر والأولوية والإجراء التالي.")),
    ("05", "Deployment Templates", l("Brownfield Factory→Model과 Greenfield Model→Factory 배포 템플릿을 정의합니다.", "Define Brownfield Factory→Model and future Greenfield Model→Factory deployment templates.", "تعريف قوالب Brownfield من Factory إلى Model وقوالب Greenfield المستقبلية من Model إلى Factory.")),
]

PAGES = {
    "operations-intelligence": {
        "label": "Operations Intelligence",
        "title": l("Flowmatic Operations Intelligence | Procurement · Consumption · Labor · Cost", "Flowmatic Operations Intelligence | Procurement · Consumption · Labor · Cost", "Flowmatic Operations Intelligence | المشتريات والاستهلاك والعمل والتكلفة"),
        "description": l("구매·소모품·공구비·공수를 실제 운영 문맥에 연결하고 생산량 기준 이상 후보를 드러냅니다.", "Connect purchasing, consumption, labor, and tool economics to operating context and surface production-normalized anomaly candidates.", "يربط المشتريات والاستهلاك والعمل واقتصاديات الأدوات بسياق التشغيل ويكشف مؤشرات الشذوذ المطبّعة بالإنتاج."),
        "hero": l("요청을 다시 타이핑하는 시간을 줄이고,|사용량과 비용의 이상 지점을 찾습니다.", "Spend less time retyping requests.|Find where usage and cost begin to move abnormally.", "قلّل وقت إعادة إدخال الطلبات.|واكتشف أين يبدأ الاستخدام والتكلفة بالانحراف."),
        "body": l("메일·메신저·현장 요청을 품목·규격·수량 후보로 구조화하고 사용자 확인을 거쳐 기존 양식으로 연결합니다. 자원 사용량은 생산문맥으로 정규화해 설비·공정 검토 후보를 찾습니다.", "Structure mail, chat, and field requests into item, specification, and quantity candidates, require user confirmation, then return confirmed data to existing forms. Normalize resource use by production context to surface machine or process review candidates.", "نظّم البريد والمحادثة وطلبات الميدان إلى مرشحات الصنف والمواصفة والكمية، ثم اطلب تأكيد المستخدم وأعد البيانات المؤكدة إلى النماذج القائمة. طبّع استخدام الموارد بسياق الإنتاج لإظهار مرشحات مراجعة المعدة أو العملية."),
        "status": l("Functional MVP / internal validation", "Functional MVP / internal validation", "MVP وظيفي / تحقق داخلي"),
        "flow": ["Intake", "Resolve", "Allocate", "Track", "Normalize", "Detect"],
        "asset": f"{ASSET_PATH}/01_operations_intelligence.svg",
        "sections": [
            ("Procurement Intelligence", l("Functional MVP", "Functional MVP", "MVP وظيفي"), l("메일·채팅에서 품명·규격·수량·UOM·문맥을 추출하고 confidence·reason과 함께 후보를 제시합니다. 담당자 확인 항목만 기존 요청양식으로 출력합니다.", "Extract item, specification, quantity, UOM, and context from free-text mail or chat; present candidates with confidence and reason; export confirmed items only to the existing request template.", "استخراج الصنف والمواصفة والكمية وUOM والسياق من البريد أو المحادثة، وعرض المرشحين مع الثقة والسبب، وتصدير العناصر المؤكدة فقط إلى القالب الحالي."), ["No silent 1EA default for missing quantity", "No auto-confirm on conflicting specifications", "No arbitrary conversion of unknown pack units", "Quantity / use-location split", "Confirmed-only template export"]),
            ("Resource Economics", l("Functional MVP", "Functional MVP", "MVP وظيفي"), l("Tool·Consumable·Labor event를 Tracked Operational Cost로 묶고 생산량과 가동시간으로 정규화합니다.", "Combine Tool, Consumable, and Labor events as Tracked Operational Cost and normalize them by production and running time.", "تجميع أحداث الأدوات والمواد المستهلكة والعمل في Tracked Operational Cost وتطبيعها حسب الإنتاج ووقت التشغيل."), ["Cost / Production EA", "Cost / Good EA", "Man-hour / 1,000 EA", "Consumption / 1,000 EA", "Consumption / running hour"]),
            ("Cost / Consumption Anomaly", l("MVP candidate detection", "MVP candidate detection", "اكتشاف مرشحين ضمن MVP"), l("Rolling Median + MAD와 EWMA로 이상 후보를 식별합니다. 예측정비 원인분석은 범위에 포함되지 않습니다.", "Use Rolling Median + MAD and EWMA to surface anomaly candidates. This is not completed predictive-maintenance root-cause reasoning.", "استخدام Rolling Median + MAD وEWMA لإظهار مؤشرات الشذوذ. وهذا ليس استدلالًا مكتملًا لسبب الصيانة التنبؤية."), ["Rolling Median + MAD", "EWMA", "Production-normalized candidates", "Human review remains required"]),
            ("Manufacturing Control Shell", l("Prototype", "Prototype", "نموذج أولي"), l("Shared Factory·Group·Period context, module launcher, aggregation을 제공하는 prototype입니다. Control Tower 통합은 계획 단계입니다.", "An upper shell with shared Factory, Group, and Period context plus module launch and aggregation. It is not a completed Control Tower.", "غلاف علوي بسياق Factory وGroup وPeriod مشترك وتشغيل وتجميع الوحدات. وليس Control Tower مكتملًا."), ["Real-time ERP/MES connectors pending", "Live inventory / budget / supplier / forecasting pending", "Maintenance correlation and full Quality adapter pending"]),
        ],
        "guardrail": l("Tracked Operational Cost는 현재 연동된 공구·소모품·공수 비용만 포함합니다. Material·Energy·Maintenance·Outsource를 포괄하는 제조원가·회계원가는 아닙니다.", "Tracked Operational Cost covers the currently connected tool, consumable, and labor cost events. It is not full manufacturing or accounting cost across Material, Energy, Maintenance, and Outsource.", "يغطي Tracked Operational Cost أحداث تكلفة الأدوات والمواد المستهلكة والعمل المتصلة حاليًا، وليس تكلفة تصنيع أو محاسبة كاملة تشمل المواد والطاقة والصيانة والتعهيد."),
    },
    "logistics-intelligence": {
        "label": "Logistics Intelligence",
        "title": l("Flowmatic Logistics Intelligence | Demand to Dispatch to Confirmation", "Flowmatic Logistics Intelligence | Demand to Dispatch to Confirmation", "Flowmatic Logistics Intelligence | من الطلب إلى الإرسال والتأكيد"),
        "description": l("자재 요구를 우선순위·배정·이동·라스트미터 확인으로 연결합니다.", "Connect material demand to priority, assignment, dispatch, last-meter execution, and confirmation.", "يربط طلب المواد بالأولوية والتوزيع والإرسال والتنفيذ في آخر متر والتأكيد."),
        "hero": l("누가 요청했고 무엇이 필요한지부터|실제 투입 확인까지", "From who needs what|to confirmation of actual input", "من صاحب الطلب وما المطلوب|إلى تأكيد الإدخال الفعلي"),
        "body": l("요청·품목·우선순위를 작업으로 만들고 사람·지게차·AMR 가운데 실행 주체를 배정한 뒤 도착과 실제 투입을 확인합니다.", "Turn requester, item, and priority into work; assign a person, forklift, or AMR; then confirm arrival and actual input.", "حوّل مقدم الطلب والصنف والأولوية إلى عمل، وعيّن شخصًا أو رافعة أو AMR، ثم أكد الوصول والإدخال الفعلي."),
        "status": l("Prototype integration", "Prototype integration", "تكامل نموذجي أولي"),
        "flow": ["Demand", "Prioritize", "Assign", "Dispatch", "Last-meter", "Confirm"],
        "asset": None,
        "sections": [
            ("Operator", l("Functional prototype", "Functional prototype", "نموذج وظيفي"), l("작업 요청·수락·예외·완료 증빙을 처리하는 사용자 interface입니다.", "The request, confirmation, and exception interface between people and work.", "واجهة الطلب والتأكيد ومعالجة الاستثناءات بين الأشخاص والعمل."), ["Demand event", "Task acceptance", "Exception / acknowledgement", "Completion evidence"]),
            ("Fleet / Dispatch", l("Simulation + prototype", "Simulation + prototype", "محاكاة + نموذج أولي"), l("Queue·actor state·priority·dispatch context를 관리합니다.", "Manage queue, actor state, priority, and dispatch context.", "إدارة قائمة الانتظار وحالة المنفذ والأولوية وسياق الإرسال."), ["Worker", "Forklift", "AMR", "Drone / mobile sensor", "Mobile Automation Cell"]),
            ("Last-meter Confirmation", l("Prototype integration", "Prototype integration", "تكامل نموذجي أولي"), l("도착·도킹·라인사이드 투입·빈 용기 회수로 Event를 종결합니다.", "Close the event through arrival, docking, line-side input, and empty-container return.", "إغلاق الحدث عبر الوصول والالتحام والإدخال بجانب الخط وإرجاع الحاوية الفارغة."), ["Arrival", "Docking", "Input confirmed", "Return / event closed"]),
            ("Mobile Automation Level 1–5", l("Long-term vision", "Long-term vision", "رؤية طويلة المدى"), l("AMR은 실행 actor 중 하나입니다. 이동형 자동화 셀·재구성 가능 배정은 장기 비전이며 안전연동은 현장검증 전입니다.", "AMR is one execution actor, not the whole product. Mobile automation cells and reconfigurable assignment are long-term vision; real safety integration remains pending field validation.", "AMR منفذ واحد وليس المنتج كله. خلايا الأتمتة المتنقلة والتوزيع القابل لإعادة التهيئة رؤية طويلة المدى، والتكامل الحقيقي للسلامة ينتظر التحقق الميداني."), ["Level 1 sensing", "Level 2 guided execution", "Level 3 mobile task actor", "Level 4 flexible line automation", "Level 5 reconfigurable factory automation"]),
        ],
        "guardrail": l("AMR 안전연동과 생산 배치는 현장검증 전입니다. 내부 안전제어는 PLC와 설비 controller가 담당합니다.", "Real AMR safety integration and production deployment remain pending field validation. PLCs and machine controllers retain responsibility for internal safety control.", "لا يزال تكامل سلامة AMR والنشر الإنتاجي بانتظار التحقق الميداني. وتبقى مسؤولية التحكم الآمن الداخلي لدى PLC ووحدات تحكم الآلات."),
    },
    "platform": {
        "label": "Flowmatic Platform / Factory OS",
        "title": l("Flowmatic Platform | Event Core & Control Tower Architecture", "Flowmatic Platform | Event Core & Control Tower Architecture", "Flowmatic Platform | بنية Event Core وControl Tower"),
        "description": l("네 전문 지능을 Shared Manufacturing Context, Event Core, 계획된 Control Tower로 연결하는 Factory OS 아키텍처입니다.", "The Factory OS architecture connecting four intelligence domains through Shared Manufacturing Context, Event Core, and a planned Control Tower.", "بنية Factory OS التي تربط أربعة مجالات ذكاء عبر سياق تصنيع مشترك وEvent Core وControl Tower مخطط لها."),
        "hero": l("네 개의 전문 지능.|공통 공장 운영 체계.", "Four specialized intelligence domains.|One factory operating language.", "أربعة مجالات ذكاء متخصصة.|لغة تشغيل واحدة للمصنع."),
        "body": l("품질·가공·운영·물류 판단을 Event Core에 통합하고 후속 행동을 조율하는 아키텍처입니다.", "Explain how quality, machining, operations, and logistics intelligence converge on one Event Core and a future integrated supervision layer.", "شرح كيفية التقاء ذكاء الجودة والتشغيل والعمليات واللوجستيات في Event Core واحدة وطبقة إشراف متكاملة مستقبلية."),
        "status": l("Architecture / integration roadmap", "Architecture / integration roadmap", "بنية / خارطة تكامل"),
        "flow": ["Quality · Machining · Operations · Logistics", "Shared Manufacturing Context", "Event Core", "Manufacturing Control Shell", "Cross-domain Control Tower · Planned"],
        "asset": f"{ASSET_PATH}/00_factory_os_four_axes.svg",
        "sections": [
            ("Shared Manufacturing Context", l("Integration foundation", "Integration foundation", "أساس التكامل"), l("Event보다 먼저 Factory·Line·Equipment·Product·LOT·Tool·Worker·Task·Material·Time의 ID와 mapping을 맞춥니다.", "Before Event integration, align identity and mapping for Factory, Line, Equipment, Product, LOT, Tool, Worker, Task, Material, and Time.", "قبل تكامل الأحداث، تتم مواءمة هوية وربط Factory وLine وEquipment وProduct وLOT وTool وWorker وTask وMaterial وTime."), PLATFORM["entities"]),
            ("Event Core", l("Next integration layer", "Next integration layer", "طبقة التكامل التالية"), l("각 도메인의 Event·State·Context·Priority·Confidence·Linkage·History를 공통 언어로 정규화하는 다음 계층입니다.", "The next layer for normalizing each domain's Event, State, Context, Priority, Confidence, Linkage, and History.", "الطبقة التالية لتوحيد Event وState وContext وPriority وConfidence وLinkage وHistory لكل مجال."), ["Not a completed unified event bus", "Adapters and cross-domain links remain integration work"]),
            ("Control Shell vs Control Tower", l("Prototype vs planned", "Prototype vs planned", "نموذج أولي مقابل مخطط"), l("현재 Manufacturing Control Shell은 공통 문맥·launcher·aggregation prototype입니다. Cross-domain Control Tower는 손실·위험·우선순위·다음 행동을 종합할 계획된 감독 계층입니다.", "The current Manufacturing Control Shell is a shared-context, launcher, and aggregation prototype. Cross-domain Control Tower is the planned supervision layer for loss, risk, priority, and next action.", "Manufacturing Control Shell الحالي نموذج أولي للسياق المشترك والتشغيل والتجميع، بينما Control Tower عبر المجالات طبقة إشراف مخطط لها للخسارة والمخاطر والأولوية والإجراء التالي."), ["Shell — Prototype", "Control Tower — Planned integrated supervision"]),
            ("Synthetic Cross-domain Examples", l("Public-safe examples", "Public-safe examples", "أمثلة عامة آمنة"), l("합성 데이터로 도메인 간 연계 방식을 제시합니다. 고객 데이터는 사용하지 않습니다.", "Use synthetic—not customer—examples to explain cross-domain direction.", "استخدام أمثلة تركيبية وليست بيانات عملاء لشرح اتجاه الربط بين المجالات."), ["Quality P1 + tool-consumption spike + CT degradation → machining review", "Material-shortage risk + production-loss forecast → logistics escalation", "Repeated defect + unit-loss context → Quality worklist elevation"]),
            ("Brownfield / Greenfield", l("Current mode / future expansion", "Current mode / future expansion", "نمط حالي / توسع مستقبلي"), l("Brownfield Factory→Model은 현재 공장을 읽는 방식입니다. Greenfield Model→Factory는 안정화 전 Event model을 설계하는 미래 확장 아키텍처이며 구축완료 사례가 아닙니다.", "Brownfield Factory→Model reads the current factory. Greenfield Model→Factory is a future-expansion architecture for designing Event models before stabilization, not a completed reference deployment.", "Brownfield من Factory إلى Model يقرأ المصنع القائم. أما Greenfield من Model إلى Factory فهي بنية توسع مستقبلية لتصميم نماذج الأحداث قبل الاستقرار وليست حالة نشر مكتملة."), ["Brownfield — Field-first deployment", "Greenfield — Deployment architecture / future expansion"]),
        ],
        "guardrail": l("Event Core와 Control Tower는 통합 로드맵 단계이며 현재 완료 범위가 아닙니다.", "The Factory OS direction is explicit, but Event Core and Control Tower integration are not presented as complete.", "اتجاه Factory OS واضح، لكن لا يُقدّم تكامل Event Core وControl Tower على أنه مكتمل."),
    },
}

QUALITY_CURRENT = {
    "title": l("검사 결과에서|개선 효과 검증까지", "Detection is only the start.", "الاكتشاف ليس سوى البداية."),
    "body": l("검사 결과를 손실·우선순위·개선업무·효과·재발 관리로 확장합니다.", "Turn quality evidence into loss context, priority, action, effect verification, and recurrence control.", "حوّل أدلة الجودة إلى سياق خسارة وأولوية وإجراء وتحقق من الأثر وضبط التكرار."),
    "flow": ["Capture", "Standardize", "Quantify", "Prioritize", "Act", "Verify"],
    "cards": [
        ("Evidence + Standardize", l("Multi-camera·LOT·checksum·timestamp 증거를 제품·그룹·원인·기간 문맥으로 표준화합니다.", "Standardize multi-camera, LOT, checksum, and timestamp evidence by product, group, cause, and period.", "توحيد أدلة الكاميرات وLOT وchecksum وtimestamp حسب المنتج والمجموعة والسبب والفترة.")),
        ("Quantify + Prioritize", l("PPM·불량수량·손실금액·기준단가 provenance를 분석기간별로 재계산하고 설명 가능한 P1–P3 순위를 만듭니다.", "Recalculate PPM, defect quantity, loss, and reference-price provenance by analysis range and create explainable P1–P3 ranking.", "إعادة حساب PPM وكمية العيوب والخسارة ومصدر السعر المرجعي حسب فترة التحليل وإنشاء ترتيب P1–P3 قابل للتفسير.")),
        ("Worklist + Verify", l("담당자·상태·다음 확인을 Worklist로 연결하고 관찰·효과확인·재발 상태를 이어갑니다.", "Connect owner, status, and next check in a worklist, then continue observation, effect confirmation, and recurrence state.", "ربط المالك والحالة والفحص التالي في قائمة عمل ثم متابعة الرصد وتأكيد الأثر وحالة التكرار.")),
        ("Inspection Roadmap", l("30%는 현장 테스트 목표, 최대 60%는 데이터 축적 후 자동판정 시나리오입니다. Optical deviation은 screening이며 CMM 대체가 아닙니다.", "30% is a field-test target; up to 60% is a future automatic-judgment scenario after data accumulation. Optical deviation is screening, not a CMM replacement.", "نسبة 30% هدف اختبار ميداني، وحتى 60% سيناريو مستقبلي للحكم الآلي بعد تراكم البيانات. والانحراف البصري فحص أولي وليس بديلًا لـ CMM.")),
    ],
}


BEFORE_AFTER = {
    "ko": {
        "title": "사람이 연결하던 공장.|운영 문맥이 연결하는 공장.",
        "body": "새 시스템을 하나 더 얹는 이야기가 아닙니다. 사람이 반복해서 비교·정리·전달하던 간극을 같은 문맥으로 연결합니다.",
        "before": "사람이 시스템 사이를 연결한다",
        "before_items": ["NC와 도면을 사람이 비교", "불량자료를 사람이 다시 정리", "구매 요청을 사람이 품번으로 변환", "자재 요청을 전화·메신저로 전달", "결과를 다시 Excel에 기록"],
        "after": "운영 문맥이 시스템 사이를 연결한다",
    },
    "en": {
        "title": "People bridge the systems today.|Operating context carries the handoff next.",
        "body": "This is not another system layered on top. It connects the comparisons, re-entry, and handoffs people repeatedly perform between existing tools.",
        "before": "People connect the systems",
        "before_items": ["Compare NC with drawings by hand", "Reformat defect data", "Translate requests into item codes", "Relay material calls by phone or chat", "Record the result again in Excel"],
        "after": "Operating context connects the systems",
    },
    "ar": {
        "title": "يربط الأشخاص الأنظمة اليوم.|وغدًا يحمل سياق التشغيل عملية التسليم.",
        "body": "ليست طبقة نظام إضافية، بل ربط للمقارنات وإعادة الإدخال وعمليات التسليم التي ينفذها الأشخاص بين الأدوات القائمة.",
        "before": "الأشخاص يربطون الأنظمة",
        "before_items": ["مقارنة NC بالرسومات يدويًا", "إعادة تنظيم بيانات العيوب", "تحويل الطلب إلى رمز الصنف", "نقل طلب المواد بالهاتف أو المحادثة", "تسجيل النتيجة مرة أخرى في Excel"],
        "after": "سياق التشغيل يربط الأنظمة",
    },
    "flow": ["Signal", "Context", "Decision", "Action", "Confirmation"],
}


OUTCOMES = {
    "ko": {
        "title": "기술 이름보다 먼저.|운영 결과를 보여줍니다.",
        "body": "Flowmatic 적용 전후에 현장 담당자가 다루는 업무 단위가 어떻게 바뀌는지 비교합니다.",
        "labels": ("영역", "이전", "이후"),
        "rows": [
            ("Quality", "불량 목록", "손실순 개선업무"),
            ("Machining", "NC·도면·측정자료", "하나의 가공 Recipe"),
            ("Operations", "Excel·메일·수기정리", "자원사용·비용·이상징후"),
            ("Logistics", "전화·메신저 호출", "요청·배정·투입 확인"),
        ],
    },
    "en": {
        "title": "Lead with the operating result.|Then explain the architecture.",
        "body": "See how the unit of work changes for the people running the factory.",
        "labels": ("Domain", "Before", "After"),
        "rows": [
            ("Quality", "Defect list", "Improvement work ranked by loss"),
            ("Machining", "NC, drawings, measurement files", "One machining Recipe"),
            ("Operations", "Excel, email, manual cleanup", "Resource use, cost, anomaly signals"),
            ("Logistics", "Phone and chat calls", "Request, assignment, input confirmation"),
        ],
    },
    "ar": {
        "title": "ابدأ بنتيجة التشغيل.|ثم اشرح البنية.",
        "body": "قارن كيف تتغير وحدة العمل لدى من يديرون المصنع.",
        "labels": ("المجال", "قبل", "بعد"),
        "rows": [
            ("Quality", "قائمة عيوب", "أعمال تحسين مرتبة حسب الخسارة"),
            ("Machining", "NC ورسومات وملفات قياس", "Recipe تشغيل واحدة"),
            ("Operations", "Excel وبريد وتنظيم يدوي", "استخدام الموارد والتكلفة وإشارات الشذوذ"),
            ("Logistics", "طلبات هاتف ومحادثة", "طلب وتعيين وتأكيد إدخال"),
        ],
    },
}


MACHINING_VNEXT = {
    "label": "Machining Intelligence",
    "title": l(
        "Machining Intelligence | Manufacturing Recipe와 관리형 NC",
        "Machining Intelligence | Manufacturing Recipe and Controlled NC",
        "Machining Intelligence | Manufacturing Recipe وNC مُدار",
    ),
    "description": l(
        "기존 NC를 이해하고 공정 Recipe를 구성하며 관리형 G-code·측정·작업표준을 같은 제조 문맥으로 연결합니다.",
        "Manufacturing intelligence for understanding existing NC, building process recipes, generating controlled G-code, and connecting measurement and work standards.",
        "ذكاء تصنيع لفهم NC القائم وبناء وصفات العملية وتوليد G-code مضبوط وربط القياس ومعايير العمل.",
    ),
    "hero": l(
        "가공 데이터를 보는 프로그램이 아닙니다.|하나의 Manufacturing Recipe로 연결합니다.",
        "More than a machining data viewer.|Connect the work as one Manufacturing Recipe.",
        "أكثر من عارض لبيانات التشغيل.|اربط العمل في Manufacturing Recipe واحدة.",
    ),
    "body": l(
        "제품·공정·Feature·NC·측정·보정을 하나의 Manufacturing Recipe로 연결합니다. 기존 G-code의 공정 문맥을 복원하고 새로운 NC에는 그 문맥을 다시 담습니다. 네트워크가 없는 현장에서도 같은 기준을 유지하도록 설계합니다.",
        "Connect product, process, feature, NC, measurement, and correction in one Manufacturing Recipe. Recover context from existing G-code, carry it into new NC, and keep the same operating baseline where no factory network is available.",
        "اربط المنتج والعملية والميزة وNC والقياس والتصحيح في Manufacturing Recipe واحدة. استعد سياق G-code القائم واحمله إلى NC الجديد مع الحفاظ على المعيار نفسه في المواقع غير المتصلة بالشبكة.",
    ),
    "status": l("Active development / PoC", "Active development / PoC", "تطوير نشط / نطاق PoC"),
    "flow": ["Understand", "Build Recipe", "Generate", "Measure", "Correct", "Standardize"],
    "asset": None,
    "hierarchy": ["Product / Item", "Line", "Process Group", "Operation", "Feature", "Machine Setup", "G-code / Measurement / Work Standard"],
    "setup_context": ["WCS", "INDEX", "Tool", "Fixture", "Reference Pin", "Pad / Setup Reference"],
    "sections": [
        ("01 — Understand Existing NC", l("Active development / PoC", "Active development / PoC", "تطوير نشط / نطاق PoC"), l("기존 NC에 별도 Flowmatic 정보가 없어도 Tool·WCS·INDEX·Cycle·좌표 이동·반복 형상과 CAD/Feature geometry를 분석해 공정과 Feature의 문맥 후보를 복원합니다. 결과는 INFERRED에서 시작해 사용자가 CONFIRMED로 전환합니다.", "Analyze tool changes, WCS, INDEX, cycles, coordinate motion, repeated geometry, and CAD features in unmanaged G-code. Results begin as INFERRED and become CONFIRMED only through user review.", "حلّل تغييرات الأدوات وWCS وINDEX والدورات وحركة الإحداثيات والهندسة المتكررة وميزات CAD في G-code غير المدار. تبدأ النتيجة INFERRED ولا تصبح CONFIRMED إلا بمراجعة المستخدم."), ["Legacy / unmanaged G-code", "probable Operation / Feature", "Code Block boundary", "Tool / WCS / INDEX context", "INFERRED → USER CONFIRMED"]),
        ("02 — Manufacturing Recipe", l("Source-level validated baseline", "Source-level validated baseline", "خط أساس متحقق على مستوى المصدر"), l("가공계획은 파일 목록이 아니라 제품·공정·Operation 단위의 Recipe로 저장됩니다. Path·Shared Hole·Machining Operation·Temporary G-code·Unit-process Code Block·Final Block Order·Final Assembled G-code를 같은 구조에서 관리합니다.", "Store the machining plan as a product, process-group, and operation Recipe—not a loose file list. Paths, shared holes, machining operations, temporary G-code, unit-process code blocks, final order, and final assembled G-code share one structure.", "احفظ خطة التشغيل كـRecipe للمنتج ومجموعة العملية وOperation، لا كقائمة ملفات منفصلة. تشترك المسارات والثقوب والعمليات وكتل G-code وترتيب التجميع وNC النهائي في بنية واحدة."), ["Product → Process Group → Operation", "Path / Shared Hole / Machining Operation", "Unit-process Code Block", "Final Block Order", "Final Assembled G-code"]),
        ("03 — Generate & Assemble", l("Source-level validated baseline", "Source-level validated baseline", "خط أساس متحقق على مستوى المصدر"), l("Feature에서 가공 단위를 만들고 여러 단위공정을 조립해 하나의 최종 NC 프로그램으로 구성합니다. 복잡한 freeform toolpath는 기존 전문 CAM의 영역으로 남깁니다.", "Create machining units from features and assemble multiple unit processes into one final NC program. Complex freeform toolpaths remain within specialist CAM.", "أنشئ وحدات تشغيل من الميزات واجمع عمليات متعددة في برنامج NC نهائي واحد. تبقى مسارات freeform المعقدة ضمن CAM المتخصص."), ["HOLE GROUP → Drill Block → Tap Block", "FACE A → Milling Block", "BORE B → Rough Block → Finish Block", "OP20 → FINAL NC"]),
        ("04 — Block Boundary Safety Contract", l("Source-level validated", "Source-level validated", "متحقق على مستوى المصدر"), l("단위공정을 단순히 이어 붙이지 않습니다. 좌표계·모달 상태·공구·사이클·안전 높이의 경계를 확인한 뒤 최종 NC를 조립합니다. fail-closed 원칙에 따라 UNKNOWN 또는 UNSAFE 상태는 조립을 중단하고 검토를 요구합니다.", "Code blocks are checked for machine-state continuity before final NC assembly. Under a fail-closed rule, UNKNOWN or UNSAFE state blocks assembly and requires review.", "تُفحص استمرارية حالة الماكينة بين كتل الكود قبل تجميع NC النهائي. وفق قاعدة fail-closed توقف حالة UNKNOWN أو UNSAFE التجميع وتتطلب المراجعة."), ["distance mode / plane / unit / WCS", "cutter and tool-length compensation", "cycle / spindle / coolant / tool state", "Safe-Z / INDEX / unsupported stateful code", "PASS → Assemble", "UNKNOWN / UNSAFE → Block assembly → Review required"]),
        ("05 — Measurement / Compensation", l("Active development / PoC", "Active development / PoC", "تطوير نشط / نطاق PoC"), l("측정 결과를 보고서로 끝내지 않고 해당 Feature와 공정의 보정 대상으로 다시 연결합니다. 현재 범위는 correction target과 operator guidance이며 machine-side autonomous correction을 완료 기능으로 표시하지 않습니다.", "Return measurement to the relevant feature and process as a correction target. The current scope is correction targets and operator guidance—not completed machine-side autonomous correction.", "أعد القياس إلى الميزة والعملية المعنية كهدف للتصحيح. النطاق الحالي هو أهداف التصحيح وإرشاد المشغّل، وليس تصحيحًا ذاتيًا مكتملًا على الماكينة."), ["Measurement → Coordinate Mapping", "ΔX / ΔY / ΔZ / Δθ", "Correction Solver", "Target Feature / NC / Setup", "future machine adapter"]),
        ("06 — Managed G-code Metadata", l("Active development / PoC", "Active development / PoC", "تطوير نشط / نطاق PoC"), l("새로 생성한 NC에는 품목·라인·공정 문맥을 Managed Metadata Comment Block으로 함께 기록해 다른 PC에서도 원래 가공 문맥을 복원하도록 설계합니다. 관리 영역은 재출력 시 Replace / Refresh하며 동일 블록을 누적하지 않습니다.", "Carry item, line, and process context in a Managed Metadata Comment Block so another PC can recover the original machining context. Managed content is replaced or refreshed on export rather than appended repeatedly.", "احمل سياق الصنف والخط والعملية في Managed Metadata Comment Block ليستعيده حاسوب آخر. يتم استبدال أو تحديث المنطقة المدارة عند التصدير بدل تراكمها."), ["Required: Item / Product, Line, Process", "Optional: Operation, Feature, Code Block, Recipe revision", "Preserve user comments", "Distinguish managed comments", "Replace / Refresh; keep one metadata block"]),
        ("07 — Air-gapped / USB Operation", l("Active development / PoC", "Active development / PoC", "تطوير نشط / نطاق PoC"), l("중앙 서버나 NAS 연결이 불가능한 현장에서도 로컬 PC가 독립적으로 동작하도록 설계합니다. USB는 파일 복사가 아니라 버전·출처·무결성을 확인하는 승인된 전달 경계입니다. Local execution remains available without cloud connectivity.", "Local execution remains available where a central server or NAS cannot be connected. USB is treated as an approved transfer boundary that verifies version, source, and integrity—not as blind file copy.", "يبقى التنفيذ المحلي متاحًا حيث لا يمكن ربط خادم مركزي أو NAS. ويُعامل USB كحد نقل معتمد يتحقق من الإصدار والمصدر والسلامة، لا كنسخ أعمى للملفات."), ["version / revision / hash / manifest", "signed or approved package / source identity", "same → no update", "newer → safe update", "divergent → conflict review", "applied revision / rollback history"]),
        ("Machine Connectivity", l("Modular adapter direction", "Modular adapter direction", "اتجاه محول معياري"), l("설비 직결은 시작 조건이 아닙니다. 로컬 데이터와 추정 상태로 시작하고 필요한 설비에는 이후 전용 Adapter를 추가합니다.", "Direct machine connection is not a starting requirement. Begin with local data and estimated state, then add a dedicated adapter where needed.", "الاتصال المباشر بالماكينة ليس شرط البداية. ابدأ بالبيانات المحلية والحالة المقدرة ثم أضف محولًا مخصصًا عند الحاجة."), ["Base: Central / Local Estimated State", "Optional future adapter", "Verified Machine State", "FOCAS / OPC UA / MTConnect / FTP-DNC / RS-232-custom examples only"]),
        ("Work Standard from the Recipe", l("Prototype", "Prototype", "نموذج أولي"), l("같은 Manufacturing Recipe에서 공구·INDEX·Feature·가공순서와 검토점을 현장 작업표준으로 전환합니다.", "Turn tool, INDEX, feature, machining order, and review points from the same Manufacturing Recipe into the field work standard.", "حوّل الأداة وINDEX والميزة وترتيب التشغيل ونقاط المراجعة من Manufacturing Recipe نفسها إلى معيار عمل ميداني."), ["Recipe → NC", "Recipe → Measurement Context", "Recipe → Work Standard"]),
    ],
    "guardrail": l("전문 CAM 전체를 대체하지 않습니다. Safety Contract는 source-level deterministic check이며 실제 CNC 안전 인증이 아닙니다. G-code 추론·관리형 메타데이터·USB 동기화·CMM 연동·설비측 자동보정은 개발 및 PoC 범위입니다.", "This does not replace specialist CAM. The Safety Contract is a deterministic source-level check, not CNC safety certification. G-code inference, managed metadata, USB synchronization, CMM integration, and machine-side autonomous correction remain development and PoC scope.", "لا يستبدل CAM المتخصص. عقد السلامة فحص حتمي على مستوى المصدر وليس اعتماد سلامة CNC. يبقى استدلال G-code والبيانات الوصفية والمزامنة عبر USB وتكامل CMM والتصحيح على الماكينة ضمن التطوير وPoC."),
}

PAGES["machining-intelligence"] = MACHINING_VNEXT

QUALITY_CURRENT.update({
    "title": l("불량 데이터에서|개선업무와 재발 확인까지", "From defect data|to improvement work and recurrence checks", "من بيانات العيوب|إلى عمل التحسين وفحص التكرار"),
    "body": l("불량 데이터를 실제 손실과 개선업무로 연결합니다. 품번·원인별 손실을 기준으로 우선순위를 정하고 분석 결과에서 업무로 이동한 뒤 효과와 재발을 다시 확인합니다. Inspection은 증거를 제공하는 입력 계층입니다.", "Connect defect data to actual loss and improvement work. Rank priorities by item and cause, move from analysis into owned work, then verify effect and recurrence. Inspection is the evidence and input layer.", "اربط بيانات العيوب بالخسارة الفعلية وعمل التحسين. رتّب الأولوية حسب الصنف والسبب، وانقل التحليل إلى عمل مسؤول، ثم تحقق من الأثر والتكرار. Inspection هي طبقة الأدلة والإدخال."),
    "flow": ["Defect", "Loss", "Priority", "Work", "Verify", "Recurrence"],
})

COMPONENT_CONTEXT = {
    "nc": ("machining-intelligence", l("Machining Intelligence component · NC Browser Demo = public local theoretical-time analysis · Desktop Engineering = separate functional prototype", "Machining Intelligence component · NC Browser Demo = public local theoretical-time analysis · Desktop Engineering = separate functional prototype", "مكوّن Machining Intelligence · عرض المتصفح تحليل زمني نظري محلي · الهندسة المكتبية نموذج وظيفي منفصل")),
    "ct": ("machining-intelligence", l("Machining Intelligence component · Model-free camera cycle intelligence · ROI/CSRT is one public implementation path", "Machining Intelligence component · Model-free camera cycle intelligence · ROI/CSRT is one public implementation path", "مكوّن Machining Intelligence · ذكاء دورة بالكاميرا دون نموذج · ROI/CSRT مسار تنفيذ عام واحد")),
    "work-standard": ("machining-intelligence", l("Machining Intelligence component · Symbolic prototype", "Machining Intelligence component · Symbolic prototype", "مكوّن Machining Intelligence · نموذج رمزي")),
    "tms": ("machining-intelligence", l("Machining Intelligence component · Tool engineering context; purchasing and consumption belong to Operations Tool Economics", "Machining Intelligence component · Tool engineering context; purchasing and consumption belong to Operations Tool Economics", "مكوّن Machining Intelligence · سياق هندسة الأداة؛ الشراء والاستهلاك ضمن Operations Tool Economics")),
    "amr": ("logistics-intelligence", l("Logistics Intelligence component · AMR is an actor, not the product · real safety integration pending field validation", "Logistics Intelligence component · AMR is an actor, not the product · real safety integration pending field validation", "مكوّن Logistics Intelligence · AMR منفذ وليس المنتج · تكامل السلامة ينتظر التحقق الميداني")),
    "quality": ("quality", l("Quality Intelligence · Dashboard + Intelligence working prototype · Inspection integration in progress", "Quality Intelligence · Dashboard + Intelligence working prototype · Inspection integration in progress", "Quality Intelligence · نموذج Dashboard وIntelligence عامل · تكامل Inspection قيد التنفيذ")),
}
