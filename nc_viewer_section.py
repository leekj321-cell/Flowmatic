"""Interactive NC viewer markup shared by the existing locale page generator."""
from html import escape as e

LABELS = {
    "ko": {
        "app": "G-code Viewer",
        "code_list": "G-code List",
        "current": "현재 Tool",
        "motion": "이송상태",
        "hide_rapid": "급속이송 숨김",
        "file": "파일",
        "file_select": "NC 파일 선택",
        "zoom_in": "확대",
        "zoom_out": "축소",
        "console": "Tool Console",
        "line": "Line",
        "code": "NC Code",
        "tool": "Tool",
        "top_button": "Top",
        "boot": "화면을 시작하는 중입니다. 안내가 계속 보이면 페이지를 새로고침하거나 브라우저에서 다시 열어주세요.",
        "title": "3D 공구 경로", "body": "NC 파일을 열고 공구별 경로와 직경을 확인하세요.",
        "prev": "Prev Tool", "next": "Next Tool", "all": "전체 공구", "fit": "3D 맞춤", "top": "위에서 보기",
        "rapid": "급속이송 표시", "diameter": "공구 직경", "selected": "선택 공구", "tools": "공구 목록",
        "hint": "드래그: 회전 · 휠: 확대 · 오른쪽 드래그: 이동 · 경로 클릭: 공구 위치",
        "touch": "한 손가락: 회전 · 두 손가락: 확대·이동", "empty": "NC 파일을 열거나 샘플을 실행하세요.",
        "review": "경로 검토 항목", "time": "기존 시간 분석", "basis": "프로그램 좌표 기준 · 직경 단위 mm",
        "canvas": "3D 공구 경로. 방향키로 회전, 더하기와 빼기로 확대, Home 키로 화면 맞춤."
    },
    "en": {
        "app": "G-code Viewer",
        "code_list": "G-code List",
        "current": "Current Tool",
        "motion": "Motion",
        "hide_rapid": "Hide rapid moves",
        "file": "File",
        "file_select": "Choose NC file",
        "zoom_in": "Zoom in",
        "zoom_out": "Zoom out",
        "console": "Tool Console",
        "line": "Line",
        "code": "NC Code",
        "tool": "Tool",
        "top_button": "Top",
        "boot": "Starting the viewer. If this message stays visible, refresh the page or reopen it in a browser.",
        "title": "3D toolpath", "body": "Open an NC file to inspect each tool's path and diameter.",
        "prev": "Prev Tool", "next": "Next Tool", "all": "All tools", "fit": "Fit 3D", "top": "Top view",
        "rapid": "Show rapid moves", "diameter": "Tool diameter", "selected": "Selected tool", "tools": "Tools",
        "hint": "Drag: orbit · Wheel: zoom · Right drag: pan · Click path: tool position",
        "touch": "One finger: orbit · Two fingers: zoom and pan", "empty": "Open an NC file or run the sample.",
        "review": "Path review", "time": "Existing time analysis", "basis": "Programmed coordinates · Diameter in mm",
        "canvas": "3D toolpath. Arrow keys rotate, plus and minus zoom, Home fits the view."
    },
    "ar": {
        "app": "عارض G-code",
        "code_list": "قائمة G-code",
        "current": "الأداة الحالية",
        "motion": "الحركة",
        "hide_rapid": "إخفاء الحركات السريعة",
        "file": "الملف",
        "file_select": "اختر ملف NC",
        "zoom_in": "تكبير",
        "zoom_out": "تصغير",
        "console": "لوحة الأدوات",
        "line": "السطر",
        "code": "كود NC",
        "tool": "الأداة",
        "top_button": "علوي",
        "boot": "جارٍ بدء العارض. إذا استمرت هذه الرسالة، حدّث الصفحة أو أعد فتحها في المتصفح.",
        "title": "مسار الأداة ثلاثي الأبعاد", "body": "افتح ملف NC لفحص مسار كل أداة وقطرها.",
        "prev": "الأداة السابقة", "next": "الأداة التالية", "all": "كل الأدوات", "fit": "عرض ثلاثي الأبعاد", "top": "عرض علوي",
        "rapid": "إظهار الحركات السريعة", "diameter": "قطر الأداة", "selected": "الأداة المحددة", "tools": "الأدوات",
        "hint": "اسحب للتدوير · العجلة للتكبير · السحب بالزر الأيمن للتحريك · انقر المسار لتحديد موضع الأداة",
        "touch": "إصبع واحد للتدوير · إصبعان للتكبير والتحريك", "empty": "افتح ملف NC أو شغّل العينة.",
        "review": "مراجعة المسار", "time": "تحليل الوقت الحالي", "basis": "إحداثيات البرنامج · القطر بالملليمتر",
        "canvas": "مسار الأداة ثلاثي الأبعاد. أسهم لوحة المفاتيح للتدوير، زائد وناقص للتكبير، Home لملاءمة العرض."
    }
}


def viewer_section(lang, t, analysis):
    v = LABELS[lang]
    extra = f'<details class="nc-analysis-details"><summary>{e(v["time"])}</summary><div class="section-grid">{analysis}</div></details>' if analysis else ''
    return f'''<section class="nc-workspace" data-nc-demo-lite aria-labelledby="nc-browser-demo-title">
<div class="nc-app-top"><h2 id="nc-browser-demo-title">{e(v['app'])}</h2><strong data-nc-meta="file">NC —</strong></div>
<div class="nc-boot-notice" data-nc-boot>{e(v['boot'])}</div><div data-nc-alert role="alert" hidden></div>
<input class="sr-only" data-nc-file id="nc-demo-file" type="file" aria-label="{e(v['file_select'])}">
<div class="nc-viewer" data-nc-viewer><div class="nc-workbench">
<div class="nc-viewer-surface" data-viewer-surface><canvas data-viewer-canvas tabindex="0" aria-label="{e(v['canvas'])}"></canvas><div class="nc-viewer-message" data-viewer-message>{e(v['empty'])}</div>
<div class="nc-viewer-camera"><button data-viewer-fit type="button">3D</button><button data-viewer-top type="button">{e(v['top_button'])}</button><button data-viewer-zoom-in type="button" aria-label="{e(v['zoom_in'])}">+</button><button data-viewer-zoom-out type="button" aria-label="{e(v['zoom_out'])}">−</button></div>
<div class="nc-viewer-coordinates" data-viewer-coordinates dir="ltr">X — &nbsp; Y — &nbsp; Z —</div></div>
<div class="nc-code-pane"><p class="nc-panel-label">{e(v['code_list'])}</p>
<div class="nc-current"><p>{e(v['current'])}: <strong data-viewer-selected>—</strong></p><p>{e(v['motion'])}: <strong data-viewer-motion>—</strong></p></div>
<button class="nc-rapid-toggle" data-viewer-rapid-toggle type="button" aria-pressed="true">{e(v['hide_rapid'])}</button><input data-viewer-rapid class="sr-only" type="checkbox" checked tabindex="-1" aria-label="{e(v['rapid'])}">
<div class="nc-navigation"><button data-viewer-prev type="button" disabled>{e(v['prev'])}</button><button data-viewer-next type="button" disabled>{e(v['next'])}</button><button data-viewer-console-toggle type="button" aria-expanded="false">{e(v['console'])}</button></div>
<fieldset class="nc-tool-console" data-viewer-console hidden><legend>{e(v['console'])}</legend><label class="nc-diameter-row">{e(v['diameter'])} Ø <input data-viewer-diameter type="number" min="0.01" max="10000" step="any" inputmode="decimal" placeholder="—" disabled aria-label="{e(v['diameter'])}"> mm <small data-viewer-diameter-source>—</small></label>
<div class="nc-viewer-tool-list" data-viewer-tools aria-label="{e(v['tools'])}"></div><button class="nc-console-all" data-viewer-all type="button" aria-pressed="true">{e(v['all'])}</button></fieldset>
<div class="nc-code-table" aria-label="{e(v['code'])}"><div class="nc-code-columns"><span>{e(v['line'])}</span><span>{e(v['code'])}</span><span>{e(v['tool'])}</span><span>D(mm)</span><span>WCS</span></div><div class="nc-code-scroll" data-viewer-code-scroll tabindex="0" aria-label="{e(v['code_list'])}"><div data-viewer-code-spacer></div><div data-viewer-code-rows></div></div></div></div>
<aside class="nc-file-pane"><fieldset><legend>{e(v['file'])}</legend><div class="nc-demo-actions"><button class="fm-button primary" data-nc-open type="button">{e(t['open'])}</button><button class="fm-button" data-nc-sample type="button">{e(t['sample'])}</button><button class="fm-button" data-nc-reset type="button">{e(t['reset'])}</button></div><p>{e(t['privacy'])}</p><div data-nc-dropzone tabindex="0" role="button" aria-controls="nc-demo-file">{e(t['drop'])}</div></fieldset></aside>
</div><div class="nc-viewer-foot"><p class="nc-viewer-desktop-hint">{e(v['hint'])}</p><p class="nc-viewer-touch-hint">{e(v['touch'])}</p><p>{e(v['basis'])}</p></div><p class="nc-viewer-status" data-viewer-status role="status">—</p><details class="nc-viewer-review" data-viewer-review hidden><summary>{e(v['review'])}</summary><ul data-viewer-warnings></ul></details></div>{extra}
</section>'''
