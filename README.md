# ReportSaathi
<<<<<<< HEAD

**AI-Assisted Medical Report Understanding Platform**

ReportSaathi is an AI-assisted healthcare application designed to help patients understand their medical reports in simple language. It aims to make medical information easier to understand while maintaining patient privacy and medical safety.

> **Important:** ReportSaathi is an educational support tool. It does not diagnose diseases, prescribe treatments or replace consultation with qualified medical professionals.

## 1. Problem Statement

Medical reports often contain complex medical terminology, abbreviations and laboratory values that patients may find difficult to understand.

ReportSaathi aims to simplify this information and help patients prepare meaningful questions for their doctors.

## 2. Project Objectives

- Help patients understand medical reports in simple language.
- Extract text from uploaded medical documents using OCR.
- Explain medical terminology and laboratory values using the reference ranges printed on the report.
- Support multiple languages and reading levels.
- Help patients prepare questions for medical consultations.
- Provide appropriate safety warnings for predefined medical red flags.
- Protect sensitive medical information throughout processing.

## 3. Proposed MVP Features

| Feature | Description |
|---|---|
| Document Upload | Upload PDF, JPG, JPEG and PNG files up to 10 MB. |
| OCR Extraction | Extract text from uploaded medical documents. |
| OCR Correction | Allow correction of incorrectly extracted text. |
| Report Explanation | Explain medical information in understandable language. |
| Reading Levels | Simple, Standard and Detailed. |
| Languages | English, Hindi and Kannada. |
| Lab Value Explanation | Use only reference ranges printed on the uploaded report. |
| Prescription Clarification | Explain existing instructions without changing medication or dosage. |
| Doctor Questions | Generate 3–6 questions for discussion with a doctor. |
| Safety Warnings | Display predefined warnings for identified red flags. |
| Save and Share | Allow users to save and share generated explanations. |
| PDF Download | Download explanations as PDF documents. |
| WhatsApp Sharing | Provide a pre-filled WhatsApp sharing link requiring user confirmation. |
| Feedback | Support optional basic user feedback. |
| Admin Monitoring | Provide basic operational monitoring and error tracking. |

**MVP limitations:**
- Patient registration and login are not mandatory.
- Permanent report history is excluded.
- WhatsApp chatbot functionality is outside the MVP.
- Medical red-flag rules require qualified medical professional review before production.
- Retention duration and backup deletion requirements require final confirmation.

## 4. Proposed Technology Stack

| Component | Proposed Technology |
|---|---|
| Frontend | React |
| Backend | Python FastAPI |
| Input Validation | Pydantic |
| OCR | Tesseract |
| AI Explanation | Gemini API |
| Database / Storage | Supabase with minimal data storage, pending final confirmation |
| Version Control | Git and GitHub |
| CI/CD | GitHub Actions |
| Frontend Deployment | Cloudflare Pages |
| Backend Deployment | Render |

The technology stack is documented as a proposal. Final implementation and deployment choices must be confirmed by the team.

## 5. Application Workflow

1. Patient uploads a medical report.
2. Backend validates the file type and size.
3. OCR extracts the document text.
4. Patient can correct OCR errors.
5. Backend uses the verified or corrected extracted text.
6. Safety checks are performed.
7. AI generates an explanation using the selected language and reading level.
8. Patient can review, save, share or download the explanation.
9. Patient can generate questions to discuss with a qualified doctor.

## 6. Medical Safety and Privacy

- ReportSaathi must not provide a medical diagnosis or treatment recommendation.
- It must not prescribe, modify or recommend stopping medication.
- Laboratory reference ranges must not be invented.
- Medical red-flag warnings must be evaluated before AI-generated explanations.
- Safety warnings must remain available even if the AI service fails.
- Medical report contents and personal health information must not be exposed in application logs or analytics.
- Uploaded documents and extracted data must follow an approved retention and deletion policy.
- Administrative access must be appropriately authenticated and restricted.

## 7. Team Responsibilities

| Team Member | Role | Main Responsibility |
|---|---|---|
| Person 1 | Product Strategy & Design Lead | Product requirements, scope, UI/UX and product documentation |
| Person 2 | Systems & DevOps Lead | Technical architecture, backend coordination, APIs, integration, CI/CD and deployment |
| Person 3 | Quality & Engineering Lead | Frontend engineering, testing, quality assurance and verification |

Responsibilities and task assignments remain subject to final team confirmation.

## 8. Repository Structure

```text
ReportSaathi-Project-Resources/
│
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI pipeline (Python tests + Vite build)
│
├── backend/
│   ├── safety/
│   │   ├── rules.py             # Deterministic biomarker evaluation & red-flag triggers
│   │   ├── banned_phrases.py    # Medical safety regex filter & safe fallback sanitizer
│   │   └── privacy.py           # PHI log sanitization & ephemeral storage lifecycle (SAFE-08, OCR-10)
│   └── integrations/
│       └── ocr.py               # Tesseract OCR engine, clarity scorer & user correction
│
├── frontend/                    # React 18 + Vite + TypeScript web application
│   ├── src/
│   │   ├── components/          # 6 core screens (Language, Upload, Check, Results, Questions, Share)
│   │   ├── types.ts             # Strict TypeScript frontend interfaces
│   │   └── api.ts               # Frontend API client with offline guard & fallback safety
│   ├── package.json
│   └── vite.config.ts
│
├── shared/
│   ├── types.ts                 # Shared contract definitions across frontend & backend
│   └── sample-report.json       # Gold-standard reference report fixture
│
├── tests/
│   ├── fixtures/                # 10 anonymized medical report fixtures (01 to 10)
│   ├── test_safety.py           # 13 deterministic safety & banned phrase tests
│   ├── test_ocr.py              # 5 OCR parser, clarity & correction tests
│   ├── test_api_contract.py     # 13 API contract & schema validation tests
│   └── test_privacy.py          # 9 PHI log sanitization, path traversal & TTL cleanup tests
│
├── docs/                        # Complete 12-stage project documentation
│   ├── 01-problem.md
│   ├── 02-research.md
│   ├── 03-scope.md
│   ├── 04-design.md
│   ├── 05-prd.md
│   ├── 06-architecture.md
│   ├── 06-test-plan.md
│   ├── 06b-safety-rules.md
│   ├── 06c-api-contracts.md
│   ├── 06d-clinical-review-protocol.md
│   ├── 07-task-breakdown.md
│   ├── 09-release.md
│   └── 10-feedback.md
│
└── README.md
```

## 9. Verification & Testing

### Running Backend & Safety Tests (100% Pass Rate)
The test suite runs with standard Python library tooling (`unittest`):

```bash
# Run all 40 tests across safety, OCR, API contracts, and privacy lifecycle
python -m unittest discover tests -v
```

### Running Frontend Build & Type Check
The React + Vite application builds cleanly:

```bash
cd frontend
npm install
npm run build
```

## 10. Documentation Index

| Document | Purpose |
|---|---|
| [Problem Definition](docs/01-problem.md) | Identifies the problem and proposed solution. |
| [Research](docs/02-research.md) | Research findings and technical background. |
| [Project Scope](docs/03-scope.md) | Defines MVP features and limitations. |
| [UI/UX Design](docs/04-design.md) | Screens and interface design references. |
| [Product Requirements](docs/05-prd.md) | Functional and non-functional requirements. |
| [System Architecture](docs/06-architecture.md) | Proposed application architecture. |
| [Test Plan](docs/06-test-plan.md) | Testing strategy and test cases. |
| [Safety Rules](docs/06b-safety-rules.md) | Medical safety and privacy requirements. |
| [API Contracts](docs/06c-api-contracts.md) | Proposed backend API specifications. |
| [Clinical Review Protocol](docs/06d-clinical-review-protocol.md) | Medical doctor review audit sheet & red-flag thresholds. |
| [Task Breakdown](docs/07-task-breakdown.md) | Development and integration tasks. |
| [Release Plan](docs/09-release.md) | Proposed deployment, QA status and release preparation. |
| [Feedback & Continuous Improvement](docs/10-feedback.md) | Defines feedback collection, monitoring and improvement. |

## 11. Development Approach

The team follows a documentation-first, safety-first development approach:

1. Complete and review project documentation.
2. Implement deterministic safety guardrails before AI text generation.
3. Scaffold frontend components and user verification flows.
4. Establish comprehensive automated test fixtures and contract tests.
5. Configure CI/CD automated validation for all PRs and pushes.
6. Conduct qualified medical professional review of red-flag thresholds.
7. Integrate backend API services and deployment pipeline.

## 12. Current Project Status

**Current phase:** Implementation & Quality Assurance.

- **Quality Assurance & Safety:** 40 out of 40 automated tests passing (100% pass rate).
- **Medical Safety Engine:** Deterministic red-flag triggers and banned phrase filters active.
- **Privacy & Data Protection:** Ephemeral file lifecycle, automatic TTL cleanup, and PHI log sanitization active.
- **Frontend Application:** React 18 + Vite 5 + TypeScript app with 6 core screens verified.
- **Continuous Integration:** GitHub Actions CI workflow configured.
- **Clinical Review:** Doctor sign-off audit protocol documented at `docs/06d-clinical-review-protocol.md`.

---

**Project:** ReportSaathi  
**Repository:** ReportSaathi-Project-Resources  
**Status:** Implementation & QA Phase (40/40 Tests Passing, Frontend Built)
=======
AI-powered medical report explainer that converts complex medical reports into simple language.
>>>>>>> 8dc615b86ee03dcd343fd4f20f4deda43da066f9
