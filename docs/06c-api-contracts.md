# ReportSaathi – API Contracts

## 1. Purpose

This document defines the communication contract between the ReportSaathi frontend and backend.

It specifies API endpoints, HTTP methods, request formats, response formats, validation requirements and error handling.

These contracts describe the proposed MVP implementation. Actual endpoint availability and schemas must be verified during backend integration.

## 2. API Overview

- **Backend framework:** FastAPI
- **Data validation:** Pydantic
- **API format:** REST
- **Request format:** JSON and multipart/form-data
- **Response format:** JSON
- **Base URL (local):** `http://127.0.0.1:8000`
- **API prefix:** `/api`

Interactive API documentation will be available at `/docs` when the FastAPI application is running.

### 2.1 MVP Configuration

| Configuration | Proposed MVP decision |
|---|---|
| Supported languages | English, Hindi and Kannada |
| Explanation levels | Simple, Standard and Detailed |
| Maximum upload size | 10 MB |
| Supported formats | PDF, JPG, JPEG and PNG |
| Doctor questions | 3–6 questions |
| Patient authentication | Not mandatory |
| Report history | Excluded |
| Save/share | Included |
| PDF download | Included |
| WhatsApp sharing | Pre-filled sharing link |
| Feedback | Optional |
| Database | Supabase with minimal data storage, subject to confirmation |

## 3. Common Response Structure

Successful responses should use a consistent structure where practical.

Example:

```json
{
  "success": true,
  "message": "Request processed successfully",
  "data": {}
}
```

Error responses:

```json
{
  "success": false,
  "message": "Invalid request",
  "error_code": "VALIDATION_ERROR"
}
```

HTTP status codes must accurately represent the result.

The `/api/health` endpoint intentionally uses a separate response structure.

## 4. API Endpoints

### 4.1 Health Check

**Endpoint:** `/api/health`

**Method:** GET

**Purpose:** Check whether the backend service is running.

Request: No body required.

Successful response – 200:

```json
{
  "status": "healthy",
  "service": "ReportSaathi API"
}
```

### 4.2 Upload Medical Document

**Endpoint:** `/api/upload`

**Method:** POST

**Content-Type:** `multipart/form-data`

**Purpose:** Accept a patient's medical document for temporary processing.

Request fields:

| Field | Type | Required |
|---|---|---|
| file | File | Yes |

Supported file formats:

- PDF
- JPG
- JPEG
- PNG

Maximum upload size: **10 MB**.

The backend must reject unsupported formats, empty files and files exceeding 10 MB.

Proposed successful response – 200:

```json
{
  "success": true,
  "message": "Document uploaded successfully",
  "data": {
    "document_id": "temporary-document-id",
    "filename": "report.pdf",
    "status": "uploaded"
  }
}
```

The document ID is a temporary processing reference, not a permanent patient record.

### 4.3 Extract Text Using OCR

**Endpoint:** `/api/extract`

**Method:** POST

**Purpose:** Extract text from an uploaded medical document using OCR.

Request:

```json
{
  "document_id": "temporary-document-id"
}
```

Proposed successful response – 200:

```json
{
  "success": true,
  "data": {
    "extracted_text": "Hemoglobin: 13.5 g/dL",
    "extraction_status": "completed",
    "requires_verification": false
  }
}
```

If the document is unclear, the response must identify that manual verification is required.

### 4.4 Correct OCR Text

**Endpoint:** `/api/extract/{document_id}/corrections`

**Method:** POST

**Purpose:** Submit user-corrected OCR text for a temporarily uploaded document.

Request:

```json
{
  "corrected_text": "Hemoglobin: 13.5 g/dL"
}
```

Proposed successful response – 200:

```json
{
  "success": true,
  "message": "Extracted text corrected successfully",
  "data": {
    "document_id": "temporary-document-id",
    "status": "corrected"
  }
}
```

Validation requirements:

- Document ID must identify an existing temporary document.
- Corrected text must not be empty.
- Corrected text must be associated with the corresponding document.
- Corrected text must be treated as untrusted input.
- Subsequent explanation processing must use the verified corrected text.

**Status:** Proposed – Pending team approval and backend implementation.

### 4.5 Explain Medical Report

**Endpoint:** `/api/explain`

**Method:** POST

**Purpose:** Generate an explanation of extracted medical information.

Request:

```json
{
  "document_id": "temporary-document-id",
  "language": "English",
  "reading_level": "Simple"
}
```

Supported language values:

- English
- Hindi
- Kannada

Supported reading levels:

- Simple
- Standard
- Detailed

The backend must retrieve the verified OCR text associated with the supplied temporary document ID. It must not blindly trust report text supplied by the frontend.

Proposed successful response – 200:

```json
{
  "success": true,
  "data": {
    "explanation": "This section explains the information in simple language.",
    "language": "English",
    "reading_level": "Simple",
    "disclaimer": "This explanation is educational and is not a medical diagnosis.",
    "requires_medical_review": false
  }
}
```

The backend must not generate diagnoses, prescribe treatment or invent laboratory reference ranges.

### 4.6 Translate Explanation

**Endpoint:** `/api/translate`

**Method:** POST

**Purpose:** Translate an existing explanation into a supported language.

Request:

```json
{
  "text": "Your report contains the following information.",
  "target_language": "Kannada"
}
```

Supported target languages:

- English
- Hindi
- Kannada

Proposed successful response – 200:

```json
{
  "success": true,
  "data": {
    "translated_text": "Translated explanation",
    "language": "Kannada"
  }
}
```

The translation must preserve medical values, units and prescription instructions.

### 4.7 Generate Questions for Doctor

**Endpoint:** `/api/questions`

**Method:** POST

**Purpose:** Generate useful questions that a patient can discuss with a healthcare professional.

Request:

```json
{
  "explanation": "The report contains some values that require clarification."
}
```

Proposed successful response – 200:

```json
{
  "success": true,
  "data": {
    "questions": [
      "Could you explain this result?",
      "Does this result require any follow-up?",
      "Should I discuss this result during my next appointment?"
    ]
  }
}
```

The API should return between 3 and 6 relevant questions.

Questions must not recommend self-treatment or medication changes.

### 4.8 Submit Feedback (Optional)

**Endpoint:** `/api/feedback`

**Method:** POST

**Purpose:** Collect optional feedback about the application's usefulness.

Request:

```json
{
  "rating": 4,
  "feedback": "The explanation was easy to understand."
}
```

Proposed successful response – 200:

```json
{
  "success": true,
  "message": "Feedback submitted successfully"
}
```

Feedback collection must not include medical report contents or unnecessary personal health information.

**Status:** Optional – Subject to development time and team confirmation.

### 4.9 Save and Share Explanation

Save/share functionality is included in the proposed MVP.

The frontend may support saving or sharing the generated explanation without introducing permanent report history.

The implementation must ensure that sensitive medical information is not exposed through public links or unauthorized access.

If backend storage or sharing endpoints are required, their request and response schemas must be documented before implementation.

### 4.10 PDF Download

PDF download is included in the proposed MVP.

The application should generate a downloadable PDF containing the explanation and appropriate medical disclaimer.

The PDF must preserve medical values and units and must not introduce unsupported medical claims.

If PDF generation requires a backend endpoint, its contract must be finalized during integration.

### 4.11 WhatsApp Sharing

WhatsApp sharing is included through a pre-filled sharing link.

The user must explicitly initiate sharing.

The application must not automatically send medical information or expose report contents without user consent.

The frontend should use a safe, user-controlled sharing workflow.

### 4.12 Admin Operational Monitoring

A basic admin dashboard is proposed for operational monitoring and error tracking.

It may display service health, processing status, system errors and aggregate usage information.

It must not expose patient report contents, extracted medical text, API secrets or unnecessary personal health information.

Any admin API endpoints and access-control requirements must be finalized before implementation.

### 4.13 Report History

Report history is excluded from the MVP.

A `/api/history` endpoint must not be considered available unless the team approves persistent history, authentication, authorization and associated privacy requirements.

## 5. HTTP Status Codes

| Status | Meaning |
|---|---|
| 200 | Request successful |
| 201 | Resource created |
| 400 | Invalid request |
| 401 | Authentication required |
| 403 | Access forbidden |
| 404 | Resource not found |
| 413 | Uploaded file too large |
| 415 | Unsupported file format |
| 422 | Request validation failed or input cannot be processed |
| 429 | Too many requests |
| 500 | Internal server error |
| 503 | External service unavailable |

An OCR or AI service outage should return an appropriate service-unavailable response, while invalid or unusable document input should return an appropriate validation response.

## 6. Validation Requirements

- Reject unsupported file formats.
- Enforce the 10 MB upload limit.
- Reject empty uploaded files.
- Validate required request fields.
- Validate document IDs before processing.
- Validate supported language selections.
- Validate reading-level selections.
- Ensure doctor question count is between 3 and 6.
- Validate feedback ratings when feedback is enabled.
- Reject empty or malformed requests.
- Reject empty corrected OCR text.
- Associate corrected OCR text with the corresponding temporary document.
- Never trust filenames or extracted document text as safe input.

## 7. Medical Safety Requirements

- Never provide a medical diagnosis.
- Never recommend changing prescribed medication.
- Never recommend starting or stopping medication.
- Never invent laboratory reference ranges.
- Preserve original laboratory values and units.
- Flag unclear OCR results for manual verification.
- Apply predefined emergency red-flag checks before waiting for an AI explanation.
- Keep emergency warnings visible even if the AI service fails.
- Provide safe fallback messages when AI output fails validation.
- Display the medical disclaimer with explanations.
- Red-flag rules must receive qualified medical professional review and approval before production use.

## 8. Privacy and Security Requirements

- Use HTTPS in deployed environments.
- Keep API keys and secrets in backend environment variables.
- Validate uploaded files before processing.
- Avoid exposing medical information in application logs.
- Do not send report contents to analytics services.
- Do not expose one patient's temporary document to another user.
- Treat corrected OCR text as sensitive user-provided information.
- Delete temporary uploaded documents and extracted data according to the approved retention policy.
- Use appropriate access controls and Supabase Row Level Security if persistent user-related data is stored.
- Do not introduce permanent report history in the MVP without explicit team approval.
- The exact retention duration and backup deletion policy require team confirmation.

## 9. Frontend and Backend Integration

The proposed frontend workflow is:

1. Upload a document using `/api/upload`.
2. Receive the temporary document ID.
3. Request OCR extraction using `/api/extract`.
4. Display extracted text for verification when required.
5. Submit corrected OCR text using `/api/extract/{document_id}/corrections` when the user makes corrections.
6. Request an explanation using `/api/explain`, passing the document ID, language and reading level.
7. Request translation using `/api/translate` when needed.
8. Request doctor questions using `/api/questions`.
9. Allow users to save, download or share their explanation through approved workflows.
10. Display errors and safe fallback messages appropriately.

The backend is responsible for validation, OCR, AI processing, safety checks and structured responses.

The frontend must not receive backend API keys or database credentials.

## 10. Error Handling

The frontend must:

- Display understandable error messages.
- Show loading indicators during processing.
- Allow users to retry failed requests where safe.
- Avoid displaying raw server errors or internal stack traces.
- Preserve user-entered information when a request fails, where practical.

The backend must return consistent error responses and avoid exposing sensitive information.

The `/api/health` endpoint is an intentional exception to the common response structure.

## 11. Testing Requirements

Every implemented endpoint and feature must be tested for:

- Successful requests.
- Missing required fields.
- Invalid input.
- Unsupported file formats.
- Empty files.
- Oversized uploads.
- OCR failures.
- Unclear OCR results.
- Successful OCR text correction.
- Empty corrected OCR text.
- Invalid or expired document IDs.
- Verification that subsequent explanation processing uses corrected text.
- Supported and unsupported languages.
- Supported and unsupported reading levels.
- Doctor question count between 3 and 6.
- AI service failures.
- Medical safety violations.
- Red-flag warnings during AI service failure.
- Privacy and access-control failures where applicable.
- Save/share and PDF download behavior.
- WhatsApp sharing consent and link behavior.
- Feedback behavior when enabled.
- Admin monitoring access restrictions.

## 12. Implementation Status

This document defines the proposed MVP API contract.

The following items remain subject to confirmation or implementation:

- Actual endpoint availability and backend integration.
- OCR correction endpoint approval and implementation.
- Final request and response schemas.
- Supabase setup and access-control configuration.
- Temporary data retention duration and backup deletion policy.
- Save/share and PDF implementation details.
- WhatsApp sharing workflow.
- Optional feedback implementation.
- Admin dashboard scope and access controls.
- Medical professional approval of red-flag rules.
- Error codes and status codes verified against the actual backend.

Optional functionality must not be presented as implemented until it has been developed and tested.

---

**Project:** ReportSaathi  
**Document:** API Contracts  
**Owner:** Systems & DevOps Lead  
**Status:** Proposed – Pending Team Approval and Backend Integration