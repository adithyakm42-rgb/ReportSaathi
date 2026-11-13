
# ReportSaathi – Product Requirements Document (PRD)

**Project Name:** ReportSaathi  
**Document:** Product Requirements Document  
**Version:** 1.0  
**Status:** Draft

---

## 1. Product Overview

ReportSaathi is an AI-assisted healthcare application designed to help patients and caregivers understand medical reports, laboratory results, prescriptions, and discharge summaries in simple and understandable language.

The application uses Optical Character Recognition (OCR) to extract information from uploaded medical documents and Artificial Intelligence (AI) to generate easy-to-understand explanations.

The system aims to reduce confusion caused by complex medical terminology and help users become better informed before consulting healthcare professionals.

## 2. Problem Statement

Many patients find it difficult to understand their medical reports because they contain technical terminology, unfamiliar abbreviations, laboratory values, and medical instructions.

Existing healthcare applications may provide access to reports and appointments, but patients can still struggle to understand the information in their documents.

The major problems include:

- Difficulty understanding medical terminology.
- Confusion about laboratory results and reference ranges.
- Difficulty understanding prescription instructions.
- Language and accessibility barriers.
- Lack of guidance when preparing questions for doctors.
- Concerns about medical information privacy and reliability.

ReportSaathi aims to address these problems through simple explanations, multilingual support, and safety-focused AI assistance.

## 3. Product Goals

The primary goals of ReportSaathi are:

1. Help users understand medical documents in simple language.
2. Extract text and relevant information from uploaded documents using OCR.
3. Explain laboratory results using reference ranges available in the original report.
4. Clarify existing prescription instructions without modifying them.
5. Support explanations in multiple languages.
6. Generate useful questions that users can discuss with healthcare professionals.
7. Identify predefined medical warning signs and encourage appropriate professional attention.
8. Protect users' sensitive medical information.

---

## 4. Target Users

ReportSaathi is designed for the following user groups:

### 4.1 Patients
- People who receive medical reports and need help understanding them.
- Users who want simple explanations of laboratory results.
- People who need help understanding existing prescription instructions.

### 4.2 Family Members and Caregivers
- People who help family members understand medical documents.
- Caregivers who manage medical reports for elderly people.
- Users who need explanations in their preferred language.

### 4.3 Healthcare Professionals
- Doctors and clinic staff who may use the platform to understand common patient difficulties.
- Healthcare professionals who may review patient-prepared questions and feedback.

## 5. User Roles

The MVP will support patient/customer access without requiring mandatory registration or login. Administrator access must be restricted through appropriate authentication and authorization.

### 5.1 Customer / Patient

- Access the application without mandatory registration or login.
- Upload supported medical documents.
- View text extracted from uploaded documents.
- Correct OCR-extracted text when necessary.
- Select a preferred explanation language: English, Hindi or Kannada.
- Select a reading level: Simple, Standard or Detailed.
- Receive simplified medical explanations.
- View laboratory values alongside only the reference ranges printed in the uploaded report.
- Receive clarification of existing prescription instructions without changing medication names, dosages, frequency or duration.
- Generate 3–6 questions to discuss with healthcare professionals.
- Save or share explanations using the available application features.
- Download explanations as PDF.
- Share explanations through a pre-filled WhatsApp sharing link, subject to user confirmation.
- Submit optional feedback about application performance or explanation quality.

Report history and mandatory patient accounts are excluded from the initial MVP.

### 5.2 Administrator

- Access the administrator dashboard through authorized credentials.
- Monitor application health and system errors.
- Monitor OCR and AI service availability and performance.
- Review optional user feedback and reported application issues.
- Monitor operational and safety-related incidents.
- Manage application-level settings and supported languages, where permitted.

**Privacy restriction:** Administrators must not routinely access uploaded medical documents or extracted medical information. Any exceptional access must be explicitly authorized, justified and governed by the approved privacy policy.

---

## 6. Functional Requirements

Functional requirements describe the features that the application must provide.

### FR-01: Patient Access

The system should allow users to access the core MVP features without mandatory registration or login. Administrator functions must require appropriate authentication and authorization.

### FR-02: Medical Document Upload

The system should allow users to upload PDF, JPG, JPEG and PNG medical documents.

- Maximum upload size: 10 MB.
- Empty files and unsupported formats must be rejected.
- Uploaded documents must be processed securely.

### FR-03: OCR Text Extraction

The system should extract readable text from uploaded documents using OCR technology and identify cases where extracted information requires user verification.

### FR-04: Manual OCR Correction

The system should allow users to correct OCR-extracted text before requesting an explanation. The backend must use the verified or corrected text associated with the uploaded document.

### FR-05: Medical Report Explanation

The system should convert complex medical terminology into understandable language while preserving the meaning of the original medical information.

Users should be able to select one of three reading levels:

- Simple
- Standard
- Detailed

### FR-06: Laboratory Result Explanation

The system should explain laboratory values using only the reference ranges printed in the uploaded report. It must not invent or assume missing reference ranges.

### FR-07: Prescription Clarification

The system should explain existing prescription instructions without changing medication names, dosages, frequency or duration. It must not recommend starting, stopping or modifying medication.

### FR-08: Multilingual Support

The system should provide explanations in the following MVP languages:

- English
- Hindi
- Kannada

Translations must preserve medical meaning and important medical terminology.

### FR-09: Doctor Question Generation

The system should generate between 3 and 6 relevant questions that users can discuss with their healthcare professionals. Questions must not encourage self-diagnosis or self-treatment.

### FR-10: Safety Warning Detection

The backend should check predefined medical warning conditions before sending relevant information to the AI service. Red-flag rules must receive qualified medical professional review and approval before production release.

### FR-11: Save and Share Explanations

The system should allow users to save or share generated explanations using the supported application features. Sharing must require user action and must not expose medical information without the user's consent.

### FR-12: PDF Download

The system should allow users to download generated explanations in PDF format.

### FR-13: WhatsApp Sharing

The system should provide a pre-filled WhatsApp sharing link. The user must review and confirm the content before sharing.

### FR-14: Optional User Feedback

The system should allow users to optionally submit feedback about incorrect explanations, OCR problems or other application issues. Feedback collection must avoid unnecessary medical information.

### FR-15: Administrator Monitoring

The system should provide a basic administrator dashboard for monitoring application health, service availability, system errors and reported operational issues. Medical report contents must not be exposed through routine monitoring.

### FR-16: Error Handling

The system should display understandable error messages when document uploads, OCR processing, translation or AI services fail. Sensitive technical details must not be exposed to users.

---

## 8. Minimum Viable Product (MVP)

The first version of ReportSaathi will focus on the following features:

1. Patient access without mandatory registration or login.
2. Medical document upload supporting PDF, JPG, JPEG and PNG formats, with a maximum size of 10 MB.
3. OCR-based text extraction.
4. Manual correction of extracted OCR text.
5. AI-assisted medical report explanation.
6. Three reading levels: Simple, Standard and Detailed.
7. Laboratory result explanation using reference ranges printed in the uploaded report.
8. Prescription instruction clarification without medication changes.
9. Multilingual explanations in English, Hindi and Kannada.
10. Generation of 3–6 doctor discussion questions.
11. Backend medical safety and predefined red-flag checks.
12. Save and share explanations.
13. PDF download.
14. WhatsApp sharing through a pre-filled sharing link.
15. Optional user feedback.
16. Basic administrator monitoring and error tracking.
17. Secure temporary document processing and automatic deletion according to the approved retention policy.

**MVP data and privacy approach:**

- Supabase is proposed for minimal data storage, subject to final team confirmation.
- Report history is excluded from the MVP.
- Mandatory patient registration and login are excluded.
- Temporary report files and extracted medical information must follow an approved retention and deletion policy.
- The exact retention duration and backup deletion policy remain pending team confirmation.

### 8.1 Features Outside the Initial MVP

The following features may be considered for future versions:

- Direct integration with hospital information systems.
- Electronic health record synchronization.
- Advanced doctor and clinic dashboards.
- Permanent patient report history.
- Mandatory patient account management.
- Human medical expert verification as an in-app feature.
- Advanced analytics and reporting.
- Support for handwritten prescriptions.
- Voice-based interaction and advanced chatbot capabilities.
- Advanced hospital and clinic integrations.

## 9. Success Metrics

The success of ReportSaathi will be evaluated using the following proposed targets:

| Metric | Target |
|---|---:|
| User comprehension improvement | Above 80% |
| Printed report OCR accuracy | Above 95% |
| Diagnostic attempts by AI | 0 |
| Prescription dosage modifications | 0 |
| User NPS | Above 50 |
| Doctors finding generated questions helpful | Above 70% |

These are project targets, not currently verified results. They must be evaluated through testing and user feedback.

## 10. Assumptions and Dependencies

### Assumptions
- Users can upload readable medical documents.
- Users have access to an internet connection.
- Uploaded documents contain sufficient information for explanation.
- Users understand that ReportSaathi is an educational assistance tool, not a replacement for doctors.

### Dependencies
- OCR technology for text extraction.
- AI API for generating simplified explanations.
- Backend framework for processing requests.
- Frontend framework for the user interface.
- Secure hosting and deployment services.
- Supported language translation capabilities.

## 11. Risks and Mitigation

| Risk | Mitigation |
|---|---|
| Incorrect OCR extraction | Validate extracted text and allow users to review it |
| AI-generated misinformation | Use restricted prompts, validation and safety checks |
| Incorrect laboratory interpretation | Use only reference ranges printed in the original report |
| Medical safety issues | Apply deterministic backend warning checks before AI processing |
| Privacy violations | Use secure transmission, access controls and data minimization |
| AI service failure | Provide error handling and retry mechanisms |
| Language translation errors | Preserve medical terminology and validate translations |

## 12. Medical Safety Limitations

ReportSaathi is an educational healthcare assistance application.

The system must never:

- Diagnose diseases or medical conditions.
- Prescribe new medicines.
- Change medication dosages or schedules.
- Recommend stopping prescribed medicines.
- Invent laboratory reference ranges.
- Replace professional medical consultation.
- Provide false reassurance when urgent medical attention may be required.

All medical explanations must clearly communicate their limitations and encourage users to consult qualified healthcare professionals.

## 13. Future Enhancements

Potential future improvements include:

- Additional Indian language support.
- Integration with diagnostic laboratories.
- Improved OCR for complex document layouts.
- Secure sharing of explanations with healthcare professionals.
- Accessibility improvements for elderly and visually impaired users.
- Additional document formats and structured health data support.

## 14. Conclusion

ReportSaathi aims to make medical information easier to understand through OCR, AI-assisted explanations and multilingual support.

The initial MVP will prioritize usability, privacy, reliability and medical safety while avoiding diagnosis and treatment recommendations.

The product will evolve through technical testing, user feedback and healthcare professional input.
