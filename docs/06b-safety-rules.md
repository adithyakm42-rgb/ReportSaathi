# ReportSaathi – Medical Safety Rules

## 1. Purpose

These rules define how ReportSaathi must handle medical information safely. The application is designed to explain medical documents in simple language, not to diagnose diseases or replace professional medical advice.

## 2. Core Safety Principles

- Explain medical information using simple, understandable language.
- Use only information extracted from the patient's uploaded document and clearly identified reference ranges.
- Never invent medical values, reference ranges, diagnoses, or treatment instructions.
- Clearly communicate uncertainty when document text is unclear or incomplete.
- Encourage users to consult qualified healthcare professionals for medical decisions.

## 3. Diagnosis Restrictions

ReportSaathi must not:

- Diagnose diseases or medical conditions.
- Predict whether a patient has a particular disease.
- Claim that a patient is healthy or disease-free based only on a report.
- Recommend treatment based on extracted laboratory values.

The application may explain what a medical term or test generally means, without concluding what condition the patient has.

## 4. Prescription Safety

ReportSaathi may explain existing prescription instructions in simpler language.

It must never:

- Change medicine names or dosages.
- Recommend increasing or decreasing a dose.
- Change medication frequency or duration.
- Tell users to stop or start medication.
- Recommend replacing prescribed medicines with alternatives.

If prescription text is unclear, the application must ask the user to confirm the instructions with a doctor or pharmacist.

## 5. Laboratory Result Safety

- Compare laboratory values only with reference ranges printed on the uploaded report.
- Preserve the original value, unit, and reference range.
- Do not create or assume missing reference ranges.
- Clearly identify values marked high or low by the report.
- Explain that reference ranges can vary between laboratories and individuals.
- Do not interpret an abnormal value as a confirmed disease.

If a value or range cannot be extracted reliably, display it as unclear and request manual verification.

## 6. OCR and Document Validation

Before explaining a report:

1. Check whether the uploaded file is readable.
2. Extract text using OCR.
3. Identify missing, unclear, or incorrectly recognized values.
4. Preserve units and reference ranges.
5. Ask the user to verify uncertain information.
6. Do not generate an explanation from unreliable extracted text.

## 7. Emergency and Red-Flag Handling

The application must use predefined safety rules to identify potentially urgent warning signs.

- Show a clear emergency warning when a predefined red-flag condition is detected.
- Advise the user to contact local emergency services or seek immediate medical care when appropriate.
- Do not delay emergency guidance while waiting for an AI-generated explanation.
- Do not use reassuring language when an urgent warning is present.

Red-flag rules must be reviewed by qualified medical professionals before production use.

## 8. AI Response Validation

Before displaying an AI-generated explanation:

- Check that it does not contain a diagnosis.
- Check that it does not modify prescription instructions.
- Check that it does not invent laboratory values or reference ranges.
- Check that it does not contradict detected safety warnings.
- Use clear language and avoid unsupported medical claims.

If validation fails, do not display the unsafe response. Show a safe fallback message instead.

## 9. Privacy and Data Protection

- Collect only information necessary for the requested functionality.
- Do not expose medical documents or extracted text in public logs.
- Never store API keys or passwords in frontend code or GitHub.
- Restrict access to patient information.
- Use secure communication between frontend and backend.
- Obtain appropriate user consent before processing medical documents.
- Do not send medical report contents to analytics services.

## 10. User Disclaimer

ReportSaathi should display a disclaimer such as:

"ReportSaathi provides educational explanations of medical documents. It does not provide medical diagnosis or treatment advice and is not a substitute for consultation with a qualified healthcare professional. Always consult your doctor before making medical decisions."

## 11. Safe Fallback Messages

**Unclear document:**

"We could not read some information clearly. Please upload a clearer image or verify the extracted values manually."

**Unclear prescription:**

"We could not confidently understand this prescription instruction. Please confirm it with your doctor or pharmacist."

**Medical diagnosis request:**

"ReportSaathi cannot diagnose medical conditions. Please discuss your symptoms and report with a qualified healthcare professional."

**Potential emergency:**

"Your information may indicate a potentially urgent health concern. Please seek immediate medical attention or contact your local emergency service."

## 12. Testing Requirements

The team should test the following cases:

- Blurry or incomplete medical reports.
- Missing laboratory reference ranges.
- Incorrect OCR extraction.
- Requests for disease diagnosis.
- Requests to change medicine dosage.
- Requests to stop prescribed medication.
- Potential emergency warning conditions.
- Attempts to expose patient information.

## 13. Implementation Status

This document defines the proposed safety requirements for ReportSaathi. These rules must be implemented and tested before the application is used with real patient information. Medical red-flag rules and safety behavior require review by qualified healthcare professionals.

---

**Document:** ReportSaathi Medical Safety Rules  
**Status:** Proposed requirements  
**Owner:** Systems & DevOps Lead