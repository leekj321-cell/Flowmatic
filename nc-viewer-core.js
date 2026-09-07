/* Browser port of the public Viewer slice in Flowmatic Machining Intelligence.
 * Source and parity boundary: docs/NC_WEB_VIEWER.md. No generator or correction engine.
 */
(function (root, factory) {
  const api = factory();
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (root) root.FlowmaticNcViewerCore = api;
})(typeof self !== "undefined" ? self : globalThis, function () {
  "use strict";
  const EPS = 1e-8;
  const MAX_SEGMENTS = 250000;
  const PALETTE = ["#20baff", "#ff792e", "#18d987", "#db8cff", "#ffdc49", "#36e0df", "#9095ff", "#ff8292"];
  const stripComments = (line) => String(line || "").replace(/\([^)]*\)/g, " ").replace(/;.*/, " ").toUpperCase();
  const toolId = (number) => `T${String(Number(number)).padStart(2, "0")}`;

  // Port of normalize_tool_name / extract_tool_info. An executable D register
  // is never interpreted as a physical diameter.
  function normalizeToolName(value) {
    let s = String(value || "").toUpperCase();
    const aliases = [["스파이럴탭", "SPIRAL TAP"], ["포밍탭", "FORM TAP"], ["롤탭", "ROLL TAP"],
      ["센터드릴", "CENTER DRILL"], ["센터 드릴", "CENTER DRILL"], ["스폿드릴", "SPOT DRILL"],
      ["스폿 드릴", "SPOT DRILL"], ["엔드밀", "END MILL"], ["드릴", "DRILL"], ["탭", "TAP"]];
    for (const [from, to] of aliases) s = s.split(from).join(to);
    s = s.replace(/\bD\s*\/\s*R\b/g, "DRILL").replace(/\bE\s*\/\s*M\b/g, "END MILL")
      .replace(/ENDMILL|END-MILL/g, "END MILL").replace(/TAPPING/g, "TAP")
      .replace(/[,、_:/\\]+/g, " ").replace(/\s+/g, " ").trim();
    if ((/[GM]\d+/.test(s.replace(/\s+/g, "")) && !s.includes("TAP")) ||
      /\b(?:OP\s*\d+|CANCEL|PROGRAM|THROUGH|COOLANT|HP\s*\d+|HIGH\s+PRESSURE|RETURN|HOME|WORK|OFFSET|PICK|PLACE)\b/.test(s)) return "";
    const names = [[/\bCENTER\s*DRILL\b/, "Center Drill"], [/\bEND\s*MILL\b|\bEM\b|\bMILLING\b/, "End Mill"],
      [/\bBALL\b|\bB(?:ALL)?\s*EM\b/, "Ball End Mill"], [/\bDRILL\b/, "Drill"], [/\bREAM(?:ER)?\b/, "Reamer"],
      [/\bTAP\b/, "Tap"], [/\bT\s*CUTTER\b/, "T-Cutter"], [/\bFACE\b/, "Face Mill"],
      [/\bCHAMFER\b|\bC\s*CUTTER\b/, "Chamfer"], [/\bBORING\b/, "Boring"]];
    return (names.find(([pattern]) => pattern.test(s)) || [null, ""])[1];
  }

  function extractToolInfo(rawLine) {
    const text = String(rawLine || "").toUpperCase().replace(/[ØΦ]/g, "D");
    let candidates = [...text.matchAll(/\((.*?)\)/g)].map((m) => m[1]);
    if (!candidates.length && /(?:^|[^A-Z0-9])D\s*\d/.test(text) && /\b(?:DRILL|TAP|END\s*MILL|ENDMILL|FACE|REAM|BORING|CUTTER|CHAMFER)\b/.test(text)) candidates = [text];
    for (const value of candidates) {
      const c = value.replace(/\s+/g, " ").trim();
      if (/\b(?:OP\s*\d+|CANCEL|PROGRAM|THROUGH|COOLANT|HP\s*\d+)\b/.test(c)) continue;
      let m = c.match(/(?:^|[^A-Z0-9])D\s*([0-9]+(?:\.[0-9]+)?)(.*)/);
      if (m) return { diameter: Number(m[1]) || null, name: normalizeToolName(m[2].replace(/^[,/_\-:]+/, "")) };
      if (/\bTAP\b/.test(c)) {
        m = c.match(/(?:^|[^A-Z0-9])M\s*([0-9]+(?:\.[0-9]+)?)(?:\s*X\s*[0-9]+(?:\.[0-9]+)?)?\s*TAP\b/) || c.match(/\bTAP\b.*?(?:^|[^A-Z0-9])M\s*([0-9]+(?:\.[0-9]+)?)/);
        return { diameter: m ? Number(m[1]) : null, name: "Tap" };
      }
      const name = normalizeToolName(c);
      if (name) return { diameter: null, name };
    }
    return { diameter: null, name: "" };
  }

  // Same center selection, sweep direction and helical interpolation as the
  // native make_arc_ij_points / make_arc_r_points (40 subdivisions).
  function arcPoints(start, end, values, clockwise, steps = 40) {
    let center;
    const angle = (point, c) => Math.atan2(point[1] - c[1], point[0] - c[0]);
    const sweep = (c) => {
      const a = angle(start, c);
      let b = angle(end, c);
      if (clockwise && b >= a) b -= 2 * Math.PI;
      if (!clockwise && b <= a) b += 2 * Math.PI;
      return b - a;
    };
    if (values.i !== undefined || values.j !== undefined) {
      center = [start[0] + (values.i || 0), start[1] + (values.j || 0)];
      const r1 = Math.hypot(start[0] - center[0], start[1] - center[1]);
      const r2 = Math.hypot(end[0] - center[0], end[1] - center[1]);
      if (r1 <= EPS || Math.abs(r1 - r2) > Math.max(0.01, r1 * 0.001)) return null;
    } else if (values.r !== undefined) {
      const dx = end[0] - start[0], dy = end[1] - start[1];
      const chord = Math.hypot(dx, dy), r = Math.abs(values.r);
      if (chord <= EPS || r <= EPS || chord > 2 * r + EPS) return null;
      const h = Math.sqrt(Math.max(0, r * r - chord * chord / 4));
      const mid = [(start[0] + end[0]) / 2, (start[1] + end[1]) / 2];
      const candidates = [[mid[0] - dy / chord * h, mid[1] + dx / chord * h], [mid[0] + dy / chord * h, mid[1] - dx / chord * h]];
      candidates.sort((a, b) => Math.abs(sweep(a)) - Math.abs(sweep(b)));
      center = candidates[values.r >= 0 ? 0 : 1];
    } else return null;
    const radius = Math.hypot(start[0] - center[0], start[1] - center[1]);
    const first = angle(start, center), delta = sweep(center), points = [];
    for (let n = 1; n <= steps; n++) {
      const t = n / steps, a = first + delta * t;
      points.push([center[0] + radius * Math.cos(a), center[1] + radius * Math.sin(a), start[2] + (end[2] - start[2]) * t]);
    }
    points[points.length - 1] = end.slice();
    return points;
  }

  function markerCircle(center, diameter, steps = 96) {
    if (!Number.isFinite(diameter) || diameter <= 0) return [];
    return Array.from({ length: steps }, (_, n) => {
      const a = n / steps * Math.PI * 2;
      return [center[0] + diameter / 2 * Math.cos(a), center[1] + diameter / 2 * Math.sin(a), center[2]];
    });
  }

  // Only arithmetic from the NC text is evaluated. No JavaScript eval or
  // implicit reads of a machine's macro variables are permitted.
  function arithmetic(expression, variables = new Map()) {
    const source = String(expression).replace(/\s+/g, '');
    let at = 0, depth = 0;
    function factor() {
      if (++depth > 32) throw new Error('expression');
      let result;
      const char = source[at];
      if (char === '+' || char === '-') { at++; result = (char === '-' ? -1 : 1) * factor(); }
      else if (char === '[') { at++; result = sum(); if (source[at++] !== ']') throw new Error('expression'); }
      else if (char === '#') {
        at++; const match = source.slice(at).match(/^\d+/);
        if (!match || !variables.has(Number(match[0]))) throw new Error('variable');
        at += match[0].length; result = variables.get(Number(match[0]));
      } else {
        const match = source.slice(at).match(/^(?:\d+(?:\.\d*)?|\.\d+)/);
        if (!match) throw new Error('expression');
        at += match[0].length; result = Number(match[0]);
      }
      depth--; return result;
    }
    function product() {
      let result = factor();
      while (source[at] === '*' || source[at] === '/') {
        const op = source[at++], value = factor();
        if (op === '/' && value === 0) throw new Error('expression');
        result = op === '*' ? result * value : result / value;
      }
      return result;
    }
    function sum() {
      let result = product();
      while (source[at] === '+' || source[at] === '-') {
        const op = source[at++], value = product();
        result = op === '+' ? result + value : result - value;
      }
      return result;
    }
    const result = sum();
    if (at !== source.length || !Number.isFinite(result) || Math.abs(result) > 1e9) throw new Error('expression');
    return result;
  }

  function toolDescription(raw) {
    const info = extractToolInfo(raw);
    for (const match of String(raw).matchAll(/\(([^)]*)\)/g)) {
      const comment = match[1].toUpperCase();
      if (/\b(?:OP\s*\d+|CANCEL|PROGRAM|THROUGH|COOLANT|HP\s*\d+)\b/.test(comment)) continue;
      const name = normalizeToolName(comment);
      if (!name) continue;
      if (!info.name) info.name = name;
      if (info.diameter == null) {
        const diameter = comment.match(/\bDIA(?:METER)?\s*([0-9]+(?:\.[0-9]+)?)/)
          || (name === 'Tap' && comment.match(/\bMC?\s*([0-9]+(?:\.[0-9]*)?)(?:\s*[X*]\s*[0-9.]+)?/));
        if (diameter) info.diameter = Number(diameter[1]);
      }
    }
    if (!info.name && info.diameter != null) {
      const literal = String(raw).match(/\([^)]*\bT\s*\d+\s+([A-Z][A-Z. -]*?)\s+D\s*\d/i);
      if (literal) info.name = literal[1].trim().toUpperCase();
    }
    return info;
  }

  function parseNcText(text) {
    text = String(text).replace(/^\uFEFF/, '').replace(/\x1a/g, '');
    if (text.length > 5 * 1024 * 1024) throw new Error('fileSize');
    if (/^\s*\d{2}[A-Z]@/.test(text) || /\x00/.test(text)) throw new Error('format');
    const lines = text.split(/\r\n|\n|\r/);
    if (lines.length > 100000) throw new Error('lineLimit');
    const cleanLines = lines.map(stripComments);
    const hasM6 = cleanLines.some(line => /M\s*0?6(?!\d)/.test(line));
    const brother = cleanLines.some(line => /G\s*100(?!\d)/.test(line));
    const tools = new Map(), order = [], warnings = [], warningKeys = new Map(), rows = [];
    const variables = new Map();
    let warningCount = 0, segmentCount = 0, stopped = false;
    let current = '—', pending = null, pos = [0, 0, 0], known = [false, false, false];
    let motion = 0, absolute = true, units = 1, plane = 17, wcs = 54, cycle = null, retract = 99;
    let initialCycleZ = null, cycleZ = null, cycleR = null;
    let shift = [0, 0, 0], rotation = null, indexAngle = null, blockedTransform = false, macroCycle = false;
    const ensure = id => {
      if (!tools.has(id)) tools.set(id, {id, name:'', diameter:null, feed:[], rapid:[], feedLines:[], rapidLines:[], first:null, firstCut:null, firstLine:null, blocks:0});
      return tools.get(id);
    };
    const warn = (index, code, detail = '') => {
      warningCount++;
      const key = code + ':' + detail;
      const old = warningKeys.get(key);
      if (old) { old.count++; return; }
      if (warnings.length >= 60) return;
      const item = {line:index + 1, code, detail, count:1};
      warnings.push(item); warningKeys.set(key, item);
    };
    const mapped = p => {
      const point = p.map((value, i) => value + shift[i]);
      if (rotation) {
        const x = point[0] - rotation.x, y = point[1] - rotation.y;
        point[0] = rotation.x + x * rotation.cos - y * rotation.sin;
        point[1] = rotation.y + x * rotation.sin + y * rotation.cos;
      }
      return point;
    };
    const append = (from, to, rapid, index) => {
      if (stopped) return;
      if (!from.concat(to).every(Number.isFinite) || from.concat(to).some(x => Math.abs(x) > 1e7)) { warn(index,'coordinates'); return; }
      if (Math.hypot(...to.map((x,i) => x - from[i])) < EPS) return;
      if (segmentCount >= MAX_SEGMENTS) { warn(index,'limit'); stopped = true; return; }
      const start = mapped(from), end = mapped(to), tool = ensure(current);
      if (!order.includes(current)) order.push(current);
      tool[rapid ? 'rapid' : 'feed'].push(...start,...end);
      tool[rapid ? 'rapidLines' : 'feedLines'].push(index);
      if (!tool.first) tool.first = start;
      if (!rapid && !tool.firstCut) { tool.firstCut = end; tool.firstCutLine = index; }
      if (tool.firstLine == null) tool.firstLine = index;
      if (rows[index]) { rows[index].point = end; rows[index].motion = rapid ? 'G00' : 'G01'; }
      segmentCount++;
    };
    const activeTool = (id,index) => {
      current = id; const tool = ensure(id);
      if (tool.firstLine == null) tool.firstLine = index;
      if (!order.includes(id)) order.push(id);
    };
    const futureTool = index => {
      for (let n = index + 1; n < Math.min(lines.length,index + 5); n++) {
        const clean = cleanLines[n].replace(/M0?97\s*T\s*\d+/g,'');
        const match = clean.match(/T\s*(\d{1,4})(?!\d)/);
        if (match) return toolId(match[1]);
      }
      return null;
    };
    const gap = () => { known.fill(false); cycle = null; };
    const endProgram = index => {
      stopped = true;
      if (cleanLines.slice(index + 1).some(line => /(?:^|\s)O\s*\d+|G\s*\d+|T\s*\d+/.test(line))) warn(index, 'multiplePrograms');
    };
    // These M codes have no XYZ path in this viewer. Other auxiliary M codes
    // are surfaced for review; their machine/PLC behavior is not simulated.
    const ordinaryM = new Set([0,1,2,3,4,5,6,7,8,9,19,29,30,97]);
    const allowedG = new Set([0,1,2,3,4,9,17,18,19,20,21,40,41,42,43,49,54,55,56,57,58,59,61,64,73,77,80,81,82,83,84,85,86,89,90,91,94,95,98,99,100]);

    for (let index = 0; index < lines.length; index++) {
      const raw = lines[index];
      let clean = cleanLines[index];
      const row = {line:index + 1, code:raw, tool:current, wcs:'G' + wcs, motion:'', point:null};
      rows.push(row);
      if (stopped) continue;
      if (raw.length > 8192) { warn(index,'lineLength'); stopped = true; continue; }
      const toolCode = clean.replace(/M0?97\s*T\s*\d+/g,'').match(/T\s*(\d{1,4})(?!\d)/);
      const id = toolCode ? toolId(toolCode[1]) : null;
      const originalGs = [...clean.matchAll(/G\s*(\d+(?:\.\d*)?)/g)].map(m => Number(m[1]));
      const originalMs = [...clean.matchAll(/M\s*(\d+)/g)].map(m => Number(m[1]));
      if (originalGs.includes(20)) units = 25.4;
      if (originalGs.includes(21)) units = 1;
      if (id) pending = id;
      if (originalMs.includes(6) && pending) { activeTool(pending,index); pending = null; }
      else if (id && (originalGs.includes(100) || !hasM6 || /^\s*(?:N\d+)?\s*T\s*\d+\s*\(\s*HV/i.test(raw))) activeTool(id,index);
      row.tool = current;
      const info = toolDescription(raw);
      if (info.diameter !== null || info.name) {
        const targetId = id || futureTool(index) || (current !== '—' ? current : null);
        if (targetId) {
          const tool = ensure(targetId);
          if (info.diameter > 0 && Number.isFinite(info.diameter)) tool.diameter = info.diameter * units;
          if (info.name) tool.name = info.name;
          row.tool = targetId;
        }
      }
      row.tool = row.tool === '—' ? current : row.tool;
      if (id && current === id) row.tool = id;
      if (!clean.trim() || /^\s*[%O]/.test(clean)) continue;
      const assignment = clean.match(/^\s*#(\d+)\s*=\s*(.+?)\s*$/);
      if (assignment) {
        try { variables.set(Number(assignment[1]),arithmetic(assignment[2],variables)); }
        catch (_) { variables.delete(Number(assignment[1])); warn(index,'expression'); }
        continue;
      }
      if (/\b(?:IF|WHILE|GOTO|END|CALL)\b/.test(clean)) { warn(index,'programFlow'); stopped = true; continue; }
      // G10 updates registers, rather than moving the tool along its X/Y/Z.
      if (originalGs.includes(10)) {
        if (originalGs.includes(90)) absolute = true;
        if (originalGs.includes(91)) absolute = false;
        row.motion = 'setup'; continue;
      }
      try {
        while (clean.includes('[')) {
          const start = clean.indexOf('['); let level = 1, end = start + 1;
          for (; end < clean.length && level; end++) { if (clean[end] === '[') level++; if (clean[end] === ']') level--; }
          if (level) throw new Error('expression');
          clean = clean.slice(0,start) + arithmetic(clean.slice(start,end),variables) + clean.slice(end);
        }
        clean = clean.replace(/#\d+/g, value => String(arithmetic(value,variables)));
        if (/[#\[\]]/.test(clean)) throw new Error('expression');
      } catch (_) {
        warn(index,'expression'); gap();
        if (originalGs.includes(68)) blockedTransform = true;
        continue;
      }
      const tokens = [...clean.matchAll(/([A-Z])\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))/g)];
      const words = {}, gs = [], ms = [];
      for (const token of tokens) {
        const value = Number(token[2]); words[token[1]] = value;
        if (token[1] === 'G') gs.push(value); if (token[1] === 'M') ms.push(value);
      }
      if (ms.includes(99)) { row.motion = 'return'; endProgram(index); continue; }
      if (ms.includes(98) || gs.includes(65)) { warn(index,'programFlow'); gap(); continue; }
      if (gs.includes(66)) { warn(index,'programFlow'); macroCycle = true; gap(); continue; }
      if (gs.includes(67)) { macroCycle = false; gap(); continue; }
      if (gs.includes(90)) absolute = true;
      if (gs.includes(91)) absolute = false;
      if (gs.includes(69)) {
        if (rotation || blockedTransform) gap();
        rotation = null; blockedTransform = false;
      }
      for (const g of gs) {
        if ([0,1,2,3].includes(g)) { motion = g; cycle = null; }
        if (g === 100) { motion = 0; cycle = null; }
        if ([17,18,19].includes(g)) plane = g;
        if ([98,99].includes(g)) retract = g;
        if (g >= 54 && g <= 59 && g !== wcs) { wcs = g; gap(); warn(index,'workOffset'); }
      }
      row.wcs = 'G' + wcs;
      if (gs.includes(80)) cycle = null;
      if (gs.includes(52)) {
        ['X','Y','Z'].forEach((axis,i) => {
          if (words[axis] === undefined) return;
          const value = words[axis] * units;
          pos[i] += shift[i] - value; shift[i] = value;
        });
        row.motion = 'offset'; continue;
      }
      if (gs.includes(68)) {
        if (plane !== 17 || words.R === undefined || !absolute) { blockedTransform = true; warn(index,'unsupported','G68'); gap(); continue; }
        const angle = words.R * Math.PI / 180;
        rotation = {x:(words.X === undefined ? pos[0] : words.X * units) + shift[0], y:(words.Y === undefined ? pos[1] : words.Y * units) + shift[1], cos:Math.cos(angle), sin:Math.sin(angle)};
        known[0] = known[1] = false; row.motion = 'rotation'; continue;
      }
      if (gs.some(g => [28,30,53].includes(g))) {
        ['X','Y','Z'].forEach((axis,i) => { if (words[axis] !== undefined) known[i] = false; });
        if (!['X','Y','Z'].some(axis => words[axis] !== undefined)) known.fill(false);
        cycle = null; warn(index,'reference'); row.motion = 'reference'; continue;
      }
      const rotaryAxes = ['A','B','C'].filter(axis => words[axis] !== undefined);
      if (rotaryAxes.length) {
        if (motion !== 0) { warn(index,'unsupported','rotary'); gap(); continue; }
        const value = rotaryAxes.map(axis => axis + words[axis]).join(' ');
        if (value !== indexAngle) { indexAngle = value; gap(); warn(index,'index'); }
      }
      const machineIndex = ms.find(m => m >= 201 && m <= 209);
      if (machineIndex != null && /INDEX|TURN|ROTAT/i.test(raw)) { gap(); warn(index,'index'); }
      for (const m of ms) if (!ordinaryM.has(m) && m !== machineIndex) warn(index,'auxiliary','M' + m);
      if (gs.some(g => [41,42].includes(g))) warn(index,'compensation');
      const unsupported = gs.find(g => !allowedG.has(g) && g !== 69);
      if (unsupported !== undefined || (['U','V','W'].some(axis => words[axis] !== undefined) && !(brother && gs.some(g => [77,83].includes(g))))) {
        warn(index,'unsupported',unsupported == null ? 'UVW' : 'G' + unsupported); gap(); continue;
      }
      if (blockedTransform || macroCycle) { gap(); continue; }
      if (gs.includes(4)) continue;
      const newCycle = gs.find(g => [73,77,81,82,83,84,85,86,89].includes(g));
      if (newCycle === 77 && !brother) { warn(index,'unsupported','G77'); gap(); continue; }
      if (newCycle !== undefined) {
        if (cycle !== newCycle) { initialCycleZ = known[2] ? pos[2] : null; cycleZ = null; cycleR = null; }
        cycle = newCycle;
      }
      const hasXYZ = ['X','Y','Z'].some(axis => words[axis] !== undefined);
      if (!hasXYZ && !(motion >= 2 && ['I','J','K','R'].some(axis => words[axis] !== undefined)) && newCycle === undefined) {
        if (ms.includes(2) || ms.includes(30)) endProgram(index);
        continue;
      }
      const target = pos.slice(), targetKnown = known.slice();
      row.motion = 'G' + String(cycle || motion).padStart(2, '0');
      ['X','Y','Z'].forEach((axis,i) => {
        if (words[axis] === undefined) return;
        target[i] = absolute ? words[axis] * units : pos[i] + words[axis] * units;
        targetKnown[i] = absolute || known[i];
      });
      if (cycle) {
        if (words.R !== undefined) cycleR = absolute ? words.R * units : pos[2] + words.R * units;
        if (words.Z !== undefined) cycleZ = absolute ? words.Z * units : (cycleR ?? pos[2]) + words.Z * units;
        if (plane !== 17 || !known.every(Boolean) || !targetKnown[0] || !targetKnown[1] || cycleZ === null || cycleR === null || cycleZ >= cycleR) { warn(index,'cycle'); gap(); continue; }
        let cursor = pos.slice();
        const move = (point,rapid) => { append(cursor,point,rapid,index); cursor = point; };
        if (cursor[2] < cycleR) move([cursor[0],cursor[1],cycleR],true);
        move([target[0],target[1],cursor[2]],true);
        if (words.L === 0) { pos = cursor; continue; }
        move([target[0],target[1],cycleR],true);
        if ([73,83].includes(cycle)) warn(index,'cycleEnvelope','G' + cycle);
        move([target[0],target[1],cycleZ],false);
        move([target[0],target[1],cycleR],![77,84,85,89].includes(cycle));
        if (retract === 98) move([target[0],target[1],Math.max(initialCycleZ ?? cycleR,cycleR)],true);
        pos = cursor; row.motion = 'G' + cycle; ensure(current).blocks++; continue;
      }
      if (!targetKnown.every(Boolean) || !known.every(Boolean)) {
        pos = target; known = targetKnown;
        if (motion !== 0 && hasXYZ) warn(index,'anchor');
        if (known.every(Boolean)) row.point = mapped(pos);
        continue;
      }
      if (motion === 0 || motion === 1) append(pos,target,motion === 0,index);
      else {
        const axes = plane === 18 ? [2,0,1] : plane === 19 ? [1,2,0] : [0,1,2];
        const offsets = ['I','J','K'], values = {};
        if (words[offsets[axes[0]]] !== undefined) values.i = words[offsets[axes[0]]] * units;
        if (words[offsets[axes[1]]] !== undefined) values.j = words[offsets[axes[1]]] * units;
        if (words.R !== undefined) values.r = words.R * units;
        const arc = arcPoints(axes.map(a => pos[a]),axes.map(a => target[a]),values,motion === 2);
        if (!arc) { warn(index,'arc'); gap(); pos = target; continue; }
        let previous = pos;
        for (const point of arc) {
          const next = [0,0,0]; axes.forEach((axis,i) => { next[axis] = point[i]; });
          append(previous,next,false,index); previous = next;
        }
        row.motion = 'G0' + motion;
      }
      pos = target; known = targetKnown; ensure(current).blocks++;
      if (ms.includes(2) || ms.includes(30)) endProgram(index);
    }
    return {tools:order.map((id,i) => {
      const tool = tools.get(id);
      return {...tool, color:PALETTE[i % PALETTE.length], feed:new Float32Array(tool.feed), rapid:new Float32Array(tool.rapid), feedLines:new Int32Array(tool.feedLines), rapidLines:new Int32Array(tool.rapidLines)};
    }), rows, segmentCount, lineCount:lines.length, warningCount, warnings, profile:brother ? 'Brother' : 'ISO / FANUC'};
  }

  return { extractToolInfo, normalizeToolName, arcPoints, markerCircle, parseNcText, toolId, arithmetic, toolDescription };
});
