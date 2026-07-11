const header = document.querySelector('[data-header]');
const navToggle = document.querySelector('[data-nav-toggle]');
const nav = document.querySelector('[data-nav]');
const revealTargets = document.querySelectorAll('.reveal');
const productCards = Array.from(document.querySelectorAll('.product-card')).filter((card) => card.querySelector('.product-link'));
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const langButtons = document.querySelectorAll('[data-lang-button]');
const skipLink = document.querySelector('.skip-link');

const LANGUAGE_KEY = 'flowmatic-lang';
const LANGUAGE_LABELS = {
  en: {
    openMenu: 'Open menu',
    closeMenu: 'Close menu',
    skip: 'Skip to content',
    ct: { home: 'HOME', running: 'RUNNING', end: 'END', saved: 'SAVED' },
    amr: ['MONITORING LINE A', 'CALL REQUEST', 'AMR DISPATCHED', 'SUPPLY COMPLETE']
  },
  ko: {
    openMenu: '메뉴 열기',
    closeMenu: '메뉴 닫기',
    skip: '본문으로 건너뛰기',
    ct: { home: '대기', running: '측정중', end: '종료', saved: '저장됨' },
    amr: ['라인 A 감시 중', '호출 요청', 'AMR 배차', '보급 완료']
  },
  ar: {
    openMenu: 'فتح القائمة',
    closeMenu: 'إغلاق القائمة',
    skip: 'تجاوز إلى المحتوى',
    ct: { home: 'الوضع الأساسي', running: 'قيد القياس', end: 'النهاية', saved: 'محفوظ' },
    amr: ['مراقبة الخط A', 'طلب استدعاء', 'تم إرسال AMR', 'اكتمل التزويد']
  }
};

const SUPPORTED_LANGUAGES = new Set(['ko', 'en', 'ar']);

const ARABIC_TRANSLATIONS = Object.freeze({
  '01 · LOAD TOOL': '01 · تحميل الأداة',
  '02 · CHECK SURFACE': '02 · فحص السطح',
  '03 · CONFIRM RESULT': '03 · تأكيد النتيجة',
  '1 · IDENTIFY THE TOOL': '1 · تعريف الأداة',
  '1 · MATERIAL RUNS LOW': '1 · انخفاض المواد',
  '1 · PROCESS + TOOL DATA': '1 · بيانات العملية والأداة',
  '1 · READ THE CODE': '1 · قراءة الكود',
  '1 · WATCH THE REFERENCE AREA': '1 · مراقبة منطقة المرجع',
  '2 · ALERT THE OPERATOR': '2 · تنبيه المشغّل',
  '2 · DETECT START / END': '2 · اكتشاف البداية / النهاية',
  '2 · MATCH THE PROCESS': '2 · مطابقة العملية',
  '2 · OPERATOR VIEW': '2 · عرض المشغّل',
  '2 · REBUILD THE MOTION': '2 · إعادة بناء الحركة',
  '3 · BUILD THE TIMELINE': '3 · بناء الخط الزمني',
  '3 · DISPATCH THE AMR': '3 · إرسال AMR',
  '3 · REVIEW BEFORE CUTTING': '3 · المراجعة قبل القطع',
  '3 · STEP-BY-STEP GUIDE': '3 · دليل خطوة بخطوة',
  '3 · UPDATE THE RECORD': '3 · تحديث السجل',
  'A factory does not need one more system. It needs operations to flow.': 'المصنع لا يحتاج إلى نظام آخر. بل يحتاج إلى أن تتدفق العمليات.',
  'A fixed camera detects cycle events. The timeline is built automatically.': 'كاميرا ثابتة تكتشف أحداث الدورة. ويتم بناء الخط الزمني تلقائياً.',
  'ACKNOWLEDGE': 'تأكيد',
  'ACTION': 'إجراء',
  'ACTION IN': 'الإجراء جاهز',
  'ALERT': 'تنبيه',
  'Act': 'تصرّف',
  'Alert the right person.': 'أبلغ الشخص المناسب.',
  'An intelligence layer for the factory': 'طبقة ذكاء للمصنع',
  'Approach': 'النهج',
  'Automate repetition. Keep approval and exceptions human.': 'أتمت التكرار. واترك الموافقة والاستثناءات للإنسان.',
  'Bring clarity to the factory you already run.': 'أضف وضوحاً إلى المصنع الذي تديره بالفعل.',
  'Bring risky tool moves out of the code and into view.': 'أخرج حركات الأداة الخطرة من الكود واجعلها مرئية.',
  'Bring tools, paths, posture, and sequence into one scene.': 'اجمع الأدوات والمسارات والوضعية والتسلسل في مشهد واحد.',
  'Build on what works.': 'ابنِ على ما يعمل.',
  'Build time data.': 'ابنِ بيانات الوقت.',
  'CALL': 'استدعاء',
  'CAMERA': 'كاميرا',
  'CHECK RAPID MOVE': 'تحقق من الحركة السريعة',
  'CLOSED': 'مغلق',
  'CONFIRM THE RESPONSE': 'تأكيد الاستجابة',
  'CREATE AN EVENT': 'إنشاء حدث',
  'CYCLE COMPLETE': 'اكتملت الدورة',
  'Call material before the line waits.': 'استدعِ المواد قبل أن ينتظر الخط.',
  'Call material before waiting.': 'استدعِ المواد قبل الانتظار.',
  'Check cycle time and risky moves before the machine runs.': 'تحقق من زمن الدورة والحركات الخطرة قبل تشغيل الماكينة.',
  'Close the loop with a verified response.': 'أغلق الحلقة باستجابة موثقة.',
  'Collect camera, NC, and operator signals.': 'اجمع إشارات الكاميرا وNC والمشغّل.',
  'Confirm': 'تأكيد',
  'Confirm supply completion and close the event state.': 'أكد اكتمال التزويد وأغلق حالة الحدث.',
  'Confirm the result.': 'أكد النتيجة.',
  'Connect every tool to its process.': 'اربط كل أداة بعمليتها.',
  'Connect material demand to an operator alert and AMR dispatch.': 'اربط طلب المواد بتنبيه المشغّل وإرسال AMR.',
  'Connect one next action.': 'اربط إجراءً تالياً واحداً.',
  'Contact': 'تواصل',
  'Contact Flowmatic': 'تواصل مع Flowmatic',
  'DATA IN': 'إدخال البيانات',
  'DEPOT': 'المستودع',
  'Delay · Risk · Demand': 'تأخير · خطر · طلب',
  'Demo coming soon': 'العرض التجريبي قريباً',
  'Design Principle': 'مبدأ التصميم',
  'Detect demand and alert the operator. Dispatch the AMR before shortage becomes downtime.': 'اكتشف الطلب ونبّه المشغّل. أرسل AMR قبل أن يتحول النقص إلى توقف.',
  'Detect demand.': 'اكتشف الطلب.',
  'Detect start and finish from changes in field movement.': 'اكتشف البداية والنهاية من تغيرات حركة الميدان.',
  'Detect the cycle boundary.': 'اكتشف حدود الدورة.',
  'Different tools. One event language.': 'أدوات مختلفة. لغة أحداث واحدة.',
  'Dispatch and close the loop.': 'أرسل وأغلق الحلقة.',
  'Do not bend the field to the system. Fit the system to the field.': 'لا تُخضع الميدان للنظام. اجعل النظام يناسب الميدان.',
  'END': 'النهاية',
  'EVENT': 'حدث',
  'EVENT CLOSED': 'تم إغلاق الحدث',
  'EVENT IN': 'الحدث وارد',
  'Each product pairs a clear animation with a real demo.': 'كل منتج يجمع بين حركة توضيحية واضحة وعرض عملي حقيقي.',
  'Eventize': 'حوّل إلى أحداث',
  'Explore AMR Calling': 'استكشف استدعاء AMR',
  'Explore CT': 'استكشف CT',
  'Explore NC': 'استكشف NC',
  'Explore TMS': 'استكشف TMS',
  'Explore Work Standard': 'استكشف معيار العمل',
  'Extract tools, feeds, coordinates, and index moves.': 'استخرج الأدوات والتغذيات والإحداثيات وحركات الفهرسة.',
  'FACE / CHAMFER': 'تسوية / شطف',
  'FIELD DATA': 'بيانات الميدان',
  'FLOWMATIC OPERATOR': 'مشغّل Flowmatic',
  'Feed the verified response into the next decision.': 'أدخل الاستجابة الموثقة في القرار التالي.',
  'Field-first Engineering': 'هندسة تبدأ من الميدان',
  'Find and confirm the corresponding process record.': 'اعثر على سجل العملية المقابل وأكده.',
  'Find the delay while there is still time to respond.': 'اكتشف التأخير بينما لا يزال هناك وقت للاستجابة.',
  'Flowmatic Products': 'منتجات Flowmatic',
  'Flowmatic coordinates people, machines, tools, and material. People stay in command.': 'ينسق Flowmatic بين الأشخاص والآلات والأدوات والمواد. ويبقى الإنسان صاحب القرار.',
  'Follow the flow': 'اتبع التدفق',
  'From Smart Factory to Flow Factory.': 'من المصنع الذكي إلى مصنع التدفق.',
  'GUIDE': 'دليل',
  'Gather the process context.': 'اجمع سياق العملية.',
  'Give operational meaning to repeated movement.': 'أعطِ الحركة المتكررة معنى تشغيلياً.',
  'Guide the next step.': 'وجّه الخطوة التالية.',
  'HOME ROI': 'منطقة المرجع ROI',
  'Home': 'الرئيسية',
  'How Flowmatic Works': 'كيف يعمل Flowmatic',
  'How it works': 'طريقة العمل',
  'Identify the physical tool and match the process. Keep life and stock information aligned.': 'عرّف الأداة الفعلية وطابق العملية. حافظ على توافق معلومات العمر والمخزون.',
  'Identify the physical tool.': 'عرّف الأداة الفعلية.',
  'Integrate naturally. Prove value step by step.': 'ادمج بشكل طبيعي. وأثبت القيمة خطوة بخطوة.',
  'Intelligence should fit the field.': 'يجب أن يناسب الذكاء أرض الواقع.',
  'Keep people in command.': 'أبقِ الإنسان صاحب القرار.',
  'Keep the equipment, workflow, and experience that already create value.': 'حافظ على المعدات وسير العمل والخبرة التي تصنع القيمة بالفعل.',
  'Keep the record current.': 'حافظ على السجل محدثاً.',
  'Keep tool identity, life, stock, and location in one operating record.': 'اجمع هوية الأداة وعمرها ومخزونها وموقعها في سجل تشغيلي واحد.',
  'Keep what already works. Add the intelligence it needs.': 'أبقِ ما يعمل بالفعل. وأضف الذكاء الذي يحتاجه.',
  'LIFE': 'العمر',
  'LINE': 'الخط',
  'LINE A': 'الخط A',
  'LOAD': 'تحميل',
  'LOCATION': 'الموقع',
  'MACHINE': 'تشغيل',
  'MATCHED': 'مطابق',
  'MATERIAL LOW': 'المواد منخفضة',
  'Make expert judgment easier to share and repeat.': 'اجعل حكم الخبير أسهل في المشاركة والتكرار.',
  'Make it visible first. Connect one action next. Automate after the value is proven.': 'اجعله مرئياً أولاً. اربط إجراءً واحداً تالياً. ثم أتمت بعد إثبات القيمة.',
  'Make the event visible and reliable before automating the response.': 'اجعل الحدث مرئياً وموثوقاً قبل أتمتة الاستجابة.',
  'Make the next action clear.': 'اجعل الإجراء التالي واضحاً.',
  'Match it to the process.': 'طابقه مع العملية.',
  'Maximum clarity.': 'أقصى وضوح.',
  'Measure every cycle. Automatically.': 'قِس كل دورة. تلقائياً.',
  'Measure the cycle from the motion.': 'قِس الدورة من الحركة.',
  'Minimal intervention.': 'أقل تدخل.',
  'NC CODE': 'كود NC',
  'NC, CT, Operator, TMS, and AMR are modules in one operating flow—not isolated screens.': 'NC وCT وOperator وTMS وAMR وحدات ضمن تدفق تشغيلي واحد، لا شاشات معزولة.',
  'Not another screen. A flow from field events to the next action.': 'ليست شاشة أخرى. بل تدفق من أحداث الميدان إلى الإجراء التالي.',
  'OPERATOR': 'المشغّل',
  'OPERATOR ACK': 'تأكيد المشغّل',
  'OPERATORACK': 'تأكيد المشغّل',
  'Observe': 'راقب',
  'Observe before automating.': 'راقب قبل الأتمتة.',
  'Observe repeated positions with a fixed camera and ROI.': 'راقب المواضع المتكررة بكاميرا ثابتة ومنطقة ROI.',
  'Observe the field.': 'راقب الميدان.',
  'Observe → Eventize Coordinate → Learn': 'راقب → حوّل إلى أحداث نسّق → تعلّم',
  'One Flow': 'تدفق واحد',
  'One field event. One clear next action.': 'حدث ميداني واحد. إجراء تالٍ واضح واحد.',
  'One operating logic. Many field events.': 'منطق تشغيل واحد. أحداث ميدانية كثيرة.',
  'Open menu': 'فتح القائمة',
  'Operating Logic': 'منطق التشغيل',
  'Operating sequence': 'تسلسل التشغيل',
  'Operational Intelligence Layer': 'طبقة ذكاء تشغيلي',
  'PATH RISK': 'خطر المسار',
  'PROCESS · OP20': 'العملية · OP20',
  'Parse the NC program.': 'حلّل برنامج NC.',
  'Present the information in the order the work is performed.': 'اعرض المعلومات وفق ترتيب تنفيذ العمل.',
  'Product demo': 'عرض المنتج',
  'Production keeps moving. Decisions arrive late.': 'يستمر الإنتاج في الحركة. وتصل القرارات متأخرة.',
  'Products': 'المنتجات',
  'Put guidance at the point of work.': 'ضع الإرشاد في نقطة العمل.',
  'READ THE FIELD': 'قراءة الميدان',
  'REVIEW': 'مراجعة',
  'Read': 'اقرأ',
  'Read movement and inputs from the work itself.': 'اقرأ الحركة والمدخلات من العمل نفسه.',
  'Read the code and rebuild the motion. Review the path before the machine runs.': 'اقرأ الكود وأعد بناء الحركة. راجع المسار قبل تشغيل الماكينة.',
  'Read the field as it moves.': 'اقرأ الميدان أثناء حركته.',
  'Read the tool identity from a label or photo.': 'اقرأ هوية الأداة من ملصق أو صورة.',
  'Reconstruct the motion.': 'أعد بناء الحركة.',
  'Reframe it for the operator.': 'أعد صياغته للمشغّل.',
  'Request a demo': 'اطلب عرضاً تجريبياً',
  'Review before cutting.': 'راجع قبل القطع.',
  'Route each event to an alert, guide, call, or review.': 'وجّه كل حدث إلى تنبيه أو دليل أو استدعاء أو مراجعة.',
  'SELECT THE NEXT ACTION': 'اختيار الإجراء التالي',
  'START': 'البداية',
  'STOCK': 'المخزون',
  'SUPPLY COMPLETE': 'اكتمل التزويد',
  'See AMR Calling in action.': 'شاهد استدعاء AMR أثناء العمل.',
  'See Flowmatic CT in action.': 'شاهد Flowmatic CT أثناء العمل.',
  'See Flowmatic NC in action.': 'شاهد Flowmatic NC أثناء العمل.',
  'See Flowmatic TMS in action.': 'شاهد Flowmatic TMS أثناء العمل.',
  'See Work Standard in action.': 'شاهد معيار العمل أثناء التطبيق.',
  'See cycle loss sooner.': 'اكتشف فقد الدورة مبكراً.',
  'See risk before cutting.': 'شاهد المخاطر قبل القطع.',
  'See the toolpath before cutting.': 'شاهد مسار الأداة قبل القطع.',
  'See what happened. Know what comes next.': 'اعرف ما حدث. واعرف ما يأتي بعده.',
  'Share demand before the line begins to wait.': 'شارك الطلب قبل أن يبدأ الخط بالانتظار.',
  'Show the next check and action at the right moment.': 'اعرض الفحص والإجراء التاليين في اللحظة المناسبة.',
  'Show the right tool, path, posture, and next step. Keep the view aligned with the operator.': 'اعرض الأداة والمسار والوضعية والخطوة التالية الصحيحة. واجعل العرض متوافقاً مع المشغّل.',
  'Show the target line and the required action clearly.': 'اعرض الخط المستهدف والإجراء المطلوب بوضوح.',
  'Show where the tool moves and in what order.': 'اعرض أين تتحرك الأداة وبأي ترتيب.',
  'Show who needs to do what, now.': 'اعرض من يحتاج إلى فعل ماذا الآن.',
  'Skip to content': 'تجاوز إلى المحتوى',
  'Start with the line as it is. Keep the equipment, workflow, and people in the picture.': 'ابدأ من الخط كما هو. أبقِ المعدات وسير العمل والأشخاص ضمن الصورة.',
  'TOOL · END MILL': 'الأداة · قاطع نهائي',
  'TOOLS': 'الأدوات',
  'The Gap': 'الفجوة',
  'The field never stops. Important events and the next action often appear too late.': 'الميدان لا يتوقف. وغالباً ما تظهر الأحداث المهمة والإجراء التالي متأخرين.',
  'The field should not bend to the system. The system should fit the field.': 'لا ينبغي أن ينحني الميدان للنظام. بل يجب أن يناسب النظام الميدان.',
  'Turn G-code into visible motion, cycle time, and review points.': 'حوّل G-code إلى حركة مرئية وزمن دورة ونقاط مراجعة.',
  'Turn detected events into cycle time and a process timeline.': 'حوّل الأحداث المكتشفة إلى زمن دورة وخط زمني للعملية.',
  'Turn each event into a clear guide, alert, call, or review.': 'حوّل كل حدث إلى دليل أو تنبيه أو استدعاء أو مراجعة واضحة.',
  'Turn field events into the next action.': 'حوّل أحداث الميدان إلى الإجراء التالي.',
  'Turn know-how into a shared standard.': 'حوّل الخبرة العملية إلى معيار مشترك.',
  'Turn process knowledge into a clear, step-by-step operator view.': 'حوّل معرفة العملية إلى عرض واضح للمشغّل خطوة بخطوة.',
  'Turn process knowledge into clear guidance.': 'حوّل معرفة العملية إلى إرشاد واضح.',
  'Turn raw signals into operational events.': 'حوّل الإشارات الخام إلى أحداث تشغيلية.',
  'Turn repeated camera motion into cycle events and time data.': 'حوّل الحركة المتكررة في الكاميرا إلى أحداث دورة وبيانات زمنية.',
  'Turn signals into events.': 'حوّل الإشارات إلى أحداث.',
  'Turn stock signals or call inputs into a material-demand event.': 'حوّل إشارات المخزون أو مدخلات الاستدعاء إلى حدث طلب مواد.',
  'UNLOAD': 'تفريغ',
  'Understand the field first. Change only what matters.': 'افهم الميدان أولاً. وغيّر فقط ما يهم.',
  'Update life, stock, location, and usage together.': 'حدّث العمر والمخزون والموقع والاستخدام معاً.',
  'Vision': 'الرؤية',
  'Watch a material alert move from detection to completion.': 'شاهد تنبيه المواد ينتقل من الاكتشاف إلى الإكمال.',
  'Watch a physical tool become connected operational data.': 'شاهد الأداة الفعلية تتحول إلى بيانات تشغيلية متصلة.',
  'Watch a reference area.': 'راقب منطقة مرجعية.',
  'Watch cycle events turn into measured time data.': 'شاهد أحداث الدورة تتحول إلى بيانات زمنية مقاسة.',
  'Watch how the product works in a real machining workflow.': 'شاهد كيف يعمل المنتج ضمن سير عمل تصنيع حقيقي.',
  'Watch process information become step-by-step work guidance.': 'شاهد معلومات العملية تتحول إلى إرشاد عمل خطوة بخطوة.',
  'What is really happening': 'ما يحدث فعلاً',
  'already working well.': 'الذي يعمل بكفاءة بالفعل.',
  '← All products': '← كل المنتجات'
});

function getCurrentLanguage() {
  return document.body.dataset.lang || 'ko';
}

function normalizeLanguageText(element) {
  const copyLines = element.querySelectorAll('.copy-line');
  if (copyLines.length) {
    return Array.from(copyLines).map((line) => line.textContent.trim()).join(' ').replace(/\s+/g, ' ').trim();
  }
  return element.textContent.replace(/\s+/g, ' ').trim();
}

function splitArabicCopy(text, preferredLineCount) {
  const explicitLines = text.split('|').map((line) => line.trim()).filter(Boolean);
  if (explicitLines.length > 1 || preferredLineCount <= 1) return explicitLines;
  const words = text.split(/\s+/).filter(Boolean);
  if (words.length <= preferredLineCount) return words;
  const lines = [];
  const wordsPerLine = Math.ceil(words.length / preferredLineCount);
  for (let i = 0; i < preferredLineCount; i += 1) {
    const start = i * wordsPerLine;
    const end = i === preferredLineCount - 1 ? words.length : start + wordsPerLine;
    const line = words.slice(start, end).join(' ');
    if (line) lines.push(line);
  }
  return lines;
}

function createArabicSpan(source, translation) {
  const span = document.createElement('span');
  span.className = Array.from(source.classList)
    .map((className) => (className === 'lang-en' ? 'lang-ar' : className))
    .join(' ');
  span.lang = 'ar';
  span.dir = 'rtl';
  const sourceLines = source.querySelectorAll('.copy-line');
  if (source.classList.contains('copy-lines') || sourceLines.length) {
    const lineCount = Math.max(sourceLines.length, 1);
    splitArabicCopy(translation, lineCount).forEach((line) => {
      const lineSpan = document.createElement('span');
      lineSpan.className = 'copy-line';
      lineSpan.textContent = line;
      span.appendChild(lineSpan);
    });
  } else {
    span.textContent = translation.replace(/\s*\|\s*/g, ' ');
  }
  return span;
}

function initArabicLanguageSpans() {
  document.querySelectorAll('.lang-en').forEach((source) => {
    const key = normalizeLanguageText(source);
    const translation = ARABIC_TRANSLATIONS[key];
    if (!translation || source.parentElement?.querySelector(':scope > .lang-ar')) return;
    const arabicSpan = createArabicSpan(source, translation);
    const koreanSibling = source.nextElementSibling?.classList.contains('lang-ko') ? source.nextElementSibling : null;
    (koreanSibling || source).after(arabicSpan);
  });
}

function setToggleLabel(isOpen) {
  if (!navToggle) return;
  const label = navToggle.querySelector('.sr-only');
  const lang = getCurrentLanguage();
  const text = isOpen ? LANGUAGE_LABELS[lang].closeMenu : LANGUAGE_LABELS[lang].openMenu;
  if (label) label.textContent = text;
}

function applyLanguage(lang) {
  const safeLang = SUPPORTED_LANGUAGES.has(lang) ? lang : 'ko';
  document.body.dataset.lang = safeLang;
  document.documentElement.lang = safeLang;
  document.documentElement.dir = safeLang === 'ar' ? 'rtl' : 'ltr';
  localStorage.setItem(LANGUAGE_KEY, safeLang);
  langButtons.forEach((button) => button.classList.toggle('is-active', button.dataset.langButton === safeLang));
  if (skipLink) skipLink.textContent = LANGUAGE_LABELS[safeLang].skip;
  setToggleLabel(document.body.classList.contains('nav-open'));
  scheduleSemanticFit();
}

function updateHeaderState() {
  if (!header) return;
  header.classList.toggle('is-scrolled', window.scrollY > 16 || document.body.classList.contains('technology-page'));
}

function closeNav() {
  document.body.classList.remove('nav-open');
  if (!navToggle) return;
  navToggle.setAttribute('aria-expanded', 'false');
  setToggleLabel(false);
}

function toggleNav() {
  if (!navToggle) return;
  const isOpen = document.body.classList.toggle('nav-open');
  navToggle.setAttribute('aria-expanded', String(isOpen));
  setToggleLabel(isOpen);
}

function initReveal() {
  if (prefersReducedMotion || !('requestAnimationFrame' in window)) {
    revealTargets.forEach((target) => target.classList.add('is-visible'));
    return;
  }
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.14, rootMargin: '0px 0px -8% 0px' });
  revealTargets.forEach((target) => observer.observe(target));
}

function initProductCtas() {
  if (!productCards.length) return;
  if (prefersReducedMotion || !('IntersectionObserver' in window)) {
    productCards.forEach((card) => {
      const link = card.querySelector('.product-link');
      if (!link) return;
      card.classList.add('is-cta-active');
      link.style.setProperty('--cta-progress', '1');
      link.style.setProperty('--cta-click-offset', '0%');
      link.style.setProperty('--cta-mondrian-offset', '0%');
      link.style.setProperty('--cta-left-padding', 'calc(var(--cta-click-width) + 14px)');
      link.style.setProperty('--cta-right-padding', '58px');
    });
    return;
  }
  let isScheduled = false;
  const smoothStep = (value) => value * value * (3 - (2 * value));
  const getLayoutTop = (element) => {
    let top = 0;
    let node = element;
    while (node) {
      top += node.offsetTop;
      node = node.offsetParent;
    }
    return top;
  };
  const getRows = () => {
    const rows = [];
    productCards.forEach((card) => {
      const link = card.querySelector('.product-link');
      if (!link) return;
      const top = getLayoutTop(card);
      let row = rows.find((item) => Math.abs(item.top - top) < 8);
      if (!row) {
        row = { top, items: [] };
        rows.push(row);
      }
      row.items.push({ card, link });
    });
    return rows;
  };
  const setCtaState = (card, link, progress) => {
    const rect = link.getBoundingClientRect();
    const clickWidth = Math.max(82, Math.min(rect.width * 0.32, 132));
    link.style.setProperty('--cta-progress', progress.toFixed(3));
    link.style.setProperty('--cta-click-offset', `${(-100 + (progress * 100)).toFixed(2)}%`);
    link.style.setProperty('--cta-mondrian-offset', `${(100 - (progress * 100)).toFixed(2)}%`);
    link.style.setProperty('--cta-left-padding', `${(16 + (progress * (clickWidth - 2))).toFixed(2)}px`);
    link.style.setProperty('--cta-right-padding', `${(16 + (progress * 42)).toFixed(2)}px`);
    card.classList.toggle('is-cta-active', progress >= 0.995);
  };
  const updateCtas = () => {
    isScheduled = false;
    const startY = window.innerHeight * 0.3;
    const completeY = window.innerHeight * 0.1;
    const travel = Math.max(startY - completeY, 1);
    const scrollY = window.scrollY || document.documentElement.scrollTop || 0;
    getRows().forEach((row) => {
      const rowBottom = Math.max(...row.items.map(({ card }) => getLayoutTop(card) + card.offsetHeight));
      const centerY = rowBottom - 32 - scrollY;
      const rawProgress = (startY - centerY) / travel;
      const progress = smoothStep(Math.min(Math.max(rawProgress, 0), 1));
      row.items.forEach(({ card, link }) => setCtaState(card, link, progress));
    });
  };
  const requestUpdate = () => {
    if (isScheduled) return;
    isScheduled = true;
    requestAnimationFrame(updateCtas);
  };
  window.addEventListener('scroll', requestUpdate, { passive: true });
  window.addEventListener('resize', requestUpdate);
  window.addEventListener('flowmatic:layout-change', requestUpdate);
  updateCtas();
}

function initNavigation() {
  if (navToggle) navToggle.addEventListener('click', toggleNav);
  if (nav) nav.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeNav));
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') closeNav();
  });
}

function initLanguageToggle() {
  const saved = localStorage.getItem(LANGUAGE_KEY);
  const initial = SUPPORTED_LANGUAGES.has(saved) ? saved : 'ko';
  applyLanguage(initial);
  langButtons.forEach((button) => {
    button.addEventListener('click', () => applyLanguage(button.dataset.langButton));
  });
}

function initDemoVideos() {
  const players = document.querySelectorAll('[data-demo-video]');
  players.forEach((player) => {
    const video = player.querySelector('video');
    const placeholder = player.querySelector('[data-video-placeholder]');
    const base = player.dataset.videoBase;
    if (!video || !base) return;
    const candidates = [`${base}.mp4`, `${base}.webm`, `${base}.mov`];
    let candidateIndex = 0;
    let settled = false;
    const showVideo = () => {
      if (settled) return;
      settled = true;
      player.classList.add('has-video');
      video.hidden = false;
      if (placeholder) placeholder.hidden = true;
    };
    const tryNext = () => {
      if (settled) return;
      if (candidateIndex >= candidates.length) {
        video.removeAttribute('src');
        video.load();
        return;
      }
      const candidate = candidates[candidateIndex];
      candidateIndex += 1;
      const onLoaded = () => { cleanup(); showVideo(); };
      const onError = () => { cleanup(); tryNext(); };
      const cleanup = () => {
        video.removeEventListener('loadedmetadata', onLoaded);
        video.removeEventListener('canplay', onLoaded);
        video.removeEventListener('error', onError);
      };
      video.addEventListener('loadedmetadata', onLoaded, { once: true });
      video.addEventListener('canplay', onLoaded, { once: true });
      video.addEventListener('error', onError, { once: true });
      video.src = candidate;
      video.load();
    };
    tryNext();
  });
}

function formatCycleTime(seconds) {
  const safe = Math.max(0, seconds);
  const whole = Math.floor(safe);
  const tenth = Math.floor((safe - whole) * 10);
  return `00:${String(whole).padStart(2, '0')}.${tenth}`;
}

function initCtExplainer() {
  const visual = document.querySelector('[data-tech-animation="ct"]');
  if (!visual || prefersReducedMotion) return;
  const timer = visual.querySelector('[data-ct-timer]');
  const state = visual.querySelector('[data-ct-state]');
  const result = visual.querySelector('[data-ct-result]');
  const loopDuration = 4800;
  const measuredCycle = 12.4;
  const start = performance.now();
  function tick(now) {
    const phase = (now - start) % loopDuration;
    const lang = getCurrentLanguage();
    const labels = LANGUAGE_LABELS[lang].ct;
    if (phase < 700) {
      if (state) state.textContent = labels.home;
      if (timer) timer.textContent = '00:00.0';
    } else if (phase < 3900) {
      const progress = (phase - 700) / 3200;
      if (state) state.textContent = labels.running;
      if (timer) timer.textContent = formatCycleTime(progress * measuredCycle);
    } else if (phase < 4450) {
      if (state) state.textContent = labels.end;
      if (timer) timer.textContent = formatCycleTime(measuredCycle);
      if (result) result.textContent = `${measuredCycle.toFixed(1)} s`;
    } else {
      if (state) state.textContent = labels.saved;
      if (timer) timer.textContent = formatCycleTime(measuredCycle);
    }
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

function initAmrExplainer() {
  const visual = document.querySelector('[data-tech-animation="amr"]');
  if (!visual || prefersReducedMotion) return;
  const message = visual.querySelector('[data-amr-message]');
  if (!message) return;
  const loopDuration = 5000;
  const start = performance.now();
  function tick(now) {
    const phase = (now - start) % loopDuration;
    const labels = LANGUAGE_LABELS[getCurrentLanguage()].amr;
    if (phase < 2100) message.textContent = labels[0];
    else if (phase < 3350) message.textContent = labels[1];
    else if (phase < 4400) message.textContent = labels[2];
    else message.textContent = labels[3];
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}



let fitTextTimer = 0;
function readCssNumber(element, propertyName, fallback) {
  const raw = getComputedStyle(element).getPropertyValue(propertyName).trim();
  const value = Number.parseFloat(raw);
  return Number.isFinite(value) ? value : fallback;
}

function visibleSemanticLines(element, lang) {
  const visibleCopy = element.querySelector(`.lang-${lang}`);
  if (visibleCopy && getComputedStyle(visibleCopy).display !== 'none') {
    return [...visibleCopy.querySelectorAll('.copy-line')];
  }
  if (element.querySelector('.lang-en, .lang-ko')) return [];
  return [...element.querySelectorAll('.copy-line')];
}

function semanticTextFits(element, lines, size, availableWidth, availableHeight = Infinity) {
  element.style.fontSize = `${size}px`;
  const widthFits = lines.every((line) => line.scrollWidth <= availableWidth + 0.5);
  const heightFits = element.scrollHeight <= availableHeight + 0.5;
  return widthFits && heightFits;
}

function fitSemanticText() {
  const lang = getCurrentLanguage();

  document.querySelectorAll('[data-fit-text]').forEach((element) => {
    const lines = visibleSemanticLines(element, lang);
    element.style.removeProperty('font-size');
    const availableWidth = Math.max(0, element.clientWidth - readCssNumber(element, '--fit-reserve', 2));
    const heightLimit = readCssNumber(element, '--fit-height', Infinity);
    const availableHeight = Number.isFinite(heightLimit)
      ? Math.max(0, heightLimit - readCssNumber(element, '--fit-height-reserve', 0))
      : Infinity;
    if (!lines.length || availableWidth <= 0) return;

    const computedSize = Number.parseFloat(getComputedStyle(element).fontSize) || 32;
    const cssMin = readCssNumber(element, '--fit-min', NaN);
    const dataMin = Number.parseFloat(element.dataset.fitMin || '');
    const minSize = Number.isFinite(cssMin)
      ? cssMin
      : (Number.isFinite(dataMin) ? dataMin : 18);
    const dataMax = Number.parseFloat(element.dataset.fitMax || '');
    const cssMax = readCssNumber(element, '--fit-max', computedSize);
    const maxSize = Math.max(minSize, Number.isFinite(dataMax) ? dataMax : cssMax);

    // Start from the largest allowed size. Binary search finds the largest size
    // that preserves every authored copy line without an extra wrap.
    let low = minSize;
    let high = maxSize;

    if (semanticTextFits(element, lines, high, availableWidth, availableHeight)) {
      element.style.fontSize = `${high}px`;
      return;
    }

    // The minimum should normally fit. If not, retain it rather than breaking the line contract.
    if (!semanticTextFits(element, lines, low, availableWidth, availableHeight)) {
      element.style.fontSize = `${low}px`;
      return;
    }

    for (let i = 0; i < 14; i += 1) {
      const mid = (low + high) / 2;
      if (semanticTextFits(element, lines, mid, availableWidth, availableHeight)) low = mid;
      else high = mid;
    }

    // A tiny safety margin prevents sub-pixel clipping at different zoom levels.
    element.style.fontSize = `${Math.max(minSize, low - 0.2).toFixed(2)}px`;
  });
}

function scheduleSemanticFit() {
  window.clearTimeout(fitTextTimer);
  fitTextTimer = window.setTimeout(() => {
    window.requestAnimationFrame(() => window.requestAnimationFrame(() => {
      fitSemanticText();
      window.dispatchEvent(new Event('flowmatic:layout-change'));
    }));
  }, 32);
}

window.addEventListener('scroll', updateHeaderState, { passive: true });
window.addEventListener('resize', () => {
  if (window.innerWidth > 768) closeNav();
  scheduleSemanticFit();
});

updateHeaderState();
initNavigation();
initArabicLanguageSpans();
initLanguageToggle();
initReveal();
initProductCtas();
initDemoVideos();
initCtExplainer();
initAmrExplainer();
scheduleSemanticFit();
if (document.fonts?.ready) document.fonts.ready.then(scheduleSemanticFit);
