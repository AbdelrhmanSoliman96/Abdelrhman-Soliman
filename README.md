# LinguaFile

Translate files between **English**, **Arabic**, **German**, and **Spanish** using Google Translate.

Upload a file → choose languages → download the translated file.

## Features

- Simple drag-and-drop upload
- Bidirectional translation across EN / AR / DE / ES
- Supported formats: TXT, MD, CSV, JSON, SRT, HTML, XML, LOG, DOCX
- Arabic preview uses right-to-left layout
- Files up to 5 MB

## Quick start

```bash
npm install
npm start
```

Open [http://localhost:3000](http://localhost:3000).

For local development with auto-reload:

```bash
npm run dev
```

## How it works

1. Upload a supported file
2. Pick source and target languages
3. The server extracts text and translates it with Google Translate
4. Download the translated file

## Notes

- Translation uses the Google Translate service via `google-translate-api-x`
- DOCX files are converted to plain paragraphs in the output DOCX
- Complex formatting, images, and tables are not preserved
