(function expose(root, factory) {
  const api = factory();
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (root) {
    root.FlowmaticNcDemoLiteWorker = api;
    if (root.addEventListener) {
      root.addEventListener("message", (event) => {
        const request = event.data || {};
        try {
          if (request.action === "parseBuffer") {
            const text = api.decodeBuffer(request.buffer);
            root.postMessage({ id: request.id, ok: true, result: api.parseNcText(text, request.options || {}) });
          } else if (request.action === "parseText") {
            root.postMessage({ id: request.id, ok: true, result: api.parseNcText(String(request.text || ""), request.options || {}) });
          }
        } catch (error) {
          root.postMessage({ id: request.id, ok: false, error: { code: error.code || "parseError", message: error.message || String(error) } });
        }
      });
    }
  }
})(typeof self !== "undefined" ? self : globalThis, function createWorkerApi() {
  "use strict";

  const MAX_FILE_SIZE = 5 * 1024 * 1024;
  const MAX_LINES = 100000;
  const MAX_PREVIEW_LINES = 40;
  const EPS = 1e-9;
  const SUPPORTED_EXTENSIONS = new Set([".nc", ".cnc", ".tap", ".txt", ".min"]);
  const SUPPORTED_G = new Set([0, 1, 2, 3, 17, 90, 91]);
  const CANNED = new Set([73, 74, 76, 77, 81, 82, 83, 84, 85, 86, 87, 88, 89]);

  function makeError(code, message) {
    const error = new Error(message);
    error.code = code;
    return error;
  }

  function decodeBuffer(buffer) {
    if (!buffer || buffer.byteLength > MAX_FILE_SIZE) {
      throw makeError("fileSize", "File is larger than 5MB.");
    }
    const bytes = new Uint8Array(buffer);
    if (bytes.length >= 3 && bytes[0] === 0xef && bytes[1] === 0xbb && bytes[2] === 0xbf) {
      return new TextDecoder("utf-8").decode(bytes.subarray(3));
    }
    try {
      return new TextDecoder("utf-8", { fatal: true }).decode(bytes);
    } catch (_) {
      try {
        return new TextDecoder("euc-kr").decode(bytes);
      } catch (_) {
        try {
          return new TextDecoder("windows-949").decode(bytes);
        } catch (_) {
          return new TextDecoder("latin1").decode(bytes);
        }
      }
    }
  }

  function safeNumber(value, fallback) {
    const number = Number(value);
    return Number.isFinite(number) ? number : fallback;
  }

  function normalizeSettings(options) {
    const rapidFeed = Math.max(1, safeNumber(options.rapidFeed, 20000));
    const defaultFeed = Math.max(1, safeNumber(options.defaultFeed, 1000));
    const toolChange = Math.max(0, safeNumber(options.toolChange, 6));
    return { rapidFeed, defaultFeed, toolChange };
  }

  function stripExecutionText(line) {
    return String(line || "")
      .replace(/\([^)]*\)/g, " ")
      .replace(/;.*/, " ")
      .replace(/%/g, " ")
      .toUpperCase();
  }

  function tokenize(cleanLine) {
    const tokens = [];
    const pattern = /([GMTFXYZIJR])\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))/g;
    let match;
    while ((match = pattern.exec(cleanLine))) {
      tokens.push({ letter: match[1], value: Number.parseFloat(match[2]) });
    }
    return tokens;
  }

  function lastToken(tokens, letter) {
    for (let i = tokens.length - 1; i >= 0; i -= 1) {
      if (tokens[i].letter === letter && Number.isFinite(tokens[i].value)) return tokens[i].value;
    }
    return null;
  }

  function formatTool(value) {
    if (!Number.isFinite(value)) return "Unassigned";
    return `T${String(Math.trunc(Math.abs(value))).padStart(2, "0")}`;
  }

  function hasM6(tokens) {
    return tokens.some((token) => token.letter === "M" && Math.trunc(Math.abs(token.value)) === 6);
  }

  function lineHasMacro(cleanLine) {
    return /#|\[[^\]]*\]|\b(WHILE|GOTO|SIN|COS|TAN|SQRT|IF)\b/.test(cleanLine);
  }

  function lineHasSubprogram(cleanLine) {
    return /\bM\s*0?98\b|\bM\s*0?99\b/.test(cleanLine);
  }

  function distance3(a, b) {
    return Math.hypot(b.x - a.x, b.y - a.y, b.z - a.z);
  }

  function sweepRadians(startAngle, endAngle, clockwise) {
    if (Math.abs(startAngle - endAngle) < EPS) return Math.PI * 2;
    if (clockwise) {
      let sweep = startAngle - endAngle;
      if (sweep <= 0) sweep += Math.PI * 2;
      return sweep;
    }
    let sweep = endAngle - startAngle;
    if (sweep <= 0) sweep += Math.PI * 2;
    return sweep;
  }

  function arcFromIj(start, end, iValue, jValue, clockwise) {
    const center = { x: start.x + iValue, y: start.y + jValue };
    const radius = Math.hypot(start.x - center.x, start.y - center.y);
    if (!Number.isFinite(radius) || radius <= EPS) return null;
    const startAngle = Math.atan2(start.y - center.y, start.x - center.x);
    const endAngle = Math.atan2(end.y - center.y, end.x - center.x);
    const sweep = sweepRadians(startAngle, endAngle, clockwise);
    const arcLength = radius * Math.abs(sweep);
    return Math.hypot(arcLength, end.z - start.z);
  }

  function arcFromR(start, end, rValue, clockwise) {
    const radius = Math.abs(rValue);
    const dx = end.x - start.x;
    const dy = end.y - start.y;
    const chord = Math.hypot(dx, dy);
    if (!Number.isFinite(radius) || radius <= EPS || chord <= EPS || radius + EPS < chord / 2) return null;
    const mid = { x: (start.x + end.x) / 2, y: (start.y + end.y) / 2 };
    const h = Math.sqrt(Math.max(0, (radius * radius) - ((chord / 2) * (chord / 2))));
    const ux = -dy / chord;
    const uy = dx / chord;
    const candidates = [
      { x: mid.x + ux * h, y: mid.y + uy * h },
      { x: mid.x - ux * h, y: mid.y - uy * h }
    ];
    const wantsLongArc = rValue < 0;
    let best = null;
    candidates.forEach((center) => {
      const startAngle = Math.atan2(start.y - center.y, start.x - center.x);
      const endAngle = Math.atan2(end.y - center.y, end.x - center.x);
      const sweep = sweepRadians(startAngle, endAngle, clockwise);
      const isLong = sweep > Math.PI + EPS;
      const score = (isLong === wantsLongArc ? 0 : 10) + Math.abs((wantsLongArc ? Math.PI * 1.5 : Math.PI / 2) - sweep);
      if (!best || score < best.score) best = { sweep, score };
    });
    if (!best) return null;
    return Math.hypot(radius * best.sweep, end.z - start.z);
  }

  function createWarningItems(counts) {
    const items = [];
    const push = (code, count, category) => { if (count > 0) items.push({ code, count, category }); };
    push("defaultFeed", counts.defaultFeedMoves, "default");
    push("canned", counts.canned, "excluded");
    push("g91", counts.g91Moves, "excluded");
    push("arcPlane", counts.arcPlane, "excluded");
    push("macro", counts.macro, "excluded");
    push("subprogram", counts.subprogram, "limited");
    push("invalidArc", counts.invalidArc, "excluded");
    push("feedInvalid", counts.feedInvalid, "file");
    push("unsupported", counts.unsupported, "limited");
    push("longLine", counts.longLine, "file");
    return items;
  }

  function parseNcText(text, options) {
    const settings = normalizeSettings(options || {});
    const rawLines = String(text || "").split(/\r\n|\n|\r/);
    if (rawLines.length > MAX_LINES) throw makeError("lineLimit", "File has more than 100,000 lines.");

    const state = {
      x: 0,
      y: 0,
      z: 0,
      feed: settings.defaultFeed,
      hasExplicitFeed: false,
      motion: null,
      plane: "G17",
      absolute: true,
      currentTool: "Unassigned",
      pendingTool: null
    };
    const counts = {
      defaultFeedMoves: 0,
      canned: 0,
      g91Moves: 0,
      arcPlane: 0,
      macro: 0,
      subprogram: 0,
      invalidArc: 0,
      feedInvalid: 0,
      unsupported: 0,
      longLine: 0
    };
    const totals = {
      rapidTime: 0,
      cuttingTime: 0,
      toolChangeTime: 0,
      toolChangeCount: 0,
      motionBlocks: 0,
      excludedBlocks: 0,
      lineCount: rawLines.length
    };
    const preview = [];
    const tools = new Map();

    const bucketFor = (tool) => {
      const key = tool || "Unassigned";
      if (!tools.has(key)) {
        tools.set(key, { tool: key, cuttingTime: 0, rapidTime: 0, toolChangeCount: 0, toolChangeTime: 0, totalTime: 0 });
      }
      return tools.get(key);
    };
    bucketFor("Unassigned");

    const addPreview = (lineNumber, source, status, label) => {
      if (preview.length >= MAX_PREVIEW_LINES) return;
      preview.push({ lineNumber, text: String(source || "").slice(0, 500), status, label });
    };

    rawLines.forEach((sourceLine, index) => {
      const lineNumber = index + 1;
      let previewStatus = "neutral";
      let previewLabel = "detected";
      if (sourceLine.length > 5000) counts.longLine += 1;
      const cleanLine = stripExecutionText(sourceLine.slice(0, 5000)).replace(/\bN\s*[+-]?\d+(?:\.\d+)?\b/g, " ");
      if (!cleanLine.trim()) {
        addPreview(lineNumber, sourceLine, "neutral", "comment");
        return;
      }

      const tokens = tokenize(cleanLine);
      const gCodes = tokens.filter((token) => token.letter === "G").map((token) => Math.trunc(Math.abs(token.value)));
      const hasCoordinates = tokens.some((token) => ["X", "Y", "Z"].includes(token.letter));
      const hasArcData = tokens.some((token) => ["I", "J", "R"].includes(token.letter));
      const hasMovementIntent = hasCoordinates || hasArcData || gCodes.some((code) => [0, 1, 2, 3].includes(code));

      if (lineHasMacro(cleanLine)) {
        counts.macro += 1;
        if (hasMovementIntent) totals.excludedBlocks += 1;
        addPreview(lineNumber, sourceLine, "excluded", "macro");
        return;
      }

      if (lineHasSubprogram(cleanLine)) {
        counts.subprogram += 1;
        addPreview(lineNumber, sourceLine, "excluded", "subprogram");
        return;
      }

      const cannedCodes = gCodes.filter((code) => CANNED.has(code));
      if (cannedCodes.length) {
        counts.canned += 1;
        totals.excludedBlocks += 1;
        addPreview(lineNumber, sourceLine, "excluded", "canned");
        return;
      }

      gCodes.forEach((code) => {
        if (code === 90) state.absolute = true;
        else if (code === 91) state.absolute = false;
        else if (code === 17) state.plane = "G17";
        else if (code === 18) state.plane = "G18";
        else if (code === 19) state.plane = "G19";
        else if ([0, 1, 2, 3].includes(code)) state.motion = `G${code}`;
        else if (!SUPPORTED_G.has(code)) counts.unsupported += 1;
      });

      const tValue = lastToken(tokens, "T");
      if (tValue !== null) {
        state.pendingTool = formatTool(tValue);
        state.currentTool = state.pendingTool;
      }
      if (hasM6(tokens)) {
        const tool = tValue !== null ? formatTool(tValue) : (state.pendingTool || state.currentTool || "Unassigned");
        state.currentTool = tool;
        state.pendingTool = tool;
        totals.toolChangeCount += 1;
        totals.toolChangeTime += settings.toolChange;
        const bucket = bucketFor(tool);
        bucket.toolChangeCount += 1;
        bucket.toolChangeTime += settings.toolChange;
        previewStatus = "detected";
        previewLabel = "tool change";
      }

      const fValue = lastToken(tokens, "F");
      if (fValue !== null) {
        if (Number.isFinite(fValue) && fValue > 0) {
          state.feed = fValue;
          state.hasExplicitFeed = true;
        } else {
          counts.feedInvalid += 1;
        }
      }

      if (!hasMovementIntent) {
        addPreview(lineNumber, sourceLine, previewStatus, previewLabel);
        return;
      }

      if (!state.absolute) {
        counts.g91Moves += 1;
        totals.excludedBlocks += 1;
        addPreview(lineNumber, sourceLine, "excluded", "G91");
        return;
      }

      const motion = state.motion;
      if (!motion) {
        addPreview(lineNumber, sourceLine, "detected", "no modal motion");
        return;
      }

      const start = { x: state.x, y: state.y, z: state.z };
      const end = {
        x: lastToken(tokens, "X") ?? state.x,
        y: lastToken(tokens, "Y") ?? state.y,
        z: lastToken(tokens, "Z") ?? state.z
      };
      const tool = state.currentTool || "Unassigned";
      const bucket = bucketFor(tool);

      if (motion === "G0") {
        const distance = distance3(start, end);
        if (distance > EPS) {
          const seconds = (distance / settings.rapidFeed) * 60;
          totals.rapidTime += seconds;
          bucket.rapidTime += seconds;
          totals.motionBlocks += 1;
          previewStatus = "normal";
          previewLabel = "rapid";
        }
        state.x = end.x; state.y = end.y; state.z = end.z;
        addPreview(lineNumber, sourceLine, previewStatus, previewLabel);
        return;
      }

      if (motion === "G1") {
        const distance = distance3(start, end);
        if (distance > EPS) {
          const seconds = (distance / state.feed) * 60;
          totals.cuttingTime += seconds;
          bucket.cuttingTime += seconds;
          totals.motionBlocks += 1;
          if (!state.hasExplicitFeed) {
            counts.defaultFeedMoves += 1;
            previewStatus = "default";
            previewLabel = "default feed";
          } else {
            previewStatus = "normal";
            previewLabel = "cut";
          }
        }
        state.x = end.x; state.y = end.y; state.z = end.z;
        addPreview(lineNumber, sourceLine, previewStatus, previewLabel);
        return;
      }

      if (motion === "G2" || motion === "G3") {
        if (state.plane !== "G17") {
          counts.arcPlane += 1;
          totals.excludedBlocks += 1;
          addPreview(lineNumber, sourceLine, "excluded", state.plane);
          return;
        }
        const clockwise = motion === "G2";
        const iValue = lastToken(tokens, "I");
        const jValue = lastToken(tokens, "J");
        const rValue = lastToken(tokens, "R");
        let length = null;
        if (iValue !== null || jValue !== null) {
          length = arcFromIj(start, end, iValue || 0, jValue || 0, clockwise);
        } else if (rValue !== null) {
          length = arcFromR(start, end, rValue, clockwise);
        }
        if (!Number.isFinite(length) || length <= EPS) {
          counts.invalidArc += 1;
          totals.excludedBlocks += 1;
          addPreview(lineNumber, sourceLine, "excluded", "arc");
          return;
        }
        const seconds = (length / state.feed) * 60;
        totals.cuttingTime += seconds;
        bucket.cuttingTime += seconds;
        totals.motionBlocks += 1;
        if (!state.hasExplicitFeed) {
          counts.defaultFeedMoves += 1;
          previewStatus = "default";
          previewLabel = "default feed";
        } else {
          previewStatus = "normal";
          previewLabel = clockwise ? "G02" : "G03";
        }
        state.x = end.x; state.y = end.y; state.z = end.z;
        addPreview(lineNumber, sourceLine, previewStatus, previewLabel);
      }
    });

    tools.forEach((tool) => {
      tool.totalTime = tool.cuttingTime + tool.rapidTime + tool.toolChangeTime;
    });

    const warningItems = createWarningItems(counts);
    const totalTheoreticalTime = totals.rapidTime + totals.cuttingTime + totals.toolChangeTime;
    const status = totals.motionBlocks === 0 ? "unable" : (warningItems.some((item) => ["excluded", "limited", "file"].includes(item.category)) ? "partial" : "basic");
    return {
      totals: { ...totals, totalTheoreticalTime },
      settings,
      status,
      warnings: warningItems,
      tools: Array.from(tools.values()).filter((tool) => tool.totalTime > EPS || tool.toolChangeCount > 0),
      preview,
      limits: { maxFileSize: MAX_FILE_SIZE, maxLines: MAX_LINES },
      supportedExtensions: Array.from(SUPPORTED_EXTENSIONS)
    };
  }

  return { parseNcText, decodeBuffer, MAX_FILE_SIZE, MAX_LINES, SUPPORTED_EXTENSIONS };
});
