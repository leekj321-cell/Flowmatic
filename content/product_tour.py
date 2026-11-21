"""Localized product-tour presentation with a deployment-controlled media switch."""
from html import escape
from pathlib import Path

MEDIA = "/media/product-tour/"
MOVIE = "Flowmatic_Factory_OS_EN_V15.mp4"
REQUIRED = (MOVIE, "poster.jpg", "captions-en.vtt", "captions-ko.vtt", "flowmatic-v15-toolpath.jpg", "flowmatic-v15-logistics.jpg", "flowmatic-v15-handover-hold.jpg", "flowmatic-v15-quality.jpg")
DIRECTORY = Path(__file__).resolve().parents[1] / "media" / "product-tour"
FILM_ENABLED = DIRECTORY.joinpath("publish-approved").is_file()
if FILM_ENABLED and not all(DIRECTORY.joinpath(name).is_file() for name in REQUIRED):
    raise ValueError("Enabled product tour is missing an approved media file")
COPY = {
 "ko": {
    "title": "제품 데모: 부품에서 공장까지", "play": "제품 데모 영상", "time": "1분 51초 · 영어 음성",
    "hold": "최신 영상 공개 준비 중", "stills": "검증 화면 보기", "transcript": "영상 내용 요약",
    "note": "실제 시제품 화면과 내부 시뮬레이션. 고객 운영 실적이나 설비 가동 승인을 의미하지 않습니다.",
    "fallback": "이 브라우저에서 재생할 수 없으면 검증 화면과 영상 내용 요약을 확인할 수 있습니다.",
    "reading": "별도 내부 검증 사례로, 아래 제품 화면은 영상의 연속 장면이 아닙니다.",
    "chapters": [
      ("00:04", "소재 형상과 완성 형상을 비교하고 첫 가공 공정의 공구 경로를 확인합니다."),
      ("00:21", "로봇이 부품을 이송하는 셀에서 공장 전체로 시점을 넓힙니다. 기존 작업장 다섯 곳에 LILT가 추가됩니다. 주황은 입고 소재 팔레트, 빨강은 공정 중인 부품, 파랑은 출고 완제품 팔레트입니다."),
      ("00:53", "별도 예시에서 이관 검토는 가능하지만 목적지가 적용되지 않아 생산 이관은 차단됩니다."),
      ("01:08", "보어 수정안을 선택하면 대응하는 가공 BOM과 NC 코드가 표시됩니다. 적용·배포는 하지 않았습니다."),
      ("01:18", "같은 작업량의 공장 배치를 비교한 시뮬레이션에서 연간 지게차 이동 거리는 1,143km에서 495km로 바뀝니다."),
      ("01:33", "외관 검사는 통과했지만 높이가 공차를 벗어나 최종 판정은 불합격입니다."),
      ("01:42", "계획 생산량을 높이면 공구 두 개가 예산 미리보기에 표시됩니다. 주문이나 회계 반영은 없습니다."),
    ],
 },
 "en": {
    "title": "Product demo: From part to factory", "play": "Product demo film", "time": "1 min 51 sec · English audio",
    "hold": "Latest film not yet available", "stills": "View verified product screens", "transcript": "Film summary",
    "note": "Recorded prototype screens and internal simulations. No customer operating results or machine-release approval.",
    "fallback": "If playback is unavailable, the verified product screens and film summary are provided below.",
    "reading": "The product screens below are separate internal validation examples, not consecutive frames from the film.",
    "chapters": [
      ("00:04", "Raw-stock and finished geometry are compared. The first machining operation’s toolpath is visible."),
      ("00:21", "A robot transfers the part in the cell. The view expands to the factory, where LILT joins five existing work areas. Orange marks incoming stock pallets, red marks parts in process, and blue marks outgoing finished pallets."),
      ("00:53", "In a separate example, the handover is reviewed. No production transfer is released because no destination is applied."),
      ("01:08", "Selecting the bore revision reveals its machining bill of materials and NC references. The change remains a draft."),
      ("01:18", "With the same workload, alternative layouts show modeled forklift travel falling from 1,143 to 495 km per year."),
      ("01:33", "The visual check passes, but face height is out of tolerance and the final result is a fail."),
      ("01:42", "Raising planned quantity brings two tools into the budget preview. No order or posting takes place."),
    ],
 },
 "ar": {
    "title": "عرض المنتج: من القطعة إلى المصنع", "play": "فيلم عرض المنتج", "time": "دقيقة و51 ثانية · صوت باللغة الإنجليزية",
    "hold": "الفيلم الأحدث غير متاح بعد", "stills": "شاشات المنتج المتحقق منها", "transcript": "ملخص الفيلم",
    "note": "شاشات مسجلة للنموذج الأولي ومحاكاة داخلية. لا تمثل نتائج تشغيل لدى العملاء أو موافقة على تشغيل المعدات.",
    "fallback": "عند تعذر التشغيل، تتوفر أدناه شاشات المنتج المتحقق منها وملخص الفيلم.",
    "reading": "شاشات المنتج أدناه أمثلة مستقلة للتحقق الداخلي وليست لقطات متتالية من الفيلم.",
    "chapters": [
      ("00:04", "مقارنة شكل المادة الخام بشكل القطعة النهائية، مع عرض مسار الأداة في عملية التشغيل الأولى."),
      ("00:21", "ينقل الروبوت القطعة داخل الخلية، ثم يمتد العرض إلى المصنع حيث تنضم منطقة LILT إلى خمس مناطق عمل. البرتقالي لمنصات المواد الواردة، والأحمر للقطع قيد التشغيل، والأزرق لمنصات المنتجات النهائية الصادرة."),
      ("00:53", "في مثال منفصل، تُراجع عملية التسليم إلى الإنتاج. ولا يُعتمد النقل لعدم تطبيق وجهة."),
      ("01:08", "يُظهر اختيار تعديل الثقب قائمة مكونات التشغيل ومراجع برنامج التحكم الرقمي. يظل التعديل مسودة."),
      ("01:18", "في محاكاة تقارن تخطيطين عند عبء العمل نفسه، تنخفض مسافة الرافعات المحسوبة من 1,143 إلى 495 كيلومترًا سنويًا."),
      ("01:33", "ينجح الفحص البصري، لكن ارتفاع السطح خارج حدود السماحية، فتكون النتيجة النهائية عدم المطابقة."),
      ("01:42", "عند زيادة كمية الإنتاج المخطط لها، تظهر أداتان في معاينة الميزانية. لا يُنفذ طلب شراء أو قيد محاسبي."),
    ],
 },
}

def render_product_tour(lang, old_image, old_image_alt, zoom):
    c = COPY[lang]
    e = lambda s: escape(s, quote=True)
    intro = f'<div class="visual-head"><strong id="product-demo-title">{e(c["title"])}</strong><bdi>{e(c["time"] if FILM_ENABLED else c["hold"])}</bdi></div>'
    if FILM_ENABLED:
        ko = '<track kind="subtitles" src="' + MEDIA + 'captions-ko.vtt" srclang="ko" label="한국어" default>' if lang == "ko" else ""
        en = f'<track kind="captions" src="{MEDIA}captions-en.vtt" srclang="en" label="English"{(" default" if lang == "en" else "")}>'
        body = f'<video controls playsinline preload="metadata" width="1600" height="1000" poster="{MEDIA}poster.jpg" aria-label="{e(c["play"])}"><source src="{MEDIA}{MOVIE}" type="video/mp4">{en}{ko}<p>{e(c["fallback"])}</p></video>'
        summary = ''.join(f'<li><bdi>{e(stamp)}</bdi><span>{e(line)}</span></li>' for stamp,line in c["chapters"])
        transcript = f'<details class="tour-transcript"><summary>{e(c["transcript"])}</summary><ol>{summary}</ol></details>'
    else:
        body = f'<button type="button" class="image-open tour-preview" data-open-shot="machining" aria-label="{e(zoom)}"><img src="{e(old_image)}" alt="{e(old_image_alt)}" width="2304" height="1294" decoding="async"></button>'
        transcript = ""
    return f'<section class="hero-visual product-tour" id="product-demo" aria-labelledby="product-demo-title">{intro}{body}<p class="tour-evidence-note">{e(c["note"])}</p><a class="tour-stills" href="#product">{e(c["stills"])}</a>{transcript}</section>'

# Field order: title, description, input, output, next, status, caption, boundary, alt.
LIVE_SHOTS = {
 "ko": [
    ("소재·완성 형상과 첫 공정 공구 경로", "소재와 완성 형상을 비교하고, 첫 가공 공정에서 공구가 지나가는 경로를 확인합니다.", "소재·완성 STEP 형상 / 대상 공정", "실제 시제품의 가공 경로와 NC 검토 화면", "검토한 공정 조건을 셀과 물류 계획에 사용합니다.", "제품 화면", "첫 공정의 공구 경로와 NC 행 번호", "물리 가공 시험이나 현장 사용 승인을 의미하지 않습니다.", "LILT 부품의 형상 옆에 첫 공정의 공구 경로와 NC 행 번호가 보이는 시제품 화면."),
    ("자동화 셀과 공장 물류 흐름", "로봇 셀의 부품 이송을 확대해 본 뒤, 공장 전체에서 입고 소재·공정 중 부품·출고 완제품이 동시에 이동하는 흐름을 확인합니다.", "설비·셀 구성 / 작업량 / 자재 공급 및 이송 조건", "다섯 기존 작업장과 추가된 LILT 작업장, 입고·가공·출고 흐름", "같은 작업량에서 배치별 운반 경로를 비교합니다.", "내부 시뮬레이션", "주황: 입고 소재 · 빨강: 공정 중 부품 · 파랑: 출고 완제품", "파란 팔레트는 기존 작업장의 출고이며 LILT의 출고가 아닙니다.", "6개 작업장의 지도에서 주황색, 빨간색, 파란색 흐름이 색상 범례와 함께 표시됩니다."),
    ("생산 이관 전 배치 검토", "별도 내부 사례에서 배치 제안과 이관 근거를 검토합니다. 목적지가 적용되지 않으면 다음 단계는 차단됩니다.", "배치 제안 / 등록된 목적지 및 검토 조건", "배치 제안과 이관이 보류된 사유", "요건을 충족하기 전에는 운영에 적용하지 않습니다.", "제품 화면 · 이관 보류", "배치 제안과 생산 이관 차단 사유", "소프트웨어의 사전 검토 화면이며 실제 이관, 설비 가동 또는 안전 승인을 뜻하지 않습니다.", "노란색으로 표시된 제안 배치와 목적지가 적용되지 않았다는 영문 이관 차단 안내."),
    ("외관·치수 근거에 따른 품질 판정", "별도 내부 검사 사례에서 외관 통과와 치수 불량이 함께 기록됩니다. 높이가 허용범위를 벗어나면 최종 결과는 불합격입니다.", "동일 검사품의 외관 결과 / 높이 측정값 및 공차", "최종 불합격과 그 근거인 높이 치수", "판정 근거를 다음 품질 검토에 사용합니다.", "제품 화면 · 내부 검사 예시", "외관 통과와 별개로 높이 공차를 벗어나 최종 불합격", "고객 현장 품질성과가 아닌 별도 내부 검사 예시입니다.", "외관 검사 통과와 높이 치수 공차 초과로 인한 최종 불합격을 함께 표시한 영어 제품 화면."),
 ],
 "en": [
    ("Geometry and the first machining toolpath", "Compare stock and finished geometry, then review the path of the tool in the first machining operation.", "Stock and finished STEP geometry / Selected operation", "Toolpath and NC review on the recorded prototype screen", "Reviewed process conditions inform cell and logistics planning.", "Recorded product screen", "The first operation’s toolpath and NC line reference", "This is not physical cutting validation or approval for shop-floor use.", "The prototype shows the first toolpath and NC line reference beside the LILT geometry."),
    ("Automation cells and factory material flow", "Follow a part through a robot cell, then review incoming stock, work in process and outgoing finished products moving together at factory scale.", "Equipment and cell configuration / Workload / Supply and transport conditions", "Five existing work areas plus LILT, with incoming, in-process and outgoing flows", "Compare transport routes using the same workload.", "Internal simulation", "Orange: incoming stock · Red: parts in process · Blue: finished products out", "The visible blue pallet ships from an existing work area, not LILT.", "The factory map and legend identify orange, red and blue flows across six work areas."),
    ("Layout review before production handover", "In a separate internal example, the proposed layout and its evidence can be reviewed. Handover remains blocked when no destination is applied.", "Proposed placement / Registered destination and review conditions", "Placement proposal and the reason handover is blocked", "The review is not released to operations before its requirements are met.", "Recorded product screen · On hold", "Proposed placement and the hold on production transfer", "This is a software review, not an actual transfer, machine start-up or safety approval.", "A yellow proposed placement and a visible English handover warning that no destination has been applied."),
    ("Inspection decisions from visual and dimensional evidence", "In a separate internal inspection example, the visual check passes while the measured face height is outside tolerance, so the final inspection result is a fail.", "Visual result / Face-height measurement and tolerance for the same inspected unit", "Final fail with its dimensional reason", "Inspection evidence is available for the next quality review.", "Recorded product screen · Internal inspection example", "Visual check passes; out-of-tolerance height leads to final fail", "A separate internal example, not a customer quality outcome.", "The recorded English quality screen displays a visual pass and an out-of-tolerance face height with an overall fail."),
 ],
 "ar": [
    ("الهندسة ومسار الأداة في عملية التشغيل الأولى", "تُقارن هندسة المادة الخام والقطعة النهائية، ثم يُراجع مسار الأداة في عملية التشغيل الأولى.", "هندسة STEP للمادة الخام والقطعة النهائية / العملية المحددة", "مسار الأداة ومراجعة برنامج التحكم الرقمي في شاشة النموذج الأولي", "تُستخدم شروط العملية المُراجعة في تخطيط الخلايا والمناولة.", "شاشة مسجلة للمنتج", "مسار الأداة ومرجع سطر برنامج التحكم الرقمي للعملية الأولى", "لا يُعد ذلك اختبار قطع فعليًا أو موافقة على الاستخدام في المصنع.", "تعرض الواجهة مسار الأداة ومرجع سطر برنامج التحكم الرقمي للعملية الأولى بجوار هندسة قطعة LILT."),
    ("خلايا الأتمتة وتدفقات المواد في المصنع", "تُتابع حركة القطعة داخل خلية روبوتية، ثم يُراجع تدفق المواد الواردة والقطع قيد التشغيل والمنتجات النهائية الصادرة على مستوى المصنع.", "تهيئة المعدات والخلايا / عبء العمل / شروط التوريد والنقل", "خمس مناطق عمل قائمة ومنطقة LILT الإضافية، مع التدفقات الواردة والجارية والصادرة", "تُقارن مسارات النقل تحت عبء العمل نفسه.", "محاكاة داخلية", "البرتقالي: مواد واردة · الأحمر: قطع قيد التشغيل · الأزرق: منتجات نهائية صادرة", "تخرج المنصة الزرقاء الظاهرة من منطقة عمل قائمة، لا من منطقة LILT.", "تحدد خريطة المصنع ومفتاح الألوان التدفقات البرتقالية والحمراء والزرقاء في ست مناطق عمل."),
    ("مراجعة التخطيط قبل التسليم للإنتاج", "في مثال داخلي منفصل، يتاح استعراض التخطيط المقترح وأدلته. ويظل التسليم متوقفًا ما لم تُطبَّق وجهة.", "التخطيط المقترح / الوجهة المسجلة وشروط المراجعة", "مقترح التخطيط وسبب إيقاف التسليم", "لا تُحال الخطة إلى التشغيل قبل استيفاء شروط المراجعة.", "شاشة مسجلة للمنتج · قيد الإيقاف", "التخطيط المقترح وسبب إيقاف النقل إلى الإنتاج", "هذه مراجعة برمجية وليست نقلًا فعليًا أو تشغيلًا للمعدات أو موافقة على السلامة.", "تخطيط مقترح باللون الأصفر وتنبيه بالإنجليزية يوضح عدم تطبيق وجهة للتسليم."),
    ("قرار الفحص استنادًا إلى أدلة بصرية وقياسية", "في مثال فحص داخلي منفصل، ينجح الفحص البصري لكن ارتفاع السطح خارج حدود السماحية، فتكون النتيجة النهائية عدم المطابقة.", "النتيجة البصرية / قياس ارتفاع السطح وحدود السماحية للقطعة نفسها", "عدم المطابقة والسبب المتعلق بالقياس", "تظل أدلة الفحص متاحة لمراجعة الجودة التالية.", "شاشة مسجلة للمنتج · مثال فحص داخلي", "نجاح الفحص البصري لا يغير النتيجة النهائية لارتفاع خارج حدود السماحية", "هذا مثال داخلي منفصل وليس نتيجة جودة لدى عميل.", "تبين شاشة الجودة بالإنجليزية نجاح الفحص البصري وقياس ارتفاع خارج حدود السماحية مع عدم المطابقة النهائية."),
 ],
}
for lang, seq, iface in [
 ("ko","공정·셀 장면과 별도로 양산이관 및 품질 판정 예시가 포함됩니다. 모두 내부 검증용입니다.","영문 제품 화면입니다."),
 ("en","The machining and cell sequence is followed by separate handover and inspection examples. All are internal demonstrations.","Recorded English-language product interface."),
 ("ar","تتبع مشاهد التشغيل والخلايا أمثلة منفصلة للتسليم والفحص. جميعها عروض داخلية.","شاشات مسجلة لواجهة المنتج باللغة الإنجليزية."),
]:
 COPY[lang]["sequence"] = seq
 COPY[lang]["reading"] = iface

def resolve_demo_shots(lang, old):
    if not FILM_ENABLED:
        return old
    keys = ['title','description','input','output','next','status','caption','boundary','alt']
    files = ['flowmatic-v15-toolpath.jpg','flowmatic-v15-logistics.jpg','flowmatic-v15-handover-hold.jpg','flowmatic-v15-quality.jpg']
    return [dict(s, **dict(zip(keys, LIVE_SHOTS[lang][i])), src=MEDIA+files[i], width=1000, height=625) for i,s in enumerate(old)]
