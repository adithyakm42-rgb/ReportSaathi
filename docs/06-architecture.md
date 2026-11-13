# ReportSaathi – System Architecture

**Project Name:** ReportSaathi  
**Document:** System Architecture  
**Version:** 1.1
**Owner:** Person 2 – Systems & DevOps Lead
**Status:** Proposed – Pending Final Team Review and Confirmation

## 1. Introduction

This document describes the proposed technical architecture of ReportSaathi, an AI-assisted healthcare application designed to help users understand medical reports, laboratory results, prescriptions and discharge summaries in simple language.

The architecture separates the frontend, backend, OCR processing, safety validation, AI services and data storage to improve maintainability, security and scalability.

ReportSaathi is an educational support tool. It does not provide medical diagnosis or treatment.

## 2. Architecture Overview

ReportSaathi follows a client-server architecture.

The frontend provides the user interface, while the backend handles document processing, OCR, safety validation, AI communication and permitted data storage.

### Main Components

1. **Frontend:** User interface, document upload and explanation display.
2. **Backend API:** Request handling, application logic and security.
3. **OCR Engine:** Extracts text from uploaded documents.
4. **OCR Correction Module:** Allows users to correct uncertain extracted text through the backend.
5. **Safety Validation Module:** Checks extracted information against predefined safety rules.
6. **AI Service:** Generates simplified and multilingual explanations.
7. **Database / Storage:** Proposed minimal storage using Supabase, subject to final team confirmation.
8. **Monitoring:** Basic operational monitoring and error tracking for administrators.

## 3. Technology Stack

| Component | Proposed Technology | Purpose |
|---|---|---|
| Frontend | React.js | User interface |
| Frontend styling | HTML, CSS, JavaScript | Responsive design |
| Backend | Python FastAPI | API development |
| Data validation | Pydantic | Request and response validation |
| OCR | Tesseract OCR | Extract text from documents |
| AI | Gemini API | Simplified explanations |
| Database | Supabase PostgreSQL | Proposed minimal structured data storage |
| Version control | Git and GitHub | Source code management |
| Frontend hosting | Cloudflare Pages | Frontend deployment |
| Backend hosting | Render | API hosting |
| CI/CD | GitHub Actions | Automated testing and deployment |

The proposed stack remains subject to final team confirmation, cost, privacy and deployment feasibility.

## 4. High-Level System Workflow

The expected application workflow is:

1. User opens ReportSaathi. Mandatory patient registration or login is not required for the MVP.
2. User selects a supported language: English, Hindi or Kannada.
3. User selects an explanation reading level: Simple, Standard or Detailed.
4. User uploads a medical document.
5. Frontend validates the file type and size.
6. Frontend sends the document securely to the backend API.
7. Backend validates the request and processes the document.
8. OCR extracts text from the document.
9. Uncertain extracted text is presented for user review and correction when necessary.
10. Backend uses the verified or corrected extracted text for further processing.
11. Safety validation checks predefined red flags and laboratory reference ranges printed on the report.
12. Relevant validated information is sent to the AI service.
13. AI generates the requested explanation.
14. Backend validates the AI response and applies safety restrictions.
15. Frontend displays the explanation, warnings and 3–6 suggested doctor questions.
16. User can save or share the result, download a PDF or use a pre-filled WhatsApp sharing link.

Optional feedback may be collected if included in the final implementation.

## 5. Architecture Diagram

```text
+--------------------------------+
|         PATIENT / USER          |
|                                |
| - No mandatory login           |
| - Language selection           |
| - Reading level selection      |
+---------------+----------------+
                |
                v
+--------------------------------+
|          REACT FRONTEND         |
|                                |
| - Document Upload              |
| - OCR Review and Correction    |
| - Results Interface            |
| - Save / Share / PDF            |
| - Doctor Questions             |
+---------------+----------------+
                |
                | HTTPS / REST API
                v
+--------------------------------+
|         FASTAPI BACKEND         |
|                                |
| - File Validation              |
| - Request Handling             |
| - OCR Processing               |
| - OCR Correction API           |
| - Safety Validation            |
| - AI Communication             |
| - Response Validation          |
+---------------+----------------+
                |
                v
+--------------------------------+
|          OCR PROCESSING         |
|                                |
| - Tesseract OCR                |
| - Text Extraction              |
| - Uncertain Field Detection    |
| - Verified Text Management     |
+---------------+----------------+
                |
                v
+--------------------------------+
|        SAFETY VALIDATION        |
|                                |
| - Deterministic Red-Flag Rules |
| - Printed Reference Ranges     |
| - Prescription Restrictions    |
+---------------+----------------+
                |
                v
+--------------------------------+
|           GEMINI API            |
|                                |
| - Medical Term Explanations    |
| - Multilingual Output          |
| - Reading-Level Adaptation     |
| - Doctor Questions             |
+---------------+----------------+
                |
                v
+--------------------------------+
|       RESPONSE VALIDATION       |
|                                |
| - Safety Restrictions          |
| - Output Validation            |
+---------------+----------------+
                |
                v
+--------------------------------+
|          REACT FRONTEND         |
|                                |
| - Explanation                  |
| - Safety Warnings              |
| - Doctor Questions             |
| - Save / Share / PDF           |
+--------------------------------+

       PROPOSED DATA STORAGE
+--------------------------------+
|       SUPABASE POSTGRESQL       |
|                                |
| - Minimal Application Data     |
| - Permitted Feedback Data      |
| - Required Operational Data    |
|                                |
| Temporary report processing    |
| Automatic deletion according   |
| to the approved retention      |
| policy                         |
+--------------------------------+
```

The diagram represents the proposed logical architecture. Actual storage and deployment details remain subject to implementation and team approval.

## 6. Frontend Architecture

The frontend is responsible for user interaction and presentation.

### Main Modules

- Patient landing page.
- Medical document upload interface.
- Language selection.
- Reading-level selection.
- OCR review and correction interface.
- Explanation results page.
- Safety warning display.
- Doctor question display.
- Save and share options.
- PDF download.
- Basic administrator monitoring interface.

### Frontend Responsibilities

- Validate basic file requirements before upload.
- Send API requests securely to the backend.
- Display loading and error states.
- Allow users to review and correct OCR text.
- Display explanations and warnings.
- Support English, Hindi and Kannada.
- Support Simple, Standard and Detailed explanations.
- Provide save, share, PDF and WhatsApp sharing options.
- Avoid storing private API keys in browser code.

Patient login and permanent report history are excluded from the MVP.

## 7. Backend Architecture

Python FastAPI will provide REST APIs for the application.

### Backend Responsibilities

- Receive medical document uploads.
- Validate file type, size and request data.
- Process documents using OCR.
- Manage verified and corrected OCR text.
- Execute deterministic safety checks before AI processing.
- Communicate with the Gemini API.
- Validate AI-generated responses.
- Apply medical safety restrictions.
- Manage permitted minimal data storage.
- Provide basic operational monitoring and error tracking.
- Handle administrator authentication and authorization where required.
- Return structured API responses.

### Proposed API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Check backend health |
| POST | `/api/upload` | Upload a medical document |
| POST | `/api/extract` | Extract document text |
| PATCH | `/api/extract/{document_id}/corrections` | Submit OCR text corrections |
| POST | `/api/explain` | Generate simplified explanation |
| POST | `/api/translate` | Translate explanation |
| POST | `/api/questions` | Generate doctor questions |
| POST | `/api/feedback` | Submit optional feedback |

The following capabilities are also planned:

- Save and share results.
- Generate PDF downloads.
- Generate pre-filled WhatsApp sharing links.
- Basic administrator monitoring.

Separate endpoints for these capabilities will be finalized according to the implementation design.

Permanent report-history retrieval is not included in the MVP. A patient-history endpoint is therefore excluded.

These are proposed API contracts. They must be implemented and tested before being treated as available.

## 8. OCR Processing Architecture

Tesseract OCR will be used to extract text from supported documents.

Supported MVP formats:

- PDF
- JPG
- JPEG
- PNG

Maximum upload size: 10 MB.

### Processing Steps

1. Receive the uploaded document.
2. Validate file format and size on the backend.
3. Convert supported PDF pages into images when necessary.
4. Apply image preprocessing where appropriate.
5. Extract text using Tesseract OCR.
6. Identify uncertain or incomplete extracted information.
7. Present extracted text for user review when necessary.
8. Accept manual corrections through the backend correction API.
9. Use verified or corrected text for subsequent processing.

The backend must associate corrected text with the corresponding temporary document identifier.

The backend must not blindly trust extracted text supplied by the frontend during explanation requests.

Scanned documents with poor image quality may require additional processing or user correction.

## 9. AI Integration Architecture

The backend will communicate with the Gemini API.

The AI service will be used to:

- Explain medical terminology.
- Simplify laboratory report information.
- Clarify existing prescription instructions without modifying them.
- Translate explanations into English, Hindi and Kannada.
- Generate 3–6 questions for doctor consultations.
- Adapt explanations to Simple, Standard and Detailed reading levels.

### AI Safety Restrictions

The AI must not:

- Diagnose medical conditions.
- Predict diseases.
- Prescribe medication.
- Change medication dosage, frequency or duration.
- Recommend stopping medication.
- Invent laboratory reference ranges.
- Provide false reassurance about urgent warning signs.
- Replace qualified medical professionals.

Laboratory interpretation must use only reference ranges printed on the uploaded report. Missing ranges must not be invented.

API keys must remain on the backend and must never be exposed in frontend code.

## 10. Data Storage Architecture

Supabase PostgreSQL is proposed for minimal data storage, subject to final team confirmation.

### Proposed Storage Principles

- Mandatory patient registration is not required for the MVP.
- Permanent report history is excluded from the MVP.
- Medical documents should use temporary processing wherever possible.
- Only necessary application and operational data should be stored.
- Optional feedback may be stored if approved.
- Access to any persisted data must be restricted.
- Temporary uploaded files and extracted medical information must be automatically deleted according to an approved retention policy.

The exact retention duration and backup deletion policy remain pending team confirmation.

Supabase Row Level Security (RLS) and suitable access controls must be configured if persisted user-related data is introduced.

Medical report contents and personal health information must not be exposed in application logs or analytics.

## 11. Security Architecture

The application should implement:

- HTTPS for production communication.
- Secure administrator authentication and authorization.
- Appropriate access controls for persisted data.
- File type and size validation on the backend.
- Server-side API key management.
- Secure handling and deletion of temporary files.
- Rate limiting and abuse protection.
- Restricted application logging.
- Privacy-conscious error monitoring.
- Supabase RLS if Supabase is used for data accessible through application clients.

Medical report contents and extracted health information must not be included in ordinary application logs or analytics.

Private credentials must never be committed to GitHub.

## 12. Deployment Architecture

The proposed deployment setup is:

- Frontend: Cloudflare Pages.
- Backend: Render.
- Source code: GitHub.
- Automated workflows: GitHub Actions.
- Database: Supabase PostgreSQL, subject to confirmation.

### Deployment Flow

```text
Developer
    |
    v
GitHub Repository
    |
    v
GitHub Actions
    |
    +------> Frontend Deployment
    |        Cloudflare Pages
    |
    +------> Backend Deployment
             Render
                 |
                 v
             FastAPI Service
                 |
                 v
        Gemini API / Supabase
        (as configured)
```

Production deployment must use environment variables and secure secret management.

## 13. Environment Variables

| Variable | Purpose | Visibility |
|---|---|---|
| VITE_API_URL | Backend API URL | Public |
| VITE_SUPABASE_URL | Supabase project URL, if used | Public |
| VITE_SUPABASE_ANON_KEY | Supabase public client key, if used | Public, with appropriate access policies |
| FRONTEND_URL | Allowed frontend origin | Backend only |
| DATABASE_URL | Database connection | Private |
| GEMINI_API_KEY | AI service authentication | Private |
| SUPABASE_SERVICE_ROLE_KEY | Privileged Supabase credential, if required | Private |

Private environment variables must never be committed to GitHub.

Public client configuration does not replace server-side access controls or database security policies.

## 14. Scalability and Maintainability

The system should support:

- Independent frontend and backend development.
- Reusable API components.
- Modular OCR and AI services.
- Future language additions.
- Additional document formats.
- Automated testing and deployment.
- Centralized operational error monitoring.
- Future enhancements without compromising existing safety rules.

## 15. Conclusion

The proposed ReportSaathi architecture separates presentation, document processing, OCR correction, safety validation, AI generation and data storage.

The architecture follows the current MVP recommendations, including no mandatory patient login, no permanent report history, English/Hindi/Kannada support, three explanation reading levels and temporary report processing.

This structure aims to provide a maintainable and privacy-conscious foundation for the MVP.

The architecture remains subject to implementation testing, privacy review and final team approval.