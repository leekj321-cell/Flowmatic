import * as THREE from './vendor/three/three.module.min.js';
import { OrbitControls } from './vendor/three/OrbitControls.js';
import { CanvasLineRenderer } from './nc-viewer-canvas.js';
import './nc-viewer-core.js?v=2.1';

const TEXT = {
  ko: {
    toolCount: (n) => `공구 ${n}개`,
    empty: 'NC 파일을 열거나 샘플을 실행하세요.', loading: '공구 경로를 읽는 중입니다.',
    unsupported: '이 브라우저에서 3D 화면을 시작하지 못했습니다. 하드웨어 가속을 지원하는 브라우저에서 다시 열어주세요.',
    missing: '직경 미입력', unit: 'mm', noPath: '표시 가능한 경로가 없습니다.',
    all: '전체 공구', tool: '공구', ready: (n) => `${n.toLocaleString()}개 경로 구간`,
    partial: (n) => `${n}개 표시 조건`,
    manual: '입력한 직경', parsed: 'NC에서 읽은 직경', line: '행',
    "hideRapid": "급속이송 숨김",
    "showRapid": "급속이송 보이기",
    "motionLabels": {"setup": "설정", "return": "복귀", "offset": "좌표 이동", "rotation": "좌표 회전", "reference": "원점 복귀"},
    "detailLabels": {"rotary": "동시 회전축"},
    "toolNames": {},
    warning: {
      "expression": "값을 확인할 수 없는 수식 구간을 제외했습니다.",
      "auxiliary": "설비 보조 동작은 계산하지 않고 기록된 XYZ 경로를 표시합니다.",
      "index": "인덱스 자세별 프로그램 좌표를 표시하며 회전 중 경로는 연결하지 않습니다.",
      "compensation": "공구경 보정 전 프로그램 좌표를 표시합니다.",
      "cycleEnvelope": "드릴 사이클은 시작·깊이·복귀 경로로 표시합니다. 중간 피킹은 생략합니다.",
      "multiplePrograms": "여러 프로그램이 포함된 파일입니다. 첫 프로그램의 종료까지 표시합니다.",

      programFlow: "서브프로그램은 전개하지 않았습니다. 불명확한 흐름을 제외하고 좌표가 다시 확인된 구간부터 표시합니다.", unsupported: "지원하지 않는 명령 구간을 제외했습니다.",
      anchor: '시작 좌표가 확인되지 않은 구간을 제외했습니다.', reference: '설비 원점 이동을 제외했습니다.', workOffset: '좌표계가 변경되어 경로 연결을 끊었습니다.',
      arc: '원호의 중심·반경을 확인할 수 없습니다.', cycle: '고정 사이클의 좌표를 확인할 수 없습니다.', peck: 'G83 피킹 동작은 설비 조건이 필요합니다.',
      limit: '경로 표시 한도에 도달했습니다.', coordinates: '좌표값이 표시 범위를 벗어났습니다.', lineLength: '지나치게 긴 행 이후 경로를 제외했습니다.'
    }
  },
  en: {
    toolCount: (n) => `${n} tool${n === 1 ? '' : 's'}`,
    empty: 'Open an NC file or run the sample.', loading: 'Reading the toolpath.',
    unsupported: 'The 3D view could not start. Open this page in a browser with hardware acceleration.',
    missing: 'Diameter not set', unit: 'mm', noPath: 'No supported toolpath to display.',
    all: 'All tools', tool: 'Tool', ready: (n) => `${n.toLocaleString()} path segments`,
    partial: (n) => `${n} review item(s) · Only supported toolpaths are shown.`,
    manual: 'Entered diameter', parsed: 'Diameter from NC', line: 'Line',
    "hideRapid": "Hide rapid moves",
    "showRapid": "Show rapid moves",
    "motionLabels": {"setup": "Setup", "return": "Return", "offset": "Local offset", "rotation": "Rotation", "reference": "Reference return"},
    "detailLabels": {"rotary": "Simultaneous rotary motion"},
    "toolNames": {},
    warning: {
      "expression": "Sections with unresolved expressions were excluded.",
      "auxiliary": "Auxiliary machine actions are not simulated; recorded XYZ paths are shown.",
      "index": "Program coordinates are shown for each index position. Paths are not joined during indexing.",
      "compensation": "Program coordinates before cutter compensation are shown.",
      "cycleEnvelope": "Drilling cycles show entry, depth and return paths. Intermediate pecks are omitted.",
      "multiplePrograms": "This file contains multiple programs. Only the first program is displayed through its end.",

      programFlow: "Subprograms are not expanded. Unresolved flow is excluded; display resumes only when coordinates are known again.", unsupported: "Sections with unsupported commands were excluded.",
      anchor: 'A segment with an unknown start position was excluded.', reference: 'Machine reference movement was excluded.', workOffset: 'Path connection was broken at a work-offset change.',
      arc: 'The arc center or radius could not be resolved.', cycle: 'The canned-cycle coordinates could not be resolved.', peck: 'G83 peck movements require machine settings.',
      limit: 'The path display limit was reached.', coordinates: 'Coordinates are outside the display range.', lineLength: 'Path after an unusually long line was excluded.'
    }
  },
  ar: {
    toolCount: (n) => `الأدوات: ${n}`,
    empty: 'افتح ملف NC أو شغّل العينة.', loading: 'جارٍ قراءة مسار الأداة.',
    unsupported: 'تعذر بدء العرض ثلاثي الأبعاد. افتح الصفحة في متصفح يدعم تسريع الرسومات.',
    missing: 'لم يُحدد القطر', unit: 'mm', noPath: 'لا يوجد مسار مدعوم للعرض.',
    all: 'كل الأدوات', tool: 'الأداة', ready: (n) => `${n.toLocaleString()} مقطع مسار`,
    partial: (n) => `${n} ملاحظة للمراجعة · تظهر المسارات المدعومة فقط.`,
    manual: 'القطر المُدخل', parsed: 'القطر من NC', line: 'السطر',
    "hideRapid": "إخفاء الحركات السريعة",
    "showRapid": "إظهار الحركات السريعة",
    "motionLabels": {"setup": "إعداد", "return": "رجوع", "offset": "إزاحة محلية", "rotation": "تدوير", "reference": "عودة مرجعية"},
    "detailLabels": {"rotary": "حركة دورانية متزامنة"},
    "toolNames": {"Drill": "مثقاب", "Center Drill": "مثقاب تمركز", "End Mill": "قاطع تفريز", "Ball End Mill": "قاطع كروي", "Tap": "أداة قلاوظ", "Reamer": "موسّع ثقوب", "Face Mill": "قاطع تسوية", "Chamfer": "قاطع شطف", "Boring": "أداة تجويف", "T-Cutter": "قاطع T"},
    warning: {
      "expression": "استُبعدت المقاطع التي تحتوي على تعبيرات لم تُعرف قيمها.",
      "auxiliary": "لا تُحاكى وظائف الماكينة المساعدة؛ تُعرض مسارات XYZ المسجلة.",
      "index": "تُعرض إحداثيات البرنامج لكل وضع فهرسة، ولا تُوصل المسارات أثناء الفهرسة.",
      "compensation": "تُعرض إحداثيات البرنامج قبل تعويض نصف قطر الأداة.",
      "cycleEnvelope": "تُعرض حركة الدخول والعمق والرجوع في دورات الثقب، مع حذف خطوات الثقب المتقطع الوسيطة.",
      "multiplePrograms": "يحتوي الملف على عدة برامج. يُعرض البرنامج الأول فقط حتى نهايته.",

      programFlow: "لا تُوسّع البرامج الفرعية. يُستبعد التدفق غير المحدد، ويُستأنف العرض فقط عندما تُعرف الإحداثيات مجددًا.", unsupported: "استُبعدت المقاطع التي تحتوي على أوامر غير مدعومة.",
      anchor: 'استُبعد مقطع ذو موضع بداية غير معروف.', reference: 'استُبعد الانتقال إلى مرجع الماكينة.', workOffset: 'قُطع اتصال المسار عند تغيير إزاحة العمل.',
      arc: 'تعذر تحديد مركز القوس أو نصف قطره.', cycle: 'تعذر تحديد إحداثيات الدورة.', peck: 'تتطلب حركات G83 إعدادات الماكينة.',
      limit: 'تم بلوغ حد عرض المسار.', coordinates: 'الإحداثيات خارج نطاق العرض.', lineLength: 'استُبعد المسار بعد سطر طويل للغاية.'
    }
  }
};

function createViewer(root) {
  const widget = root.querySelector('[data-nc-viewer]');
  if (!widget) return;
  const t = TEXT[document.documentElement.lang] || TEXT.ko;
  const find = (name) => widget.querySelector(`[data-viewer-${name}]`);
  const surface = find('surface'), canvas = find('canvas'), message = find('message');
  const status = find('status'), list = find('tools'), selectedLabel = find('selected');
  const diameterInput = find('diameter'), diameterSource = find('diameter-source');
  const prev = find('prev'), next = find('next'), rapid = find('rapid');
  const coordinates = find('coordinates'), warningList = find('warnings'), review = find('review');
  const codeScroll = find('code-scroll'), codeRows = find('code-rows'), codeSpacer = find('code-spacer');
  const motionLabel = find('motion'), rapidToggle = find('rapid-toggle');
  let renderer;
  try {
    const context = canvas.getContext('webgl2', { antialias: true, alpha: false });
    renderer = context ? new THREE.WebGLRenderer({ canvas, context, antialias: true, alpha: false }) : new CanvasLineRenderer(canvas);
    if (context) canvas.dataset.renderer = 'webgl';
  } catch {
    message.textContent = t.unsupported;
    message.hidden = false;
    widget.querySelectorAll('button, input').forEach((el) => { el.disabled = true; });
    return;
  }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor('#000000');
  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-100, 100, 100, -100, 0.01, 1000000);
  camera.up.set(0, 0, 1);
  const controls = new OrbitControls(camera, canvas);
  controls.enableDamping = false;
  controls.minZoom = 0.02; controls.maxZoom = 200;
  controls.touches.ONE = THREE.TOUCH.ROTATE;
  controls.touches.TWO = THREE.TOUCH.DOLLY_PAN;
  const paths = new THREE.Group(), decorations = new THREE.Group(), marker = new THREE.Group();
  scene.add(paths, decorations, marker);
  let data = null, selected = -1, span = 100, halfHeight = 80;
  let markerAt = null, contextLost = false;
  const pathObjects = [], raycaster = new THREE.Raycaster(), pointer = new THREE.Vector2();
  const center = new THREE.Vector3();
  let bounds = null;
  let selectedLine = -1;
  let frame = 0;
  const draw = () => {
    if (frame || contextLost) return;
    frame = requestAnimationFrame(() => { frame = 0; renderer.render(scene, camera); });
  };
  const disposeGroup = (group) => {
    while (group.children.length) {
      const object = group.children[0]; group.remove(object);
      object.geometry?.dispose();
      if (Array.isArray(object.material)) object.material.forEach((m) => m.dispose());
      else object.material?.dispose();
    }
  };
  function resize() {
    const width = Math.max(1, surface.clientWidth), height = Math.max(1, surface.clientHeight);
    renderer.setSize(width, height, false);
    const aspect = width / height;
    camera.left = -halfHeight * aspect; camera.right = halfHeight * aspect;
    camera.top = halfHeight; camera.bottom = -halfHeight;
    camera.updateProjectionMatrix(); draw();
  }
  function fit(top = false) {
    const aspect = Math.max(0.1, surface.clientWidth / Math.max(1, surface.clientHeight));
    halfHeight = span * 0.8 * Math.max(1, 1 / aspect);
    camera.zoom = 1;
    camera.position.copy(center).add(new THREE.Vector3(...(top ? [0, -0.0001 * span, span * 2] : [span, -span * 1.35, span * 1.1])));
    controls.target.copy(center); camera.lookAt(center); camera.updateMatrixWorld();
    if (bounds) {
      const right = new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld, 0);
      const up = new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld, 1);
      let width = 0, height = 0;
      for (const x of [bounds.min.x, bounds.max.x]) for (const y of [bounds.min.y, bounds.max.y]) for (const z of [bounds.min.z, bounds.max.z]) {
        const offset = new THREE.Vector3(x,y,z).sub(center);
        width = Math.max(width, Math.abs(offset.dot(right)));
        height = Math.max(height, Math.abs(offset.dot(up)));
      }
      halfHeight = Math.max(height, width / aspect, 1) * 1.16;
    }
    controls.update(); resize();
  }
  function updateMarker() {
    disposeGroup(marker);
    const tool = data?.tools[selected];
    if (!tool || !markerAt) { coordinates.textContent = 'X —   Y —   Z —'; draw(); return; }
    coordinates.textContent = markerAt.map((n, i) => `${'XYZ'[i]} ${n.toFixed(3)}`).join('   ') + ' mm';
    const diameter = tool.overrideDiameter ?? tool.diameter;
    const circle = self.FlowmaticNcViewerCore.markerCircle(markerAt, diameter);
    if (circle.length) {
      const geometry = new THREE.BufferGeometry().setFromPoints(circle.map((p) => new THREE.Vector3(...p)));
      const ring = new THREE.LineLoop(geometry, new THREE.LineBasicMaterial({ color: '#ffe76a', depthTest: false }));
      ring.renderOrder = 5; marker.add(ring);
    }
    const size = span * 0.012 / camera.zoom;
    const points = [[markerAt[0] - size, markerAt[1], markerAt[2]], [markerAt[0] + size, markerAt[1], markerAt[2]],
      [markerAt[0], markerAt[1] - size, markerAt[2]], [markerAt[0], markerAt[1] + size, markerAt[2]]];
    const cross = new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints(points.map((p) => new THREE.Vector3(...p))),
      new THREE.LineBasicMaterial({ color: tool.color, depthTest: false }));
    cross.renderOrder = 6; marker.add(cross); draw();
  }
  function renderCode() {
    if (!codeRows || !codeScroll || !codeSpacer) return;
    const rows = data?.rows || [];
    codeSpacer.style.height = `${rows.length * 28}px`;
    const start = Math.max(0, Math.floor(codeScroll.scrollTop / 28) - 8);
    const end = Math.min(rows.length, start + Math.ceil(codeScroll.clientHeight / 28) + 20);
    const fragment = document.createDocumentFragment();
    for (let i = start; i < end; i++) {
      const row = rows[i], element = document.createElement('div');
      element.className = 'nc-code-row' + (i === selectedLine ? ' is-current' : '');
      element.style.top = `${i * 28}px`;
      element.setAttribute('role', 'button'); element.setAttribute('aria-label', `${t.line} ${row.line}: ${row.code}`);
      element.setAttribute('aria-pressed', String(i === selectedLine));
      const tool = data.tools.find(item => item.id === row.tool);
      const diameter = tool?.overrideDiameter ?? tool?.diameter;
      [row.line, row.code || ' ', row.tool, diameter ?? '—', row.wcs].forEach((value, column) => {
        const cell = document.createElement('span'); cell.textContent = String(value); cell.title = String(value);
        element.append(cell);
      });
      element.addEventListener('click', () => selectLine(i)); fragment.append(element);
    }
    codeRows.replaceChildren(fragment);
  }
  function focusCode() {
    if (!codeScroll || selectedLine < 0) return;
    const top = selectedLine * 28;
    if (top < codeScroll.scrollTop || top > codeScroll.scrollTop + codeScroll.clientHeight - 28) codeScroll.scrollTop = Math.max(0, top - 56);
    renderCode();
  }
  function selectLine(index) {
    const row = data?.rows?.[index]; if (!row) return;
    selectedLine = index;
    const toolIndex = data.tools.findIndex(tool => tool.id === row.tool);
    if (toolIndex >= 0) selected = toolIndex;
    if (row.point) markerAt = row.point;
    else { const tool = data.tools[selected]; markerAt = tool?.firstCut || tool?.first || null; }
    syncSelection(); focusCode();
  }
  function syncSelection() {
    const tool = data?.tools[selected];
    for (const object of pathObjects) {
      const focused = selected < 0 || object.userData.tool === selected;
      object.visible = !object.userData.rapid || rapid.checked;
      object.material.opacity = focused ? (object.userData.rapid ? 0.55 : 1) : (object.userData.rapid ? 0.16 : 0.38);
      object.renderOrder = focused ? 2 : 0;
    }
    list.querySelectorAll('button').forEach((button, i) => {
      button.setAttribute('aria-pressed', String(i === selected));
      button.classList.toggle('is-selected', i === selected);
    });
    find('all').setAttribute('aria-pressed', String(selected === -1));
    selectedLabel.textContent = tool ? tool.id : t.all;
    selectedLabel.title = tool?.name || '';
    if (motionLabel) { const mode = data?.rows?.[selectedLine]?.motion; motionLabel.textContent = t.motionLabels[mode] || mode || '—'; }
    if (rapidToggle) {
      rapidToggle.textContent = rapid.checked ? t.hideRapid : t.showRapid;
      rapidToggle.setAttribute('aria-pressed', String(rapid.checked));
    }
    diameterInput.disabled = !tool;
    diameterInput.setCustomValidity('');
    diameterInput.value = tool ? (tool.overrideDiameter ?? tool.diameter ?? '') : '';
    diameterSource.textContent = tool ? (tool.overrideDiameter != null ? t.manual : tool.diameter != null ? t.parsed : t.missing) : '—';
    prev.disabled = !data?.tools.length || selected <= 0;
    next.disabled = !data?.tools.length || selected >= data.tools.length - 1;
    updateMarker(); renderCode();
  }
  function select(index) {
    if (!data || index < -1 || index >= data.tools.length) return;
    selected = index;
    const tool = data.tools[index]; markerAt = tool ? (tool.firstCut || tool.first) : null;
    selectedLine = tool?.firstCutLine ?? tool?.firstLine ?? -1;
    syncSelection(); focusCode();
  }
  function clear() {
    data = null; bounds = null; selected = -1; selectedLine = -1; markerAt = null; pathObjects.length = 0;
    disposeGroup(paths); disposeGroup(decorations); disposeGroup(marker);
    list.replaceChildren(); warningList.replaceChildren(); review.hidden = true;
    status.classList.remove('has-warning');
    message.textContent = t.empty; message.hidden = false; status.textContent = '—';
    span = 100; center.set(0, 0, 0); syncSelection(); fit();
  }
  function show(result) {
    clear(); data = result;
    if (!data) return;
    message.textContent = t.noPath; message.hidden = data.segmentCount > 0;
    status.textContent = `${t.ready(data.segmentCount)} · ${t.toolCount(data.tools.length)}` + (data.warningCount ? ` · ${t.partial(data.warnings.length)}` : '');
    status.classList.toggle('has-warning', data.warningCount > 0);
    review.hidden = !data.warningCount;
    for (const warning of data.warnings) {
      const label = t.warning[warning.code] || t.warning.unsupported;
      const detail = t.detailLabels[warning.detail] || warning.detail;
      const li = document.createElement('li'); li.textContent = `${t.line} ${warning.line}: ${label}${detail ? ' (' + detail + ')' : ''}${warning.count > 1 ? ' × ' + warning.count : ''}`;
      warningList.append(li);
    }
    const box = new THREE.Box3();
    data.tools.forEach((tool, index) => {
      const button = document.createElement('button'); button.type = 'button';
      button.className = 'nc-viewer-tool'; button.style.setProperty('--tool-color', tool.color);
      const title = document.createElement('strong'); title.textContent = tool.id;
      const name = document.createElement('span'); name.textContent = t.toolNames[tool.name] || tool.name || t.tool;
      const size = document.createElement('small'); size.textContent = tool.diameter ? `Ø ${tool.diameter} mm` : t.missing;
      button.append(title, name, size); button.addEventListener('click', () => select(index)); list.append(button);
      for (const kind of ['feed', 'rapid']) {
        if (!tool[kind]?.length) continue;
        const geometry = new THREE.BufferGeometry();
        geometry.setAttribute('position', new THREE.BufferAttribute(tool[kind], 3));
        geometry.computeBoundingBox(); box.union(geometry.boundingBox);
        const material = kind === 'rapid' ? new THREE.LineDashedMaterial({ color: tool.color, transparent: true, opacity: 0.55 }) :
          new THREE.LineBasicMaterial({ color: tool.color, transparent: true, opacity: 1 });
        const object = new THREE.LineSegments(geometry, material);
        object.userData = { tool: index, rapid: kind === 'rapid', lines: tool[kind + 'Lines'] };
        paths.add(object); pathObjects.push(object);
      }
    });
    if (!box.isEmpty()) {
      box.getCenter(center);
      const size = box.getSize(new THREE.Vector3()); span = Math.max(size.x, size.y, size.z, 1);
      const largestTool = Math.max(0, ...data.tools.map((tool) => tool.diameter || 0));
      bounds = box.clone().expandByScalar(largestTool / 2);
      span = Math.max(span + largestTool, 1);
      camera.near = Math.max(0.0001, span / 10000); camera.far = span * 10000;
      decorations.add(new THREE.AxesHelper(span * 0.2));
      pathObjects.filter((o) => o.userData.rapid).forEach((object) => {
        object.material.dashSize = span * 0.012; object.material.gapSize = span * 0.009; object.computeLineDistances();
      });
    }
    fit(); select(data.tools.length ? 0 : -1);
  }
  let lastZoom = camera.zoom;
  controls.addEventListener('change', () => { if (camera.zoom !== lastZoom) { lastZoom = camera.zoom; updateMarker(); } draw(); });
  prev.addEventListener('click', () => select(selected - 1));
  next.addEventListener('click', () => select(selected + 1));
  find('all').addEventListener('click', () => select(-1));
  find('fit').addEventListener('click', () => fit());
  find('top').addEventListener('click', () => fit(true));
  rapid.addEventListener('change', syncSelection);
  rapidToggle?.addEventListener('click', () => { rapid.checked = !rapid.checked; syncSelection(); });
  find('console-toggle')?.addEventListener('click', () => {
    const panel = find('console'); panel.hidden = !panel.hidden;
    find('console-toggle').setAttribute('aria-expanded', String(!panel.hidden));
    renderCode();
  });
  const zoomBy = factor => { camera.zoom = THREE.MathUtils.clamp(camera.zoom * factor, .02, 200); camera.updateProjectionMatrix(); updateMarker(); };
  find('zoom-in')?.addEventListener('click', () => zoomBy(1.3));
  find('zoom-out')?.addEventListener('click', () => zoomBy(1 / 1.3));
  codeScroll?.addEventListener('scroll', renderCode, {passive:true});
  codeScroll?.addEventListener('keydown', event => {
    if (event.key === 'ArrowDown' || event.key === 'ArrowUp') { event.preventDefault(); selectLine(selectedLine + (event.key === 'ArrowDown' ? 1 : -1)); }
  });
  diameterInput.addEventListener('input', () => {
    const tool = data?.tools[selected]; if (!tool) return;
    const value = Number(diameterInput.value);
    if (diameterInput.value === '') tool.overrideDiameter = null;
    else if (!Number.isFinite(value) || value <= 0 || value > 10000) { diameterInput.setCustomValidity('0 < Ø ≤ 10000 mm'); return; }
    else tool.overrideDiameter = value;
    diameterInput.setCustomValidity('');
    diameterSource.textContent = tool.overrideDiameter !== null ? t.manual : tool.diameter != null ? t.parsed : t.missing;
    const badge = list.children[selected]?.querySelector('small');
    if (badge) badge.textContent = (tool.overrideDiameter ?? tool.diameter) ? `Ø ${tool.overrideDiameter ?? tool.diameter} mm` : t.missing;
    updateMarker(); renderCode();
  });
  let pointerDown = null;
  canvas.addEventListener('pointerdown', (event) => { pointerDown = { x: event.clientX, y: event.clientY, id: event.pointerId }; });
  canvas.addEventListener('pointerup', (event) => {
    if (!pointerDown || pointerDown.id !== event.pointerId || Math.hypot(event.clientX - pointerDown.x, event.clientY - pointerDown.y) > 5 || !data) return;
    pointerDown = null;
    const rect = canvas.getBoundingClientRect();
    pointer.set((event.clientX - rect.left) / rect.width * 2 - 1, -(event.clientY - rect.top) / rect.height * 2 + 1);
    raycaster.params.Line.threshold = halfHeight * 12 / Math.max(1, surface.clientHeight) / camera.zoom;
    raycaster.setFromCamera(pointer, camera);
    const hit = raycaster.intersectObjects(pathObjects.filter((o) => o.visible && (selected < 0 || o.userData.tool === selected)), false)[0];
    if (hit) { selected = hit.object.userData.tool; markerAt = hit.point.toArray(); selectedLine = hit.object.userData.lines?.[Math.floor(hit.index / 2)] ?? selectedLine; syncSelection(); focusCode(); }
  });
  canvas.addEventListener('keydown', (event) => {
    if (event.key === 'Home' || event.key.toLowerCase() === 'f') { event.preventDefault(); fit(); }
    else if (event.key === '+' || event.key === '=' || event.key === '-') {
      event.preventDefault(); camera.zoom = THREE.MathUtils.clamp(camera.zoom * (event.key === '-' ? 0.8 : 1.25), 0.02, 200); camera.updateProjectionMatrix(); updateMarker();
    } else if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(event.key)) {
      event.preventDefault();
      const offset = camera.position.clone().sub(controls.target);
      const axis = event.key === 'ArrowLeft' || event.key === 'ArrowRight' ? new THREE.Vector3(0, 0, 1) : new THREE.Vector3().crossVectors(offset, camera.up).normalize();
      offset.applyAxisAngle(axis, (event.key === 'ArrowLeft' || event.key === 'ArrowUp' ? 1 : -1) * 0.12);
      camera.position.copy(controls.target).add(offset); camera.lookAt(controls.target); controls.update(); draw();
    }
  });
  canvas.addEventListener('webglcontextlost', (event) => { event.preventDefault(); contextLost = true; message.hidden = false; message.textContent = t.unsupported; });
  canvas.addEventListener('webglcontextrestored', () => { contextLost = false; show(data); });
  root.addEventListener('flowmatic:nc-result', (event) => show(event.detail));
  root.addEventListener('flowmatic:nc-reset', clear);
  root.addEventListener('flowmatic:nc-loading', () => { clear(); message.textContent = t.loading; });
  if (typeof ResizeObserver !== 'undefined') new ResizeObserver(resize).observe(surface);
  else window.addEventListener('resize', resize);
  clear();
  if (root.ncViewerScene) show(root.ncViewerScene);
}
document.querySelectorAll('[data-nc-demo-lite]').forEach(createViewer);
