const express = require("express");
const multer = require("multer");
const cors = require("cors");
const path = require("path");
const fs = require("fs");
const os = require("os");
const { translate } = require("google-translate-api-x");
const mammoth = require("mammoth");
const { Document, Packer, Paragraph, TextRun } = require("docx");

const app = express();
const PORT = process.env.PORT || 3000;

const SUPPORTED_LANGUAGES = {
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

const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 5 * 1024 * 1024 },
  fileFilter(_req, file, cb) {
    const ext = path.extname(file.originalname).toLowerCase();
    if (TEXT_EXTENSIONS.has(ext) || ext === ".docx") {
      cb(null, true);
      return;
    }
    cb(new Error("Unsupported file type. Use TXT, MD, CSV, JSON, SRT, HTML, XML, LOG, or DOCX."));
  },
});

app.use(cors());
app.use(express.json({ limit: "1mb" }));
app.use(express.static(path.join(__dirname, "public")));

function chunkText(text, maxChars = 4000) {
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

async function translateText(text, sourceLang, targetLang) {
  if (!text || !text.trim()) return text;

  const chunks = chunkText(text);
  const translated = [];

  for (const chunk of chunks) {
    if (!chunk.trim()) {
      translated.push(chunk);
      continue;
    }

    const result = await translate(chunk, {
      from: sourceLang,
      to: targetLang,
      forceBatch: false,
    });

    translated.push(typeof result.text === "string" ? result.text : String(result.text));
  }

  return translated.join("");
}

async function extractText(file) {
  const ext = path.extname(file.originalname).toLowerCase();

  if (ext === ".docx") {
    const result = await mammoth.extractRawText({ buffer: file.buffer });
    return { text: result.value, kind: "docx" };
  }

  return {
    text: file.buffer.toString("utf8"),
    kind: "text",
  };
}

async function buildOutputBuffer(translatedText, originalName, kind) {
  const ext = path.extname(originalName).toLowerCase();
  const base = path.basename(originalName, ext);

  if (kind === "docx" || ext === ".docx") {
    const paragraphs = translatedText.split(/\r?\n/).map(
      (line) =>
        new Paragraph({
          children: [new TextRun({ text: line || " ", size: 24 })],
        })
    );

    const doc = new Document({
      sections: [{ children: paragraphs.length ? paragraphs : [new Paragraph("")] }],
    });

    const buffer = await Packer.toBuffer(doc);
    return {
      buffer,
      filename: `${base}-translated.docx`,
      mime: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    };
  }

  return {
    buffer: Buffer.from(translatedText, "utf8"),
    filename: `${base}-translated${ext || ".txt"}`,
    mime: "text/plain; charset=utf-8",
  };
}

app.get("/api/languages", (_req, res) => {
  res.json(SUPPORTED_LANGUAGES);
});

app.post("/api/translate", upload.single("file"), async (req, res) => {
  try {
    const { sourceLang, targetLang } = req.body;

    if (!req.file) {
      return res.status(400).json({ error: "Please upload a file." });
    }

    if (!SUPPORTED_LANGUAGES[sourceLang] || !SUPPORTED_LANGUAGES[targetLang]) {
      return res.status(400).json({
        error: "Only English, Arabic, German, and Spanish are supported.",
      });
    }

    if (sourceLang === targetLang) {
      return res.status(400).json({
        error: "Source and target languages must be different.",
      });
    }

    const { text, kind } = await extractText(req.file);

    if (!text.trim()) {
      return res.status(400).json({ error: "The file appears to be empty." });
    }

    const translatedText = await translateText(text, sourceLang, targetLang);
    const output = await buildOutputBuffer(translatedText, req.file.originalname, kind);

    const tempPath = path.join(os.tmpdir(), `linguafile-${Date.now()}-${output.filename}`);
    fs.writeFileSync(tempPath, output.buffer);

    res.json({
      success: true,
      downloadUrl: `/api/download?path=${encodeURIComponent(tempPath)}&name=${encodeURIComponent(output.filename)}`,
      filename: output.filename,
      preview: translatedText.slice(0, 1200),
      sourceLang,
      targetLang,
      originalName: req.file.originalname,
    });
  } catch (error) {
    console.error("Translation error:", error);
    res.status(500).json({
      error: error.message || "Translation failed. Please try again.",
    });
  }
});

app.get("/api/download", (req, res) => {
  const filePath = req.query.path;
  const fileName = req.query.name || "translated.txt";

  if (!filePath || typeof filePath !== "string") {
    return res.status(400).json({ error: "Missing file path." });
  }

  const resolved = path.resolve(filePath);
  if (!resolved.startsWith(os.tmpdir())) {
    return res.status(403).json({ error: "Invalid download path." });
  }

  if (!fs.existsSync(resolved)) {
    return res.status(404).json({ error: "File expired or not found. Translate again." });
  }

  res.download(resolved, fileName, (err) => {
    if (!err) {
      fs.unlink(resolved, () => {});
    }
  });
});

app.use((err, _req, res, _next) => {
  console.error(err);
  res.status(400).json({ error: err.message || "Request failed." });
});

app.listen(PORT, () => {
  console.log(`LinguaFile running at http://localhost:${PORT}`);
});
