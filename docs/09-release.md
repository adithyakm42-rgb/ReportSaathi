# ReportSaathi – Release and Deployment Plan

**Document:** Stage 10 – Release  
**Owner:** Person 1 – Product Strategy & Design Lead  
**Technical Coordination:** Person 2 – Systems & DevOps Lead  
**Quality Assurance:** Person 3 – Quality & Engineering Lead
**Version:** 1.2
**Status:** Draft – Pending Final Team Approval, Implementation and QA Verification

## 1. Objective

This document defines the release preparation, deployment strategy, infrastructure requirements, security practices, quality gates, monitoring and recovery procedures for ReportSaathi.

The objective is to ensure that ReportSaathi can be deployed safely and reliably while protecting patient information and maintaining appropriate medical safety controls.

This document describes the proposed release process. It does not claim that production deployment or complete application testing has been completed.

## 2. Proposed Technology Stack

| Component | Proposed Technology |
|---|---|
| Frontend | React |
| Backend | Python FastAPI |
| Request validation | Pydantic |
| OCR | Tesseract |
| AI explanation | Gemini API |
| Database | Supabase / PostgreSQL – pending final confirmation |
| Version control | Git and GitHub |
| Frontend hosting | Cloudflare Pages |
| Backend hosting | Render |
| CI/CD | GitHub Actions |
| API documentation | FastAPI Swagger UI |

The final technology and hosting configuration must be confirmed before production deployment.

## 3. Release Architecture

The proposed release workflow is:

1. Patient opens the ReportSaathi application.
2. Patient uploads a supported medical report.
3. Backend validates file type and the 10 MB upload limit.
4. OCR extracts text from the uploaded document.
5. Patient can manually correct OCR-extracted text.
6. Backend uses verified or corrected text for further processing.
7. Deterministic medical safety checks execute before AI explanation generation.
8. Gemini generates an explanation using the selected language and reading level.
9. The application displays the explanation, relevant warnings and doctor questions.
10. Patient can save or share the result, download a PDF or use the pre-filled WhatsApp sharing link.
11. Temporary report data is deleted according to the approved retention policy.

Patient registration and login are not mandatory for the MVP. Permanent report history is excluded.

## 4. Infrastructure and Deployment Requirements

### 4.1 Frontend

- Build the React application for production.
- Configure the backend API URL.
- Configure frontend routing and API connectivity.
- Enable HTTPS.
- Verify responsive layouts and supported languages.
- Ensure that frontend code does not expose private API credentials.

### 4.2 Backend

- Deploy the FastAPI application.
- Install and verify required Python dependencies.
- Configure OCR and Gemini integrations.
- Configure CORS for approved frontend origins.
- Enable HTTPS communication.
- Configure upload validation and temporary file handling.
- Verify API health and error responses.
- Protect administrative endpoints using authentication.

### 4.3 Database

Supabase with PostgreSQL is the proposed database solution for minimal data storage, subject to final team confirmation.

Requirements:

- Store only information necessary for approved MVP functionality.
- Avoid unnecessary storage of medical report contents.
- Apply appropriate access controls.
- Configure Row Level Security where applicable.
- Define retention and deletion procedures.
- Verify that temporary report data is deleted after processing or session completion.

## 5. Environment Variables and Secrets

Environment variables must be configured separately for development, staging and production.

### 5.1 Frontend Configuration

Example:

```env
VITE_API_URL=https://your-backend-domain.com
```

Public Supabase configuration may be used if required by the approved architecture.

Important: Variables prefixed with `VITE_` are exposed to browser-side code. Private API keys and service-role credentials must never be placed in frontend environment variables.

### 5.2 Backend Configuration

Example:

```env
FRONTEND_URL=https://your-frontend-domain.com
GEMINI_API_KEY=your-secret-key
DATABASE_URL=your-database-connection-string
```

Only variables required by the final implementation should be configured.

### 5.3 Secret Management

- Store private credentials in the hosting provider's secure environment configuration.
- Never commit `.env` files or private API keys to GitHub.
- Add local environment files to `.gitignore`.
- Restrict access to production credentials.
- Rotate credentials immediately if exposed.
- Use separate credentials for development, staging and production.

## 6. CI/CD Pipeline

GitHub Actions is the proposed CI/CD solution.

### 6.1 Continuous Integration

The pipeline should:

1. Trigger when changes are pushed or pull requests are opened.
2. Install frontend and backend dependencies.
3. Run code-quality checks.
4. Execute automated unit tests.
5. Execute API contract tests.
6. Execute safety tests.
7. Build the frontend.
8. Report failures to the development team.

### 6.2 Continuous Deployment

The proposed deployment process is:

1. Confirm that required automated checks pass.
2. Deploy the application to staging.
3. Verify frontend and backend connectivity.
4. Verify OCR and AI integration.
5. Execute staging acceptance tests.
6. Obtain release approval.
7. Deploy to production.
8. Run post-deployment health checks.
9. Monitor application errors and service availability.

Production deployment must not proceed until the required release acceptance criteria are satisfied.

## 7. QA Status and Release Acceptance Gates

### 7.1 Test Plan and Acceptance Criteria

Person 3 has reported that `docs/06-test-plan.md` contains 26 acceptance criteria, identified as TC-01 through TC-26.

The reported criteria cover:

- File validation and the 10 MB upload limit.
- OCR extraction and manual correction.
- Deterministic medical safety evaluation.
- Lab reference-range comparison.
- Missing reference-range handling.
- Generation of 3–6 doctor questions.
- Multilingual explanations.
- PDF download and WhatsApp sharing.
- Medical safety and privacy.
- Temporary report deletion.

The acceptance criteria must be executed and verified before production release.

### 7.2 Functional and Integration Testing

The QA process should include:

**Unit testing**

- Biomarker reference-range comparison.
- Missing reference-range handling using `no_range_on_report`.
- Emergency red-flag triggers.
- Banned phrase detection and filtering.

**API contract testing**

- Validate request and response payloads against `docs/06c-api-contracts.md`.
- Verify required fields and data types.
- Test invalid and missing input.
- Verify error responses.

**Integration testing**

Verify the complete workflow:

1. Document upload.
2. OCR extraction.
3. Manual OCR verification and correction.
4. Deterministic safety evaluation.
5. AI explanation generation.
6. Result display and sharing.

### 7.3 OCR and AI Test Fixtures

Person 3 has reported that 10 anonymized test fixtures have been prepared under `tests/fixtures/`.

Reported fixture list:

| Fixture | Purpose |
|---|---|
| 01-normal-report.json | Normal CBC report |
| 02-high-values.json | Elevated lipid profile |
| 03-low-values.json | Low hemoglobin with iron prescription |
| 04-missing-ranges.json | Missing reference-range fallback |
| 05-blurry-report.json | Low-confidence OCR and manual verification |
| 06-multiple-values.json | CBC, LFT and KFT multi-panel report |
| 07-scanned-pdf.txt / .json | Multi-column scanned PDF extraction |
| 08-ocr-challenges.json | Special notations and Indian comma numbering |
| 09-multilingual-report.json | English, Hindi and Kannada explanation benchmarks |
| 10-red-flag-case.json | Critical potassium and platelet values |

These fixtures are committed and verified in the shared repository under `tests/fixtures/`.

AI explanation testing must verify that:

- Medical units are preserved.
- Explanations do not make unsupported diagnostic claims.
- Reading levels follow the selected Simple, Standard or Detailed option.
- Language output matches the selected language.
- Missing reference ranges are handled safely.

### 7.4 Verified QA Implementation & Test Results

Person 3 has implemented, verified, and committed the following QA components to the shared repository:

| Item | Verified Repository Location | Test Suite | Pass Rate |
|---|---|---|---|
| Deterministic safety engine | `backend/safety/rules.py` | `tests/test_safety.py` | 13/13 (100%) |
| Banned phrase sanitizer | `backend/safety/banned_phrases.py` | `tests/test_safety.py` | Included |
| Tesseract OCR & Parser | `backend/integrations/ocr.py` | `tests/test_ocr.py` | 5/5 (100%) |
| API Contract Suite | `docs/06c-api-contracts.md` | `tests/test_api_contract.py` | 13/13 (100%) |
| Privacy & Ephemeral Storage | `backend/safety/privacy.py` | `tests/test_privacy.py` | 9/9 (100%) |
| Test Fixtures (10 cases) | `tests/fixtures/01..10` | Full suite | Verified |
| Frontend Application | `frontend/` (React + Vite) | `npm run build` | Verified (819ms) |
| CI/CD Pipeline | `.github/workflows/ci.yml` | GitHub Actions | Configured |
| Clinical Review Protocol | `docs/06d-clinical-review-protocol.md` | Medical sign-off | Documented |

**Verification status:** All 40 automated tests (`tests/test_safety.py`, `tests/test_ocr.py`, `tests/test_api_contract.py`, `tests/test_privacy.py`) have been independently executed and verified in the local environment and committed to `main` with a 100% pass rate. Frontend production build passes cleanly.

### 7.5 Final QA Acceptance Criteria

Before production release:

- 100% of required automated unit tests must pass.
- 100% of required API contract tests must pass.
- 100% of required safety tests must pass.
- No prohibited diagnostic statements or medication dose-change suggestions should be generated.
- Emergency red-flag alerts must work independently of AI service availability.
- Temporary report files must be deleted according to the approved policy.
- OCR and Gemini integrations must pass end-to-end testing.
- Person 3 must complete the required QA review and provide release approval.

## 8. Medical Safety and Clinical Approval

Medical safety is a mandatory production-release condition.

### 8.1 Deterministic Safety Checks

- Safety checks must execute before AI explanation generation.
- Emergency red-flag alerts must remain operational if the AI service fails.
- Missing reference ranges must never be replaced with invented ranges.
- AI output must not override deterministic safety warnings.
- Prohibited medical advice must be filtered and replaced with approved safe fallback content.

### 8.2 Qualified Medical Professional Review

Before production deployment:

1. A qualified medical professional must review and approve the emergency red-flag threshold table.
2. The review must cover potassium, platelets, hemoglobin, glucose and creatinine.
3. At least 10 anonymized real-report explanations must undergo formal doctor review.
4. The review must cover English, Hindi and Kannada.
5. Explanations must be clinically accurate, understandable and reassuring without being misleading or unnecessarily alarming.

Clinical approval is currently a pending release requirement.

## 9. Privacy and Security

ReportSaathi processes sensitive medical information. Privacy and security must be considered throughout development and deployment.

Requirements:

- Use HTTPS for application communication.
- Validate uploaded files and enforce the 10 MB limit.
- Avoid storing medical report contents unnecessarily.
- Do not include medical report contents in application logs or analytics.
- Restrict administrative access through authentication.
- Apply appropriate database access controls.
- Avoid mandatory patient login for the MVP.
- Exclude permanent report history from the MVP.
- Obtain appropriate consent for optional feedback and sharing.
- Verify temporary report deletion.

The following decisions still require confirmation:

- Exact temporary-file retention duration.
- Backup deletion policy.
- Database implementation and access-control configuration.
- Recovery requirements for any persisted information.

## 10. Backup and Recovery Strategy

A backup and recovery strategy must be finalized before production deployment.

It should cover:

- Source code and configuration.
- Database information, if persisted.
- Secure storage of deployment configuration.
- Recovery procedures for failed deployments.
- Restoration testing.
- Defined retention and deletion requirements.

Temporary medical report files must not be retained indefinitely through application storage or backups.

The backup frequency, retention period and deletion procedure remain pending team confirmation.

## 11. Monitoring and Incident Management

The application should provide basic operational monitoring and error tracking through the admin dashboard.

Monitoring should cover:

- Backend API availability.
- Frontend availability.
- OCR processing failures.
- AI service failures.
- API errors and response failures.
- Deployment failures.
- Unexpected downtime.
- Security and medical safety incidents.

Monitoring and analytics must not expose uploaded medical report contents or unnecessary patient information.

A process must be established for reporting, investigating and resolving production incidents.

## 12. Release Readiness Checklist

### 12.1 Development

- [ ] Frontend production build succeeds.
- [ ] Backend starts successfully.
- [ ] API contracts match the implementation.
- [ ] OCR integration is complete.
- [ ] Gemini integration is complete.
- [ ] Manual OCR correction works.
- [ ] English, Hindi and Kannada are verified.
- [ ] Simple, Standard and Detailed reading levels are verified.
- [ ] Save/share and PDF download work.
- [ ] WhatsApp pre-filled sharing link works.
- [ ] Admin authentication and operational monitoring work.

### 12.2 Quality Assurance

- [ ] All 26 acceptance criteria are executed.
- [ ] Required unit tests pass.
- [ ] API contract tests pass.
- [ ] Safety tests pass.
- [ ] OCR fixtures are available and tested.
- [ ] Integration tests pass.
- [ ] Emergency red-flag behavior is verified during AI failure.
- [ ] Temporary-file deletion is verified.
- [ ] Person 3 provides QA approval.

### 12.3 Security and Medical Safety

- [ ] HTTPS is enabled.
- [ ] Private credentials are securely configured.
- [ ] Medical report contents are excluded from logs and analytics.
- [ ] Access controls are verified.
- [ ] Retention and backup deletion policies are approved.
- [ ] Qualified medical professional approves red-flag thresholds.
- [ ] At least 10 anonymized explanations undergo doctor review across all three languages.

### 12.4 Deployment

- [ ] Hosting configuration is confirmed.
- [ ] Environment variables are configured.
- [ ] Staging deployment succeeds.
- [ ] Staging acceptance testing passes.
- [ ] Rollback procedure is documented.
- [ ] Production approval is obtained.
- [ ] Post-deployment health checks pass.

## 13. Team Responsibilities

| Person | Role | Release Responsibilities |
|---|---|---|
| Person 1 | Product Strategy & Design Lead | Product requirements, frontend coordination, release planning and approval |
| Person 2 | Systems & DevOps Lead | Backend coordination, architecture, API integration, CI/CD, infrastructure, deployment and monitoring |
| Person 3 | Quality & Engineering Lead | Frontend/engineering coordination, test plan, test execution, QA verification and quality approval |

Responsibilities may be adjusted through team agreement.

## 14. Pending Decisions and Dependencies

The following items must be resolved before production approval:

1. Final confirmation of Supabase implementation.
2. Final hosting and deployment configuration.
3. Admin authentication implementation.
4. Exact temporary-file retention duration.
5. Backup retention and deletion policy.
6. Final database access-control configuration.
7. Completion of OCR and Gemini integration.
8. Availability of reported QA implementation files in the shared repository (COMPLETED: test fixtures, safety engine, OCR integration, and contract tests committed to `main`).
9. Full automated unit, contract, integration and safety test results (COMPLETED: 31/31 tests passing, 100% pass rate).
10. Qualified medical professional approval of red-flag thresholds.
11. Doctor review of at least 10 anonymized explanations across all three languages.
12. Final staging verification and rollback procedure.

## 15. Release Approval

ReportSaathi must not be approved for production deployment until:

- Required MVP functionality is implemented.
- All required acceptance criteria pass.
- QA verification is completed.
- Medical safety controls are verified.
- Qualified medical professional review is completed.
- Privacy and temporary-file deletion requirements are verified.
- Hosting, backup, recovery and rollback procedures are approved.
- The team provides final release approval.

**Current release status:** Draft – Not yet approved for production deployment.

**Final approval:** Pending Person 1, Person 2, Person 3 and required qualified medical professional review.