const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const core = require('../nc-viewer-core.js');
const worker = require('../nc-demo-lite-worker.js');
const fixture = require('./fixtures/nc-native-viewer.json');

test('public tool-description parser matches the executed native module', () => {
  for (const item of fixture.tools) assert.deepEqual(core.extractToolInfo(item.line), item.expected, item.line);
});

test('IJ, helical, full-circle and signed-R arcs match native point coordinates', () => {
  for (const item of fixture.arcs) {
    const points = core.arcPoints(item.start, item.end, item.values, item.clockwise);
    assert.equal(points.length, item.points.length, item.label);
    points.forEach((p, i) => p.forEach((n, axis) => assert.ok(Math.abs(n - item.points[i][axis]) < 1e-10, `${item.label} ${i}/${axis}`)));
  }
});

test('diameter circles use physical world scale and preserve the tool center', () => {
  const center = [15, -20, 8];
  for (const diameter of [6, 8, 20, 31.5]) {
    const points = core.markerCircle(center, diameter);
    assert.equal(points.length, 96);
    for (const point of points) {
      assert.ok(Math.abs(Math.hypot(point[0] - center[0], point[1] - center[1]) - diameter / 2) < 1e-10);
      assert.equal(point[2], center[2]);
    }
  }
  for (const value of [undefined, null, 0, -2, NaN, Infinity]) assert.deepEqual(core.markerCircle(center, value), []);
});

test('sample has three distinct tools, expected diameters, paths and rapid segments', () => {
  const sample = fs.readFileSync(path.join(__dirname, '../demo-data/flowmatic-nc-sample.nc'), 'utf8');
  const result = worker.parseNcText(sample, {});
  assert.deepEqual(result.scene.tools.map((tool) => [tool.id, tool.diameter]), [['T01', 20], ['T02', 8], ['T03', 6]]);
  assert.equal(result.scene.warningCount, 0);
  assert.ok(result.scene.segmentCount > 180);
  for (const tool of result.scene.tools) {
    assert.ok(tool.feed instanceof Float32Array); assert.ok(tool.rapid instanceof Float32Array);
    assert.ok(tool.feed.length > 0 && tool.rapid.length > 0);
    assert.ok(tool.feed.every(Number.isFinite)); assert.ok(tool.rapid.every(Number.isFinite));
  }
  assert.ok(result.totals.totalTheoreticalTime > 0);
});

test('T preselection does not change the active tool before M6; comments do not create tools', () => {
  const result = core.parseNcText('T01 M6 (D10 DRILL)\nT02\nG0 X0 Y0 Z5\nG1 Z0 F100 (T16)\nM6\nG1 X10\nM30');
  assert.deepEqual(result.tools.map((t) => t.id), ['T01', 'T02']);
  assert.deepEqual([...result.tools[0].feed], [0,0,5,0,0,0]);
  assert.deepEqual([...result.tools[1].feed], [0,0,0,10,0,0]);
});

test('native Fanuc tool comments attach the diameter and M97 preselection stays excluded', () => {
  const result = core.parseNcText('N110M1(D18.5 DRILL)\nT07(HV10000_T1007)\nM97T08\nG90G54G0X0Y0Z10\nG1 Z0 F100\nG0X0Y0T11M6\nG1X10F100');
  assert.deepEqual(result.tools.map((t) => t.id), ['T07', 'T11']);
  assert.equal(result.tools[0].diameter, 18.5);
});

test('incremental moves and inch units are converted into consistent millimetres', () => {
  const result = core.parseNcText('G20\nT1 (D0.5 ENDMILL)\nG90 G0 X0 Y0 Z1\nG91 G1 X1 Y0 Z-0.5 F10\nG90 G1 X0 Y1');
  assert.equal(result.warningCount, 0);
  assert.equal(result.tools[0].diameter, 12.7);
  const points = [...result.tools[0].feed];
  assert.ok(Math.abs(points[3]-25.4)<0.00001);
  assert.ok(Math.abs(points[5]-12.7)<0.00001);
  assert.ok(Math.abs(points[10]-25.4)<0.00001);
});

test('G81 separates feed and rapid motion and observes G98 return height', () => {
  const result = core.parseNcText('T1\nG0 X0 Y0 Z10\nG98 G81 X5 Y5 Z-5 R2 F100\nX10 Y5\nG80\nG0 Z20');
  assert.equal(result.warningCount, 0);
  assert.deepEqual([...result.tools[0].feed], [5,5,2,5,5,-5,10,5,2,10,5,-5]);
  const rapid = [...result.tools[0].rapid];
  assert.deepEqual(rapid.slice(-6), [10,5,10,10,5,20]);
});

test('G18 and G19 arcs remain on their programmed planes', () => {
  const xz = core.parseNcText('T1\nG0 X0 Y3 Z0\nG18 G3 X10 Z10 I0 K10');
  assert.equal(xz.warningCount, 0);
  const a = [...xz.tools[0].feed];
  for(let n=1; n<a.length; n+=3) assert.equal(a[n], 3);
  const yz = core.parseNcText('T1\nG0 X4 Y0 Z0\nG19 G3 Y10 Z10 J0 K10');
  assert.equal(yz.warningCount, 0);
  const b = [...yz.tools[0].feed];
  for(let n=0; n<b.length; n+=3) assert.equal(b[n], 4);
});

test('machine reference return creates a gap until absolute coordinates are known again', () => {
  const result = core.parseNcText('T1\nG0 X0 Y0 Z5\nG1 X10\nG91 G28 Z0\nG90 G0 X0 Y0 Z5\nG1 X20');
  assert.deepEqual([...result.tools[0].feed], [0,0,5,10,0,5,0,0,5,20,0,5]);
  assert.ok(result.warnings.some((w) => w.code === 'reference'));
});

test('macro flow and unsupported transforms cannot silently produce invented paths', () => {
  for (const command of ['G1 X#100', 'M98 P1234', 'G68 X0 Y0 R30']) {
    const result = core.parseNcText(`T1\nG0 X0 Y0 Z5\nG1 X10\n${command}\nG1 X999`);
    assert.deepEqual([...result.tools[0].feed], [0,0,5,10,0,5]);
    assert.ok(result.warningCount > 0);
  }
  assert.equal(core.arcPoints([0,0,0], [100,0,0], {r:1}, false), null);
});

test('empty input and unassigned tools have usable empty or path states', () => {
  assert.equal(core.parseNcText('').segmentCount, 0);
  const result = core.parseNcText('G0 X0 Y0 Z5\nG1 X10 F100');
  assert.equal(result.tools[0].id, '—');
  assert.equal(result.tools[0].diameter, null);
  assert.equal(result.segmentCount, 1);
});

test('worker keeps the existing theoretical-time result for a known straight move', () => {
  const result = worker.parseNcText('T01 M6\nG0 X0 Y0 Z10\nG1 Z0 F300\nG1 X100 F600\nM30', {});
  assert.ok(Math.abs(result.totals.cuttingTime - 12) < 1e-9);
  assert.ok(Math.abs(result.totals.rapidTime - 0.03) < 1e-9);
  assert.ok(Math.abs(result.totals.totalTheoreticalTime - 18.03) < 1e-9);
});

test('setup registers do not create tool motion; Brother tool changes and depth envelopes remain visible', () => {
  const text = 'G90 G10 L2 P1 X-400 Y-100 Z350\n(#JOB06 HOLE T1 DRILL D20.)\nG100 T01 G43 H1 X0 Y0 Z10\nG83 Z-10 R2 W240 V18 F100\nG0 Z30\n(#JOB07 TAP T7 R.TAP MC8.*1.25)\nG100 T7 M6 X10 Y10 Z10\nG77 Z-8 R2 F100\nM30';
  const result = core.parseNcText(text);
  assert.deepEqual(result.tools.map(t => [t.id,t.diameter]), [['T01',20],['T07',8]]);
  assert.deepEqual([...result.tools[0].feed], [0,0,2,0,0,-10]);
  assert.deepEqual([...result.tools[1].feed], [10,10,2,10,10,-8,10,10,-8,10,10,2]);
  assert.ok(result.warnings.some(w => w.code === 'cycleEnvelope'));
  assert.ok(result.tools.every(t => [...t.feed,...t.rapid].every(v => Math.abs(v) <= 30)));
  assert.equal(result.rows[3].motion, 'G83');
  assert.equal(result.tools[0].firstCutLine, 3);
  for (const t of result.tools) for(const kind of ['feed','rapid']) assert.equal(t[kind+'Lines'].length,t[kind].length/6);
});

test('only constant arithmetic or assigned variables can produce coordinates', () => {
  const result = core.parseNcText('T1\n#100=5\nG0 X0 Y0 Z5\nG1 X[10+#100*2] Y[3-1]\nG1 X#999\nG1 X200\nG0 X0 Y0 Z5\nG1 X[2*(3+4)]');
  assert.deepEqual([...result.tools[0].feed], [0,0,5,20,2,5]);
  assert.ok(result.warnings.some(w => w.code === 'expression'));
  assert.equal(core.arithmetic('[2+[3*4]]'),14);
  for(const expression of ['1/0','#999','SIN[30]','process.exit()']) assert.throws(() => core.arithmetic(expression));
});

test('known XY rotation and local shifts change coordinates without joining incompatible frames', () => {
  const result = core.parseNcText('T1\nG0 X0 Y0 Z5\nG52 X10 Y20\nG0 X0 Y0 Z5\nG1 X10\nG68 X0 Y0 R90\nG0 X0 Y0 Z5\nG1 X10');
  assert.deepEqual([...result.tools[0].feed], [10,20,5,20,20,5,10,20,5,10,30,5]);
});

test('unexpanded calls and reference moves resume only from fully known coordinates', () => {
  const result = core.parseNcText('T1\nG0 X0 Y0 Z5\nG1 X10\nM98 P1234\nG1 X999\nG0 X0 Y0 Z5\nG1 X20');
  assert.deepEqual([...result.tools[0].feed], [0,0,5,10,0,5,0,0,5,20,0,5]);
  assert.ok(result.warnings.some(w => w.code === 'programFlow'));
});

test('multiple standalone programs are not silently concatenated into one executed path', () => {
  const result = core.parseNcText('O1\nT1\nG0 X0 Y0 Z5\nG1 X10\nM30\nO2\nT2\nG0 X0 Y0 Z5\nG1 X20\nM30');
  assert.equal(result.tools.length,1);
  assert.equal(result.segmentCount,1);
  assert.ok(result.warnings.some(w => w.code === 'multiplePrograms'));
});

test('unresolved rotary transforms and machine container formats are explicit exclusions', () => {
  const result = core.parseNcText('T1\nG0 X0 Y0 Z5\nG68 X0 Y0 R#999\nG0 X0 Y0 Z5\nG1 X10\nG69\nG0 X0 Y0 Z5\nG1 X20');
  assert.deepEqual([...result.tools[0].feed], [0,0,5,20,0,5]);
  assert.throws(() => core.parseNcText('10A@ABCDEF'),/format/);
  assert.throws(() => core.parseNcText('G0\x00X0'),/format/);
});
