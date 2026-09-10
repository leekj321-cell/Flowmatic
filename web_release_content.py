"""Approved 2026-09-10 public website narrative (KO / EN / AR).

KICXUP customer-facing scope. Synthetic workflow examples are not live factory
results. The approved composition/Operations animations are owned by the base
renderer and are deliberately not reconstructed here.
"""
from html import escape as e

RELEASE = '2026.09.10-r1'
LANGS = ('ko', 'en', 'ar')
TEXT = {
'ko': {
'intro': '제조 현장의 기존 설비와 데이터를 활용해, 사람에 의존하던 생산·품질·관리 업무를 시스템화하는 제조 AI 플랫폼.',
'support': '자료·작업 기준·판단과 처리 이력을 연결해, 담당자가 바뀌어도 다음 업무에 활용하도록 합니다.',
'nav': ['제품', '데모', '플랫폼 구조', '회사', '파일럿 상담'],
'run': 'NC 3D 데모 실행', 'consult': '우리 공장 적용 상담', 'details': '제품과 적용 범위',
'work_title': '자료가 있어도, 업무를 이어받으려면 다시 물어야 합니다.',
'work_body': '최신 자료를 찾고, 이전 판단을 묻고, 진행 상황을 다시 정리하는 부담. 공통 기준과 분석·계산·검토 지원으로 담당자의 역량이 회사의 운영역량으로 남도록 합니다.',
'people': [('신규 담당자의 적응', '작업 자료와 이전 처리 근거를 찾아보고 다음 업무를 이어받습니다.'), ('숙련자의 판단·개선', '반복 검색과 설명의 부담을 줄이고 전문적인 검토와 개선에 집중하도록 돕습니다.'), ('관리자의 업무 연속성', '대상·담당·현재 상태·처리 이력을 함께 보며 인수인계와 업무 배분을 지원합니다.')],
'goal': '고객 현장에서 정확도·사용성·업무 부담을 비교할 도입 목표입니다. 인력 감축이나 성과 개선을 보장하는 수치가 아닙니다.',
'products_title': '지금 바꿀 업무부터 선택하세요.',
'products_body': '네 지능축을 유지하면서, 필요한 업무와 입력·결과를 기준으로 적용 범위를 정합니다.',
'products': [('가공 준비·검토', '도면·NC·공구·측정 정보를 대조하고 경로와 변경 근거를 검토합니다.', '공개 NC 3D 데모 · 기능형 프로토타입'), ('검사·품질 대응', '검사기록과 불량·손실을 정리하고 우선 업무와 조치 이력을 확인합니다.', '기능형 프로토타입 · 현장 연계 검증 예정'), ('구매·소모품·공수 관리', '요청을 품목·수량으로 정리하고 생산량 대비 사용량과 비용의 이상 후보를 찾습니다.', '기능형 MVP · 내부 검증'), ('자재 요청·운반 확인', '요청·배정·운반·투입 확인을 같은 상태 이력으로 이어가는 범위를 검토합니다.', '프로토타입 통합 · 현장 검증 필요')],
'demos_title': '설명보다 먼저, 작동하는 제품을 확인하세요.',
'demos_body': '브라우저에서 직접 실행하는 기능과 실제 프로그램 녹화를 구분했습니다. 두 데모는 서로 다른 입력의 개별 시연입니다.',
'live': '직접 실행 · 공개 합성 샘플', 'recorded': '실제 프로그램 녹화 · 내부 시연',
'nc_demo': 'G-code를 3D 공구 경로로', 'nc_body': '공개 합성 샘플이 바로 표시됩니다. 공구 전환·회전·확대와 로컬 NC 파일 검토를 체험하세요.',
'ct_demo': '작업 영상을 시간 기록으로', 'ct_body': '작업 구간·CT·가동/비가동·간트를 확인하는 프로그램 녹화입니다. 브라우저에서 새 영상을 분석하는 기능과는 구분합니다.',
'ct_run': '영상 분석 시연 보기', 'nc_alt': '공개 합성 NC 샘플을 표시한 실제 Flowmatic 브라우저 3D 뷰어', 'ct_alt': '기존 Flowmatic CT 시연 영상의 실제 프로그램 화면',
'workflow_title': '가공 준비에서 품질 대응까지, 같은 작업을 이어봅니다.',
'workflow_note': '업무 연결 시나리오 · 개별 기능을 연결하는 적용 구상입니다. 통합 자동진단·CNC 자동전송·고객 현장 성과를 뜻하지 않습니다.',
'workflow': [('라인 → 선택 설비', '설비·품목·공정으로 작업 대상을 확인'), ('가공 준비·검토', '도면·NC·경로와 프로그램 리비전 확인'), ('상태·품질 검토', '수량·치수·진동·검사 증빙을 대조'), ('다음 담당 업무', '대상·담당·기한·조치와 재검사 결과 기록')],
'quality_note': '진동 추이·치수 SPC·불량률과 검사 증빙을 함께 보고 다음 조치를 검토하는 연결 예시입니다. 자동 원인 판정이나 실측 LOT의 통합 결과로 표시하지 않습니다.',
'pre_title': 'AI가 일하기 좋은 구조는, 사람도 일하기 좋은 구조입니다.',
'pre_body': '매번 파일을 처음부터 해석하는 대신, 필요한 정보와 계산 결과·처리 이력을 정리해 다음 업무에 다시 활용합니다.',
'pre_steps': [('현장 원자료', '도면·NC·영상·검사기록'), ('Flowmatic 전처리', '구조화·계산·이력 재사용'), ('사람과 AI의 활용', '확인·검토·후속 업무의 판단 근거')],
'pre_note': 'NC 구조화와 로컬 이력을 확보했습니다. USB 파일 교환과 AI 연계는 추가 구현·검증 범위이며, 토큰·시간 절감률은 전처리를 포함한 동등 조건에서 측정할 목표입니다.',
'reuse_title': '같은 기반으로, 다른 현장 요청을 검토합니다.',
'reuse_body': '예: 비슷한 제품을 모아 기존 가공라인을 재구성할 때',
'reuse': [('제품군 후보', '가공 분석·작업표준 재사용 / 지그·설비 호환 규칙 추가'), ('배치안 비교', '물류 경로·배차 재사용 / 도면 변환·공간 제약 추가'), ('이전·재가동 계획', '품질·업무목록·이력 재사용 / 일정·자원·승인 규칙 추가')],
'reuse_note': '조합안과 추가 개발 범위를 함께 설명하는 적용 구상입니다. 자동 안전 승인이나 즉시 재가동을 수행하는 완제품이 아닙니다.',
'pilot_title': '한 라인 · 한 업무 · 4~8주 제안',
'pilot_body': '자동차부품·정밀가공 등 기존 설비와 자료는 있지만 반복 확인·인수인계 부담이 큰 제조기업부터 시작합니다. 범위와 기간은 착수 전에 합의합니다.',
'pilot_steps': [('업무와 책임자', '생산기술·품질·생산관리 사용자와 공장장·대표 등 도입 승인권자를 정합니다.'), ('자료와 기준선', '접근할 자료, 보안·보관 조건, 현재 처리시간과 반복 확인 부담을 합의합니다.'), ('4~8주 비교 검증', '같은 업무의 정확도·사용성·공수와 인수인계 부담을 기존 방식과 비교합니다.'), ('총비용·확장 판단', '설치·교육·지원을 포함한 총비용과 보유 시스템 확장 대안을 함께 비교합니다.')],
'commercial': '업무 도입비 + 지속 이용료 구조. 연결할 자료·현장 설정·설치·교육·지원 범위에 따라 견적합니다. 첫 업무 이후 관련 업무·인접 라인·다른 공장으로의 확장은 고객별 설정과 현장 검증을 거칩니다.',
'contact': '현재 반복 공수가 큰 업무, 사용할 자료와 담당자를 알려주세요. 한 라인·한 업무의 4~8주 검증 범위와 총비용을 함께 구체화합니다.',
'mach_title': '도면과 NC를, 담당자가 검토할 수 있는 작업으로.',
'mach_body': 'NC·도면·공구·측정 정보를 찾아 대조하는 가공 준비 업무를 지원합니다. 공개 브라우저에서는 합성 샘플의 공구 경로를 직접 확인할 수 있습니다.',
'inputs': '입력', 'outputs': '확인할 결과', 'scope_title': '직접 실행 · 프로그램 기능 · 추가 연동',
'scopes': [('공개 브라우저', 'NC 텍스트의 지원 경로·공구·직경을 표시하고 기본 이동시간을 참고값으로 계산합니다.'), ('가공 프로그램', '가공 정보 구조화·로컬 이력·NC 구성과 검토 기능은 별도 프로그램 범위입니다. 웹 데모에 모두 포함된 것은 아닙니다.'), ('추가 검증', '도면 자동 해석·전체 공정 자동 생성·CNC 전송·USB 동기화·AI 연계는 각각 별도 구현·검증이 필요합니다.')],
'input_body': 'NC 텍스트 · 도면/참조 형상 · 공구/가공 조건 · 측정·변경 기록',
'output_body': '공구별 경로 · 검토할 조건 · 가공 자료와 변경 이력 · 담당자의 다음 판단 근거',
'engineering': '기술 구조와 상세 적용 조건 보기',
'example': '설명용 애니메이션 · 고정 수치는 예시이며 위 파일의 분석 결과가 아닙니다.',
'sample_note': '공개용 합성 샘플 자동 표시 · 실제 사내 가공코드가 아닙니다. 로컬 파일은 업로드하지 않습니다.',
'limits': '경로 검토와 이론시간 참고용입니다. 실제 절삭·충돌 검증·설비 안전 승인·자동 제어를 대신하지 않습니다.',
'platform_link': '플랫폼 구조 상세',
'ops_title': '구매·소모품·공수의 반복 정리를 운영 판단으로.',
'ops_body': '요청의 품목·수량을 정리하고 생산량 대비 자원 사용과 비용의 이상 후보를 검토합니다. 설비 상태·CT는 가공/영상 분석과 연결할 데이터이며, 완전한 제조원가나 회계원가를 뜻하지 않습니다.',
},
'en': {
'intro': 'A manufacturing AI platform that uses existing factory equipment and data to systematize production, quality and management workflows that depend on individual expertise.',
'support': 'Connect work materials, standards, decisions and outcomes so the next person can pick up the work with its context intact.',
'nav': ['Products', 'Demos', 'Platform structure', 'Company', 'Discuss a pilot'],
'run': 'Run the NC 3D demo', 'consult': 'Discuss your factory workflow', 'details': 'Product and deployment scope',
'work_title': 'The files exist. The next person still has to ask.',
'work_body': 'Finding the latest information, asking why a decision was made and checking progress takes effort. Shared standards and analysis, calculation and review support help turn individual expertise into organizational capability.',
'people': [('Help new owners get started', 'Find work materials and the basis for earlier decisions before taking over the next task.'), ('Free expertise for improvement', 'Reduce repetitive searching and explanation so experienced staff can focus on judgment and improvement.'), ('Keep work continuous', 'Review the subject, owner, status and history together to support handovers and workload allocation.')],
'goal': 'Intended benefits to compare for accuracy, usability and work effort at the customer site—not guaranteed staffing reductions or measured customer outcomes.',
'products_title': 'Start with the workflow you need to change.',
'products_body': 'Four intelligence domains, with deployment defined by the actual work, inputs and outputs.',
'products': [('Machining preparation and review', 'Compare drawings, NC, tools and measurements; review paths and the reasons for changes.', 'Public NC 3D demo · functional prototype'), ('Inspection and quality response', 'Organize inspection records, defects and losses; review priority work and action history.', 'Functional prototype · field integration to validate'), ('Purchasing, consumables and labor', 'Structure item and quantity requests; surface usage and cost anomalies relative to production.', 'Functional MVP · internal validation'), ('Material requests and delivery', 'Review how requests, assignments, transport and input confirmation connect through status history.', 'Prototype integration · field validation required')],
'demos_title': 'See the working product before the architecture.',
'demos_body': 'Interactive browser functionality and recordings of real programs are labeled separately. These are individual demonstrations using different inputs.',
'live': 'Interactive · public synthetic sample', 'recorded': 'Real program recording · internal demonstration',
'nc_demo': 'From G-code to a 3D toolpath', 'nc_body': 'The public synthetic sample appears immediately. Switch tools, orbit, zoom and inspect a local NC file.',
'ct_demo': 'From work video to time records', 'ct_body': 'A program recording showing work intervals, cycle time, operating/idle time and Gantt views. It is not a browser service for analyzing new videos.',
'ct_run': 'Watch the video-analysis demo', 'nc_alt': 'Actual Flowmatic browser 3D viewer displaying the public synthetic NC sample', 'ct_alt': 'Actual program frame from the existing Flowmatic CT demonstration',
'workflow_title': 'Connect machining preparation to quality response.',
'workflow_note': 'Workflow integration scenario—not a commissioned end-to-end system, automatic diagnosis, CNC transmission or measured customer outcome.',
'workflow': [('Line → selected machine', 'Identify equipment, product and operation'), ('Machining review', 'Review drawings, NC, paths and program revisions'), ('State and quality', 'Compare quantity, dimensions, vibration and inspection evidence'), ('The next owned task', 'Record subject, owner, due date, action and reinspection result')],
'quality_note': 'An integration example for reviewing vibration trends, dimensional SPC, defect rates and inspection evidence before deciding the next action. It is not automatic root-cause diagnosis or an integrated measured LOT result.',
'pre_title': 'A structure that works for AI also works for people.',
'pre_body': 'Rather than interpreting every file from scratch, structure the relevant information, calculations and processing history for reuse in the next task.',
'pre_steps': [('Field inputs', 'Drawings · NC · video · inspection records'), ('Flowmatic preprocessing', 'Structure · calculate · reuse history'), ('People and AI', 'Evidence for review, decisions and follow-up work')],
'pre_note': 'NC structuring and local history are available. USB exchange and AI integration require further implementation and validation. Token and time savings are targets to measure under equivalent conditions, including preprocessing.',
'reuse_title': 'Use the same foundation for a different field request.',
'reuse_body': 'Example: regroup similar products and reorganize an existing machining line',
'reuse': [('Product-family candidates', 'Reuse machining analysis and work standards / add fixture and equipment compatibility rules'), ('Layout comparison', 'Reuse material routing and dispatch / add drawing conversion and spatial constraints'), ('Relocation and restart plan', 'Reuse quality, worklists and history / add calendar, resource and approval rules')],
'reuse_note': 'An application concept identifying reusable capabilities and additional development—not a turnkey product for automatic safety approval or immediate restart.',
'pilot_title': 'One line · one workflow · a 4–8-week proposal',
'pilot_body': 'Start with automotive-parts and precision-machining manufacturers that have usable equipment and records but face repeated checks and handover burdens. Scope and duration are agreed before kickoff.',
'pilot_steps': [('Workflow and owners', 'Identify production-engineering, quality and planning users, plus plant or executive approval owners.'), ('Data and baseline', 'Agree on data access, security, retention, current handling time and repeated checks.'), ('4–8-week comparison', 'Compare accuracy, usability, effort and handover burden for the same workflow against the existing approach.'), ('Total cost and expansion', 'Include installation, training and support, and compare extending the systems the customer already owns.')],
'commercial': 'Workflow implementation fees plus ongoing usage fees. Quotes depend on data connections, site configuration, installation, training and support. Expansion to related work, adjacent lines and other sites requires customer-specific configuration and field validation.',
'contact': 'Tell us about the repetitive task, available records and responsible team. Together we can define a 4–8-week evaluation for one workflow on one line and its total cost.',
'mach_title': 'Turn drawings and NC into work people can review.',
'mach_body': 'Support machining preparation by comparing NC, drawings, tool and measurement information. Inspect the synthetic sample toolpath directly in the public browser demo.',
'inputs': 'Inputs', 'outputs': 'Results to review', 'scope_title': 'Browser functionality · program scope · further integration',
'scopes': [('Public browser', 'Display supported NC paths, tools and diameters, with a basic-motion time estimate for reference.'), ('Machining program', 'Structured machining information, local history, NC assembly and review belong to the separate program scope; they are not all included in the web demo.'), ('Further validation', 'Automatic drawing interpretation, complete process generation, CNC transfer, USB synchronization and AI integration each require separate implementation and validation.')],
'input_body': 'NC text · drawings/reference geometry · tools/conditions · measurements and change records',
'output_body': 'Per-tool paths · review conditions · machining information and change history · evidence for the next decision',
'engineering': 'View technical architecture and detailed deployment conditions',
'example': 'Explanatory animation · fixed figures are illustrative, not analysis results for the file above.',
'sample_note': 'Public synthetic sample loads automatically—not company production G-code. Local files are not uploaded.',
'limits': 'For path review and theoretical time reference. Not a replacement for cutting trials, collision validation, machine safety approval or control.',
'platform_link': 'Platform structure in detail',
'ops_title': 'Turn purchasing, consumables and labor records into operational insight.',
'ops_body': 'Structure request items and quantities, then review resource-use and cost anomalies relative to production. Machine state and CT are inputs to connect with machining/video analysis—not full manufacturing or accounting cost.',
},
'ar': {
'intro': 'منصة ذكاء اصطناعي للتصنيع تستفيد من معدات المصنع وبياناته القائمة لتنظيم أعمال الإنتاج والجودة والإدارة التي تعتمد على خبرة الأفراد.',
'support': 'نربط مواد العمل والمعايير والقرارات ونتائج المعالجة ليتمكن المسؤول التالي من متابعة العمل مع فهم سياقه.',
'nav': ['المنتجات', 'العروض', 'بنية المنصة', 'الشركة', 'ناقش تجربة ميدانية'],
'run': 'جرّب عارض NC ثلاثي الأبعاد', 'consult': 'ناقش التطبيق في مصنعك', 'details': 'المنتج ونطاق التطبيق',
'work_title': 'الملفات موجودة، لكن المسؤول التالي لا يزال بحاجة إلى السؤال.',
'work_body': 'البحث عن أحدث المعلومات وفهم أسباب القرارات ومتابعة التقدم يتطلب جهداً متكرراً. تساعد المعايير المشتركة ودعم التحليل والحساب والمراجعة على تحويل خبرة الأفراد إلى قدرة تشغيلية للمؤسسة.',
'people': [('تيسير بدء المسؤول الجديد', 'الرجوع إلى مواد العمل وأسباب القرارات السابقة قبل متابعة المهمة التالية.'), ('توجيه الخبرة إلى التحسين', 'تقليل البحث والشرح المتكرر ليتفرغ أصحاب الخبرة للمراجعة والتحسين.'), ('استمرارية العمل والإدارة', 'عرض المهمة والمسؤول والحالة والسجل معاً لدعم تسليم العمل وتوزيعه.')],
'goal': 'فوائد مستهدفة تُقارن في موقع العميل من حيث الدقة وسهولة الاستخدام وجهد العمل؛ وليست ضماناً لخفض العمالة أو نتائج ميدانية مقاسة.',
'products_title': 'ابدأ بالعمل الذي تحتاج إلى تحسينه.',
'products_body': 'أربعة مجالات للذكاء، مع تحديد نطاق التطبيق بحسب العمل الفعلي ومدخلاته ونتائجه.',
'products': [('إعداد التشغيل ومراجعته', 'مقارنة الرسومات وNC والأدوات والقياسات، ومراجعة المسارات وأسباب التعديلات.', 'عرض NC ثلاثي الأبعاد متاح · نموذج وظيفي'), ('الفحص والاستجابة للجودة', 'تنظيم سجلات الفحص والعيوب والخسائر، ومراجعة أولويات العمل وسجل الإجراءات.', 'نموذج وظيفي · التكامل الميداني يحتاج إلى تحقق'), ('المشتريات والمستهلكات وجهد العمل', 'تنظيم الأصناف والكميات المطلوبة وكشف مؤشرات اختلاف الاستخدام والتكلفة بالنسبة إلى الإنتاج.', 'MVP وظيفي · تحقق داخلي'), ('طلبات المواد وتأكيد النقل', 'مراجعة ربط الطلبات والتكليف والنقل وتأكيد الإدخال ضمن سجل الحالة.', 'تكامل نموذج أولي · يحتاج إلى تحقق ميداني')],
'demos_title': 'شاهد المنتج يعمل قبل استعراض بنيته.',
'demos_body': 'نميّز بوضوح بين الوظائف التفاعلية في المتصفح وتسجيلات البرامج الفعلية. هذه عروض منفصلة تستخدم مدخلات مختلفة.',
'live': 'تفاعلي · عينة اصطناعية عامة', 'recorded': 'تسجيل برنامج فعلي · عرض داخلي',
'nc_demo': 'من G-code إلى مسار ثلاثي الأبعاد', 'nc_body': 'تظهر العينة الاصطناعية العامة مباشرة. بدّل الأدوات ودوّر العرض وكبّره أو افحص ملف NC محلياً.',
'ct_demo': 'من فيديو العمل إلى سجل زمني', 'ct_body': 'تسجيل للبرنامج يوضح فترات العمل وزمن الدورة والتشغيل والتوقف ومخطط غانت. وليس خدمة لتحليل فيديو جديد داخل المتصفح.',
'ct_run': 'شاهد عرض تحليل الفيديو', 'nc_alt': 'عارض Flowmatic الفعلي في المتصفح يعرض عينة NC اصطناعية عامة ثلاثية الأبعاد', 'ct_alt': 'لقطة فعلية للبرنامج من فيديو عرض Flowmatic CT القائم',
'workflow_title': 'اربط إعداد التشغيل بالاستجابة للجودة في سياق العمل نفسه.',
'workflow_note': 'سيناريو لربط الأعمال؛ ليس نظاماً متكاملاً مطبقاً لدى عميل، ولا تشخيصاً آلياً أو إرسالاً إلى CNC أو نتيجة ميدانية مقاسة.',
'workflow': [('الخط ← المعدة المختارة', 'تحديد المعدة والمنتج والعملية'), ('مراجعة التشغيل', 'مراجعة الرسم وNC والمسار وإصدارات البرنامج'), ('الحالة والجودة', 'مقارنة الكمية والأبعاد والاهتزاز وأدلة الفحص'), ('المهمة التالية ومسؤولها', 'تسجيل المهمة والمسؤول والموعد والإجراء ونتيجة إعادة الفحص')],
'quality_note': 'مثال لربط اتجاه الاهتزاز وSPC للأبعاد ومعدل العيوب بأدلة الفحص لمراجعة الإجراء التالي. لا يمثل تشخيصاً آلياً للسبب أو نتائج قياس متكاملة للدفعة نفسها.',
'pre_title': 'البنية المناسبة للذكاء الاصطناعي مناسبة أيضاً للإنسان.',
'pre_body': 'بدلاً من تفسير كل ملف من البداية، ننظم المعلومات والحسابات وسجل المعالجة لإعادة استخدامها في المهمة التالية.',
'pre_steps': [('المدخلات الميدانية', 'رسومات · NC · فيديو · سجلات فحص'), ('معالجة Flowmatic المسبقة', 'تنظيم · حساب · إعادة استخدام السجل'), ('استخدام الإنسان والذكاء الاصطناعي', 'أدلة للمراجعة والقرار ومتابعة العمل')],
'pre_note': 'تتوفر هيكلة NC والسجلات المحلية. يتطلب تبادل ملفات USB وربط الذكاء الاصطناعي مزيداً من التنفيذ والتحقق. خفض الرموز ووقت المعالجة هدف يُقاس بشروط متكافئة تشمل المعالجة المسبقة.',
'reuse_title': 'استخدم الأساس نفسه لطلب ميداني مختلف.',
'reuse_body': 'مثال: تجميع المنتجات المتشابهة وإعادة تنظيم خط تشغيل قائم',
'reuse': [('مجموعات المنتجات المرشحة', 'إعادة استخدام تحليل التشغيل ومعايير العمل / إضافة قواعد توافق المثبتات والمعدات'), ('مقارنة التوزيع', 'إعادة استخدام مسارات المواد والتوزيع / إضافة تحويل الرسومات والقيود المكانية'), ('خطة النقل وإعادة التشغيل', 'إعادة استخدام الجودة وقوائم العمل والسجلات / إضافة قواعد الوقت والموارد والموافقة')],
'reuse_note': 'تصور تطبيقي يحدد القدرات القابلة لإعادة الاستخدام والتطوير الإضافي، وليس منتجاً جاهزاً للموافقة الآلية على السلامة أو إعادة التشغيل الفوري.',
'pilot_title': 'خط واحد · مهمة واحدة · مقترح من 4 إلى 8 أسابيع',
'pilot_body': 'نبدأ بمصنّعي قطع السيارات والتشغيل الدقيق الذين يملكون معدات وسجلات قابلة للاستخدام لكن يواجهون عبء التحقق المتكرر وتسليم الأعمال. يُتفق على النطاق والمدة قبل البدء.',
'pilot_steps': [('العمل والمسؤولون', 'تحديد مستخدمي هندسة الإنتاج والجودة والتخطيط، والجهة المخولة بالموافقة في إدارة المصنع أو الشركة.'), ('البيانات وخط الأساس', 'الاتفاق على الوصول إلى البيانات والأمن والاحتفاظ بها وزمن المعالجة الحالي وعبء التحقق المتكرر.'), ('مقارنة من 4 إلى 8 أسابيع', 'مقارنة دقة المهمة نفسها وسهولة استخدامها وجهدها وعبء تسليمها بالأسلوب القائم.'), ('التكلفة الكلية والتوسع', 'احتساب التثبيت والتدريب والدعم ومقارنة خيار توسيع الأنظمة التي يملكها العميل بالفعل.')],
'commercial': 'رسوم لتطبيق العمل ورسوم للاستخدام المستمر. يعتمد العرض على ربط البيانات وإعداد الموقع والتثبيت والتدريب والدعم. يتطلب التوسع إلى أعمال مرتبطة وخطوط مجاورة ومصانع أخرى إعداداً خاصاً بالعميل وتحققاً ميدانياً.',
'contact': 'أخبرنا بالمهمة المتكررة والسجلات المتاحة والفريق المسؤول لتحديد نطاق تقييم من 4 إلى 8 أسابيع لمهمة واحدة في خط واحد وتكلفته الكلية.',
'mach_title': 'حوّل الرسومات وNC إلى عمل يستطيع المسؤول مراجعته.',
'mach_body': 'دعم إعداد التشغيل بمقارنة NC والرسومات والأدوات والقياسات. يمكنك فحص مسار العينة الاصطناعية مباشرة في عرض المتصفح العام.',
'inputs': 'المدخلات', 'outputs': 'النتائج المطلوب مراجعتها', 'scope_title': 'وظائف المتصفح · نطاق البرنامج · التكامل الإضافي',
'scopes': [('المتصفح العام', 'عرض مسارات NC المدعومة والأدوات وأقطارها، مع تقدير مرجعي لزمن الحركات الأساسية.'), ('برنامج التشغيل', 'هيكلة معلومات التشغيل والسجل المحلي وتجميع NC ومراجعته ضمن نطاق برنامج منفصل؛ ليست كلها متاحة في عرض الويب.'), ('التحقق الإضافي', 'تحتاج قراءة الرسومات آلياً وتوليد العملية الكاملة ونقل CNC ومزامنة USB وربط الذكاء الاصطناعي إلى تنفيذ وتحقق مستقل لكل منها.')],
'input_body': 'نص NC · رسومات/هندسة مرجعية · أدوات/شروط تشغيل · قياسات وسجلات تعديل',
'output_body': 'مسارات كل أداة · شروط المراجعة · معلومات التشغيل وسجل التعديل · أساس القرار التالي',
'engineering': 'عرض البنية التقنية وشروط التطبيق التفصيلية',
'example': 'رسم متحرك توضيحي · الأرقام الثابتة أمثلة وليست نتائج تحليل الملف أعلاه.',
'sample_note': 'تظهر عينة اصطناعية عامة تلقائياً، وليست كود إنتاج خاصاً بشركة. لا تُرفع الملفات المحلية إلى الخادم.',
'limits': 'لمراجعة المسار والاسترشاد بالزمن النظري، ولا يحل محل تجارب القطع أو التحقق من التصادم أو اعتماد سلامة المعدة أو التحكم بها.',
'platform_link': 'تفاصيل بنية المنصة',
'ops_title': 'حوّل سجلات المشتريات والمستهلكات وجهد العمل إلى معلومات تشغيلية.',
'ops_body': 'نظّم الأصناف والكميات المطلوبة وراجع اختلاف استخدام الموارد والتكلفة بالنسبة إلى الإنتاج. حالة المعدة وزمن الدورة مدخلات تُربط بتحليل التشغيل والفيديو؛ ولا تمثل تكلفة تصنيع أو تكلفة محاسبية كاملة.',
}}

SLUGS = ('machining-intelligence', 'quality', 'operations-intelligence', 'logistics-intelligence')
NAMES = ('Machining Intelligence', 'Quality Intelligence', 'Operations Intelligence', 'Logistics Intelligence')

def section(lang, ident, title, body='', content='', note=''):
    return f'<section class="wr-section" id="{ident}" aria-labelledby="{ident}-title"><div class="wr-heading"><h2 id="{ident}-title">{e(title)}</h2>{f"<p>{e(body)}</p>" if body else ""}</div>{content}{f"<p class=wr-note>{e(note)}</p>" if note else ""}</section>'

def cards(items, cls='wr-grid-three'):
    return f'<div class="wr-grid {cls}">' + ''.join(f'<article class="wr-card"><span class="wr-number" dir="ltr">{i:02}</span><h3>{e(title)}</h3><p>{e(body)}</p></article>' for i,(title,body) in enumerate(items,1)) + '</div>'

def customer_section(lang):
    t=TEXT[lang]
    return section(lang,'field-problem',t['work_title'],t['work_body'],cards(t['people']),t['goal'])

def products_section(lang):
    t=TEXT[lang]; html='<span id="what-changes" class="wr-anchor" aria-hidden="true"></span><div class="wr-grid wr-grid-four">'
    for i,(slug,name,(title,body,status)) in enumerate(zip(SLUGS,NAMES,t['products'])):
        extra=f'<a class="fm-button primary" href="/{lang}/nc/">{e(t["run"])}</a>' if i==0 else ''
        html+=f'<article class="wr-card wr-product"><p class="wr-label" dir="ltr">{e(name)}</p><h3>{e(title)}</h3><p>{e(body)}</p><p class="wr-status">{e(status)}</p><div class="wr-links"><a href="/{lang}/{slug}/">{e(t["details"])}</a>{extra}</div></article>'
    return section(lang,'products',t['products_title'],t['products_body'],html+'</div>')

def demos_section(lang):
    t=TEXT[lang]
    entries=[('nc',t['live'],t['nc_demo'],t['nc_body'],t['run'],t['nc_alt']),('ct',t['recorded'],t['ct_demo'],t['ct_body'],t['ct_run'],t['ct_alt'])]
    html='<div class="wr-grid wr-grid-two">'
    for slug,badge,title,body,cta,alt in entries:
        src=f'/media/web-release/nc-{lang}.webp' if slug=='nc' else '/media/web-release/ct-program.webp'
        html+=f'<article class="wr-card wr-demo"><a class="wr-preview" href="/{lang}/{slug}/"><img src="{src}" alt="{e(alt)}" width="960" height="600" loading="lazy" decoding="async"></a><div class="wr-demo-copy"><p class="wr-label">{e(badge)}</p><h3>{e(title)}</h3><p>{e(body)}</p><a class="fm-button primary" href="/{lang}/{slug}/">{e(cta)}</a></div></article>'
    return section(lang,'demos',t['demos_title'],t['demos_body'],html+'</div>')

def workflow_section(lang, quality=False):
    t=TEXT[lang]
    return section(lang,'workflow-example',t['workflow_title'],'',cards(t['workflow'],'wr-grid-four wr-workflow'), t['quality_note']+' '+t['workflow_note'] if quality else t['workflow_note'])

def preprocessing_section(lang):
    t=TEXT[lang]
    return section(lang,'preprocessing',t['pre_title'],t['pre_body'],cards(t['pre_steps']),t['pre_note'])

def reuse_section(lang):
    t=TEXT[lang]
    return f'<details class="wr-technical"><summary>{e(t["reuse_title"])}</summary>'+section(lang,'reuse-example',t['reuse_body'],'',cards(t['reuse']),t['reuse_note'])+'</details>'

def pilot_section(lang):
    t=TEXT[lang]
    return section(lang,'pilot',t['pilot_title'],t['pilot_body'],cards(t['pilot_steps'],'wr-grid-four'),t['commercial'])

def machining_overview(lang):
    t=TEXT[lang]
    content=f'<div class="wr-grid wr-grid-two"><article class="wr-card"><h3>{e(t["inputs"])}</h3><p>{e(t["input_body"])}</p><h3>{e(t["outputs"])}</h3><p>{e(t["output_body"])}</p><a class="fm-button primary" href="/{lang}/nc/">{e(t["run"])}</a></article><figure class="wr-card wr-preview"><a href="/{lang}/nc/"><img src="/media/web-release/nc-{lang}.webp" alt="{e(t["nc_alt"])}" width="960" height="600" loading="lazy"></a><figcaption>{e(t["live"])}</figcaption></figure></div>'
    return section(lang,'machining-workflow',t['mach_title'],t['mach_body'],content)+section(lang,'product-scope',t['scope_title'],'',cards(t['scopes']),t['limits'])

def sample_banner(lang):
    t=TEXT[lang]
    return f'<div class="wr-sample-note" data-public-sample-note><p>{e(t["sample_note"])}</p><p>{e(t["limits"])}</p></div>'

def configure(site):
    """Update shared text before rendering; no changes to animation definitions."""
    for lang,t in TEXT.items():
        site['HOME'][lang].update(body=t['intro'],description=t['intro'],support=t['support'],primary=t['run'],secondary=t['consult'],pilot_title=t['pilot_title'],contact_body=t['contact'])
        site['FACTORY_OS_PAGES']['machining-intelligence']['hero'][lang]=t['mach_title']
        site['FACTORY_OS_PAGES']['machining-intelligence']['body'][lang]=t['mach_body']
        site['FACTORY_OS_PAGES']['machining-intelligence']['description'][lang]=t['mach_body']
        site['FACTORY_OS_PAGES']['operations-intelligence']['hero'][lang]=t['ops_title']
        site['FACTORY_OS_PAGES']['operations-intelligence']['body'][lang]=t['ops_body']
        site['DEPLOYMENT_MODES'][0][1][lang]=t['pilot_body']
        site['PRODUCTS']['nc']['description'][lang]=t['nc_body']+' '+t['limits']
        site['PRODUCTS']['nc']['hero_body'][lang]=t['nc_body']
        site['COMPANY_STORY'][lang]['body']=t['intro']+' '+t['support']
    # Assert the translation schema and card counts rather than falling back to Korean.
    expected=set(TEXT['ko'])
    for lang,t in TEXT.items():
        assert set(t)==expected, (lang,expected.symmetric_difference(t))
        assert len(t['products'])==4 and len(t['pilot_steps'])==4 and len(t['nav'])==5
