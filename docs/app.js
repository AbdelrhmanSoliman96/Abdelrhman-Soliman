const LANGUAGE_NAMES = {
  en: "English",
  ar: "Arabic",
  de: "German",
  es: "Spanish",
};

const TEXT_EXTENSIONS = new Set([
  ".txt",
  ".md",
  ".csv",
  ".json",
  ".srt",
  ".html",
  ".htm",
  ".xml",
  ".log",
]);

const form = document.getElementById("translate-form");
const fileInput = document.getElementById("file-input");
const dropzone = document.getElementById("dropzone");
const fileChip = document.getElementById("file-chip");
const sourceLang = document.getElementById("source-lang");
const targetLang = document.getElementById("target-lang");
const swapBtn = document.getElementById("swap-langs");
const submitBtn = document.getElementById("submit-btn");
const statusEl = document.getElementById("status");
const resultEl = document.getElementById("result");
const resultMeta = document.getElementById("result-meta");
const previewEl = document.getElementById("preview");
const downloadLink = document.getElementById("download-link");

let downloadObjectUrl = null;

function setStatus(message, type = "") {
  statusEl.textContent = message;
  statusEl.className = `status ${type}`.trim();
}

function setLoading(isLoading) {
  submitBtn.disabled = isLoading;
  submitBtn.classList.toggle("loading", isLoading);
}

function showSelectedFile(file) {
  if (!file) {
    fileChip.hidden = true;
    fileChip.textContent = "";
    return;
  }

  const sizeKb = Math.max(1, Math.round(file.size / 1024));
  fileChip.hidden = false;
  fileChip.textContent = `${file.name} · ${sizeKb} KB`;
}

function getExtension(filename) {
  const match = filename.toLowerCase().match(/\.[^.]+$/);
  return match ? match[0] : "";
}

function chunkText(text, maxChars = 3500) {
  if (text.length <= maxChars) return [text];

  const chunks = [];
  let remaining = text;

  while (remaining.length > 0) {
    if (remaining.length <= maxChars) {
      chunks.push(remaining);
      break;
    }

    let cut = remaining.lastIndexOf("\n", maxChars);
    if (cut < maxChars * 0.4) {
      cut = remaining.lastIndexOf(" ", maxChars);
    }
    if (cut < maxChars * 0.4) {
      cut = maxChars;
    }

    chunks.push(remaining.slice(0, cut));
    remaining = remaining.slice(cut);
  }

  return chunks;
}

async function translateChunk(text, from, to) {
  const url =
    "https://translate.googleapis.com/translate_a/single?client=gtx&sl=" +
    encodeURIComponent(from) +
    "&tl=" +
    encodeURIComponent(to) +
    "&dt=t&q=" +
    encodeURIComponent(text);

  const response = await fetch(url);
  if (!response.ok) {
    throw new Error("Google Translate request failed.");
  }

  const data = await response.json();
  if (!Array.isArray(data) || !Array.isArray(data[0])) {
    throw new Error("Unexpected translation response.");
  }

  return data[0].map((part) => part[0]).join("");
}

async function translateText(text, from, to) {
  if (!text.trim()) return text;

  const parts = chunkText(text);
  const translated = [];

  for (let i = 0; i < parts.length; i += 1) {
    const part = parts[i];
    if (!part.trim()) {
      translated.push(part);
      continue;
    }

    setStatus(`Translating with Google Translate… (${i + 1}/${parts.length})`);
    translated.push(await translateChunk(part, from, to));
  }

  return translated.join("");
}

function readAsArrayBuffer(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = () => reject(new Error("Could not read the file."));
    reader.readAsArrayBuffer(file);
  });
}

function readAsText(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = () => reject(new Error("Could not read the file."));
    reader.readAsText(file, "utf-8");
  });
}

async function extractText(file) {
  const ext = getExtension(file.name);

  if (ext === ".docx") {
    if (typeof mammoth === "undefined") {
      throw new Error("DOCX support failed to load. Refresh and try again.");
    }
    const buffer = await readAsArrayBuffer(file);
    const result = await mammoth.extractRawText({ arrayBuffer: buffer });
    return { text: result.value || "", kind: "docx" };
  }

  if (!TEXT_EXTENSIONS.has(ext) && file.type && !file.type.startsWith("text/")) {
    throw new Error("Unsupported file type. Use TXT, MD, CSV, JSON, SRT, HTML, XML, LOG, or DOCX.");
  }

  return { text: await readAsText(file), kind: "text" };
}

function buildDownload(translatedText, originalName, kind) {
  const ext = getExtension(originalName);
  const base = originalName.replace(/\.[^.]+$/, "") || "translated";

  if (kind === "docx" || ext === ".docx") {
    const content = translatedText;
    const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
    return {
      blob,
      filename: `${base}-translated.txt`,
    };
  }

  const mime = ext === ".html" || ext === ".htm" ? "text/html;charset=utf-8" : "text/plain;charset=utf-8";
  return {
    blob: new Blob([translatedText], { type: mime }),
    filename: `${base}-translated${ext || ".txt"}`,
  };
}

fileInput.addEventListener("change", () => {
  showSelectedFile(fileInput.files[0]);
  resultEl.hidden = true;
  setStatus("");
});

["dragenter", "dragover"].forEach((eventName) => {
  dropzone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropzone.classList.add("dragover");
  });
});

["dragleave", "drop"].forEach((eventName) => {
  dropzone.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropzone.classList.remove("dragover");
  });
});

dropzone.addEventListener("drop", (event) => {
  const file = event.dataTransfer.files[0];
  if (!file) return;

  const transfer = new DataTransfer();
  transfer.items.add(file);
  fileInput.files = transfer.files;
  showSelectedFile(file);
  resultEl.hidden = true;
  setStatus("");
});

swapBtn.addEventListener("click", () => {
  const previousSource = sourceLang.value;
  sourceLang.value = targetLang.value;
  targetLang.value = previousSource;
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const file = fileInput.files[0];
  if (!file) {
    setStatus("Please choose a file to translate.", "error");
    return;
  }

  if (file.size > 5 * 1024 * 1024) {
    setStatus("File is too large. Maximum size is 5 MB.", "error");
    return;
  }

  if (sourceLang.value === targetLang.value) {
    setStatus("Choose two different languages.", "error");
    return;
  }

  setLoading(true);
  setStatus("Reading your file…");
  resultEl.hidden = true;

  try {
    const { text, kind } = await extractText(file);
    if (!text.trim()) {
      throw new Error("The file appears to be empty.");
    }

    const translatedText = await translateText(text, sourceLang.value, targetLang.value);
    const output = buildDownload(translatedText, file.name, kind);

    if (downloadObjectUrl) {
      URL.revokeObjectURL(downloadObjectUrl);
    }
    downloadObjectUrl = URL.createObjectURL(output.blob);

    resultMeta.textContent = `${file.name} · ${LANGUAGE_NAMES[sourceLang.value]} → ${LANGUAGE_NAMES[targetLang.value]} · ${output.filename}`;
    previewEl.textContent = translatedText.slice(0, 1200) || "(No preview available)";
    previewEl.dir = targetLang.value === "ar" ? "rtl" : "ltr";
    downloadLink.href = downloadObjectUrl;
    downloadLink.download = output.filename;
    resultEl.hidden = false;
    setStatus("Translation complete. Download your file below.", "success");
  } catch (error) {
    setStatus(error.message || "Something went wrong.", "error");
  } finally {
    setLoading(false);
  }
});
