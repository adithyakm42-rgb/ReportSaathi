# ReportSaathi – Test Plan

**Document:** Stage 6 – Test Plan  
**Owner:** Person 3 – Quality & Engineering Lead  
**Prepared with:** Person 2 – Systems & DevOps Lead
**Status:** Proposed – Pending Final Team Confirmation and Backend Integration

## 1. Objective

Define the testing strategy for ReportSaathi to verify functionality, API contracts, input validation, medical safety, privacy and reliability.

Testing must ensure that the application explains medical information responsibly without diagnosing patients, recommending medication changes or inventing laboratory reference ranges.

**Important:** The requirements and decisions in this document reflect the team's current MVP recommendations. They do not confirm that the backend or frontend currently implements these features.

## 2. Testing Scope

### 2.1 Proposed MVP features

- Language selection: English, Hindi and Kannada.
- Reading levels: Simple, Standard and Detailed.
- Medical document upload: PDF, JPG, JPEG and PNG.
- Maximum upload size: 10 MB.
- OCR text extraction.
- Manual verification and correction of unclear extracted text.
- Plain-language medical report explanations.
- Comparison with reference ranges printed on the report.
- Deterministic red-flag checks before AI explanation generation.
- Medical explanation disclaimer.
- Translation into supported languages.
- Generation of 3–6 questions for a doctor.
- Save and share explanations.
- PDF summary download.
- WhatsApp sharing through a pre-filled sharing link.
- Basic optional feedback.
- Basic administrator dashboard for operational monitoring and error tracking.
- Safe handling of OCR and AI failures.

### 2.2 Excluded or conditional features

| Feature | Testing status |
|---|---|
| Patient registration/login | Not mandatory for MVP |
| Patient report history | Excluded from MVP |
| Save/share | Included in MVP |
| PDF download | Included in MVP |
| WhatsApp sharing | Included through a pre-filled sharing link |
| Feedback | Optional, subject to development time |
| Supabase database | Proposed for minimal data storage |
| Advanced patient history and trends | Post-MVP |
| Nearby labs/clinics map | Post-MVP |
| Medicine reminders | Post-MVP |
| Voice readout | Post-MVP |
| WhatsApp chatbot | Post-MVP |

Save/share functionality must not expose medical report contents through public or unsecured links.

## 3. Proposed API Contract Coverage

| Endpoint | Method | Testing priority |
|---|---|---|
| `/api/health` | GET | MVP |
| `/api/upload` | POST | MVP |
| `/api/extract` | POST | MVP |
| `/api/extract/{document_id}/corrections` | POST | MVP |
| `/api/explain` | POST | MVP |
| `/api/translate` | POST | MVP |
| `/api/questions` | POST | MVP |
| `/api/feedback` | POST | Optional |
| `/api/history` | GET | Excluded from MVP |

The API contracts are proposed and must be checked against the actual FastAPI implementation.

Save/share, PDF generation, WhatsApp sharing and administrator monitoring must also be tested according to their final frontend and backend implementation. Their API contracts must be documented if separate backend endpoints are introduced.

## 4. Proposed Validation and Error Handling

### 4.1 Upload validation

| Scenario | Expected HTTP status |
|---|---:|
| Valid PDF, JPG, JPEG or PNG within 10 MB | 200 |
| Empty upload | 400 |
| Unsupported file format | 415 |
| File larger than 10 MB | 413 |

The 10 MB limit follows the current team recommendation and must be enforced consistently by the frontend and backend.

### 4.2 Other API validation

| Scenario | Expected HTTP status |
|---|---:|
| Invalid or nonexistent document ID | 404 |
| Missing or malformed required fields | 422 |
| Unsupported language | 422 |
| Empty corrected OCR text | 422 |
| Invalid feedback rating | 422 |
| Invalid document input that cannot be processed | 422 |
| OCR or AI service unavailable | 503 |

Unexpected internal server errors should return HTTP 500 without exposing internal implementation details.

The exact error codes and messages must be verified against the final implementation.

### 4.3 Proposed Error Response Structure

Error responses should follow the common format defined in `docs/06c-api-contracts.md`.

Example:

```json
{
  "success": false,
  "message": "The requested document was not found.",
  "error_code": "INVALID_DOCUMENT_ID"
}
```

The `/api/health` endpoint is an intentional exception and follows its separately documented response format.

The frontend must display understandable error messages rather than raw server errors, stack traces or sensitive information.

The final response schemas and error codes must be verified against the actual backend implementation.

## 5. Acceptance Test Cases

### TC-01: Language selection

**Given:** The user opens the application.

**When:** The user selects English, Hindi or Kannada.

**Then:** The selected language should be accepted and used for the requested explanation.

### TC-02: Unsupported language

**Given:** The API receives an unsupported language.

**When:** The request is submitted.

**Then:** The API should return HTTP 422 and clearly identify the supported languages: English, Hindi and Kannada.

### TC-03: Reading-level selection

**Given:** The user requests a medical explanation.

**When:** The user selects Simple, Standard or Detailed.

**Then:** The application should present the explanation at the selected reading level without changing the medical meaning.

The final API request field for reading level must be confirmed and documented.

### TC-04: Valid document upload

**Given:** The user selects a supported PDF, JPG, JPEG or PNG file within the 10 MB limit.

**When:** The user uploads the document.

**Then:** The API should return HTTP 200 with a temporary document ID, filename and upload status.

### TC-05: Empty document upload

**Given:** The user submits an empty file.

**When:** The upload request is processed.

**Then:** The API should return HTTP 400 with a safe validation message.

### TC-06: Unsupported document format

**Given:** The user selects an unsupported file format.

**When:** The file is uploaded.

**Then:** The API should return HTTP 415.

### TC-07: Oversized document upload

**Given:** The user selects a document larger than 10 MB.

**When:** The file is uploaded.

**Then:** The API should return HTTP 413 and reject the file.

### TC-08: Successful OCR extraction

**Given:** A valid document has been uploaded.

**When:** The user requests text extraction using its document ID.

**Then:** The API should return extracted text and an extraction status.

### TC-09: Unclear OCR result

**Given:** An uploaded report contains blurry or unclear text.

**When:** OCR processing is performed.

**Then:** The application should request manual verification or correction and must not confidently explain uncertain values.

### TC-10: Manual OCR correction

**Given:** OCR extraction returns incorrect or uncertain text.

**When:** The user corrects the extracted information and submits it through `/api/extract/{document_id}/corrections`.

**Then:**
- The backend should validate the document ID.
- Corrected text must not be empty.
- The correction should be associated with the correct temporary document.
- The API should return a successful correction response when the operation succeeds.
- Subsequent explanation processing must use the verified corrected text.

### TC-11: Invalid document ID

**Given:** An invalid or nonexistent document ID is submitted.

**When:** Extraction, correction or explanation is requested.

**Then:** The API should return HTTP 404 with a safe error response.

### TC-12: Reference range comparison

**Given:** A report contains a medical value and its printed reference range.

**When:** The application processes the report.

**Then:** The displayed status should be based on the printed reference range and original value.

### TC-13: Missing reference range

**Given:** A report contains a medical value without a printed reference range.

**When:** The application explains the report.

**Then:** It must not invent a reference range or confidently classify the value using an assumed range.

### TC-14: Deterministic red-flag checks

**Given:** A report contains information matching a predefined red-flag rule.

**When:** The backend processes the report.

**Then:** Deterministic safety checks must execute before AI explanation generation, and the relevant warning must be preserved.

Red-flag rules must receive qualified medical professional review and approval before production release.

### TC-15: AI service failure

**Given:** The AI service is unavailable or times out.

**When:** An explanation is requested.

**Then:** The API should return HTTP 503 with a safe fallback message and must not invent a medical explanation.

### TC-16: Red-flag warning during AI failure

**Given:** A report triggers a predefined red-flag rule and the AI service fails.

**When:** The application displays the result.

**Then:** The red-flag warning must remain visible even when AI explanation generation fails.

### TC-17: Unsafe AI output

**Given:** The AI produces a diagnosis, medication change recommendation or other prohibited medical advice.

**When:** The backend safety validation checks the output.

**Then:** The unsafe output must be rejected and replaced with a safe fallback response.

### TC-18: Translation accuracy

**Given:** An explanation contains medical values, units and prescription instructions.

**When:** The explanation is translated into Hindi or Kannada.

**Then:** The translation must preserve the original values, units and instructions.

### TC-19: Doctor-question generation

**Given:** A valid medical explanation is available.

**When:** The user requests questions for a doctor.

**Then:** The application should generate 3–6 relevant questions without recommending self-treatment or medication changes.

### TC-20: Save and share explanation

**Given:** An explanation has been generated.

**When:** The user selects the save or share option.

**Then:** The application should perform the approved save/share action without exposing medical information through unauthorized access.

### TC-21: PDF summary download

**Given:** An explanation is available.

**When:** The user selects PDF download.

**Then:** The application should generate a readable summary containing the appropriate explanation and medical disclaimer.

The PDF must preserve medical values and units accurately.

### TC-22: WhatsApp sharing

**Given:** The user selects WhatsApp sharing.

**When:** The application opens the pre-filled sharing link.

**Then:** The sharing action should work as intended, and no report contents or personal health information should be included without explicit user approval.

### TC-23: Feedback validation (optional)

**Given:** The feedback feature is included in the MVP.

**When:** A user submits a rating between 1 and 5.

**Then:** The API should accept the valid rating.

Invalid ratings should be rejected using the agreed validation response.

This test is conditional on feedback being included in the release.

### TC-24: Administrator dashboard monitoring

**Given:** The administrator accesses the operational dashboard.

**When:** Application health, errors and service status are monitored.

**Then:** The dashboard should display appropriate operational information without exposing medical report contents or unnecessary personal health information.

### TC-25: Sensitive information in logs

**Given:** A document is uploaded and processed.

**When:** Backend operations and error handling are recorded.

**Then:** Medical report contents and personal health information must not appear in application logs or analytics.

### TC-26: Temporary document deletion

**Given:** A document has completed processing or reached the agreed session-retention limit.

**When:** The retention policy is executed.

**Then:** Temporary uploaded documents and extracted text should be deleted according to the finalized policy.

The exact retention period and backup deletion requirements are pending team confirmation.

## 6. Medical Safety Test Requirements

Medical safety is a critical part of the testing process.

The following conditions must be verified:

1. Deterministic red-flag checks execute before AI explanation generation.
2. Red-flag warnings remain available even if the AI service fails.
3. The application never provides a medical diagnosis.
4. The application never recommends starting, stopping or changing prescribed medication.
5. The application never invents laboratory reference ranges.
6. Original laboratory values and units are preserved.
7. Unclear OCR results require manual verification.
8. Unsafe AI output is rejected.
9. Safe fallback messages are displayed when AI processing fails.
10. Medical disclaimers accompany explanations.
11. Red-flag rules receive qualified medical professional approval before production release.

**Critical rule:** Safety tests must never be weakened or removed just to make the test suite pass.

## 7. Privacy and Security Testing

Verify the following requirements:

- Uploaded files are validated before processing.
- API keys and secrets are not exposed in frontend code.
- HTTPS is used in deployed environments.
- Medical report contents are excluded from application logs and analytics.
- Temporary files and extracted text follow the approved deletion policy.
- Authentication is not mandatory for the proposed MVP.
- If authentication or persistent patient records are introduced, unauthorized access and cross-user access must be tested.
- Supabase access controls and Row Level Security must be verified if patient-related records are stored.
- Invalid document IDs must not expose another user's medical information.
- Filenames and extracted text must be treated as untrusted input.
- Save/share functionality must not expose private medical information through unsecured links.
- Backup deletion must follow the approved retention policy.

## 8. Test Fixtures

Prepare 10 anonymized sample medical-report fixtures under `tests/fixtures/`.

| Fixture | Purpose |
|---|---|
| `01-normal-report` | Normal-looking values with printed ranges |
| `02-high-values` | Values above printed ranges |
| `03-low-values` | Values below printed ranges |
| `04-missing-ranges` | Values without reference ranges |
| `05-blurry-report` | OCR uncertainty |
| `06-multiple-values` | Multiple medical values |
| `07-scanned-pdf` | PDF OCR processing |
| `08-ocr-challenges` | Difficult text extraction |
| `09-multilingual-report` | Language and translation testing |
| `10-red-flag-case` | Deterministic safety-rule testing |

All fixtures must be anonymized and must not contain identifiable patient information.

Red-flag test fixtures and expected outcomes must be reviewed by a qualified medical professional before production use.

## 9. Testing Types and Tools

| Testing type | Purpose | Proposed tools |
|---|---|---|
| Unit testing | Test individual functions and validation rules | Pytest, Vitest |
| Integration testing | Test communication between frontend and backend | Pytest, MSW |
| API contract testing | Verify request and response structures | Bruno / Hoppscotch, automated API tests |
| End-to-end testing | Test complete user journeys | Playwright |
| Security testing | Verify privacy and input validation | Pytest and manual checks |
| Medical safety testing | Verify deterministic rules and safe AI output handling | Pytest |
| Manual testing | Verify usability and error messages | Browser testing |

## 10. Test Execution and Completion Criteria

A feature or task should be considered tested only when:

- Its acceptance criteria have been verified.
- Relevant unit tests pass.
- Relevant integration tests pass.
- API contract tests pass.
- Medical safety tests pass where applicable.
- Lint and type checks pass.
- No known critical privacy or security issue remains.
- Error handling and safe fallback behavior have been verified.
- Save/share and PDF features have been tested where implemented.
- Required medical safety approvals have been obtained before production release.

Tests should be written before implementation wherever practical.

## 11. Implementation Status

| Area | Status |
|---|---|
| Proposed API endpoints | Documented; backend verification pending |
| Upload formats | PDF, JPG, JPEG and PNG proposed |
| Maximum upload size | 10 MB – current team recommendation |
| Supported languages | English, Hindi and Kannada – current team recommendation |
| Reading levels | Simple, Standard and Detailed – current team recommendation |
| Doctor questions | 3–6 – current team recommendation |
| OCR correction endpoint | Documented as proposed; implementation pending |
| Deterministic red-flag execution | Required; implementation and medical review pending |
| Supabase database | Proposed; final setup pending |
| Authentication | Not mandatory for MVP |
| Report history | Excluded from MVP |
| Save/share and PDF download | Included in proposed MVP |
| WhatsApp sharing | Pre-filled sharing link proposed |
| Feedback | Optional MVP feature |
| Admin monitoring | Basic operational monitoring proposed |
| Retention policy | Exact duration and backup deletion process pending |
| Backend integration testing | Pending implementation |
| Test fixtures | To be prepared |
| Automated test execution | Pending implementation |
| Medical professional approval | Pending |

## 12. Pending Team Confirmations

The following items still require confirmation or implementation details:

1. Exact temporary document retention duration.
2. Backup deletion and recovery policy.
3. Qualified medical professional approval of red-flag rules.
4. Final Supabase setup and data access policies.
5. Final API schema for reading-level selection.
6. Final API language validation for English, Hindi and Kannada.
7. API contract and implementation for save/share and PDF generation, if backend endpoints are required.
8. Feedback implementation, depending on development time.
9. Admin dashboard monitoring scope and access permissions.
10. Verification of all proposed API schemas and error responses against the running backend.

---

**Project:** ReportSaathi  
**Stage:** 6 – Test Plan  
**Owner:** Person 3 – Quality & Engineering Lead  
**Technical coordination:** Person 2 – Systems & DevOps Lead
**Document status:** Proposed – Pending Final Team Confirmation, Backend Integration and QA Verification