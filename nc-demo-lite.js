(function initFlowmaticNcDemoLite() {
  "use strict";

  const roots = document.querySelectorAll("[data-nc-demo-lite]");
  if (!roots.length) return;

  const TEXT = {
    ko: {
      idle: "샘플을 실행하거나 로컬 NC 파일을 선택하세요.",
      working: "분석 중입니다.",
      basic: "Basic Estimate · 기본 이동 명령 기준으로 계산되었습니다.",
      partial: "Partial Estimate · 일부 명령이 계산에서 제외된 부분 결과입니다.",
      unable: "Unable to Estimate · 이 파일에서는 계산 가능한 기본 이동 명령을 찾지 못했습니다.",
      defaultFeed: (n) => `F값이 없는 이동 ${n}개에 기본 Feed를 사용했습니다.`,
      canned: (n) => `Canned Cycle ${n}개가 감지되었으며 공개 데모 계산에서 제외되었습니다.`,
      g91: (n) => `G91 증분좌표 구간 이동 ${n}개를 계산에서 제외했습니다.`,
      arcPlane: (n) => `G18/G19 원호 ${n}개는 공개 데모 계산에서 제외했습니다.`,
      macro: (n) => `Macro Variable 또는 수식이 포함된 ${n}개 행을 계산에서 제외했습니다.`,
      subprogram: (n) => `Subprogram 호출 ${n}개는 공개 데모에서 전개하지 않습니다.`,
      invalidArc: (n) => `유효하지 않은 원호 ${n}개를 계산에서 제외했습니다.`,
      feedInvalid: (n) => `유효하지 않은 F값 ${n}개를 무시했습니다.`,
      unsupported: (n) => `지원하지 않는 G-code ${n}개를 감지했습니다.`,
      longLine: (n) => `비정상적으로 긴 행 ${n}개는 앞부분만 분석했습니다.`,
      fileSize: "5MB 이하 파일만 분석할 수 있습니다.",
      lineLimit: "100,000행 이하 파일만 분석할 수 있습니다.",
      extension: "지원 확장자는 .nc, .cnc, .tap, .txt, .min 입니다.",
      readError: "파일을 읽을 수 없습니다.",
      noWarnings: "표시할 경고가 없습니다.",
      noTools: "공구별 결과가 아직 없습니다.",
      sampleName: "flowmatic-nc-sample.nc",
      sampleLoadError: "샘플 파일을 불러올 수 없습니다.",
      unassigned: "No Tool",
      previewEmpty: "읽기 전용 미리보기는 분석 후 표시됩니다.",
      normal: "정상 계산",
      default: "기본값 적용",
      excluded: "계산 제외",
      detected: "감지 전용",
      neutral: "무시",
      cut: "Cut",
      rapid: "Rapid",
      change: "Change",
      total: "Total"
    },
    en: {
      idle: "Run the sample or choose a local NC file.",
      working: "Analyzing.",
      basic: "Basic Estimate · Calculated from basic motion commands.",
      partial: "Partial Estimate · Some commands were excluded from the calculation.",
      unable: "Unable to Estimate · No calculable basic motion commands were found.",
      defaultFeed: (n) => `Default feed was used for ${n} move(s) without F values.`,
      canned: (n) => `${n} canned cycle block(s) were detected and excluded from this public estimate.`,
      g91: (n) => `${n} G91 incremental move(s) were excluded.`,
      arcPlane: (n) => `${n} G18/G19 arc(s) were excluded from this public estimate.`,
      macro: (n) => `${n} line(s) with macro variables or expressions were excluded.`,
      subprogram: (n) => `${n} subprogram call(s) were detected but not expanded.`,
      invalidArc: (n) => `${n} invalid arc(s) were excluded.`,
      feedInvalid: (n) => `${n} invalid F value(s) were ignored.`,
      unsupported: (n) => `${n} unsupported G-code command(s) were detected.`,
      longLine: (n) => `${n} unusually long line(s) were partially analyzed.`,
      fileSize: "Only files up to 5MB can be analyzed.",
      lineLimit: "Only files up to 100,000 lines can be analyzed.",
      extension: "Supported extensions are .nc, .cnc, .tap, .txt, and .min.",
      readError: "The file could not be read.",
      noWarnings: "No warnings to show.",
      noTools: "No tool result yet.",
      sampleName: "flowmatic-nc-sample.nc",
      sampleLoadError: "The sample file could not be loaded.",
      unassigned: "No Tool",
      previewEmpty: "The read-only preview appears after analysis.",
      normal: "Calculated",
      default: "Default used",
      excluded: "Excluded",
      detected: "Detected",
      neutral: "Ignored",
      cut: "Cut",
      rapid: "Rapid",
      change: "Change",
      total: "Total"
    },
    ar: {
      idle: "شغّل العينة أو اختر ملف NC محليًا.",
      working: "جارٍ التحليل.",
      basic: "Basic Estimate · تم الحساب من أوامر الحركة الأساسية.",
      partial: "Partial Estimate · تم استبعاد بعض الأوامر من الحساب.",
      unable: "Unable to Estimate · لم يتم العثور على أوامر حركة أساسية قابلة للحساب.",
      defaultFeed: (n) => `تم استخدام Feed الافتراضي في ${n} حركة بدون قيمة F.`,
      canned: (n) => `تم اكتشاف ${n} دورة Canned Cycle واستبعادها من هذا التقدير العام.`,
      g91: (n) => `تم استبعاد ${n} حركة G91 incremental.`,
      arcPlane: (n) => `تم استبعاد ${n} قوس G18/G19 من هذا التقدير العام.`,
      macro: (n) => `تم استبعاد ${n} سطر يحتوي على Macro أو تعبيرات.`,
      subprogram: (n) => `تم اكتشاف ${n} استدعاء Subprogram دون توسيعه.`,
      invalidArc: (n) => `تم استبعاد ${n} قوس غير صالح.`,
      feedInvalid: (n) => `تم تجاهل ${n} قيمة F غير صالحة.`,
      unsupported: (n) => `تم اكتشاف ${n} أمر G-code غير مدعوم.`,
      longLine: (n) => `تم تحليل بداية ${n} سطر طويل بشكل غير معتاد.`,
      fileSize: "يمكن تحليل ملفات حتى 5MB فقط.",
      lineLimit: "يمكن تحليل ملفات حتى 100,000 سطر فقط.",
      extension: "الصيغ المدعومة هي .nc و .cnc و .tap و .txt و .min.",
      readError: "تعذرت قراءة الملف.",
      noWarnings: "لا توجد تحذيرات.",
      noTools: "لا توجد نتيجة حسب الأداة بعد.",
      sampleName: "flowmatic-nc-sample.nc",
      sampleLoadError: "تعذر تحميل ملف العينة.",
      unassigned: "No Tool",
      previewEmpty: "تظهر المعاينة للقراءة فقط بعد التحليل.",
      normal: "محسوب",
      default: "استخدم الافتراضي",
      excluded: "مستبعد",
      detected: "مكتشف",
      neutral: "متجاهل",
      cut: "Cut",
      rapid: "Rapid",
      change: "Change",
      total: "Total"
    }
  };

  const MAX_FILE_SIZE = 5 * 1024 * 1024;
  const VALID_EXTENSIONS = [".nc", ".cnc", ".tap", ".txt", ".min"];

  function currentLang() {
    const lang = document.body.dataset.lang || document.documentElement.lang || "ko";
    return TEXT[lang] ? lang : "ko";
  }

  function copy() {
    return TEXT[currentLang()];
  }

  function formatSeconds(seconds) {
    if (!Number.isFinite(seconds)) return "—";
    const value = seconds >= 100 ? seconds.toFixed(1) : seconds.toFixed(2);
    return currentLang() === "ko" ? `${value}초` : `${value} sec`;
  }

  function formatBytes(bytes) {
    if (!Number.isFinite(bytes)) return "—";
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  }

  function setText(root, selector, value) {
    const element = root.querySelector(selector);
    if (element) element.textContent = value;
  }

  function createElement(tag, className, text) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text !== undefined) element.textContent = text;
    return element;
  }

  function supportedFileName(fileName) {
    const lower = String(fileName || "").toLowerCase();
    return VALID_EXTENSIONS.some((extension) => lower.endsWith(extension));
  }

  function readSettings(root, previous) {
    const next = { ...previous };
    const fields = root.querySelectorAll("[data-nc-setting]");
    fields.forEach((field) => {
      const key = field.dataset.ncSetting;
      const fallback = previous[key];
      const value = Number.parseFloat(field.value);
      const valid = Number.isFinite(value) && value >= 0 && (key === "toolChange" || value > 0);
      if (!valid) {
        field.value = String(fallback);
        return;
      }
      next[key] = value;
    });
    return next;
  }

  function resetBars(root) {
    root.querySelectorAll("[data-nc-bar]").forEach((bar) => {
      bar.style.flexBasis = "0%";
      bar.textContent = "";
    });
  }

  function renderEmpty(root) {
    const t = copy();
    setText(root, '[data-nc-result="total"]', "—");
    setText(root, '[data-nc-result="status"]', t.idle);
    ["cutting", "rapid", "toolChange", "tools", "motionBlocks", "excludedBlocks"].forEach((key) => {
      setText(root, `[data-nc-result="${key}"]`, "—");
    });
    ["file", "size", "lines", "motions", "excluded"].forEach((key) => {
      setText(root, `[data-nc-meta="${key}"]`, "—");
    });
    resetBars(root);
    const warnings = root.querySelector("[data-nc-warnings]");
    if (warnings) {
      warnings.textContent = "";
      warnings.appendChild(createElement("li", "", t.noWarnings));
    }
    const tools = root.querySelector("[data-nc-tools]");
    if (tools) tools.textContent = t.noTools;
    const preview = root.querySelector("[data-nc-preview]");
    if (preview) preview.textContent = t.previewEmpty;
    const alert = root.querySelector("[data-nc-alert]");
    if (alert) {
      alert.hidden = true;
      alert.textContent = "";
    }
  }

  function renderError(root, message) {
    const alert = root.querySelector("[data-nc-alert]");
    if (alert) {
      alert.hidden = false;
      alert.textContent = message;
    }
    setText(root, '[data-nc-result="status"]', message);
  }

  function warningText(item) {
    const t = copy();
    const formatter = t[item.code];
    return typeof formatter === "function" ? formatter(item.count) : `${item.code}: ${item.count}`;
  }

  function renderWarnings(root, warnings) {
    const t = copy();
    const list = root.querySelector("[data-nc-warnings]");
    const toggle = root.querySelector("[data-nc-show-warnings]");
    if (!list) return;
    list.textContent = "";
    const all = warnings.length ? warnings : [{ code: "none", count: 0, category: "default" }];
    const visible = warnings.length ? warnings.slice(0, root.dataset.ncWarningsExpanded === "true" ? warnings.length : 5) : all;
    visible.forEach((item) => {
      const li = createElement("li", item.category ? `is-${item.category}` : "", item.code === "none" ? t.noWarnings : warningText(item));
      list.appendChild(li);
    });
    if (toggle) {
      toggle.hidden = warnings.length <= 5 || root.dataset.ncWarningsExpanded === "true";
    }
  }

  function renderTools(root, tools) {
    const t = copy();
    const list = root.querySelector("[data-nc-tools]");
    if (!list) return;
    list.textContent = "";
    if (!tools.length) {
      list.textContent = t.noTools;
      return;
    }
    tools.forEach((tool) => {
      const card = createElement("article", "nc-demo-tool-card");
      const name = createElement("strong", "", tool.tool === "Unassigned" ? t.unassigned : tool.tool);
      const meta = createElement("span", "", `${t.cut} ${formatSeconds(tool.cuttingTime)} | ${t.rapid} ${formatSeconds(tool.rapidTime)} | ${t.change} ${tool.toolChangeCount} | ${t.total} ${formatSeconds(tool.totalTime)}`);
      card.append(name, meta);
      list.appendChild(card);
    });
  }

  function renderPreview(root, previewLines) {
    const t = copy();
    const preview = root.querySelector("[data-nc-preview]");
    if (!preview) return;
    preview.textContent = "";
    if (!previewLines.length) {
      preview.textContent = t.previewEmpty;
      return;
    }
    previewLines.forEach((line) => {
      const row = createElement("div", `is-${line.status || "neutral"}`);
      row.append(
        createElement("span", "nc-demo-line-number", String(line.lineNumber).padStart(4, "0")),
        createElement("span", "nc-demo-line-badge", t[line.status] || line.label || t.detected),
        createElement("code", "", line.text || "")
      );
      preview.appendChild(row);
    });
  }

  function renderBars(root, totals) {
    const values = {
      cutting: totals.cuttingTime || 0,
      rapid: totals.rapidTime || 0,
      toolChange: totals.toolChangeTime || 0
    };
    const sum = Math.max(values.cutting + values.rapid + values.toolChange, 0);
    root.querySelectorAll("[data-nc-bar]").forEach((bar) => {
      const key = bar.dataset.ncBar;
      const percent = sum > 0 ? (values[key] / sum) * 100 : 0;
      bar.style.flexBasis = `${percent}%`;
      bar.textContent = percent >= 8 ? `${percent.toFixed(0)}%` : "";
    });
  }

  function renderResult(root, result, fileMeta) {
    const totals = result.totals || {};
    const t = copy();
    setText(root, '[data-nc-result="total"]', formatSeconds(totals.totalTheoreticalTime));
    setText(root, '[data-nc-result="status"]', t[result.status] || t.partial);
    setText(root, '[data-nc-result="cutting"]', formatSeconds(totals.cuttingTime));
    setText(root, '[data-nc-result="rapid"]', formatSeconds(totals.rapidTime));
    setText(root, '[data-nc-result="toolChange"]', formatSeconds(totals.toolChangeTime));
    setText(root, '[data-nc-result="tools"]', String((result.tools || []).length));
    setText(root, '[data-nc-result="motionBlocks"]', String(totals.motionBlocks || 0));
    setText(root, '[data-nc-result="excludedBlocks"]', String(totals.excludedBlocks || 0));
    setText(root, '[data-nc-meta="file"]', fileMeta.name || "—");
    setText(root, '[data-nc-meta="size"]', formatBytes(fileMeta.size));
    setText(root, '[data-nc-meta="lines"]', String(totals.lineCount || "—"));
    setText(root, '[data-nc-meta="motions"]', String(totals.motionBlocks || 0));
    setText(root, '[data-nc-meta="excluded"]', String(totals.excludedBlocks || 0));
    renderBars(root, totals);
    renderWarnings(root, result.warnings || []);
    renderTools(root, result.tools || []);
    renderPreview(root, result.preview || []);
  }

  function workerRequest(worker, action, payload, transfer) {
    const id = `${Date.now()}-${Math.random().toString(16).slice(2)}`;
    return new Promise((resolve, reject) => {
      const onMessage = (event) => {
        if (!event.data || event.data.id !== id) return;
        worker.removeEventListener("message", onMessage);
        if (event.data.ok) resolve(event.data.result);
        else reject(event.data.error || new Error("Worker error"));
      };
      worker.addEventListener("message", onMessage);
      worker.postMessage({ id, action, ...payload }, transfer || []);
    });
  }

  roots.forEach((root) => {
    let settings = { rapidFeed: 20000, defaultFeed: 1000, toolChange: 6 };
    let lastSource = null;
    const worker = new Worker("/nc-demo-lite-worker.js?v=1.0");
    const fileInput = root.querySelector("[data-nc-file]");
    const dropzone = root.querySelector("[data-nc-dropzone]");
    const sampleButton = root.querySelector("[data-nc-sample]");
    const resetButton = root.querySelector("[data-nc-reset]");
    const recalculateButton = root.querySelector("[data-nc-recalculate]");
    const warningsButton = root.querySelector("[data-nc-show-warnings]");

    async function analyzeSource(source) {
      const t = copy();
      settings = readSettings(root, settings);
      setText(root, '[data-nc-result="status"]', t.working);
      const meta = { name: source.name, size: source.size };
      try {
        let result;
        if (source.type === "file") {
          const buffer = await source.file.arrayBuffer();
          result = await workerRequest(worker, "parseBuffer", { buffer, options: settings }, [buffer]);
        } else {
          result = await workerRequest(worker, "parseText", { text: source.text, options: settings });
        }
        renderResult(root, result, meta);
      } catch (error) {
        const message = t[error.code] || error.message || t.readError;
        renderError(root, message);
      }
    }

    async function useFile(file) {
      const t = copy();
      if (!file) return;
      if (!supportedFileName(file.name)) {
        renderError(root, t.extension);
        return;
      }
      if (file.size > MAX_FILE_SIZE) {
        renderError(root, t.fileSize);
        return;
      }
      lastSource = { type: "file", file, name: file.name, size: file.size };
      await analyzeSource(lastSource);
    }

    if (fileInput) {
      fileInput.addEventListener("change", () => useFile(fileInput.files && fileInput.files[0]));
    }

    if (dropzone) {
      ["dragenter", "dragover"].forEach((name) => {
        dropzone.addEventListener(name, (event) => {
          event.preventDefault();
          dropzone.classList.add("is-dragging");
        });
      });
      ["dragleave", "drop"].forEach((name) => {
        dropzone.addEventListener(name, (event) => {
          event.preventDefault();
          dropzone.classList.remove("is-dragging");
        });
      });
      dropzone.addEventListener("drop", (event) => {
        const file = event.dataTransfer && event.dataTransfer.files && event.dataTransfer.files[0];
        useFile(file);
      });
      dropzone.addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          if (fileInput) fileInput.click();
        }
      });
    }

    if (sampleButton) {
      sampleButton.addEventListener("click", async () => {
        const t = copy();
        try {
          const response = await fetch("/demo-data/flowmatic-nc-sample.nc", { cache: "no-store" });
          if (!response.ok) throw new Error(t.sampleLoadError);
          const text = await response.text();
          lastSource = { type: "text", text, name: t.sampleName, size: new Blob([text]).size };
          await analyzeSource(lastSource);
        } catch (_) {
          renderError(root, t.sampleLoadError);
        }
      });
    }

    if (resetButton) {
      resetButton.addEventListener("click", () => {
        lastSource = null;
        root.dataset.ncWarningsExpanded = "false";
        if (fileInput) fileInput.value = "";
        renderEmpty(root);
      });
    }

    if (recalculateButton) {
      recalculateButton.addEventListener("click", () => {
        settings = readSettings(root, settings);
        if (lastSource) analyzeSource(lastSource);
      });
    }

    if (warningsButton) {
      warningsButton.addEventListener("click", () => {
        root.dataset.ncWarningsExpanded = "true";
        if (lastSource) analyzeSource(lastSource);
      });
    }

    renderEmpty(root);
  });
})();
