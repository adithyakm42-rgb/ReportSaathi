# ReportSaathi — Stage 7: Task Breakdown

**Stage:** 7 — Task Breakdown  
**Owner:** Person 1 — Product Strategy & Design Lead  
**Technical Coordination:** Person 2 — Systems & DevOps Lead
**Quality Review:** Person 3 — Quality & Engineering Lead
**Status:** Draft — Pending Final Team Review and Confirmation
**Version:** 1.1

## 1. Purpose

This document breaks the proposed ReportSaathi MVP into manageable development, integration, testing and release-preparation tasks.

It identifies priorities, dependencies, expected deliverables, responsibility areas and completion criteria.

This is a planning document. Listing a task does not mean that it has been implemented or tested.

## 2. Project Objective

ReportSaathi helps patients and caregivers understand medical reports, laboratory results, prescriptions and discharge summaries through clear, accessible and multilingual educational explanations.

The application must preserve medical information accurately, identify unclear OCR results, use only reference ranges printed on uploaded reports and follow the project's medical safety rules.

It must not diagnose diseases or recommend medication changes.

## 3. Priority Definitions

| Priority | Meaning |
|---|---|
| P0 — Critical | Required for a safe and functional MVP |
| P1 — High | Required for the agreed MVP experience or quality |
| P2 — Later | Optional or post-MVP enhancement |

## 4. Task Breakdown

### 4.1 Product, UI/UX and Frontend

| ID | Task | Priority | Dependency | Deliverable |
|---|---|---|---|---|
| UI-01 | Finalize English, Hindi and Kannada language options | P0 | Scope confirmation | Language selector |
| UI-02 | Implement Simple, Standard and Detailed reading-level options | P0 | PRD confirmation | Reading-level selector |
| UI-03 | Finalize user journey and screen navigation | P0 | Scope and design review | Approved user flow |
| UI-04 | Implement medical document upload interface | P0 | UI-03 | Upload screen |
| UI-05 | Implement OCR processing and loading states | P0 | OCR API | Processing interface |
| UI-06 | Display extracted information for manual correction | P0 | OCR correction API | Editable verification screen |
| UI-07 | Implement medical explanation results screen | P0 | Explanation API | Explanation interface |
| UI-08 | Display printed reference ranges and unclear values correctly | P0 | OCR and explanation APIs | Lab-value presentation |
| UI-09 | Display deterministic safety warnings and disclaimer | P0 | Safety API/backend | Warning interface |
| UI-10 | Implement translation interface | P1 | Translation API | Translated explanation display |
| UI-11 | Display 3–6 suggested doctor questions | P1 | Questions API | Doctor-question interface |
| UI-12 | Implement Save and Share functionality | P1 | Backend and privacy review | Save/share workflow |
| UI-13 | Implement PDF download | P1 | Explanation results | Downloadable PDF |
| UI-14 | Implement pre-filled WhatsApp sharing link | P1 | Share functionality | WhatsApp sharing workflow |
| UI-15 | Implement basic administrator monitoring interface | P1 | Admin requirements and access design | Admin monitoring interface |
| UI-16 | Implement optional feedback interface | P1 | Feedback API | Feedback interface |
| UI-17 | Implement accessible and responsive layouts | P1 | Screen designs | Desktop and mobile layouts |

**Responsibility:** Person 1 leads product requirements, frontend and UI/UX coordination. Person 3 supports engineering quality and frontend testing.

Patient registration and login screens are not mandatory for the MVP.

### 4.2 Document Upload and OCR

| ID | Task | Priority | Dependency | Deliverable |
|---|---|---|---|---|
| OCR-01 | Configure PDF, JPG, JPEG and PNG upload formats | P0 | Upload API | File-format validation |
| OCR-02 | Implement maximum upload size of 10 MB | P0 | Scope confirmation | File-size validation |
| OCR-03 | Validate empty, malformed and unsupported files | P0 | OCR-01 | Upload validation |
| OCR-04 | Implement secure temporary document processing | P0 | Upload API and retention policy | Temporary document handling |
| OCR-05 | Implement image preprocessing where required | P0 | OCR engine | Preprocessing module |
| OCR-06 | Implement Tesseract-based text extraction | P0 | OCR-05 | OCR extraction module |
| OCR-07 | Identify unclear or incomplete extracted information | P0 | OCR-06 | OCR uncertainty detection |
| OCR-08 | Preserve original medical values, units and printed reference ranges | P0 | OCR-06 | Structured extraction output |
| OCR-09 | Implement manual correction through the backend API | P0 | Verification interface and API contract | Correction workflow |
| OCR-10 | Delete temporary files and extracted text according to the approved retention policy | P0 | OCR-04 and retention decision | Deletion mechanism |

Scanned documents with poor image quality may require additional processing or user correction.

### 4.3 Medical Explanation and AI Integration

| ID | Task | Priority | Dependency | Deliverable |
|---|---|---|---|---|
| AI-01 | Configure backend AI service integration | P0 | AI provider configuration | Backend AI service |
| AI-02 | Store AI API keys in backend environment variables | P0 | Backend setup | Secure configuration |
| AI-03 | Generate plain-language medical report explanations | P0 | Verified OCR text | Explanation endpoint |
| AI-04 | Support Simple, Standard and Detailed explanations | P0 | AI-03 | Reading-level functionality |
| AI-05 | Explain medical terms without diagnosing | P0 | AI-03 and safety rules | Safe explanation behavior |
| AI-06 | Compare laboratory results only with printed reference ranges | P0 | OCR-08 | Range-comparison logic |
| AI-07 | Handle missing or unclear reference ranges | P0 | OCR-08 | Uncertainty handling |
| AI-08 | Clarify existing prescription instructions without modifying them | P0 | AI-03 and safety rules | Prescription-safe explanation |
| AI-09 | Support English, Hindi and Kannada | P0 | Language configuration | Multilingual functionality |
| AI-10 | Generate 3–6 doctor consultation questions | P1 | Explanation API | Questions endpoint |
| AI-11 | Validate AI responses before displaying them | P0 | Safety rules | AI output validator |
| AI-12 | Implement safe fallback messages for AI failures | P0 | AI-11 | Fallback response handling |
| AI-13 | Include medical disclaimers with explanations | P0 | Explanation interface | Disclaimer display |

### 4.4 Medical Safety and Privacy

| ID | Task | Priority | Dependency | Deliverable |
|---|---|---|---|---|
| SAFE-01 | Implement deterministic red-flag rules | P0 | Proposed rules and medical review | Backend safety rules |
| SAFE-02 | Execute red-flag checks before AI explanation generation | P0 | SAFE-01 and AI integration | Correct processing sequence |
| SAFE-03 | Preserve urgent warnings when AI is unavailable | P0 | SAFE-01 and fallback handling | Persistent safety warning |
| SAFE-04 | Block diagnosis and disease-prediction responses | P0 | AI response validation | Diagnosis restriction |
| SAFE-05 | Block medication-change recommendations | P0 | AI response validation | Prescription safety validation |
| SAFE-06 | Prevent invented laboratory values and reference ranges | P0 | OCR and AI validation | Value and range validation |
| SAFE-07 | Protect medical information from unauthorized access | P0 | Security and access-control design | Access-control implementation |
| SAFE-08 | Prevent medical report contents from appearing in logs or analytics | P0 | Backend logging configuration | Privacy-conscious logging |
| SAFE-09 | Validate uploaded files and treat extracted text as untrusted input | P0 | OCR implementation | Input validation |
| SAFE-10 | Configure HTTPS for deployed environments | P0 | Deployment setup | Secure communication |
| SAFE-11 | Define consent and temporary-data retention requirements | P0 | Team and privacy review | Approved privacy policy |
| SAFE-12 | Arrange qualified medical-professional review of red-flag rules | P0 before production | SAFE-01 | Documented review and approval |

Medical red-flag rules must receive qualified medical-professional review and approval before production use.

### 4.5 Backend and API Integration

| ID | Task | Priority | Dependency | Deliverable |
|---|---|---|---|---|
| API-01 | Implement and verify `GET /api/health` | P0 | FastAPI setup | Health endpoint |
| API-02 | Implement and verify `POST /api/upload` | P0 | OCR-01 to OCR-04 | Upload endpoint |
| API-03 | Implement and verify `POST /api/extract` | P0 | OCR-06 | OCR endpoint |
| API-04 | Implement and verify `POST /api/extract/{document_id}/corrections` | P0 | OCR-09 | Correction endpoint |
| API-05 | Implement and verify `POST /api/explain` | P0 | AI integration | Explanation endpoint |
| API-06 | Implement and verify `POST /api/translate` | P1 | AI language support | Translation endpoint |
| API-07 | Implement and verify `POST /api/questions` | P1 | AI-10 | Questions endpoint |
| API-08 | Implement optional feedback API | P1 | Feedback decision | Feedback endpoint |
| API-09 | Implement administrator authentication and authorization | P0 | Admin security design | Secure admin access |
| API-10 | Standardize success and error responses | P0 | API contract review | Consistent API responses |
| API-11 | Implement appropriate HTTP status codes | P0 | API-10 | Correct error handling |
| API-12 | Validate request fields, document IDs and language values | P0 | API implementation | Input validation |
| API-13 | Add rate limiting and safe retry handling | P1 | Backend setup | Request protection |
| API-14 | Implement or integrate approved Save/Share functionality | P1 | UI-12 and privacy review | Save/share support |
| API-15 | Implement PDF generation or download support | P1 | UI-13 | PDF functionality |
| API-16 | Generate pre-filled WhatsApp sharing links | P1 | UI-14 | WhatsApp sharing support |

The backend must retrieve verified or corrected OCR text using the temporary document identifier. It must not blindly trust medical text supplied directly by the frontend.

Patient history retrieval is excluded from the MVP. A permanent patient-history endpoint is therefore not planned.

### 4.6 Administrator, Storage and Feedback

| ID | Task | Priority | Dependency | Deliverable |
|---|---|---|---|---|
| ADM-01 | Confirm basic administrator monitoring requirements | P0 | PRD and team review | Approved admin requirements |
| ADM-02 | Implement basic application-health monitoring | P1 | Backend health endpoint | Monitoring interface |
| ADM-03 | Implement operational error tracking | P1 | Backend logging configuration | Error monitoring |
| ADM-04 | Define administrator access restrictions | P0 | Security requirements | Role and permission specification |
| ADM-05 | Avoid routine administrator access to medical report contents | P0 | Privacy requirements | Restricted admin access |
| ADM-06 | Support optional feedback review if approved | P1 | Feedback implementation | Feedback management |
| DATA-01 | Confirm Supabase PostgreSQL implementation | P0 | Architecture and team decision | Storage decision |
| DATA-02 | If approved, design the minimum required database schema | P1 | DATA-01 | Database schema |
| DATA-03 | If approved, configure secure record access and RLS | P1 | DATA-02 | Database access controls |
| DATA-04 | Exclude permanent patient report history from MVP | P0 | Scope confirmation | Documented exclusion |
| DATA-05 | Define temporary-data deletion and backup deletion requirements | P0 | Retention decision | Approved deletion policy |

Supabase PostgreSQL is proposed for minimal data storage, subject to final team confirmation.

Mandatory patient login and permanent report history are excluded from the MVP. Exact retention duration and backup deletion policy remain pending confirmation.

### 4.7 Testing and Quality Assurance

| ID | Task | Priority | Dependency | Deliverable |
|---|---|---|---|---|
| TEST-01 | Prepare anonymized medical-report test fixtures | P0 | Test plan | Test fixtures |
| TEST-02 | Test upload formats and 10 MB file-size validation | P0 | OCR and API implementation | Upload test results |
| TEST-03 | Test successful and failed OCR extraction | P0 | OCR implementation | OCR test results |
| TEST-04 | Test manual correction workflow | P0 | Correction API | Correction test results |
| TEST-05 | Test printed-range comparison and missing ranges | P0 | Extraction and safety modules | Range safety test results |
| TEST-06 | Test deterministic red-flag execution | P0 | SAFE-01 and SAFE-02 | Red-flag test results |
| TEST-07 | Test AI service failures and safe fallbacks | P0 | AI-12 | Failure-handling test results |
| TEST-08 | Test unsafe AI output rejection | P0 | AI-11 | Safety validation test results |
| TEST-09 | Test English, Hindi and Kannada output | P0 | AI-09 | Language test results |
| TEST-10 | Test Simple, Standard and Detailed explanations | P0 | AI-04 | Reading-level test results |
| TEST-11 | Test doctor-question generation (3–6 questions) | P1 | AI-10 | Questions test results |
| TEST-12 | Test Save/Share, PDF and WhatsApp link workflows | P1 | API-14 to API-16 | Sharing and download test results |
| TEST-13 | Test privacy, logging and temporary-file deletion | P0 | Security implementation | Privacy test results |
| TEST-14 | Test administrator permissions and monitoring | P1 | Admin implementation | Admin test results |
| TEST-15 | Test optional feedback functionality if implemented | P1 | Feedback implementation | Feedback test results |
| TEST-16 | Execute API contract and integration tests | P0 | API implementation | API test report |
| TEST-17 | Execute end-to-end user journey tests | P1 | Frontend/backend integration | E2E test report |
| TEST-18 | Verify linting, type checks and critical issue resolution | P0 | Development tasks | Quality checklist |

Proposed testing tools include Pytest, Vitest, MSW, Bruno or Hoppscotch, Playwright and manual browser testing.

Person 3 leads quality assurance, test execution and verification.

### 4.8 Deployment and Release Preparation

| ID | Task | Priority | Dependency | Deliverable |
|---|---|---|---|---|
| REL-01 | Prepare frontend deployment configuration | P1 | Frontend integration | Deployment-ready frontend |
| REL-02 | Prepare backend deployment configuration | P1 | Backend integration | Deployment-ready backend |
| REL-03 | Configure production environment variables | P0 | Deployment setup | Secure configuration |
| REL-04 | Configure GitHub Actions where approved | P1 | Repository and test setup | CI workflow |
| REL-05 | Verify deployed frontend/backend communication | P0 | REL-01 and REL-02 | Integration verification |
| REL-06 | Verify HTTPS and privacy requirements | P0 | Security tasks | Deployment security checklist |
| REL-07 | Prepare release notes and known limitations | P1 | Team review | Release documentation |
| REL-08 | Obtain team approval before production release | P0 | Testing and safety review | Release approval |

Person 2 leads backend, API integration, DevOps coordination and deployment preparation.

## 5. Responsibility Allocation

| Person | Role | Main responsibilities |
|---|---|---|
| Person 1 | Product Strategy & Design Lead | Product requirements, frontend, UI/UX and product coordination |
| Person 2 | Systems & DevOps Lead | Backend, API contracts, system architecture, integration, infrastructure and deployment |
| Person 3 | Quality & Engineering Lead | QA, test planning, test execution, engineering verification and quality review |

Individual subtask assignments may be further divided by the team according to availability and expertise.

## 6. Dependencies and Implementation Sequence

The proposed implementation sequence is:

1. Confirm MVP decisions and finalize requirements.
2. Finalize screen flows, API contracts and technical responsibilities.
3. Configure frontend and backend project structures.
4. Implement upload validation and temporary document handling.
5. Implement OCR and manual verification.
6. Implement deterministic red-flag checks.
7. Integrate AI explanations and response validation.
8. Integrate translation and doctor-question generation.
9. Implement Save/Share, PDF download and WhatsApp sharing.
10. Implement basic administrator monitoring and optional feedback.
11. Configure Supabase minimal storage if approved.
12. Complete frontend/backend integration.
13. Execute safety, privacy, functional and end-to-end tests.
14. Fix critical issues and prepare release documentation.
15. Obtain team and required medical approval before production release.

**Critical dependency:** AI explanation generation must not bypass OCR verification or deterministic safety checks.

## 7. Pending Team Decisions

The following items still require explicit confirmation.

| No. | Decision required | Current position |
|---|---|---|
| 1 | Exact temporary report retention duration | Pending confirmation |
| 2 | Backup deletion and recovery policy | Pending confirmation |
| 3 | Qualified medical-professional review and approval | Required before production; reviewer and process pending |
| 4 | Final Supabase implementation and configuration | Proposed for minimal data storage; pending confirmation |
| 5 | Supabase RLS and access-control configuration | Required if applicable data is persisted |
| 6 | Exact scope of basic administrator monitoring | Basic operational monitoring and error tracking proposed |
| 7 | Optional feedback implementation | Included subject to development time |
| 8 | Save/Share and PDF API design | Included in MVP; exact implementation contracts to be finalized |
| 9 | WhatsApp pre-filled sharing implementation | Included in MVP; privacy and user-confirmation flow required |
| 10 | Final integration and deployment responsibilities | Person 2 leads backend and DevOps; detailed assignments to be confirmed |

The following MVP recommendations have already been agreed in principle:

- English, Hindi and Kannada.
- Simple, Standard and Detailed reading levels.
- Maximum upload size of 10 MB.
- 3–6 suggested doctor questions.
- No mandatory patient login.
- Permanent report history excluded.
- Save/Share and PDF download included.
- WhatsApp sharing through a pre-filled link.
- Supabase proposed for minimal data storage.
- OCR manual correction supported through the backend API.
- Basic administrator operational monitoring and error tracking.

These are planning decisions and do not mean that implementation is complete.

## 8. Definition of Done

A task can be marked complete only when:

- The agreed requirements have been implemented.
- Its deliverable is available in the project repository.
- Dependencies and integration points have been verified.
- Relevant acceptance criteria pass.
- Required automated and manual tests pass.
- Medical safety requirements are preserved.
- No known critical privacy or security issue remains.
- Documentation is updated where necessary.
- The responsible team member has reviewed the work.

A planned task must not be marked completed merely because its code or documentation has been drafted.

## 9. Stage 7 Completion Checklist

- [ ] All MVP requirements have been converted into development tasks.
- [ ] Each task has a priority.
- [ ] Dependencies are identified.
- [ ] Deliverables are defined.
- [ ] Responsibility areas are identified.
- [ ] Individual task assignments are confirmed.
- [ ] Remaining decisions are recorded.
- [ ] Acceptance criteria and Definition of Done are agreed.
- [ ] Stage 7 document is reviewed and approved.
- [ ] Final document is committed and pushed to GitHub.

## 10. Out-of-Scope / Post-MVP Work

Unless the team explicitly changes the scope, the following remain later enhancements:

- Full WhatsApp chatbot integration.
- Nearby laboratories and clinics map.
- Medicine reminders.
- Voice readout.
- Advanced patient report history and trends.
- HIS/EHR integration.
- Advanced doctor dashboards.
- Human medical expert verification as an in-app service.
- Handwritten prescription support.

The MVP's pre-filled WhatsApp sharing link is not the same as a full WhatsApp chatbot.

## 11. Document Status

This task breakdown is a planning draft based on the current project requirements, architecture, API contracts, safety rules and test plan.

All implementation statuses must be verified against the actual repository and running application. Remaining decisions require team confirmation before the affected implementation tasks are finalized.

**Project:** ReportSaathi  
**Stage:** 7 — Task Breakdown  
**Owner:** Person 1 — Product Strategy & Design Lead  
**Technical Coordination:** Person 2 — Systems & DevOps Lead
**Quality Review:** Person 3 — Quality & Engineering Lead
**Status:** Draft — Pending Team Review and Confirmation
