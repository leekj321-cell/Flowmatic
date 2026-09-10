"""Business-first static website composition. Original animation/viewer code is reused."""
from html import escape as e
from bs4 import BeautifulSoup
RELEASE='2026.09.10-r3'
from pathlib import Path
import json
DECLARATION='|'.join(json.loads((Path(__file__).parent/'homepage-declaration.json').read_text())['lines'])
COPY={k:{} for k in ('ko','en','ar')}
def text(key,ko,en,ar):
    for lang,value in zip(COPY,(ko,en,ar)): COPY[lang][key]=value
text('hero','기존 설비와 데이터로,|제조업무를 시스템화합니다.','Systematize manufacturing work.|Use the equipment and data you have.','نُنظّم أعمال التصنيع،|بالمعدات والبيانات المتاحة لديك.')
text('promise','반복 확인을 줄이고,|경험이 회사에 남게.','Less repeated checking.|Experience that stays with the business.','تكرار أقل في التحقق،|وخبرة تبقى داخل الشركة.')
text('note','사용 가능한 설비와 자료는 살리고, 사람이 이어오던 생산·품질·관리 업무에 필요한 프로그램을 더합니다.','Keep usable equipment and information. Add software that helps people prepare, review and manage production.','نستفيد من المعدات والمعلومات القابلة للاستخدام، ونضيف برامج تدعم العاملين في الإنتاج والجودة والإدارة.')
text('explore','제품 살펴보기','Explore the products','تعرّف على المنتجات')
text('consult','도입 문의','Discuss deployment','ناقش التطبيق')
text('run','공구 경로 3D로 보기','View the toolpath in 3D','اعرض مسار الأداة ثلاثي الأبعاد')
text('nav',['제품','제품 시연','플랫폼 구조','회사','도입 문의'],['Products','Product demonstrations','Platform structure','Company','Contact'],['المنتجات','عروض المنتجات','بنية المنصة','الشركة','تواصل معنا'])
text('problem','자료가 있어도, 업무를 이어받으려면 다시 확인해야 합니다.','The files exist. Taking over the work still means asking again.','الملفات موجودة، لكن تسلّم العمل لا يزال يتطلب السؤال من جديد.')
text('problem_body','최신 자료를 찾고, 이전 판단을 묻고, 진행 상태를 다시 정리하는 일. 자료와 실제 업무 사이의 빈칸을 몇 사람의 기억과 수작업이 메우고 있습니다.','Finding the latest information, understanding past decisions and checking progress still depend on a few people. They bridge the gap between stored information and the work that needs to happen.','البحث عن أحدث المعلومات وفهم القرارات السابقة والتحقق من التقدم يعتمد على عدد قليل من الأشخاص. فهم يسدّون الفجوة بين المعلومات المخزنة والعمل المطلوب.')
text('people',[('“최신 도면이 어느 것입니까?”','새 담당자는 작업을 시작하기 전에 자료를 다시 찾아보고 묻습니다.'),('“이 조건은 왜 바꿨습니까?”','숙련자는 사람에게 남아 있는 판단 근거를 반복해서 설명합니다.'),('“검사는 어디까지 했습니까?”','관리자는 담당자마다 연락해 진행 상태를 모읍니다.')],[('“Which drawing is current?”','A new team member searches and asks again before work can begin.'),('“Why was this setting changed?”','Experienced staff repeat the reasoning when it was never recorded.'),('“How far has inspection progressed?”','Managers contact each person to assemble the current status.')],[('«أي رسم هو الأحدث؟»','يبحث الموظف الجديد ويسأل قبل أن يبدأ العمل.'),('«لماذا تغيّر هذا الإعداد؟»','يكرر أصحاب الخبرة شرح أسباب القرارات التي لم تُسجّل.'),('«إلى أين وصل الفحص؟»','يتواصل المدير مع كل مسؤول لجمع حالة التقدم.')])
text('problem_end','담당자 변경이나 물량·사업장 확대가 있을 때 확인·교육·조정 부담도 함께 커집니다.','Staff changes, higher volumes and more sites increase the burden of checking, training and coordination.','يزداد عبء التحقق والتدريب والتنسيق مع تغيّر الموظفين أو زيادة الإنتاج أو توسّع المواقع.')
text('workflow','자료와 판단, 처리 결과가 다음 업무에 남도록 합니다.','Keep the information, decision and outcome with the work.','نُبقي المعلومات والقرار والنتيجة مع العمل.')
text('workflow_body','자료를 읽고 필요한 결과를 정리한 뒤, 담당자가 검토하고 처리할 업무로 연결합니다. 무엇을 근거로 판단했고 어떻게 처리했는지 다음 담당자가 활용하도록 설계합니다.','Prepare the information and analysis a person needs to review a task. Record what informed the decision and what happened next, so the next person can use it.','نجهّز المعلومات والتحليل اللازمين لمراجعة المهمة، ونحفظ أساس القرار وما جرى بعده ليستفيد منه المسؤول التالي.')
text('workflow_steps',[('자료를 정리합니다','도면·NC·영상·검사기록에서 검토할 정보와 계산 결과를 준비합니다.'),('사람의 판단을 돕습니다','담당자는 근거를 보고 필요한 조치와 책임 범위를 결정합니다.'),('다음 업무로 이어갑니다','처리 결과와 변경 이유를 다시 참고할 기준과 이력으로 남깁니다.')],[('Prepare the information','Organize drawings, NC, video and inspection records for review.'),('Support human judgment','The responsible person reviews the evidence and decides the next action.'),('Carry the result forward','Retain the outcome and the reason for a change for the next task.')],[('تجهيز المعلومات','تنظيم الرسومات وNC والفيديو وسجلات الفحص للمراجعة.'),('دعم الحكم البشري','يراجع المسؤول الأدلة ويقرر الإجراء التالي.'),('نقل النتيجة إلى العمل التالي','حفظ النتيجة وسبب التغيير للرجوع إليهما لاحقًا.')])
text('principle','작동 원리 예시','Illustration of the operating principle','رسم توضيحي لمبدأ العمل')
text('principle_note','현장 신호 → 업무 알림 → 담당자 확인의 연결 원리입니다. 개별 프로그램은 확보했으며, 여러 업무의 현장 연계는 도입 범위에 따라 검증합니다.','Field signal → work notification → human confirmation. Individual applications are available; cross-workflow integration requires deployment-specific validation.','إشارة ميدانية ← تنبيه عمل ← تأكيد المسؤول. التطبيقات الفردية متاحة، أما ربط سير العمل في الموقع فيتطلب التحقق وفق نطاق التطبيق.')
text('products','가공 준비부터 품질 대응까지, 반복 업무를 바꿉니다.','Change recurring work, from machining review to quality response.','تحسين العمل المتكرر، من مراجعة التشغيل إلى الاستجابة للجودة.')
text('products_body','필요한 업무부터 적용하고, 입력 자료·담당자의 판단·처리 결과를 기준으로 적용 범위를 정합니다.','Start with the workflow that matters. Define its inputs, the decisions people make and the results they need.','نبدأ بالعمل المهم، ونحدد مدخلاته والقرارات التي يتخذها الفريق والنتائج المطلوبة.')
text('demos','설명한 업무 변화를 실제 화면에서 확인합니다.','See the working software behind the workflow.','شاهد البرامج العملية التي تدعم سير العمل.')
text('demos_body','가공 프로그램은 공구 경로로, 작업 영상은 시간 기록으로 확인합니다. 서로 다른 입력과 프로그램의 개별 시연입니다.','Review a machining program as a toolpath and a work video as a time record. These are separate demonstrations with different inputs and applications.','راجع برنامج التشغيل كمسار للأداة وفيديو العمل كسجل زمني. هذه عروض منفصلة بمدخلات وتطبيقات مختلفة.')
text('nc_title','문자로 된 가공 프로그램을, 공구 움직임으로 확인합니다.','See how the tool moves—not just the lines of code.','شاهد حركة الأداة، لا أسطر البرنامج فقط.')
text('nc_body','샘플의 공구별 경로를 선택하고 회전·확대하며 검토합니다. 가공 준비·검토 제품 중 브라우저에서 체험할 수 있는 기능입니다.','Select a sample toolpath, rotate the view and zoom in. This browser experience demonstrates one part of machining preparation and review.','اختر مسار أداة من العينة ودوّر العرض وكبّره. هذه التجربة في المتصفح تعرض جزءًا من إعداد التشغيل ومراجعته.')
text('ct_title','작업 영상을, 비교할 수 있는 시간 기록으로 정리합니다.','Turn work video into a time record that can be compared.','حوّل فيديو العمل إلى سجل زمني قابل للمقارنة.')
text('ct_body','작업 구간과 가동·비가동 시간을 영상과 함께 확인하는 실제 프로그램 녹화입니다. 이 페이지에서 새 영상을 분석하는 기능은 아닙니다.','A recording of the actual application showing work intervals and running or idle periods. This page does not analyze a new video.','تسجيل للتطبيق الفعلي يوضح فترات العمل والتشغيل والتوقف مع الفيديو. هذه الصفحة لا تحلل فيديو جديدًا.')
text('capability','한 사람의 경험이, 회사가 반복해서 활용할 수 있는 역량이 됩니다.','Make individual experience reusable across the business.','اجعل خبرة الفرد قابلة لإعادة الاستخدام داخل الشركة.')
text('capability_body','분석·계산·검토로 담당자의 업무 수행을 돕고, 공통 자료와 기준·이력으로 다른 담당자가 이어받을 수 있는 업무를 만듭니다.','Analysis, calculation and review support the person doing the work. Shared information, standards and history help another person take it over.','يدعم التحليل والحساب والمراجعة أداء المسؤول، وتساعد المعلومات والمعايير والسجلات المشتركة شخصًا آخر على تسلّم العمل.')
text('benefits',[('신규 담당자의 업무 적응','필요한 자료와 이전 판단 근거를 찾아보고 업무를 시작합니다.'),('숙련자의 전문역량 활용','반복 정리와 설명보다 검토와 개선에 집중하도록 돕습니다.'),('업무 연속성과 성장 대응','사람이 바뀌고 일이 늘어도 기준과 처리 경험을 조직에 남기는 것이 목표입니다.')],[('Help new team members get started','Find relevant information and reasons for previous decisions.'),('Use expertise for improvement','Focus on review and improvement rather than repeated organization and explanation.'),('Maintain continuity as work grows','Keep standards and experience available when people change or workloads increase.')],[('مساعدة الموظفين الجدد','الوصول إلى المعلومات وأسباب القرارات السابقة.'),('توجيه الخبرة إلى التحسين','التركيز على المراجعة والتحسين بدل تكرار التنظيم والشرح.'),('استمرارية العمل والنمو','إبقاء المعايير والخبرة متاحة عند تغيّر الموظفين أو زيادة العمل.')])
text('benefit_note','원가·품질·납기의 일관성과 업무 부담 개선은 고객 현장의 기존 방식과 비교해 확인할 도입 효과입니다.','Effects on work effort and cost, quality and delivery consistency are deployment goals to compare against the customer’s current process.','تحسين عبء العمل واتساق التكلفة والجودة والتسليم أهداف تُقارن بطريقة العمل الحالية لدى العميل.')
text('assembly','공통 기능을 조합해, 필요한 제조업무로 확장합니다.','Reuse common capabilities across manufacturing workflows.','إعادة استخدام القدرات المشتركة في أعمال تصنيع متعددة.')
text('assembly_body','Flowmatic이 공통 분석 기능과 업무 모듈을 조합합니다. 고객은 개선할 업무를 정하고, 현장별 설정과 추가 연결 범위를 함께 확인합니다.','Flowmatic combines analysis capabilities and workflow modules. Customers choose the work to improve; we define site-specific configuration and additional connections together.','تجمع Flowmatic قدرات التحليل ووحدات العمل. يختار العميل العمل المراد تحسينه، ونحدد معًا إعدادات الموقع والروابط الإضافية.')
text('assembly_steps',[('01 · 흩어진 자료와 기능','설비·제품·공구의 기준과 분석 기능이 따로 놓여 있습니다.'),('02 · 같은 기준으로 연결','공통 기준 위에서 필요한 분석 기능을 연결합니다.'),('03 · 업무 프로그램 구성','담당자가 사용할 작업표준·공구·품질 업무로 구성합니다.'),('04 · 적용 업무 확장','같은 기반을 가공·품질·운영·물류에 활용합니다.')],[('01 · Separate information and tools','Equipment, product and tool references sit apart from analysis capabilities.'),('02 · Shared reference','Connect the required capabilities using the same manufacturing context.'),('03 · Workflow applications','Compose the work standards, tool review and quality tasks people use.'),('04 · Broader use','Apply the same foundation across machining, quality, operations and logistics.')],[('01 · معلومات وأدوات متفرقة','مراجع المعدات والمنتجات والأدوات منفصلة عن قدرات التحليل.'),('02 · مرجع مشترك','ربط القدرات المطلوبة باستخدام سياق التصنيع نفسه.'),('03 · تطبيقات العمل','تكوين معايير العمل ومراجعة الأدوات ومهام الجودة.'),('04 · استخدام أوسع','تطبيق الأساس نفسه على التشغيل والجودة والإدارة واللوجستيات.')])
text('growth','한 업무의 도입에서, 지속 이용과 후속 현장으로.','From a first workflow to recurring use and further sites.','من تطبيق أول إلى استخدام مستمر ومواقع أخرى.')
text('growth_body','공통 기능·연결 방식·설치 절차는 재사용하고, 고객별 설비·품목·업무 기준은 별도로 설정합니다. 고객이 직접 모듈을 조립할 필요는 없습니다.','Reuse common capabilities, connectors and deployment procedures. Configure each customer’s equipment, products and standards separately. Customers do not have to assemble the modules themselves.','نُعيد استخدام القدرات والروابط وإجراءات التطبيق، ونضبط معدات كل عميل ومنتجاته ومعاييره على حدة. لا يحتاج العميل إلى تجميع الوحدات بنفسه.')
text('growth_steps',[('첫 업무','한 라인·한 업무의 유료 적용과 사용 정착'),('관련 업무·인접 라인','같은 기준과 이력을 활용할 업무 확대'),('다른 공장·다음 고객','공통 제품을 재사용하되 설치·지원 공수는 현장에서 확인')],[('First workflow','A paid deployment for one workflow on one line'),('Related work and adjacent lines','Extend the use of shared standards and history'),('Further sites and customers','Reuse the product while measuring actual deployment and support effort')],[('العمل الأول','تطبيق مدفوع لعمل واحد في خط واحد'),('أعمال مرتبطة وخطوط مجاورة','توسيع استخدام المعايير والسجلات المشتركة'),('مواقع وعملاء آخرون','إعادة استخدام المنتج مع قياس جهد التطبيق والدعم الفعلي')])
text('growth_note','사업모델은 업무 도입비와 지속 이용료, 적용 확대에 따른 추가 구축입니다. 반복 설치의 경제성은 후속 현장에서 검증합니다.','The model combines deployment fees, recurring usage fees and additional implementation as scope expands. Repeat-deployment economics require field validation.','يجمع النموذج رسوم التطبيق والاستخدام المستمر والتنفيذ الإضافي عند التوسع. وتتطلب جدوى تكرار التطبيق التحقق الميداني.')
text('pilot','한 업무에서 도입 가치를 확인하고, 필요한 범위로 넓힙니다.','Verify the value in one workflow, then expand where it helps.','تحقّق من القيمة في عمل واحد، ثم توسّع حيث يفيد.')
text('pilot_body','자동차부품·정밀가공 등 제조기업의 한 라인·한 업무부터 시작합니다. 4~8주는 제안 범위이며 자료·연결·교육·지원 조건을 확인해 기간과 총비용을 합의합니다.','Start with one workflow on one line at an automotive-parts or precision-machining manufacturer. Four to eight weeks is a proposal, not a guaranteed schedule. Agree on data, integration, training, support and total cost.','نبدأ بعمل واحد في خط واحد لدى مصنع لقطع السيارات أو التشغيل الدقيق. أربعة إلى ثمانية أسابيع مدة مقترحة وليست مضمونة؛ ويُتفق على البيانات والربط والتدريب والدعم والتكلفة الإجمالية.')
text('contact','현재 가장 번거로운|업무부터 들려주세요.','Tell us which work|takes too much effort.','أخبرنا عن العمل|الذي يستهلك جهدًا كبيرًا.')
text('contact_body','제품명을 정하지 않아도 됩니다. 반복해서 확인하거나 정리하는 업무를 알려주시면, 사용할 자료와 적용 범위를 함께 검토합니다. 투자·사업협력 문의도 같은 창구로 받습니다.','You do not need to choose a product first. Describe the repeated checking or organization and we will review the information and deployment scope with you. Investment and partnership inquiries are also welcome.','لا تحتاج إلى اختيار منتج أولًا. صِف أعمال التحقق أو التنظيم المتكررة لنراجع معك المعلومات ونطاق التطبيق. ونرحّب أيضًا باستفسارات الاستثمار والشراكة.')
text('brief','현재 어려운 업무 또는 문의 내용','Current workflow problem or inquiry','صعوبة العمل الحالية أو موضوع الاستفسار')
text('company','현장 경험이 기업의 운영역량으로 남도록.','Keep field experience inside the business.','إبقاء الخبرة الميدانية داخل الشركة.')
text('company_body','Flowmatic은 제조 현장의 반복 확인·정리·전달 업무에서 출발했습니다. 기존 설비와 자료를 활용하는 업무 프로그램을 바탕으로, 한 업무의 도입과 지속 이용, 후속 현장 확장을 추진합니다.','Flowmatic started with repeated checking, organization and handoffs in manufacturing. We are pursuing initial paid deployments, recurring use and further sites using software built around existing equipment and information.','انطلقت Flowmatic من أعمال التحقق والتنظيم والتسليم المتكررة في التصنيع. نسعى إلى التطبيقات المدفوعة الأولى والاستخدام المستمر والتوسع، ببرامج تستفيد من المعدات والمعلومات الموجودة.')
text('example','업무 흐름 예시 · 고정 수치는 사용 장면을 설명하는 예시입니다.','Workflow illustration. Fixed numbers explain the example; they are not measured results.','رسم توضيحي للعمل. الأرقام الثابتة لشرح المثال وليست نتائج مقاسة.')
text('technical','기술 구조·세부 적용 조건','Technical structure and detailed conditions','البنية التقنية وشروط التطبيق التفصيلية')
text('input','사용할 자료','Information used','المعلومات المستخدمة')
text('output','담당자가 받는 결과','What the team receives','النتائج التي يحصل عليها الفريق')
text('scope','현재 제공 범위와 적용 조건','Current scope and deployment conditions','النطاق الحالي وشروط التطبيق')
text('mach','도면과 가공 프로그램을 함께 검토합니다.','Review the drawing and machining program together.','راجع الرسم وبرنامج التشغيل معًا.')
text('mach_body','도면·NC·공구·가공 조건과 변경 기록을 대조해 가공 준비와 검토를 지원합니다. 3D 체험은 전체 가공 프로그램 중 공구 경로를 확인하는 기능입니다.','Compare drawings, NC, tools, conditions and change records during preparation and review. The 3D experience is the toolpath-viewing component, not the entire machining application.','قارن الرسومات وNC والأدوات والظروف وسجلات التغيير أثناء الإعداد والمراجعة. التجربة ثلاثية الأبعاد مكوّن لعرض المسار، وليست تطبيق التشغيل كاملًا.')
text('nc_hero','샘플 가공 프로그램의|공구 경로를 3D로 확인합니다.','Review a sample machining|toolpath in 3D.','راجع مسار أداة العينة|ثلاثي الأبعاد.')
text('back','가공 준비·검토 제품으로 돌아가기','Back to machining preparation and review','العودة إلى إعداد التشغيل ومراجعته')
text('quality','불량 기록에서, 먼저 처리할 품질 업무까지.','From defect records to the quality work that needs attention first.','من سجلات العيوب إلى مهام الجودة ذات الأولوية.')
text('quality_body','불량 추이·손실·검사 증빙을 함께 검토하고, 개선 우선순위와 후속 업무를 정리합니다. 검사수량 집계에 그치지 않고 무엇부터 처리할지 판단하는 업무를 지원합니다.','Review defect trends, losses and inspection evidence, then organize improvement priorities and follow-up work. Support the decision on what to address, not only the counting of inspections.','راجع اتجاهات العيوب والخسائر وأدلة الفحص، ثم نظّم أولويات التحسين والمتابعة. الهدف دعم قرار ما يجب معالجته، وليس عدّ الفحوص فقط.')
text('quality_steps',[('불량과 손실 확인','기간·품목·공정별 기록을 대조'),('우선 업무 선정','반복 발생과 영향도를 기준으로 검토'),('조치와 담당자 연결','대상·담당·다음 조치를 정리'),('결과와 재발 확인','처리 결과와 이후 발생을 확인')],[('Review defects and losses','Compare records by period, product and process'),('Prioritize the work','Review recurrence and impact'),('Connect the action and assignee','Organize the subject, responsible person and next action'),('Verify and revisit','Check the outcome and subsequent recurrence')],[('مراجعة العيوب والخسائر','مقارنة السجلات حسب الفترة والمنتج والعملية'),('تحديد الأولويات','مراجعة التكرار والأثر'),('ربط الإجراء والمسؤول','تنظيم الموضوع والمسؤول والخطوة التالية'),('التحقق والمتابعة','مراجعة النتيجة وتكرار العيوب لاحقًا')])
text('quality_scope','기능형 프로토타입을 확보했습니다. 우선순위 기준·데이터 연결·후속 업무 범위는 고객의 품질 절차에 맞춰 설정하고 검증합니다. 자동 원인 확정이나 무검토 설비 제어를 제공하는 장면은 아닙니다.','A functional prototype is available. Rules, data connections and follow-up scope require configuration and validation against the customer’s quality process. This is not automatic root-cause confirmation or unreviewed equipment control.','نموذج أولي وظيفي متاح. تتطلب القواعد وربط البيانات ونطاق المتابعة الضبط والتحقق وفق إجراءات جودة العميل. لا يمثل ذلك تأكيدًا آليًا للسبب الجذري أو تحكمًا بالمعدات دون مراجعة.')
text('inspection','검사 기록은 품질 판단의 근거가 됩니다.','Inspection records provide evidence for quality decisions.','سجلات الفحص أدلة تدعم قرارات الجودة.')
text('inspection_body','촬영·판정·집계는 품질 업무에 필요한 입력입니다. 아래 애니메이션은 검사 입력 흐름을 설명하며 실제 불량 추세나 엔진 산출 결과는 아닙니다.','Capture, judgment and counts are inputs to quality work. The animation illustrates inspection input, not an actual defect trend or live engine result.','التصوير والحكم والعدّ مدخلات لأعمال الجودة. يوضح الرسم المتحرك إدخال الفحص، وليس اتجاه عيوب فعليًا أو نتيجة مباشرة للمحرك.')
text('ops','적어둔 메모를 그대로 넣으면 됩니다.','Start with the request note you already have.','ابدأ بملاحظة الطلب الموجودة لديك.')
text('ops_body','품목과 수량은 알아서 정리됩니다. 담당자는 확인이 필요한 항목을 검토하고 발주 요청 업무로 이어갑니다.','Item names and quantities are organized for you. The responsible person reviews uncertain entries and carries the request into purchasing.','تُنظّم أسماء الأصناف والكميات. يراجع المسؤول البنود غير المؤكدة ويتابع طلب الشراء.')
text('ops_example','입력·출력 예시','Illustrative input and output','مثال توضيحي للمدخلات والمخرجات')
text('memo','M8 볼트 30개, 금요일까지 필요','Need 30 M8 bolts by Friday','نحتاج إلى 30 مسمار M8 بحلول الجمعة')
text('fields',[('품목','M8 볼트'),('수량','30개'),('요청 납기','금요일 · 날짜 확인 필요')],[('Item','M8 bolt'),('Quantity','30'),('Requested delivery','Friday — confirm the date')],[('الصنف','مسمار M8'),('الكمية','30'),('موعد التسليم المطلوب','الجمعة — يجب تأكيد التاريخ')])
text('ops_scope','기능형 MVP·내부 검증 단계입니다. 거래처·단가 연결과 발주 양식은 현장 기준에 맞춰 설정하며, 담당자 확인 없이 구매를 확정하거나 자동 발주하지 않습니다.','Functional MVP under internal validation. Supplier and price links and request forms require site-specific configuration. It does not approve purchases or place orders without human review.','منتج أولي وظيفي قيد التحقق الداخلي. تتطلب روابط الموردين والأسعار ونماذج الطلب إعدادًا خاصًا بالموقع. لا يُعتمد الشراء ولا تُرسل الطلبات دون مراجعة بشرية.')
text('resources','사용량과 비용도, 다시 확인할 항목부터.','Find the usage and cost items that need another look.','حدّد بنود الاستخدام والتكلفة التي تحتاج إلى مراجعة.')
text('resources_body','생산량 대비 공구·소모품·공수 사용을 비교해 검토할 이상 후보를 정리합니다. 수집한 항목의 운영비용 분석이며 완전한 제조원가나 회계원가는 아닙니다.','Compare tool, consumable and labor usage against output to identify items for review. This analyzes the operating costs captured, not complete manufacturing or accounting costs.','قارن استخدام الأدوات والمستهلكات والعمل بالإنتاج لتحديد البنود التي تحتاج إلى مراجعة. هذا تحليل للتكاليف التشغيلية المسجلة، وليس للتكلفة التصنيعية أو المحاسبية الكاملة.')
text('logistics','자재 요청부터, 운반과 투입 확인까지.','From a material request to delivery and confirmation.','من طلب المواد إلى التسليم والتأكيد.')
text('logistics_body','누가 무엇을 요청했고, 누구에게 배정됐으며, 현장에 도착했는지 확인하는 물류 업무를 연결합니다. AMR은 이를 수행하는 연계 대상 중 하나입니다.','Connect what was requested, who it was assigned to and whether it reached the line. An AMR is one possible execution endpoint.','اربط ما طُلب ولمن أُسند وما إذا وصل إلى الخط. الروبوت المتنقل المستقل إحدى وسائل التنفيذ الممكن ربطها.')
text('logistics_scope','프로토타입과 업무 연결 구상입니다. 실제 차량·현장 시스템 연결, 공간 제약, 통행·안전 규칙은 현장에서 별도 설정·검증합니다.','Prototype and integration concept. Vehicle and site-system connections, spatial constraints, traffic rules and safety require separate configuration and field validation.','نموذج أولي وتصوّر للربط. تتطلب المركبات وأنظمة الموقع والقيود المكانية وقواعد الحركة والسلامة ضبطًا وتحققًا ميدانيين منفصلين.')
text('platform','한 번 만든 기능을,|여러 제조업무에 활용합니다.','Use common capabilities|across different manufacturing work.','قدرات مشتركة،|لأعمال تصنيع متعددة.')
text('standard','공정 지식을 작업 기준으로 정리합니다.','Turn process knowledge into usable work standards.','نحوّل معرفة العملية إلى معايير عمل قابلة للاستخدام.')
text('standard_body','공정 순서·조건·도면과 확인 항목을 작업자가 참고할 기준으로 정리합니다.','Organize the process sequence, conditions, drawings and checkpoints people need.','تنظيم تسلسل العملية وظروفها ورسوماتها ونقاط التحقق التي يحتاج إليها العاملون.')

def action(url,label,primary=True):
    return f'<a class="fm-button{" primary" if primary else ""}" href="{url}">{e(label)}</a>'
def cards(items,cols=3):
    cls={2:'two',3:'three',4:'four'}[cols]
    return f'<div class="wr-grid wr-grid-{cls}">'+''.join(f'<article class="wr-card"><span class="bn-number">{i+1:02}</span><h3>{e(a)}</h3><p>{e(b)}</p></article>' for i,(a,b) in enumerate(items))+'</div>'
def section(ident,title,body='',content='',note=''):
    return f'<section class="wr-section bn-section" id="{ident}" aria-labelledby="{ident}-title"><div class="wr-section-head"><h2 id="{ident}-title">{e(title)}</h2><p>{e(body)}</p></div>{content}<p class="wr-footnote">{e(note)}</p></section>'
def subhero(title,body,label,cta=''):
    return f'<section class="bn-subhero" aria-labelledby="page-title"><p class="eyebrow">{e(label)}</p><h1 id="page-title">{e(title).replace("|","<br>")}</h1><p class="body-large">{e(body)}</p>{cta}</section>'

def configure(site):
    wr=site['web_release'];wr.RELEASE=RELEASE
    original_product=site['product_page'];original_intelligence=site['intelligence_page'];original_quality=site['quality_status_section']
    for lang,t in COPY.items():
        assert set(t)==set(COPY['ko'])
        x=wr.TEXT[lang]
        x.update(nav=t['nav'],run=t['run'],consult=t['consult'],work_title=t['problem'],work_body=t['problem_body'],people=t['people'],goal=t['problem_end'],products_title=t['products'],products_body=t['products_body'],demos_title=t['demos'],demos_body=t['demos_body'],nc_demo=t['nc_title'],nc_body=t['nc_body'],ct_demo=t['ct_title'],ct_body=t['ct_body'],pilot_title=t['pilot'],pilot_body=t['pilot_body'],example=t['example'],engineering=t['technical'])
        site['HOME'][lang].update(h1=DECLARATION,primary=t['explore'],secondary=t['consult'],contact_title=t['contact'],contact_body=t['contact_body'])
        site['CONTACT_FORM'][lang].update(brief=t['brief'],brief_template='')
        site['HOME_COMPOSITION_COPY'][lang].update(kicker='Flowmatic',title=t['assembly'],body=t['assembly_body'],steps=t['assembly_steps'])
        site['PRODUCTS']['work-standard']['hero'][lang]=t['standard']
        site['PRODUCTS']['work-standard']['hero_body'][lang]=t['standard_body']
        site['PRODUCTS']['work-standard']['description'][lang]=t['standard_body']
    def document(lang,slug,path,body,description=None,extra=''):
        t=COPY[lang];x=wr.TEXT[lang]
        head=site['meta_head'](lang,slug,'Flowmatic | '+t['hero'].replace('|',' '),description or x['intro'],path)
        head=head.replace('</head>',f'<link rel="stylesheet" href="/business-narrative.css?v={RELEASE}"></head>')
        if slug=='nc':head=head.replace('</head>','<link rel="stylesheet" href="/nc-viewer-3d.css?v=2.1"></head>')
        return f'<!doctype html><html lang="{lang}" dir="{site["LANGS"][lang]["dir"]}">{head}<body class="bn-page" data-lang="{lang}" data-static-lang="true">{site["header"](lang,slug)}<main id="main">{body}</main>{site["footer"](lang)}<script src="{site["SCRIPT_SRC"]}"></script>{extra}</body></html>'
    def workflow(lang):
        t=COPY[lang]
        steps=''.join(f'<li><strong>{e(a)}</strong><span>{e(b)}</span></li>' for a,b in t['workflow_steps'])
        return section('workflow',t['workflow'],t['workflow_body'],cards(t['workflow_steps']))
    def operations_motion(lang):
        t=COPY[lang]
        html=site['operations_story_section'](lang).replace('class="field-flow section-grid"','class="field-flow section-grid bn-workflow"')
        visual=site['field_story'](lang)
        return html.replace(visual+'</div>',visual+f'<p class="wr-label">{e(t["principle"])}</p><p class="wr-footnote">{e(t["principle_note"])}</p></div>')
    def composition(lang):
        html=site['home_composition_section'](lang)
        pairs={'ko':('설비상태 · Cycle · 손실 · 예방보전 · 운영판단','발주 요청 · 소모품 · 공수 · 운영비용'),'en':('Machine state · cycle · loss · maintenance · operating decisions','Purchase requests · consumables · labor · operating costs'),'ar':('حالة الآلة · الدورة · الخسارة · الصيانة · القرار','طلبات الشراء · المستهلكات · العمل · التكاليف التشغيلية')}
        a,b=pairs[lang];return html.replace(a,b)
    def growth(lang):
        t=COPY[lang];return section('growth',t['growth'],t['growth_body'],cards(t['growth_steps']),t['growth_note'])
    def demos(lang):
        t=COPY[lang];x=wr.TEXT[lang]
        nc=f'<article class="wr-card wr-demo"><a class="wr-preview" href="/{lang}/nc/"><img src="/media/web-release/nc-{lang}.webp" alt="{e(x["nc_alt"])}" width="960" height="600" loading="lazy"></a><div class="wr-demo-copy"><p class="wr-label">{e(x["live"])}</p><h3>{e(t["nc_title"])}</h3><p>{e(t["nc_body"])}</p>{action(f"/{lang}/nc/",t["run"])}</div></article>'
        ct=f'<article class="wr-card wr-demo"><video controls playsinline preload="none" poster="/media/web-release/ct-program.webp" aria-label="{e(t["ct_title"])}"><source src="/flowmatic_ct_demo.mp4" type="video/mp4"></video><div class="wr-demo-copy"><p class="wr-label">{e(x["recorded"])}</p><h3>{e(t["ct_title"])}</h3><p>{e(t["ct_body"])}</p>{action(f"/{lang}/ct/",x["ct_run"],False)}</div></article>'
        return section('demos',t['demos'],t['demos_body'],'<div class="wr-grid wr-grid-two">'+nc+ct+'</div>')
    def end(lang,slug):
        t=COPY[lang];return '<div class="bn-end-actions">'+action(f'/{lang}/?interest={slug}#contact',t['consult'])+action(f'/{lang}/#products',t['explore'],False)+'</div>'
    def home(lang,path):
        t=COPY[lang];x=wr.TEXT[lang]
        hero=f'<section id="hero" class="hero section-grid bn-hero" aria-labelledby="hero-title"><div class="cell span-7 hero-copy"><p class="eyebrow">Flowmatic</p><h1 id="hero-title" class="hero-title semantic-copy brand-hero-title" lang="en" dir="ltr" data-brand-contract="WEB-019">{site["lines"](DECLARATION)}</h1><p class="body-large bn-definition">{e(x["intro"])}</p><div class="hero-actions">{action("#products",t["explore"])}{action("#contact",t["consult"],False)}</div></div><div class="cell blue span-5 bn-promise"><h2>{e(t["promise"]).replace("|","<br>")}</h2><p>{e(t["note"])}</p></div></section>'
        body=hero+wr.customer_section(lang)+workflow(lang)+wr.products_section(lang)+demos(lang)
        body+=section('capability',t['capability'],t['capability_body'],cards(t['benefits']),t['benefit_note'])+wr.preprocessing_section(lang)+composition(lang)+growth(lang)+wr.pilot_section(lang)
        body+=section('company',t['company'],t['company_body'],action('#contact',t['consult'],False))+site['contact_section'](lang).replace('rows="8"','rows="5"')
        return document(lang,'home',path,body)
    def intelligence(lang,slug,path):
        t=COPY[lang];x=wr.TEXT[lang]
        if slug=='machining-intelligence':
            old=BeautifulSoup(original_intelligence(lang,slug,path),'html.parser');deep=old.select_one('details.wr-technical')
            body=subhero(t['mach'],t['mach_body'],'Machining Intelligence')+wr.machining_overview(lang)+(str(deep) if deep else '')+end(lang,slug)
            return document(lang,slug,path,body,t['mach_body'])
        if slug=='operations-intelligence':
            fields=''.join(f'<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>' for a,b in t['fields'])
            example=f'<div class="wr-grid wr-grid-two"><article class="wr-card"><h3>{e(t["input"])}</h3><blockquote>{e(t["memo"])}</blockquote></article><article class="wr-card"><h3>{e(t["output"])}</h3><dl class="bn-request">{fields}</dl></article></div>'
            body=subhero(t['ops'],t['ops_body'],'Operations Intelligence')+section('request-example',t['ops_example'],'',example,t['ops_scope'])+section('operating-resources',t['resources'],t['resources_body'])+operations_motion(lang)+end(lang,slug)
            return document(lang,slug,path,body,t['ops_body'])
        if slug=='logistics-intelligence':
            body=subhero(t['logistics'],t['logistics_body'],'Logistics Intelligence')+section('material-work',t['scope'],'','',t['logistics_scope'])
            body+=f'<section class="bn-media-section"><p class="wr-label">{e(t["example"])}</p>{site["tech_visual"]("amr",lang)}{action(f"/{lang}/amr/","AMR",False)}</section>'+end(lang,slug)
            return document(lang,slug,path,body,t['logistics_body'])
        if slug=='platform':
            body=subhero(t['platform'],t['assembly_body'],'Flowmatic Platform')+composition(lang)+growth(lang)+workflow(lang)+wr.reuse_section(lang)+end(lang,slug)
            return document(lang,slug,path,body,t['assembly_body'])
        return original_intelligence(lang,slug,path)
    def product(lang,slug,path):
        t=COPY[lang];x=wr.TEXT[lang]
        if slug=='nc':
            back=action(f'/{lang}/machining-intelligence/',t['back'],False)
            body=subhero(t['nc_hero'],t['nc_body'],'Machining Intelligence · 3D',back)+wr.sample_banner(lang)+site['nc_browser_demo_section'](lang)
            body+=section('product-scope',x['scope_title'],'',cards(x['scopes']),x['limits'])+f'<section class="detail-demo section-grid" aria-labelledby="demo-title">{site["demo_panel"](site["PRODUCTS"]["nc"],"nc",lang)}</section>'+end(lang,'machining-intelligence')
            return document(lang,slug,path,body,t['nc_body'],f'<script src="{site["NC_DEMO_SRC"]}"></script><script type="module" src="/nc-viewer-3d.js?v=2.1"></script>')
        if slug=='quality':
            body=subhero(t['quality'],t['quality_body'],'Quality Intelligence')+section('quality-work',t['output'],'',cards(t['quality_steps'],4),t['quality_scope'])
            body+=f'<section class="bn-media-section" id="inspection-evidence"><h2>{e(t["inspection"])}</h2><p>{e(t["inspection_body"])}</p><p class="wr-label">{e(t["example"])}</p>{site["tech_visual"]("quality",lang)}</section><details class="wr-technical"><summary>{e(t["technical"])}</summary>{original_quality(lang)}</details>'+end(lang,slug)
            return document(lang,slug,path,body,t['quality_body'])
        html=original_product(lang,slug,path).replace('</head>',f'<link rel="stylesheet" href="/business-narrative.css?v={RELEASE}"></head>')
        soup=BeautifulSoup(html,'html.parser')
        for node in soup.select('.component-context'):node.decompose()
        for node in soup.select('.detail-animation-head .eyebrow'):node.string={'ko':'업무 흐름 예시','en':'Workflow illustration','ar':'رسم توضيحي لسير العمل'}[lang]
        return str(soup)
    site['home_page']=home;site['intelligence_page']=intelligence;site['product_page']=product
    site['notes']=lambda: '# Website release '+RELEASE+'\n\nCompany proposition -> field problem -> workflow -> products and actual demos -> organizational capability -> reusable information -> composition and expansion -> paid pilot and inquiry.\n\nNC is a scoped machining component, not the company proposition. WEB-019 / RT-022: canonical first-screen English declaration is the primary three-line H1 in all locales. WEB-020 / RT-023: original operational animation belongs only to the Operations page, with an illustrative integration boundary. Original animation scripts, render functions, viewer and video bytes are unchanged.\n\nReview: author content review and browser regression, not independent Strategy Office sign-off or native Arabic proofreading.\n'
