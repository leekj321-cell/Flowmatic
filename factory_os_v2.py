"""Public-safe multilingual content for the Factory OS v2 information architecture."""


def l(ko, en, ar):
    return {"ko": ko, "en": en, "ar": ar}


ASSET_PATH = "/assets/factory-os"

HOME_OVERRIDES = {
    "ko": {
        "title": "Flowmatic | Factory Operating Intelligence",
        "description": "Flowmatic은 품질·가공·운영·물류 지능을 공통 제조 문맥과 Event Core로 연결하는 Factory Operating Intelligence 아키텍처입니다.",
        "body": "현장의 움직임과 데이터를 Event로 바꾸고, 품질·가공·운영원가·물류의 전문 지능을 사람과 기계의 다음 행동으로 연결합니다.",
        "products_title": "네 개의 전문 지능.|하나의 공장 운영 언어.",
        "products_body": "각 도메인은 독립적으로 시작할 수 있지만, 같은 Manufacturing Context와 Event 언어를 사용하도록 설계합니다.",
        "workflow_title": "구축된 증거와|다음 통합을 구분합니다.",
        "workflow_body": "실제 데모와 작동 프로토타입은 그대로 확인하고, Event Core와 Control Tower는 다음 통합 단계로 명확히 표시합니다.",
    },
    "en": {
        "title": "Flowmatic | Factory Operating Intelligence",
        "description": "Flowmatic connects quality, machining, operations, and logistics intelligence through shared manufacturing context and an Event Core architecture.",
        "body": "Turn field motion and data into events, then connect quality, machining, operations, and logistics intelligence to the next action for people and machines.",
        "products_title": "Four specialized intelligence domains.|One factory operating language.",
        "products_body": "Each domain can start independently while using the same Manufacturing Context and Event language by design.",
        "workflow_title": "Separate built evidence|from the next integration.",
        "workflow_body": "Inspect real demos and working prototypes while Event Core and Control Tower remain clearly labeled as the next integration stages.",
    },
    "ar": {
        "title": "Flowmatic | ذكاء تشغيل المصنع",
        "description": "يربط Flowmatic ذكاء الجودة والتشغيل والعمليات واللوجستيات بسياق تصنيع مشترك وبنية Event Core.",
        "body": "نحوّل حركة الميدان وبياناته إلى أحداث، ثم نربط ذكاء الجودة والتشغيل والعمليات واللوجستيات بالإجراء التالي للإنسان والآلة.",
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
        "flow": "Inspect → Prioritize → Act → Verify",
        "body": l(
            "검사 증거와 LOT를 손실·우선순위·업무·효과확인·재발로 연결합니다.",
            "Connect inspection evidence and LOT context to loss, priority, work, effect verification, and recurrence.",
            "يربط أدلة الفحص وسياق LOT بالخسارة والأولوية والعمل والتحقق من الأثر والتكرار.",
        ),
        "components": ["Quality Inspection", "Quality Dashboard", "Priority / Worklist / Recurrence / Effect"],
    },
    {
        "slug": "machining-intelligence",
        "name": "Machining Intelligence",
        "status": l("Integration in progress", "Integration in progress", "التكامل قيد التنفيذ"),
        "flow": "Understand → Observe → Optimize → Standardize",
        "body": l(
            "NC·CT·보정·작업표준·공구정보를 하나의 가공 문맥으로 묶습니다.",
            "Unify NC, CT, compensation, work standards, and tool information in one machining context.",
            "يوحّد NC وCT والتعويض ومعايير العمل ومعلومات الأدوات في سياق تشغيل واحد.",
        ),
        "components": ["NC", "CT", "Compensator", "Work Standard", "TMS Engineering Context"],
    },
    {
        "slug": "operations-intelligence",
        "name": "Operations Intelligence",
        "status": l("Functional MVP / internal validation", "Functional MVP / internal validation", "MVP وظيفي / تحقق داخلي"),
        "flow": "Intake → Allocate → Track → Normalize → Detect",
        "body": l(
            "구매·소모품·공구비·공수를 생산량 문맥에서 추적하고 이상 후보를 드러냅니다.",
            "Track purchasing, consumables, tool economics, and labor in production context and surface anomaly candidates.",
            "يتتبع المشتريات والمواد المستهلكة واقتصاديات الأدوات والعمل ضمن سياق الإنتاج ويكشف مؤشرات الشذوذ.",
        ),
        "components": ["Procurement", "Consumables", "Tool Economics", "Labor", "Tracked Operational Cost", "Anomaly"],
    },
    {
        "slug": "logistics-intelligence",
        "name": "Logistics Intelligence",
        "status": l("Prototype integration", "Prototype integration", "تكامل نموذجي أولي"),
        "flow": "Demand → Prioritize → Dispatch → Confirm",
        "body": l(
            "자재 요구를 작업으로 바꾸고 사람·지게차·AMR에 배정한 뒤 실제 투입까지 확인합니다.",
            "Turn material demand into work, assign it to people, forklifts, or AMRs, and confirm actual input.",
            "يحوّل طلب المواد إلى عمل، ويوزعه على الأشخاص أو الرافعات أو AMR، ثم يؤكد الإدخال الفعلي.",
        ),
        "components": ["Operator", "Fleet / Dispatch", "AMR / Forklift / Worker", "Last-meter confirmation"],
    },
]

CERTIFIED_CORE = {
    "title": l(
        "인증된 핵심은 남기고,|사람이 메우던 간극을 자동화합니다.",
        "Keep the certified core.|Automate the manual gap.",
        "نُبقي النواة المعتمدة.|ونؤتمت الفجوة اليدوية.",
    ),
    "body": l(
        "Flowmatic은 안전제어·전문 CAM·정밀측정·기준정보 시스템을 억지로 대체하지 않습니다. 그 사이의 관찰·문맥·우선순위·업무·증빙·확인을 연결합니다.",
        "Flowmatic does not force-replace safety control, specialist CAM, precision metrology, or systems of record. It connects observation, context, priority, workflow, evidence, and confirmation between them.",
        "لا يستبدل Flowmatic قسرًا التحكم الآمن أو CAM المتخصص أو القياس الدقيق أو أنظمة السجل. بل يربط الرصد والسياق والأولوية وسير العمل والدليل والتأكيد بينها.",
    ),
    "cards": [
        ("PLC / Safety", l("비상정지·인터록·인증 안전제어는 기존 계층에 남깁니다.", "Keep E-stop, interlocks, and certified safety control in the existing layer.", "تبقى أنظمة الإيقاف الطارئ والتشابك والتحكم الآمن المعتمد في طبقتها الحالية.")),
        ("CAM", l("복잡한 Toolpath 생성은 전문 CAM에 남기고, 현장 review workflow를 연결합니다.", "Keep complex toolpath generation in specialist CAM and connect the field review workflow.", "يبقى توليد مسار الأداة المعقد في CAM المتخصص، مع ربط سير مراجعة الميدان.")),
        ("Precision Metrology", l("µm급 판정은 전용 측정기에 남기고 Vision은 screening과 triage를 보조합니다.", "Keep micron-level acceptance in dedicated metrology; Vision supports screening and triage.", "يبقى حكم القبول بمستوى الميكرون لأجهزة القياس المخصصة، وتدعم الرؤية الفحص والفرز.")),
        ("ERP / MES / WMS", l("System of Record는 유지하고 필요한 Adapter와 Event layer로 연결합니다.", "Keep the system of record and connect only the adapters and Event layer required.", "نُبقي نظام السجل ونربط فقط المحولات وطبقة الأحداث المطلوبة.")),
    ],
}

PLATFORM = {
    "title": l(
        "도메인은 달라도,|공장을 가리키는 ID와 Event는 하나여야 합니다.",
        "Different domains.|One identity and Event language for the factory.",
        "تختلف المجالات.|لكن هوية المصنع ولغة الأحداث واحدة.",
    ),
    "body": l(
        "네 지능축은 Shared Manufacturing Context를 먼저 맞추고 Event Core로 연결됩니다. Control Tower는 이 토대 위의 계획된 통합 감독 계층입니다.",
        "The four domains first align on Shared Manufacturing Context, then connect through Event Core. Control Tower is the planned integrated supervision layer above that foundation.",
        "تتوافق المجالات الأربعة أولًا على سياق تصنيع مشترك، ثم تتصل عبر Event Core. أما Control Tower فهي طبقة إشراف متكاملة مخطط لها فوق هذا الأساس.",
    ),
    "entities": ["Factory", "Area", "Line", "Group", "Equipment", "Product", "LOT", "Tool", "Worker", "Task", "Material", "Time"],
    "layers": [
        ("Shared Manufacturing Context", l("Integration foundation", "Integration foundation", "أساس التكامل"), l("공장·설비·제품·LOT·공구·작업·자재·시간의 안정된 ID와 매핑입니다.", "Stable identity and mapping for factory, equipment, product, LOT, tool, work, material, and time.", "هوية وربط مستقر للمصنع والمعدات والمنتج وLOT والأداة والعمل والمواد والوقت.")),
        ("Event Core", l("Next integration layer", "Next integration layer", "طبقة التكامل التالية"), l("도메인 신호를 공통 Event·State·Context·Linkage로 정규화하는 다음 계층입니다.", "The next layer that normalizes domain signals into common Event, State, Context, and Linkage.", "الطبقة التالية التي توحّد إشارات المجالات إلى Event وState وContext وLinkage مشتركة.")),
        ("Manufacturing Control Shell", l("Prototype", "Prototype", "نموذج أولي"), l("공통 Factory·Group·Period 문맥과 모듈 실행·집계를 제공하는 현재 상위 Shell입니다.", "The current upper shell for shared Factory, Group, and Period context plus module launch and aggregation.", "الغلاف العلوي الحالي لسياق Factory وGroup وPeriod المشترك وتشغيل الوحدات وتجميعها.")),
        ("Cross-domain Control Tower", l("Planned integrated supervision", "Planned integrated supervision", "إشراف متكامل مخطط"), l("손실·위험·우선순위·다음 행동을 도메인 간에 종합하는 계획 단계입니다.", "The planned layer for cross-domain loss, risk, priority, and next-action supervision.", "الطبقة المخطط لها للإشراف عبر المجالات على الخسارة والمخاطر والأولوية والإجراء التالي.")),
    ],
}

EVIDENCE = [
    ("NC", l("Public demo", "Public demo", "عرض عام"), l("브라우저 로컬 이론시간 분석과 별도의 데스크톱 engineering prototype.", "Local browser theoretical-time analysis plus a separate desktop engineering prototype.", "تحليل زمني نظري محلي في المتصفح مع نموذج هندسي مكتبي منفصل."), "nc"),
    ("CT", l("Functional prototype", "Functional prototype", "نموذج وظيفي"), l("Model-free camera cycle intelligence. 현장 검증은 진행 중입니다.", "Model-free camera cycle intelligence; field validation remains ongoing.", "ذكاء دورة بالكاميرا دون نموذج مدرّب، والتحقق الميداني مستمر."), "ct"),
    ("Quality", l("Working prototype", "Working prototype", "نموذج عامل"), l("검사 증거에서 우선순위·업무·효과확인·재발까지 연결합니다.", "Connect evidence to priority, work, effect verification, and recurrence.", "يربط الأدلة بالأولوية والعمل والتحقق من الأثر والتكرار."), "quality"),
    ("Operations", l("Functional MVP / internal validation", "Functional MVP / internal validation", "MVP وظيفي / تحقق داخلي"), l("구매·소모·공수·Tracked Operational Cost와 이상 후보를 연결합니다.", "Connect purchasing, consumption, labor, Tracked Operational Cost, and anomaly candidates.", "يربط المشتريات والاستهلاك والعمل وTracked Operational Cost ومؤشرات الشذوذ."), "operations-intelligence"),
]

DEPLOYMENT_MODES = [
    ("Brownfield — Factory → Model", l("현재 공장의 움직임·문서·NC·작업방식을 읽고 운영모델을 복원합니다.", "Read the existing factory's motion, documents, NC, and work methods to reconstruct an operating model.", "نقرأ حركة المصنع القائم ووثائقه وNC وأساليب العمل لإعادة بناء نموذج التشغيل."), l("Field-first deployment", "Field-first deployment", "نشر يبدأ من الميدان")),
    ("Greenfield — Model → Factory", l("안정화 전부터 Process·Quality·Material·Work·Control Event model을 설계하는 미래 확장 아키텍처입니다.", "A future-expansion architecture that designs Process, Quality, Material, Work, and Control Event models before stabilization.", "بنية توسع مستقبلية تصمم نماذج أحداث العملية والجودة والمواد والعمل والتحكم قبل الاستقرار."), l("Deployment architecture / future expansion", "Deployment architecture / future expansion", "بنية نشر / توسع مستقبلي")),
]

ROADMAP = [
    ("01", "Specialized Intelligence", l("Quality / NC / CT / Operations / Operator / Fleet 프로토타입을 각 도메인에서 검증합니다.", "Validate Quality, NC, CT, Operations, Operator, and Fleet prototypes within each domain.", "التحقق من نماذج Quality وNC وCT وOperations وOperator وFleet داخل كل مجال.")),
    ("02", "Domain Integration", l("Machining·Operations·Logistics 지능의 내부 문맥과 workflow를 닫습니다.", "Close the internal context and workflows of Machining, Operations, and Logistics intelligence.", "استكمال السياق الداخلي وسير العمل لذكاء التشغيل والعمليات واللوجستيات.")),
    ("03", "Shared Context + Event Core", l("공통 ID·Event schema·도메인 간 linkage를 연결합니다.", "Connect common identity, Event schema, and cross-domain linkage.", "ربط الهوية المشتركة ومخطط الأحداث والعلاقات بين المجالات.")),
    ("04", "Control Tower", l("도메인 간 손실·위험·우선순위·다음 행동을 종합하는 통합 감독 단계입니다.", "Integrate cross-domain loss, risk, priority, and next-action supervision.", "دمج الإشراف عبر المجالات على الخسارة والمخاطر والأولوية والإجراء التالي.")),
    ("05", "Deployment Templates", l("Brownfield Factory→Model과 Greenfield Model→Factory 미래 확장 템플릿을 정리합니다.", "Define Brownfield Factory→Model and future Greenfield Model→Factory deployment templates.", "تعريف قوالب Brownfield من Factory إلى Model وقوالب Greenfield المستقبلية من Model إلى Factory.")),
]

PAGES = {
    "machining-intelligence": {
        "label": "Machining Intelligence",
        "title": l("Flowmatic Machining Intelligence | NC · CT · Compensation · Tool Context", "Flowmatic Machining Intelligence | NC · CT · Compensation · Tool Context", "Flowmatic Machining Intelligence | سياق NC وCT والتعويض والأداة"),
        "description": l("NC·CT·보정·작업표준·공구정보를 하나의 가공 문맥으로 연결합니다.", "Connect NC, CT, compensation, work standards, and tool information in one machining context.", "يربط NC وCT والتعويض ومعايير العمل ومعلومات الأدوات في سياق تشغيل واحد."),
        "hero": l("가공 프로그램을 읽고, 실제 움직임을 보고,|다음 개선을 연결합니다.", "Read the program. Observe actual motion.|Connect the next improvement.", "اقرأ البرنامج وراقب الحركة الفعلية.|واربط التحسين التالي."),
        "body": l("NC·CT·보정·작업표준·공구정보를 하나의 가공 문맥으로 묶습니다.", "Unify NC, CT, compensation, work standards, and tool information in one machining context.", "نوحّد NC وCT والتعويض ومعايير العمل ومعلومات الأدوات في سياق تشغيل واحد."),
        "status": l("Integration in progress", "Integration in progress", "التكامل قيد التنفيذ"),
        "flow": ["Understand", "Observe", "Diagnose", "Correct", "Standardize", "Verify"],
        "asset": None,
        "sections": [
            ("NC — Intended Process Context", l("Functional prototype", "Functional prototype", "نموذج وظيفي"), l("Posted NC/G-code의 공구·index·cycle 문맥과 이론 CT를 읽고 검토 workflow를 만듭니다.", "Read tool, index, cycle, and theoretical-CT context from posted NC/G-code and build a review workflow.", "قراءة سياق الأداة والفهرس والدورة والزمن النظري من NC/G-code المنشور وبناء سير مراجعة."), ["Posted NC / G-code parsing", "Controller/profile-specific index interpretation", "CT Optimize Advisor", "STEP/STL overlay and tool-envelope visual review", "PDF Smart Selection → XY-only draft G-code"]),
            ("CT — Actual Execution Context", l("Functional prototype / field validation ongoing", "Functional prototype / field validation ongoing", "نموذج وظيفي / تحقق ميداني مستمر"), l("학습된 객체모델 없이 고정 카메라 움직임을 deterministic cycle event로 바꿉니다. 공개 데모는 단순 ROI 경로를 보여주며 다른 관찰·replay 경로는 검증 중입니다.", "Convert fixed-camera motion into deterministic cycle events without a trained object model. The public demo shows a simpler ROI path while other observation and replay paths remain under validation.", "تحويل حركة الكاميرا الثابتة إلى أحداث دورة حتمية دون نموذج كائن مدرّب. يعرض العرض العام مسار ROI أبسط بينما تخضع مسارات الرصد والإعادة الأخرى للتحقق."), ["Model-free observation", "ROI / CSRT as one implementation path", "Autonomous and replay-assisted paths under validation"]),
            ("Compensator + Work Standard", l("Prototype framework / symbolic prototype", "Prototype framework / symbolic prototype", "إطار أولي / نموذج رمزي"), l("Feature·position·operation 문맥의 보정기록과 before/after NC preview를 작업자 표준으로 연결합니다. 전체 좌표변환 자동화는 아직 완료되지 않았습니다.", "Connect feature, position, and operation compensation records plus before/after NC previews to operator standards. Full coordinate-transform automation is not complete.", "ربط سجلات التعويض وسياق الموضع والعملية ومعاينة NC قبل/بعد بمعايير المشغّل. أتمتة تحويل الإحداثيات الكاملة غير مكتملة."), ["Compensation record", "Before / after NC preview", "Operator-facing symbolic work standard"]),
            ("TMS Engineering Context", l("Development preview", "Development preview", "معاينة تطوير"), l("어떤 공정에서 어떤 Tool을 왜 쓰는지, Tool life와 operation mapping을 관리합니다. 구매·단가·재고·소모율은 Operations Tool Economics 역할입니다.", "Manage why a tool is used in a process, its life, and operation mapping. Purchasing, price, stock, and consumption rate belong to Operations Tool Economics.", "إدارة سبب استخدام الأداة في العملية وعمرها وربطها بالعملية. أما الشراء والسعر والمخزون ومعدل الاستهلاك فتتبع Operations Tool Economics."), ["Tool identity and process mapping", "Tool life / machining usage", "Future linkage through the same tool_id"]),
        ],
        "guardrail": l("PDF 출력은 XY-only draft이며 machine-ready NC가 아닙니다. Tool envelope는 시각적 engineering review이며 certified collision 또는 stock-removal simulation이 아닙니다. Flowmatic은 full CAM replacement가 아닙니다.", "PDF output is an XY-only draft, not machine-ready NC. Tool envelope is visual engineering review, not certified collision or stock-removal simulation. Flowmatic is not a full CAM replacement.", "مخرجات PDF مسودة XY فقط وليست NC جاهزة للآلة. وغلاف الأداة مراجعة هندسية بصرية وليس محاكاة تصادم أو إزالة مخزون معتمدة. Flowmatic ليس بديلًا كاملًا لـ CAM."),
    },
    "operations-intelligence": {
        "label": "Operations Intelligence",
        "title": l("Flowmatic Operations Intelligence | Procurement · Consumption · Labor · Cost", "Flowmatic Operations Intelligence | Procurement · Consumption · Labor · Cost", "Flowmatic Operations Intelligence | المشتريات والاستهلاك والعمل والتكلفة"),
        "description": l("구매·소모품·공구비·공수를 실제 운영 문맥에 연결하고 생산량 기준 이상 후보를 드러냅니다.", "Connect purchasing, consumption, labor, and tool economics to operating context and surface production-normalized anomaly candidates.", "يربط المشتريات والاستهلاك والعمل واقتصاديات الأدوات بسياق التشغيل ويكشف مؤشرات الشذوذ المطبّعة بالإنتاج."),
        "hero": l("공구·소모품·공수·구매를|실제 생산 운영의 문맥으로 연결합니다.", "Connect purchasing, consumption, labor, and tool economics|to the real operating context.", "اربط المشتريات والاستهلاك والعمل|واقتصاديات الأدوات|بسياق التشغيل الفعلي."),
        "body": l("반복 입력을 줄이고, 생산량에 맞춰 자원소모를 정규화하고, 이상한 비용 상승을 먼저 드러냅니다.", "Reduce repetitive input, normalize resource use by production, and surface abnormal cost movement early.", "تقليل الإدخال المتكرر وتطبيع استهلاك الموارد حسب الإنتاج وإظهار حركة التكلفة غير الطبيعية مبكرًا."),
        "status": l("Functional MVP / internal validation", "Functional MVP / internal validation", "MVP وظيفي / تحقق داخلي"),
        "flow": ["Intake", "Resolve", "Allocate", "Track", "Normalize", "Detect"],
        "asset": f"{ASSET_PATH}/01_operations_intelligence.svg",
        "sections": [
            ("Procurement Intelligence", l("Functional MVP", "Functional MVP", "MVP وظيفي"), l("메일·채팅 자유문에서 품명·규격·수량·UOM·문맥을 추출하고 후보·confidence·reason을 제시한 뒤 사람이 확인한 항목만 기존 요청양식으로 내보냅니다.", "Extract item, specification, quantity, UOM, and context from free-text mail or chat; present candidates with confidence and reason; export confirmed items only to the existing request template.", "استخراج الصنف والمواصفة والكمية وUOM والسياق من البريد أو المحادثة، وعرض المرشحين مع الثقة والسبب، وتصدير العناصر المؤكدة فقط إلى القالب الحالي."), ["No silent 1EA default for missing quantity", "No auto-confirm on conflicting specifications", "No arbitrary conversion of unknown pack units", "Quantity / use-location split", "Confirmed-only template export"]),
            ("Resource Economics", l("Functional MVP", "Functional MVP", "MVP وظيفي"), l("Tool·Consumable·Labor event를 Tracked Operational Cost로 묶고 생산량과 가동시간으로 정규화합니다.", "Combine Tool, Consumable, and Labor events as Tracked Operational Cost and normalize them by production and running time.", "تجميع أحداث الأدوات والمواد المستهلكة والعمل في Tracked Operational Cost وتطبيعها حسب الإنتاج ووقت التشغيل."), ["Cost / Production EA", "Cost / Good EA", "Man-hour / 1,000 EA", "Consumption / 1,000 EA", "Consumption / running hour"]),
            ("Cost / Consumption Anomaly", l("MVP candidate detection", "MVP candidate detection", "اكتشاف مرشحين ضمن MVP"), l("Rolling Median + MAD와 EWMA로 이상 후보를 먼저 보여줍니다. 예측정비 원인판단을 완성했다고 주장하지 않습니다.", "Use Rolling Median + MAD and EWMA to surface anomaly candidates. This is not completed predictive-maintenance root-cause reasoning.", "استخدام Rolling Median + MAD وEWMA لإظهار مؤشرات الشذوذ. وهذا ليس استدلالًا مكتملًا لسبب الصيانة التنبؤية."), ["Rolling Median + MAD", "EWMA", "Production-normalized candidates", "Human review remains required"]),
            ("Manufacturing Control Shell", l("Prototype", "Prototype", "نموذج أولي"), l("Shared Factory·Group·Period context와 module launcher·aggregation을 가진 상위 Shell입니다. 완성된 Control Tower가 아닙니다.", "An upper shell with shared Factory, Group, and Period context plus module launch and aggregation. It is not a completed Control Tower.", "غلاف علوي بسياق Factory وGroup وPeriod مشترك وتشغيل وتجميع الوحدات. وليس Control Tower مكتملًا."), ["Real-time ERP/MES connectors pending", "Live inventory / budget / supplier / forecasting pending", "Maintenance correlation and full Quality adapter pending"]),
        ],
        "guardrail": l("Tracked Operational Cost는 현재 연결된 공구·소모품·공수 비용 이벤트의 추적값입니다. Material·Energy·Maintenance·Outsource 전체가 연결된 완전 제조원가 또는 회계원가가 아닙니다.", "Tracked Operational Cost covers the currently connected tool, consumable, and labor cost events. It is not full manufacturing or accounting cost across Material, Energy, Maintenance, and Outsource.", "يغطي Tracked Operational Cost أحداث تكلفة الأدوات والمواد المستهلكة والعمل المتصلة حاليًا، وليس تكلفة تصنيع أو محاسبة كاملة تشمل المواد والطاقة والصيانة والتعهيد."),
    },
    "logistics-intelligence": {
        "label": "Logistics Intelligence",
        "title": l("Flowmatic Logistics Intelligence | Demand to Dispatch to Confirmation", "Flowmatic Logistics Intelligence | Demand to Dispatch to Confirmation", "Flowmatic Logistics Intelligence | من الطلب إلى الإرسال والتأكيد"),
        "description": l("자재 요구를 우선순위·배정·이동·라스트미터 확인으로 연결합니다.", "Connect material demand to priority, assignment, dispatch, last-meter execution, and confirmation.", "يربط طلب المواد بالأولوية والتوزيع والإرسال والتنفيذ في آخر متر والتأكيد."),
        "hero": l("자재 요구를|실행 가능한 작업으로 바꿉니다.", "Turn material demand|into executable work.", "حوّل طلب المواد|إلى عمل قابل للتنفيذ."),
        "body": l("부족을 감지하고, 우선순위를 계산하고, 사람·지게차·AMR에 배정한 뒤 실제 투입까지 확인합니다.", "Detect shortages, calculate priority, assign people, forklifts, or AMRs, and confirm actual input.", "اكتشاف النقص وحساب الأولوية والتوزيع على الأشخاص أو الرافعات أو AMR ثم تأكيد الإدخال الفعلي."),
        "status": l("Prototype integration", "Prototype integration", "تكامل نموذجي أولي"),
        "flow": ["Demand", "Prioritize", "Assign", "Dispatch", "Last-meter", "Confirm"],
        "asset": None,
        "sections": [
            ("Operator", l("Functional prototype", "Functional prototype", "نموذج وظيفي"), l("사람과 작업 사이의 요청·확인·예외처리 interface입니다.", "The request, confirmation, and exception interface between people and work.", "واجهة الطلب والتأكيد ومعالجة الاستثناءات بين الأشخاص والعمل."), ["Demand event", "Task acceptance", "Exception / acknowledgement", "Completion evidence"]),
            ("Fleet / Dispatch", l("Simulation + prototype", "Simulation + prototype", "محاكاة + نموذج أولي"), l("Queue·actor state·priority·dispatch context를 관리합니다.", "Manage queue, actor state, priority, and dispatch context.", "إدارة قائمة الانتظار وحالة المنفذ والأولوية وسياق الإرسال."), ["Worker", "Forklift", "AMR", "Drone / mobile sensor", "Mobile Automation Cell"]),
            ("Last-meter Confirmation", l("Prototype integration", "Prototype integration", "تكامل نموذجي أولي"), l("도착·도킹·라인사이드 투입·빈 용기 회수까지 Event 상태를 닫습니다.", "Close the event through arrival, docking, line-side input, and empty-container return.", "إغلاق الحدث عبر الوصول والالتحام والإدخال بجانب الخط وإرجاع الحاوية الفارغة."), ["Arrival", "Docking", "Input confirmed", "Return / event closed"]),
            ("Mobile Automation Level 1–5", l("Long-term vision", "Long-term vision", "رؤية طويلة المدى"), l("AMR은 제품 전체가 아니라 실행 actor 중 하나입니다. 이동형 자동화 셀과 재구성 가능한 배정은 장기 비전이며 실제 안전연동은 현장검증 전입니다.", "AMR is one execution actor, not the whole product. Mobile automation cells and reconfigurable assignment are long-term vision; real safety integration remains pending field validation.", "AMR منفذ واحد وليس المنتج كله. خلايا الأتمتة المتنقلة والتوزيع القابل لإعادة التهيئة رؤية طويلة المدى، والتكامل الحقيقي للسلامة ينتظر التحقق الميداني."), ["Level 1 sensing", "Level 2 guided execution", "Level 3 mobile task actor", "Level 4 flexible line automation", "Level 5 reconfigurable factory automation"]),
        ],
        "guardrail": l("실제 AMR 안전연동과 생산 배치는 아직 현장검증 전입니다. PLC와 설비 controller가 내부 안전제어 책임을 유지합니다.", "Real AMR safety integration and production deployment remain pending field validation. PLCs and machine controllers retain responsibility for internal safety control.", "لا يزال تكامل سلامة AMR والنشر الإنتاجي بانتظار التحقق الميداني. وتبقى مسؤولية التحكم الآمن الداخلي لدى PLC ووحدات تحكم الآلات."),
    },
    "platform": {
        "label": "Flowmatic Platform / Factory OS",
        "title": l("Flowmatic Platform | Event Core & Control Tower Architecture", "Flowmatic Platform | Event Core & Control Tower Architecture", "Flowmatic Platform | بنية Event Core وControl Tower"),
        "description": l("네 전문 지능을 Shared Manufacturing Context, Event Core, 계획된 Control Tower로 연결하는 Factory OS 아키텍처입니다.", "The Factory OS architecture connecting four intelligence domains through Shared Manufacturing Context, Event Core, and a planned Control Tower.", "بنية Factory OS التي تربط أربعة مجالات ذكاء عبر سياق تصنيع مشترك وEvent Core وControl Tower مخطط لها."),
        "hero": l("네 개의 전문 지능.|하나의 공장 운영 언어.", "Four specialized intelligence domains.|One factory operating language.", "أربعة مجالات ذكاء متخصصة.|لغة تشغيل واحدة للمصنع."),
        "body": l("품질·가공·운영원가·물류의 판단을 하나의 Event Core로 연결하고, 공장 전체의 다음 행동을 조율하는 방향을 설명합니다.", "Explain how quality, machining, operations, and logistics intelligence converge on one Event Core and a future integrated supervision layer.", "شرح كيفية التقاء ذكاء الجودة والتشغيل والعمليات واللوجستيات في Event Core واحدة وطبقة إشراف متكاملة مستقبلية."),
        "status": l("Architecture / integration roadmap", "Architecture / integration roadmap", "بنية / خارطة تكامل"),
        "flow": ["Field Inputs", "Domain Intelligence", "Shared Context", "Event Core", "Control Tower", "Actors"],
        "asset": f"{ASSET_PATH}/00_factory_os_four_axes.svg",
        "sections": [
            ("Shared Manufacturing Context", l("Integration foundation", "Integration foundation", "أساس التكامل"), l("Event보다 먼저 Factory·Line·Equipment·Product·LOT·Tool·Worker·Task·Material·Time의 ID와 mapping을 맞춥니다.", "Before Event integration, align identity and mapping for Factory, Line, Equipment, Product, LOT, Tool, Worker, Task, Material, and Time.", "قبل تكامل الأحداث، تتم مواءمة هوية وربط Factory وLine وEquipment وProduct وLOT وTool وWorker وTask وMaterial وTime."), PLATFORM["entities"]),
            ("Event Core", l("Next integration layer", "Next integration layer", "طبقة التكامل التالية"), l("각 도메인의 Event·State·Context·Priority·Confidence·Linkage·History를 공통 언어로 정규화하는 다음 계층입니다.", "The next layer for normalizing each domain's Event, State, Context, Priority, Confidence, Linkage, and History.", "الطبقة التالية لتوحيد Event وState وContext وPriority وConfidence وLinkage وHistory لكل مجال."), ["Not a completed unified event bus", "Adapters and cross-domain links remain integration work"]),
            ("Control Shell vs Control Tower", l("Prototype vs planned", "Prototype vs planned", "نموذج أولي مقابل مخطط"), l("현재 Manufacturing Control Shell은 공통 문맥·launcher·aggregation prototype입니다. Cross-domain Control Tower는 손실·위험·우선순위·다음 행동을 종합할 계획된 감독 계층입니다.", "The current Manufacturing Control Shell is a shared-context, launcher, and aggregation prototype. Cross-domain Control Tower is the planned supervision layer for loss, risk, priority, and next action.", "Manufacturing Control Shell الحالي نموذج أولي للسياق المشترك والتشغيل والتجميع، بينما Control Tower عبر المجالات طبقة إشراف مخطط لها للخسارة والمخاطر والأولوية والإجراء التالي."), ["Shell — Prototype", "Control Tower — Planned integrated supervision"]),
            ("Synthetic Cross-domain Examples", l("Public-safe examples", "Public-safe examples", "أمثلة عامة آمنة"), l("실제 고객 데이터가 아닌 합성 예시로 도메인 연결방향을 설명합니다.", "Use synthetic—not customer—examples to explain cross-domain direction.", "استخدام أمثلة تركيبية وليست بيانات عملاء لشرح اتجاه الربط بين المجالات."), ["Quality P1 + tool-consumption spike + CT degradation → machining review", "Material-shortage risk + production-loss forecast → logistics escalation", "Repeated defect + unit-loss context → Quality worklist elevation"]),
            ("Brownfield / Greenfield", l("Current mode / future expansion", "Current mode / future expansion", "نمط حالي / توسع مستقبلي"), l("Brownfield Factory→Model은 현재 공장을 읽는 방식입니다. Greenfield Model→Factory는 안정화 전 Event model을 설계하는 미래 확장 아키텍처이며 구축완료 사례가 아닙니다.", "Brownfield Factory→Model reads the current factory. Greenfield Model→Factory is a future-expansion architecture for designing Event models before stabilization, not a completed reference deployment.", "Brownfield من Factory إلى Model يقرأ المصنع القائم. أما Greenfield من Model إلى Factory فهي بنية توسع مستقبلية لتصميم نماذج الأحداث قبل الاستقرار وليست حالة نشر مكتملة."), ["Brownfield — Field-first deployment", "Greenfield — Deployment architecture / future expansion"]),
        ],
        "guardrail": l("Factory OS 방향은 분명히 제시하지만 Event Core와 Control Tower 통합이 완료됐다고 주장하지 않습니다.", "The Factory OS direction is explicit, but Event Core and Control Tower integration are not presented as complete.", "اتجاه Factory OS واضح، لكن لا يُقدّم تكامل Event Core وControl Tower على أنه مكتمل."),
    },
}

QUALITY_V513 = {
    "title": l("불량을 찾는 것에서|끝내지 않습니다.", "Detection is only the start.", "الاكتشاف ليس سوى البداية."),
    "body": l("검사 결과를 손실, 우선순위, 개선업무, 효과확인과 재발까지 연결합니다.", "Turn quality evidence into loss context, priority, action, effect verification, and recurrence control.", "حوّل أدلة الجودة إلى سياق خسارة وأولوية وإجراء وتحقق من الأثر وضبط التكرار."),
    "flow": ["Capture", "Standardize", "Quantify", "Prioritize", "Act", "Verify"],
    "cards": [
        ("Evidence + Standardize", l("Multi-camera·LOT·checksum·timestamp 증거를 제품·그룹·원인·기간 문맥으로 표준화합니다.", "Standardize multi-camera, LOT, checksum, and timestamp evidence by product, group, cause, and period.", "توحيد أدلة الكاميرات وLOT وchecksum وtimestamp حسب المنتج والمجموعة والسبب والفترة.")),
        ("Quantify + Prioritize", l("PPM·불량수량·손실금액·기준단가 provenance를 분석기간별로 재계산하고 설명 가능한 P1–P3 순위를 만듭니다.", "Recalculate PPM, defect quantity, loss, and reference-price provenance by analysis range and create explainable P1–P3 ranking.", "إعادة حساب PPM وكمية العيوب والخسارة ومصدر السعر المرجعي حسب فترة التحليل وإنشاء ترتيب P1–P3 قابل للتفسير.")),
        ("Worklist + Verify", l("담당자·상태·다음 확인을 Worklist로 연결하고 관찰·효과확인·재발 상태를 이어갑니다.", "Connect owner, status, and next check in a worklist, then continue observation, effect confirmation, and recurrence state.", "ربط المالك والحالة والفحص التالي في قائمة عمل ثم متابعة الرصد وتأكيد الأثر وحالة التكرار.")),
        ("Inspection Roadmap", l("30%는 현장 테스트 목표, 최대 60%는 데이터 축적 후 자동판정 시나리오입니다. Optical deviation은 screening이며 CMM 대체가 아닙니다.", "30% is a field-test target; up to 60% is a future automatic-judgment scenario after data accumulation. Optical deviation is screening, not a CMM replacement.", "نسبة 30% هدف اختبار ميداني، وحتى 60% سيناريو مستقبلي للحكم الآلي بعد تراكم البيانات. والانحراف البصري فحص أولي وليس بديلًا لـ CMM.")),
    ],
}

COMPONENT_CONTEXT = {
    "nc": ("machining-intelligence", l("Machining Intelligence component · NC Browser Demo = public local theoretical-time analysis · Desktop Engineering = separate functional prototype", "Machining Intelligence component · NC Browser Demo = public local theoretical-time analysis · Desktop Engineering = separate functional prototype", "مكوّن Machining Intelligence · عرض المتصفح تحليل زمني نظري محلي · الهندسة المكتبية نموذج وظيفي منفصل")),
    "ct": ("machining-intelligence", l("Machining Intelligence component · Model-free camera cycle intelligence · ROI/CSRT is one public implementation path", "Machining Intelligence component · Model-free camera cycle intelligence · ROI/CSRT is one public implementation path", "مكوّن Machining Intelligence · ذكاء دورة بالكاميرا دون نموذج · ROI/CSRT مسار تنفيذ عام واحد")),
    "work-standard": ("machining-intelligence", l("Machining Intelligence component · Symbolic prototype", "Machining Intelligence component · Symbolic prototype", "مكوّن Machining Intelligence · نموذج رمزي")),
    "tms": ("machining-intelligence", l("Machining Intelligence component · Tool engineering context; purchasing and consumption belong to Operations Tool Economics", "Machining Intelligence component · Tool engineering context; purchasing and consumption belong to Operations Tool Economics", "مكوّن Machining Intelligence · سياق هندسة الأداة؛ الشراء والاستهلاك ضمن Operations Tool Economics")),
    "amr": ("logistics-intelligence", l("Logistics Intelligence component · AMR is an actor, not the product · real safety integration pending field validation", "Logistics Intelligence component · AMR is an actor, not the product · real safety integration pending field validation", "مكوّن Logistics Intelligence · AMR منفذ وليس المنتج · تكامل السلامة ينتظر التحقق الميداني")),
    "quality": ("quality", l("Quality Intelligence · Dashboard + Intelligence working prototype · Inspection integration in progress", "Quality Intelligence · Dashboard + Intelligence working prototype · Inspection integration in progress", "Quality Intelligence · نموذج Dashboard وIntelligence عامل · تكامل Inspection قيد التنفيذ")),
}
