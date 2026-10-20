"""Public product evidence. Separate synthetic runs; no customer outcomes."""
from html import escape as e

MEDIA = '/media/product-20261020/'
COPY = {
 'ko': {
  'title':'계획 변경의 실행 기록과 3D 작업표준서',
  'intro':'통합 시제품에서 확인한 두 가지 업무 사례입니다. 각 사례는 서로 다른 합성 시험 데이터를 사용합니다.',
  'label':'CURRENT · 내부 검증', 'open':'원본 이미지 보기',
  'detail':'사례와 적용 범위', 'pdf':'작업표준서 PDF 보기',
  'language':'화면과 PDF는 한국어 제품에서 나온 실제 결과물입니다.',
  'change': {
   'title':'생산량 변경에 따른 계획 승인과 실행 기준',
   'body':'변경된 생산량과 납기 조건으로 대안을 비교하고, 담당자가 승인한 계획을 작업지시와 자원 예약에 반영합니다. 이후 LOT·품질 기록에서 적용 계획과 근거를 확인합니다.',
   'steps':[('대안 비교','물량·납기와 설비·물류 조건을 함께 검토'),('담당자 승인','선택 계획을 작업지시·자원 예약으로 반영'),('근거 검토','LOT·품질 기록을 연결하고 재사용 가능 범위를 확인')],
   'caption':'합성 시험에서 공장 검토계획이 승인·적용된 이력을 확인한 화면.',
   'boundary':'합성 데이터로 소프트웨어의 연결·기록·재사용 조건을 확인한 사례입니다. 고객 생산성 향상이나 실제 설비 제어를 입증한 결과는 아닙니다.',
   'gallery':[('plan-comparison.png','변경 조건으로 검토한 선택 계획의 설비·물류 일정.'),('approved-work-orders.png','담당자 승인 후 공장 검토계획이 적용된 이력.'),('lot-quality-trace.png','LOT·품질 기록에 남은 적용 계획과 합성 시험 근거.')],
  },
  'standard': {
   'title':'가공 정보 기반 3D 작업표준서',
   'body':'가공 자세별 경로와 작업 순서를 3D 개요와 상세 보기로 정리합니다. 공구·NC 행·회전수·이송 정보를 포함한 작업표준서를 PDF로 내보냅니다.',
   'steps':[('가공 정보','자세별 경로·순서·공구 조건 확인'),('작업 기준','3D 개요와 자세별 상세 구성'),('문서 출력','검토와 공유를 위한 PDF 내보내기')],
   'caption':'합성 가공 데이터를 제품에서 PDF로 내보낸 결과물의 첫 페이지.',
   'boundary':'공개 샘플은 합성 형상·NC를 사용한 별도 시험입니다. 실제 절삭, 충돌 검증 또는 현장 작업표준의 승인까지 완료한 자료는 아닙니다.',
  },
 },
 'en': {
  'title':'Plan-change records and 3D work instructions',
  'intro':'Two workflows verified in the integrated prototype. Each case uses a separate synthetic test dataset.',
  'label':'CURRENT · Internal validation', 'open':'Open original image',
  'detail':'Case and scope', 'pdf':'View work-instruction PDF',
  'language':'Screens and the PDF are actual outputs from the Korean-language product.',
  'change': {
   'title':'Plan approval and execution criteria after a volume change',
   'body':'Compare alternatives against revised volumes and due dates. A responsible reviewer approves the selected plan before it is applied to work orders and resource reservations. LOT and quality records retain the applied plan and its evidence.',
   'steps':[('Compare alternatives','Review volume, due dates, equipment and logistics together'),('Approve the plan','Apply the selected plan to work orders and resource reservations'),('Review the evidence','Link LOT and quality records and check the permitted reuse scope')],
   'caption':'Actual screen showing approval and application of a factory review plan in a synthetic test.',
   'boundary':'Synthetic data verifies software links, records and reuse conditions. This is not evidence of customer productivity gains or control of physical equipment.',
   'gallery':[('plan-comparison.png','Equipment and logistics schedule for the selected plan reviewed under revised conditions.'),('approved-work-orders.png','Record of a factory review plan applied after reviewer approval.'),('lot-quality-trace.png','Applied plan and synthetic-test evidence retained in LOT and quality records.')],
  },
  'standard': {
   'title':'3D work instructions from machining information',
   'body':'Organize machining paths and operation order by orientation, with a 3D overview and detailed views. Export work instructions containing tools, NC lines, spindle speeds and feed rates to PDF.',
   'steps':[('Machining information','Review paths, operation order and tool conditions by orientation'),('Work instructions','Compose the 3D overview and orientation details'),('Document export','Export a PDF for review and sharing')],
   'caption':'First page of a PDF exported by the product using synthetic machining data.',
   'boundary':'The public sample uses synthetic geometry and NC in a separate test. It does not establish cutting performance, collision clearance or approval for shop-floor use.',
  },
 },
 'ar': {
  'title':'سجلات تغيير الخطة وتعليمات العمل ثلاثية الأبعاد',
  'intro':'مسارا عمل جرى التحقق منهما في النموذج الأولي المتكامل. تستخدم كل حالة مجموعة مستقلة من بيانات الاختبار الاصطناعية.',
  'label':'CURRENT · تحقق داخلي', 'open':'فتح الصورة الأصلية',
  'detail':'الحالة ونطاق التطبيق', 'pdf':'عرض ملف تعليمات العمل PDF',
  'language':'الشاشات وملف PDF مخرجات فعلية من المنتج باللغة الكورية.',
  'change': {
   'title':'اعتماد الخطة ومعايير التنفيذ بعد تغيير حجم الإنتاج',
   'body':'مقارنة البدائل وفق الكميات ومواعيد التسليم المعدلة. يعتمد المسؤول الخطة المختارة قبل تطبيقها على أوامر العمل وحجوزات الموارد. تحتفظ سجلات الدُفعات والجودة بالخطة المطبقة وأدلتها.',
   'steps':[('مقارنة البدائل','مراجعة الكميات والمواعيد والمعدات واللوجستيات معًا'),('اعتماد الخطة','تطبيق الخطة المختارة على أوامر العمل وحجوزات الموارد'),('مراجعة الأدلة','ربط سجلات الدُفعات والجودة والتحقق من نطاق إعادة الاستخدام المسموح')],
   'caption':'شاشة فعلية تعرض سجل اعتماد خطة مراجعة المصنع وتطبيقها في اختبار ببيانات اصطناعية.',
   'boundary':'تتحقق البيانات الاصطناعية من روابط البرمجيات وسجلاتها وشروط إعادة الاستخدام. لا تثبت هذه الحالة تحسن إنتاجية العملاء أو التحكم بالمعدات الفعلية.',
   'gallery':[('plan-comparison.png','جدول المعدات واللوجستيات للخطة المختارة بعد مراجعتها وفق الشروط المعدلة.'),('approved-work-orders.png','سجل تطبيق خطة مراجعة المصنع بعد اعتماد المسؤول.'),('lot-quality-trace.png','الخطة المطبقة وأدلة الاختبار الاصطناعي المحفوظة في سجلات الدُفعات والجودة.')],
  },
  'standard': {
   'title':'تعليمات عمل ثلاثية الأبعاد من معلومات التشغيل',
   'body':'تنظيم مسارات التشغيل وترتيب العمليات حسب وضعية القطعة، مع نظرة عامة ثلاثية الأبعاد وعروض تفصيلية. تصدير تعليمات العمل إلى PDF مع الأدوات وأسطر NC وسرعات دوران المغزل ومعدلات التغذية.',
   'steps':[('معلومات التشغيل','مراجعة المسارات وترتيب العمليات وشروط الأدوات حسب الوضعية'),('تعليمات العمل','إعداد النظرة العامة ثلاثية الأبعاد وتفاصيل الوضعيات'),('تصدير المستند','تصدير PDF للمراجعة والمشاركة')],
   'caption':'الصفحة الأولى من ملف PDF صدّره المنتج باستخدام بيانات تشغيل اصطناعية.',
   'boundary':'تستخدم العينة العامة أشكالًا هندسية وبرامج NC اصطناعية في اختبار مستقل. وهي لا تثبت أداء القطع أو خلو المسارات من التصادم أو اعتماد الاستخدام في المصنع.',
  },
 },
}

def figure(lang, filename, caption):
    c=COPY[lang]
    return f'<figure class="case-figure"><a href="{MEDIA}{filename}" target="_blank" rel="noopener" aria-label="{e(c["open"]+": "+caption)}"><img src="{MEDIA}{filename}" alt="{e(caption)}" loading="lazy" decoding="async"></a><figcaption>{e(caption)}</figcaption></figure>'

def render_cases(lang, kinds=('change','standard'), detailed=False):
    c=COPY[lang]; articles=[]
    for kind in kinds:
        t=c[kind]; slug='platform' if kind=='change' else 'work-standard'
        filename='approved-work-orders.png' if kind=='change' else 'work-standard-overview.png'
        steps='<ol class="case-steps">'+''.join(f'<li><strong>{e(a)}</strong><span>{e(b)}</span></li>' for a,b in t['steps'])+'</ol>'
        pics=''.join(figure(lang,f,cap) for f,cap in t['gallery']) if detailed and kind=='change' else figure(lang,filename,t['caption'])
        links='' if detailed else f'<a class="case-link" href="/{lang}/{slug}/#case-{kind}">{e(c["detail"])} ↗</a>'
        if kind=='standard': links+=f'<a class="case-link" href="{MEDIA}synthetic-work-standard.pdf" target="_blank" rel="noopener" data-case-pdf>{e(c["pdf"])} ↗</a>'
        articles.append(f'<article class="product-case" id="case-{kind}"><p class="case-state">{e(c["label"])}</p><h3>{e(t["title"])}</h3><p class="case-body">{e(t["body"])}</p>{steps}<div class="case-gallery">{pics}</div><p class="case-boundary">{e(t["boundary"])}</p><div class="case-links">{links}</div></article>')
    intro=f'<div class="cases-intro"><h2>{e(c["title"])}</h2><p>{e(c["intro"])}</p></div>' if len(kinds)>1 else ''
    return f'<section class="product-cases {"cases-detailed" if detailed else ""}" id="product-cases">{intro}<div class="cases-grid">{"".join(articles)}</div><p class="case-language">{e(c["language"])}</p></section>'
