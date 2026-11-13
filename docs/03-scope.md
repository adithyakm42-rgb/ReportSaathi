# ReportSaathi — Project Scope

**Stage:** 3 — Scope Definition  
**Owner:** Person 1 — Product Strategy & Design Lead
**Status:** Draft — Pending Final Team Review and Confirmation

## 1. Project Objective

ReportSaathi helps patients and caregivers understand medical laboratory reports, prescriptions and other medical documents through simple, understandable and multilingual explanations.

The application provides educational information only. It does not diagnose medical conditions, prescribe treatment or replace professional medical advice.

## 2. Core User Journey

1. Access the application without mandatory patient registration or login.
2. Choose a preferred explanation language: English, Hindi or Kannada.
3. Select a reading level: Simple, Standard or Detailed.
4. Upload a medical report as a PDF, JPG, JPEG or PNG file.
5. Ensure the uploaded file does not exceed 10 MB.
6. Extract report information using OCR.
7. Allow the user to review and manually correct extracted information.
8. Explain medical terms and report values in the selected language and reading level.
9. Display laboratory value status using only reference ranges printed on the report.
10. Show relevant deterministic red-flag alerts.
11. Generate 3–6 questions that users can ask their doctor.
12. Allow users to save or share explanations and download them as PDF.
13. Provide WhatsApp sharing through a pre-filled sharing link, subject to user confirmation.
14. Allow users to optionally submit feedback.

## 3. Feature Prioritization

### MVP — Must Have

- Medical document upload supporting PDF, JPG, JPEG and PNG formats.
- Maximum upload size of 10 MB.
- OCR-based text extraction.
- Manual correction of extracted information.
- Explanation of medical terms in understandable language.
- Three explanation reading levels: Simple, Standard and Detailed.
- Three language options: English, Hindi and Kannada.
- Value comparison using reference ranges printed on the report.
- Clear handling when reference ranges are unavailable.
- Deterministic backend red-flag alerts.
- Prescription instruction clarification without medication changes.
- Generation of 3–6 suggested questions for doctor consultations.
- Appropriate medical safety disclaimer.
- Save and share explanations.
- PDF download.
- WhatsApp sharing through a pre-filled sharing link.
- Optional user feedback.
- Basic administrator dashboard for operational monitoring and error tracking.
- Secure temporary document processing and automatic deletion according to the approved retention policy.

### 3.1 Data and Storage Approach

- Supabase is proposed for minimal data storage, subject to final team confirmation.
- Mandatory patient registration and login are not required for the MVP.
- Permanent report history is excluded from the MVP.
- Uploaded reports and extracted medical information should be processed temporarily.
- Automatic deletion must follow an approved retention and deletion policy.
- The exact retention duration and backup deletion policy remain pending team confirmation.

### Later — Future Enhancements

- WhatsApp chatbot integration.
- Nearby laboratories and clinics map integration.
- Medicine reminders.
- Medical report history and trends.
- Voice-based explanation.
- Advanced doctor and clinic dashboards.
- Direct hospital information system integration.
- Electronic health record synchronization.
- Advanced analytics and reporting.
- Support for handwritten prescriptions.

### Never — Excluded Features

- Medical diagnosis or disease prediction.
- Starting, stopping or changing medication doses.
- Recommending medication changes or treatment plans.
- Inventing missing laboratory reference ranges.
- Replacing qualified medical professionals.
- Online medical consultations or automated treatment decisions.

## 4. Medical Safety Requirements

1. Red-flag checks must be implemented using deterministic backend Python logic.
2. Red-flag checks must execute before the LLM generates explanations.
3. AI must never diagnose medical conditions.
4. AI must never recommend starting, stopping or changing medication doses, frequency or duration.
5. Value status must be based only on reference ranges printed on the uploaded report.
6. Missing reference ranges must never be invented.
7. Red-flag alerts must remain visible even if the AI service fails.
8. Every explanation must include an appropriate medical disclaimer.
9. Unclear OCR results must be presented for user verification rather than treated as confirmed medical information.
10. Red-flag rules and test fixtures must receive qualified medical professional review and approval before production release.

## 5. Scope Boundaries

This stage defines what the ReportSaathi MVP will include, what can be developed later and what must never be included.

Detailed technical architecture, infrastructure configuration, API implementation and production deployment are documented in their respective project stages.

The MVP prioritizes patient understanding, medical safety, privacy and simplicity.

## 6. Completion Criteria

- Core user journey documented.
- MVP features identified and aligned with current team recommendations.
- Supported languages and reading levels specified.
- Upload formats and 10 MB size limit documented.
- Save/share, PDF download and WhatsApp sharing included in the scope.
- Later enhancements identified.
- Excluded features documented.
- Medical safety requirements documented.
- Data storage and retention considerations documented.
- Scope reviewed against the PRD, API contracts, test plan and master ReportSaathi workflow.
- Final team review and approval obtained.

---

**Document maintained by:** Person 1 — Product Strategy & Design Lead
**Technical coordination:** Person 2 — Systems & DevOps Lead
**Quality review:** Person 3 — Quality & Engineering Lead