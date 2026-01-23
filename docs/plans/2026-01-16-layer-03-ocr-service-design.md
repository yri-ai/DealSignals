# Layer 03 OCR Service Design (OCRmyPDF + Tesseract)

**Goal:** Provide a deterministic, auditable OCR parsing service for Layer 03 document parsing comparison.

**Why this matters:** Layer 03 evaluates parsing quality. The OCR service must preserve page boundaries, return reproducible outputs, and provide rich metadata so errors can be attributed to parsing rather than model reasoning.

## Research Requirements
- **Deterministic output:** Same input + config → identical output and hashes.
- **Page-aware text:** Per-page text output for citation (page + quote).
- **Traceability:** Record input/output hashes, engine versions, flags, runtime, page count.
- **Comparability:** Each response includes `run_id`, `document_id`, `parser_profile`.
- **Failure visibility:** Structured error taxonomy with diagnostics.
- **Local-only:** No external services; all artifacts remain on disk.

## API Overview (Async + Webhook)
The service is async. Clients submit a job and receive callbacks with a status + result URL.

### Endpoints
- `GET /v1/health`
- `POST /v1/ocr`
- `GET /v1/ocr/{job_id}`
- `GET /v1/ocr/{job_id}/result`

### `GET /v1/health`
**Response**:
```json
{
  "status": "ok",
  "ocrmypdf_version": "16.x",
  "tesseract_version": "5.x",
  "languages": ["eng"],
  "uptime_s": 12345
}
```

### `POST /v1/ocr`
Accepts a PDF file or URL.

**Required fields**
- `run_id`
- `document_id`
- `parser_profile` (e.g., `ocrmypdf_tesseract_v1`)
- `callback_url`

**Optional fields**
- `source_url` (if not uploading a file)
- `language` (default `eng`)
- `deskew` (default `true`)
- `rotate_pages` (default `true`)
- `force_ocr` (default `false`)
- `skip_text` (default `false`)
- `callback_secret` (optional shared secret for webhook verification)

**Response**
```json
{
  "job_id": "...",
  "status": "queued",
  "submitted_at": "2026-01-16T20:15:10Z"
}
```

### `GET /v1/ocr/{job_id}`
**Response**
```json
{
  "job_id": "...",
  "status": "queued|running|succeeded|failed",
  "progress": 0,
  "started_at": "...",
  "finished_at": "..."
}
```

### `GET /v1/ocr/{job_id}/result`
Returns artifact paths plus metadata.

**Response**
```json
{
  "job_id": "...",
  "run_id": "...",
  "document_id": "...",
  "parser_profile": "ocrmypdf_tesseract_v1",
  "status": "succeeded",
  "artifacts": {
    "searchable_pdf_path": "/data/ocr/<job_id>/output_searchable.pdf",
    "text_path": "/data/ocr/<job_id>/output_text.txt",
    "pages_path": "/data/ocr/<job_id>/output_pages.jsonl",
    "meta_path": "/data/ocr/<job_id>/output_meta.json"
  },
  "metadata": {
    "page_count": 214,
    "runtime_ms": 53210,
    "input_hash": "...",
    "output_hash": "...",
    "tesseract_version": "5.x",
    "ocrmypdf_version": "16.x",
    "language": "eng",
    "flags": {
      "deskew": true,
      "rotate_pages": true,
      "force_ocr": false,
      "skip_text": false
    }
  }
}
```

## Webhook Contract
The OCR service POSTs to `callback_url` on completion (success/failure).

**Payload**
```json
{
  "job_id": "...",
  "run_id": "...",
  "document_id": "...",
  "parser_profile": "ocrmypdf_tesseract_v1",
  "status": "succeeded|failed",
  "result_url": "http://localhost:8000/v1/ocr/<job_id>/result",
  "error": {"code": "...", "message": "..."},
  "timing": {"queued_ms": 1200, "runtime_ms": 53210}
}
```

**Delivery rules**
- 3 retries with exponential backoff on non-2xx
- Idempotent: client should dedupe by `job_id`
- Optional: include `X-OCR-Signature` HMAC header if `callback_secret` is provided

## Artifacts & Formats
- `output_searchable.pdf` — searchable PDF/A output from OCRmyPDF
- `output_text.txt` — full OCR text (sidecar)
- `output_pages.jsonl` — one JSON line per page:
  ```json
  {"page": 1, "text": "...", "char_count": 1234}
  ```
- `output_meta.json` — metadata snapshot with hashes and flags

## System Requirements
- **Python** 3.10+
- **OCRmyPDF** 16.x
- **Tesseract** 5.x + `eng` trained data
- **Ghostscript**
- Optional: `unpaper`, `jbig2enc`

**Threading:** OCRmyPDF is not thread-safe in-process. Run jobs in subprocesses.

## Deterministic Defaults
- `language=eng`
- `deskew=true`
- `rotate_pages=true`
- `force_ocr=false`
- `skip_text=false`
- `output_type=pdfa`
- `sidecar_text=output_text.txt`
- Fixed output layout: `/data/ocr/<job_id>/...`

## Error Taxonomy
- `E_INPUT_NOT_FOUND` — source file missing/unreadable
- `E_INVALID_PDF` — PDF parsing failure
- `E_OCR_TIMEOUT` — job exceeded time limit
- `E_OCR_ENGINE` — OCRmyPDF/Tesseract failure (non-zero exit)
- `E_OUTPUT_WRITE` — output write failure
- `E_INTERNAL` — unhandled exception

**Failure response** should include: `error.code`, `error.message`, `error.stage`, `diagnostics` (exit code, stderr tail).

## Operational Defaults
- Max file size: 500MB (configurable)
- Max pages: configurable
- Concurrency: 1–2 workers initially
- Timeouts: 10 minutes per 100 pages (configurable)
- Retention: 30 days (configurable)

## Notes for Layer 03
- Include `run_id` and `parser_profile` in every Layer 03 run to compare OCR outputs.
- Store artifact hashes for auditability in `output_meta.json`.
- Keep OCR settings fixed for the entire Layer 03 comparison set.
