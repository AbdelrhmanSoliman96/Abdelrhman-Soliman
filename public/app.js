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

const LANGUAGE_NAMES = {
  en: "English",
  ar: "Arabic",
  de: "German",
  es: "Spanish",
};

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

  if (sourceLang.value === targetLang.value) {
    setStatus("Choose two different languages.", "error");
    return;
  }

  const data = new FormData();
  data.append("file", file);
  data.append("sourceLang", sourceLang.value);
  data.append("targetLang", targetLang.value);

  setLoading(true);
  setStatus("Translating with Google Translate…");
  resultEl.hidden = true;

  try {
    const response = await fetch("/api/translate", {
      method: "POST",
      body: data,
    });

    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.error || "Translation failed.");
    }

    resultMeta.textContent = `${payload.originalName} · ${LANGUAGE_NAMES[payload.sourceLang]} → ${LANGUAGE_NAMES[payload.targetLang]} · ${payload.filename}`;
    previewEl.textContent = payload.preview || "(No preview available)";
    previewEl.dir = payload.targetLang === "ar" ? "rtl" : "ltr";
    downloadLink.href = payload.downloadUrl;
    downloadLink.download = payload.filename;
    resultEl.hidden = false;
    setStatus("Translation complete. Download your file below.", "success");
  } catch (error) {
    setStatus(error.message || "Something went wrong.", "error");
  } finally {
    setLoading(false);
  }
});
