"""Localized product film and genuine frame evidence for the latest approved demo."""
import json
from html import escape
from pathlib import Path

MEDIA = "/media/product-tour/"
MOVIE = "Flowmatic_V28_Quality_Restored_EN_20261126.mp4"
POSTER = "poster-v28.jpg"
TOUR_FILES = ["flowmatic-v28-process.jpg", "flowmatic-v28-fixture.jpg", "flowmatic-v28-scada.jpg", "flowmatic-v28-logistics.jpg"]
REQUIRED = (MOVIE, POSTER, "captions-en-v28-quality-20261126.vtt", "captions-ko-v28-quality-20261126.vtt", *TOUR_FILES)
DIRECTORY = Path(__file__).resolve().parents[1] / "media" / "product-tour"
FILM_ENABLED = DIRECTORY.joinpath("publish-approved").is_file()
if FILM_ENABLED and not all(DIRECTORY.joinpath(name).is_file() for name in REQUIRED):
    raise ValueError("Enabled product tour is missing an approved media file")
COPY = json.loads(r'''{
  "ko": {
    "title": "제품 데모: 부품에서 공장까지",
    "play": "Flowmatic 제품 데모",
    "time": "2분 35초 · 영어 화면 · 한·영 자막 · 배경음악",
    "hold": "제품 영상 준비 중",
    "stills": "제품 화면 보기",
    "contact": "도입 범위 논의하기",
    "transcript": "영상의 8개 장면",
    "note": "실제 제품 실행 화면과 시뮬레이션. 생산능력과 물류 비교는 영상에 제시된 모델 조건을 기준으로 합니다.",
    "fallback": "동영상 재생이 지원되지 않으면 아래 장면 설명과 제품 화면을 확인할 수 있습니다.",
    "reading": "최신 데모 영상에서 추출한 영문 제품 화면입니다.",
    "sequence": "공정·지그 준비, 운영 상태 확인, 조건 변경과 물류 비교를 하나의 데모에서 확인합니다. 카메라 상태 인식에는 렌더 영상을 입력하며, 생산능력·물류 수치는 시뮬레이션 결과입니다.",
    "hint": "장면을 선택하면 해당 구간부터 재생됩니다.",
    "chapters": [
      [
        "00:00",
        0,
        "생산목표와 공정 재배분",
        "같은 4개 셀·48대 CNC 조건에서 공정 재배분 전후의 모델 생산능력을 비교합니다."
      ],
      [
        "00:22",
        22,
        "공정설계·NC 검토",
        "소재·완성 형상, 공구 경로와 NC 프로그램을 함께 검토합니다."
      ],
      [
        "00:47",
        47,
        "지그 설계·BOM",
        "양쪽 면의 홀 클램프와 지지 구조를 확인하고 완성 지그를 회전해 살펴봅니다."
      ],
      [
        "01:06",
        66,
        "생산계획·공구 비용",
        "생산계획에 따라 달라지는 공구 수량과 비용을 확인합니다."
      ],
      [
        "01:14",
        74,
        "생산·물류·양산이관",
        "완성된 P06 지그에서 신규 작업장으로 이어진 뒤 공장 전체로 시야를 넓히며, 계속되는 생산·물류와 팔레트 반송 흐름을 확인합니다."
      ],
      [
        "01:39",
        98.966667,
        "SCADA·셀 동작 모니터링",
        "렌더 영상의 상태 인식과 셀 시뮬레이션을 같은 시점에서 비교합니다. 이 구간은 2배속입니다."
      ],
      [
        "02:08",
        127.966667,
        "형상 변경·측정 보정",
        "형상과 NC의 변경을 함께 검토하고 측정값에 따른 보정 제안을 확인합니다."
      ],
      [
        "02:21",
        141.466667,
        "공장 물류 개선 비교",
        "6개 작업장의 운반 경로를 비교하고 공정·반송 조건에 따른 모델 생산능력을 확인합니다."
      ]
    ]
  },
  "en": {
    "title": "Product demo: From part to factory",
    "play": "Flowmatic product demo",
    "time": "2 min 35 sec · English interface & captions · Instrumental music",
    "hold": "Product film in preparation",
    "stills": "Explore product screens",
    "contact": "Discuss a pilot",
    "transcript": "Eight chapters",
    "note": "Recorded product operation and simulations. Capacity and logistics comparisons use the model conditions shown in the film.",
    "fallback": "If video playback is unavailable, explore the chapter summaries and product screens below.",
    "reading": "English product screens captured from the latest demo film.",
    "sequence": "The demo follows process and fixture preparation, operating-state review, design changes and logistics comparison. Camera tracking uses rendered input; capacity and logistics figures are simulation results.",
    "hint": "Select a chapter to play that section.",
    "chapters": [
      [
        "00:00",
        0,
        "Production targets & process balancing",
        "Compare modeled capacity before and after process balancing across the same four cells and 48 CNC machines."
      ],
      [
        "00:22",
        22,
        "Process planning & NC review",
        "Review stock and finished geometry alongside toolpaths and NC programs."
      ],
      [
        "00:47",
        47,
        "Fixture design & BOM",
        "Inspect bore clamps on both faces and work supports, then rotate the completed fixture."
      ],
      [
        "01:06",
        66,
        "Production plans & tooling costs",
        "Review how tool quantities and costs change with the production plan."
      ],
      [
        "01:14",
        74,
        "Production, logistics & handover",
        "Follow the completed P06 fixture into the new workplace, then zoom out to the whole factory as production, logistics and pallet transport continue."
      ],
      [
        "01:39",
        98.966667,
        "SCADA & cell monitoring",
        "Compare state tracking from a rendered camera clip with the cell simulation on the same timeline. Shown at 2× playback."
      ],
      [
        "02:08",
        127.966667,
        "Design changes & correction review",
        "Review geometry and NC changes together, then inspect a correction proposed from a sample measurement."
      ],
      [
        "02:21",
        141.466667,
        "Factory logistics comparison",
        "Compare transport routes across six workplaces and review modeled capacity under revised process and handling conditions."
      ]
    ]
  },
  "ar": {
    "title": "عرض المنتج: من القطعة إلى المصنع",
    "play": "عرض منتج Flowmatic",
    "time": "دقيقتان و35 ثانية · واجهة وترجمة إنجليزية · موسيقى دون تعليق صوتي",
    "hold": "فيلم المنتج قيد الإعداد",
    "stills": "استعراض شاشات المنتج",
    "contact": "مناقشة تجربة تطبيقية",
    "transcript": "ثمانية فصول",
    "note": "تشغيل مسجل للمنتج ومحاكاة. تعتمد مقارنات الطاقة الإنتاجية واللوجستيات على شروط النموذج الموضحة في الفيلم.",
    "fallback": "عند تعذر تشغيل الفيديو، تتوفر أدناه ملخصات الفصول وشاشات المنتج.",
    "reading": "شاشات واجهة إنجليزية مأخوذة من أحدث فيلم للمنتج.",
    "sequence": "يتابع العرض إعداد العمليات وتجهيزات التثبيت، ومراجعة حالة التشغيل، وتغييرات التصميم ومقارنة اللوجستيات. يستخدم تتبع الكاميرا مقطعًا مرئيًا مُولّدًا، وتُحسب مؤشرات الطاقة الإنتاجية واللوجستيات بالمحاكاة.",
    "hint": "اختيار الفصل يبدأ التشغيل من المقطع المطلوب.",
    "chapters": [
      [
        "00:00",
        0,
        "أهداف الإنتاج وموازنة العمليات",
        "مقارنة الطاقة الإنتاجية المحسوبة قبل إعادة توزيع العمليات وبعدها ضمن أربع خلايا و48 ماكينة CNC نفسها."
      ],
      [
        "00:22",
        22,
        "تخطيط العمليات ومراجعة NC",
        "مراجعة هندسة المادة الخام والقطعة النهائية إلى جانب مسارات الأدوات وبرامج التحكم الرقمي."
      ],
      [
        "00:47",
        47,
        "تصميم تجهيزات التثبيت وقائمة المكونات",
        "مراجعة مشابك الثقوب على الوجهين ونقاط الإسناد، ثم تدوير التجهيز المكتمل لفحصه."
      ],
      [
        "01:06",
        66,
        "خطة الإنتاج وتكاليف الأدوات",
        "مراجعة تغير كميات الأدوات وتكاليفها مع خطة الإنتاج."
      ],
      [
        "01:14",
        74,
        "الإنتاج واللوجستيات والتسليم",
        "متابعة تجهيز تثبيت P06 المكتمل وصولًا إلى منطقة العمل الجديدة، ثم توسيع الرؤية إلى المصنع بالكامل مع استمرار الإنتاج واللوجستيات ونقل المنصات."
      ],
      [
        "01:39",
        98.966667,
        "SCADA ومراقبة الخلية",
        "مقارنة تتبع الحالة من مقطع كاميرا مُولّد بمحاكاة الخلية على الخط الزمني نفسه. يُعرض المقطع بضعف السرعة."
      ],
      [
        "02:08",
        127.966667,
        "تعديلات التصميم ومراجعة التعويض",
        "مراجعة تغييرات الهندسة وبرنامج NC معًا، ثم فحص تعويض مقترح استنادًا إلى قياس عينة."
      ],
      [
        "02:21",
        141.466667,
        "مقارنة لوجستيات المصنع",
        "مقارنة مسارات النقل في ست مناطق عمل والطاقة الإنتاجية المحسوبة وفق شروط العمليات والمناولة المعدلة."
      ]
    ]
  }
}''')
LIVE_SHOTS = json.loads(r'''{
  "ko": [
    [
      "공정·NC",
      "형상에서 공정과 가공 경로까지",
      "소재와 완성품의 형상을 바탕으로 공정을 나누고, 공구 이동과 NC 프로그램을 같은 화면에서 검토합니다.",
      "소재·완성품 형상 / 가공 조건",
      "공정별 형상, 공구 경로와 NC 프로그램",
      "선택한 가공면과 공정 조건을 지그·공구 준비에 사용합니다.",
      "제품 실행 화면",
      "형상·공구 경로·NC를 함께 검토하는 공정설계 화면",
      "지원 형상의 공정 검토 예시입니다. 실제 가공 적용에는 담당자의 검토가 필요합니다.",
      "영문 Flowmatic 공정설계 화면에 제품 형상, 공구 경로와 NC 프로그램이 함께 표시되어 있다."
    ],
    [
      "지그·생산 준비",
      "가공면에 맞춘 지그와 공구 준비",
      "양쪽 가공면의 홀 클램프와 지지 구조를 확인하고, 지그 구성과 부품 목록을 함께 검토합니다. 영상에서는 생산량에 따른 공구 수량과 비용까지 이어집니다.",
      "가공면 / 제품 형상 / 생산계획",
      "지그 조립 형상과 BOM / 공구 수량·비용 검토",
      "공정과 자원 조건을 생산·물류 계획 및 양산이관에 반영합니다.",
      "제품 실행 화면",
      "양쪽 면의 홀 클램프와 지그 조립 구조",
      "영상 01:00부터 지그를 회전해 보고 01:06부터 공구 비용을 확인할 수 있습니다.",
      "Flowmatic 지그설계 화면에 양쪽 면의 홀 클램프, 지지대와 지그 부품 목록이 표시되어 있다."
    ],
    [
      "운영 모니터링",
      "카메라 상태 인식과 셀 동작의 연결",
      "카메라 영상에서 인식한 상태를 셀 시뮬레이션과 나란히 확인합니다. 로봇의 P01·P02 이송과 소재 투입, 도어 닫힘을 같은 시간축에서 추적합니다.",
      "카메라 입력 / 셀 배치 / 공정 기준",
      "동작 상태와 작업장 운영 화면",
      "운영 상태와 측정값을 바탕으로 변경·보정 조건을 검토합니다.",
      "제품 실행 화면 · 렌더 영상 입력",
      "SCADA의 상태 인식과 셀 시뮬레이션 동기화",
      "카메라 입력에는 렌더 영상을 사용합니다. 실제 상태 추적 프로그램의 처리 결과를 표시합니다.",
      "SCADA 화면에 렌더 카메라 입력, 인식 상태와 자동화 셀 시뮬레이션이 나란히 표시되어 있다."
    ],
    [
      "변경·개선",
      "측정 보정과 공장 물류의 개선 검토",
      "형상 변경과 측정 기반 보정 제안을 검토한 뒤, 공장 전체의 배치 대안을 비교합니다. 6개 작업장의 운반 경로와 합산 이동거리를 함께 확인합니다.",
      "변경 형상·측정값 / 작업장 배치·운반 조건",
      "NC 보정 제안 / 물류 경로와 모델 생산능력 비교",
      "검토한 변경 조건을 다음 생산계획의 기준으로 사용합니다.",
      "제품 실행 화면 · 시뮬레이션",
      "6개 작업장의 운반 경로와 연간 이동거리 비교",
      "물류 거리는 6개 작업장 합산값입니다. 생산능력 비교는 같은 4개 셀·48대 CNC의 모델 조건을 사용합니다.",
      "여섯 작업장의 개선 전후 운반 경로와 연간 이동거리, 모델 생산능력을 비교한 Flowmatic 화면."
    ]
  ],
  "en": [
    [
      "Process & NC",
      "From geometry to process and toolpath",
      "Stock and finished-part geometry define the operations. Tool movement and NC programs are reviewed together on the same screen.",
      "Stock and finished geometry / Machining conditions",
      "Operation geometry, toolpaths and NC programs",
      "Selected machining faces and process conditions inform fixture and tooling preparation.",
      "Recorded product operation",
      "Process planning with geometry, toolpaths and NC in one view",
      "An example for supported geometry. Engineering review is required before machining use.",
      "English Flowmatic process-planning screen showing part geometry, toolpaths and NC programs."
    ],
    [
      "Fixtures & preparation",
      "Fixtures and tooling for the machining task",
      "Inspect bore clamps on both machining faces, work supports and the fixture bill of materials. The film then follows tool quantities and costs as production volume changes.",
      "Machining faces / Part geometry / Production plan",
      "Fixture assembly and BOM / Tool quantities and cost review",
      "Process and resource conditions inform production, logistics and handover.",
      "Recorded product operation",
      "Bore clamps on both faces and the fixture assembly",
      "The fixture rotates from 01:00; the tooling-cost review follows at 01:06.",
      "Flowmatic fixture-design screen showing bore clamps on both faces, work supports and a component list."
    ],
    [
      "Operations monitoring",
      "Camera state tracking alongside cell operation",
      "Review states detected from camera input alongside the cell simulation. The robot's P01–P02 transfer, stock loading and door closure share the same timeline.",
      "Camera input / Cell layout / Process criteria",
      "Tracked operating states and the workplace monitor",
      "Operating states and measurements support design-change and correction review.",
      "Product operation · Rendered camera input",
      "SCADA state tracking synchronized with the cell simulation",
      "The camera input is a rendered clip processed by the actual state-tracking software.",
      "SCADA screen showing rendered camera input, detected states and the automation-cell simulation side by side."
    ],
    [
      "Changes & improvement",
      "Measurement correction and factory logistics review",
      "Review geometry changes and measurement-based correction proposals, then compare factory layouts. Transport routes and total travel are shown across six workplaces.",
      "Geometry changes and measurements / Workplace layouts and transport conditions",
      "Proposed NC correction / Route and modeled-capacity comparisons",
      "Reviewed changes provide conditions for the next production plan.",
      "Product operation · Simulation",
      "Transport routes and annual travel across six workplaces",
      "Travel totals cover six workplaces. Capacity comparisons use the same four cells and 48 CNC machines in the model.",
      "Flowmatic comparison of transport routes, annual travel and modeled capacity before and after layout improvement."
    ]
  ],
  "ar": [
    [
      "العمليات وNC",
      "من الهندسة إلى العملية ومسار الأداة",
      "تحدد هندسة المادة الخام والقطعة النهائية عمليات التشغيل. وتُراجع حركة الأداة وبرامج التحكم الرقمي معًا على الشاشة نفسها.",
      "هندسة المادة الخام والقطعة النهائية / شروط التشغيل",
      "هندسة العمليات ومسارات الأدوات وبرامج NC",
      "تُستخدم أسطح التشغيل وشروط العملية المختارة لإعداد تجهيزات التثبيت والأدوات.",
      "تشغيل مسجل للمنتج",
      "تخطيط العمليات مع الهندسة ومسارات الأدوات وبرامج NC",
      "مثال للأشكال المدعومة. يلزم إجراء مراجعة هندسية قبل الاستخدام في التشغيل الفعلي.",
      "واجهة Flowmatic الإنجليزية لتخطيط العمليات تعرض هندسة القطعة ومسارات الأدوات وبرامج NC."
    ],
    [
      "التثبيت والتحضير",
      "تجهيزات التثبيت والأدوات وفق مهمة التشغيل",
      "تُراجع مشابك الثقوب على وجهي التشغيل ونقاط الإسناد وقائمة مكونات التجهيز. ثم يتابع الفيلم كميات الأدوات وتكاليفها مع تغير حجم الإنتاج.",
      "أسطح التشغيل / هندسة القطعة / خطة الإنتاج",
      "تجميع تجهيزات التثبيت وقائمة المكونات / كميات الأدوات وتكاليفها",
      "تدعم شروط العملية والموارد تخطيط الإنتاج واللوجستيات والتسليم.",
      "تشغيل مسجل للمنتج",
      "مشابك الثقوب على الوجهين وتجميع تجهيزات التثبيت",
      "يبدأ تدوير التجهيز عند 01:00، ثم مراجعة تكاليف الأدوات عند 01:06.",
      "شاشة تصميم تجهيزات التثبيت تعرض مشابك الثقوب على الوجهين ونقاط الإسناد وقائمة المكونات."
    ],
    [
      "مراقبة التشغيل",
      "تتبع حالة الكاميرا إلى جانب تشغيل الخلية",
      "تُراجع الحالات المكتشفة من مدخل الكاميرا إلى جانب محاكاة الخلية. وتُتابع حركة الروبوت بين P01 وP02 وتحميل المادة وإغلاق الباب على خط زمني واحد.",
      "مدخل الكاميرا / تخطيط الخلية / معايير العملية",
      "حالات التشغيل المتتبعة وشاشة منطقة العمل",
      "تدعم حالات التشغيل والقياسات مراجعة تغييرات التصميم والتعويض.",
      "تشغيل المنتج · مدخل كاميرا مُولّد",
      "تتبع حالة SCADA متزامنًا مع محاكاة الخلية",
      "مدخل الكاميرا مقطع مُولّد يعالجه برنامج تتبع الحالة الفعلي.",
      "شاشة SCADA تعرض مقطع الكاميرا المُولّد والحالات المكتشفة ومحاكاة خلية الأتمتة جنبًا إلى جنب."
    ],
    [
      "التغييرات والتحسين",
      "مراجعة التعويض واللوجستيات على مستوى المصنع",
      "تُراجع تغييرات الهندسة ومقترحات التعويض المبنية على القياس، ثم تُقارن تخطيطات المصنع. تُعرض مسارات النقل وإجمالي المسافة لست مناطق عمل.",
      "تغييرات الهندسة والقياسات / تخطيط مناطق العمل وشروط النقل",
      "تعويض NC مقترح / مقارنة المسارات والطاقة الإنتاجية المحسوبة",
      "توفر التغييرات المراجعة شروطًا لخطة الإنتاج التالية.",
      "تشغيل المنتج · محاكاة",
      "مسارات النقل والمسافة السنوية لست مناطق عمل",
      "تشمل مسافة النقل ست مناطق عمل. وتستخدم مقارنة الطاقة الإنتاجية أربع خلايا و48 ماكينة CNC نفسها ضمن النموذج.",
      "مقارنة Flowmatic لمسارات النقل والمسافة السنوية والطاقة الإنتاجية المحسوبة قبل تحسين التخطيط وبعده."
    ]
  ]
}''')

def render_product_tour(lang, old_image, old_image_alt, zoom):
    c = COPY[lang]
    e = lambda value: escape(str(value), quote=True)
    intro = f'<div class="visual-head"><strong id="product-demo-title">{e(c["title"])}</strong><bdi>{e(c["time"] if FILM_ENABLED else c["hold"])}</bdi></div>'
    if FILM_ENABLED:
        tracks = "".join(f'<track kind="subtitles" src="{MEDIA}captions-{code}-v28-quality-20261126.vtt" srclang="{code}" label="{label}"{(" default" if code == ("ko" if lang == "ko" else "en") else "")}>' for code, label in [("en","English"),("ko","한국어")])
        body = f'<video id="product-film" controls playsinline preload="metadata" width="1920" height="1200" poster="{MEDIA}{POSTER}" aria-label="{e(c["play"])}"><source src="{MEDIA}{MOVIE}" type="video/mp4">{tracks}<p>{e(c["fallback"])}</p></video>'
        chapters = "".join(f'<li><button type="button" class="tour-chapter" data-video-time="{seconds}" aria-controls="product-film"><bdi>{e(stamp)}</bdi><span>{e(label)}</span></button><p>{e(line)}</p></li>' for stamp, seconds, label, line in c["chapters"])
        transcript = f'<details class="tour-transcript"><summary>{e(c["transcript"])}</summary><p class="tour-chapter-hint">{e(c["hint"])}</p><ol>{chapters}</ol></details>'
    else:
        body = f'<button type="button" class="image-open tour-preview" data-open-shot="machining" aria-label="{e(zoom)}"><img src="{e(old_image)}" alt="{e(old_image_alt)}" width="2304" height="1294" decoding="async"></button>'
        transcript = ""
    links = f'<div class="tour-links"><a class="tour-stills" href="#product">{e(c["stills"])}</a><a class="tour-stills" href="#contact">{e(c["contact"])}</a></div>'
    return f'<section class="hero-visual product-tour" id="product-demo" aria-labelledby="product-demo-title">{intro}{body}<p class="tour-evidence-note">{e(c["note"])}</p>{links}{transcript}</section>'

def resolve_demo_shots(lang, old):
    if not FILM_ENABLED:
        return old
    keys = ["label","title","description","input","output","next","status","caption","boundary","alt"]
    return [dict(s, **dict(zip(keys, LIVE_SHOTS[lang][i])), src=MEDIA+TOUR_FILES[i], width=1600, height=1000) for i,s in enumerate(old)]
