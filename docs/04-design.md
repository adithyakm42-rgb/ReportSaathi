# Stage 4 – UI/UX Design

## 1. Project Overview

**Project:** ReportSaathi  
**Stage:** 4 – Design  
**Owner:** Person 1 – Product Strategy & Design Lead

ReportSaathi helps users understand medical reports and prescription information in simple language. It does not replace professional medical advice.

## 2. Design Reference

**Google Stitch Project:**

https://stitch.google.com/projects/7501070406470619204

The project contains seven main screen designs for the MVP.

## 3. Screen Designs

### Screen 1 – Language and Reading Level
- Select English, Hindi or Kannada.
- Choose Simple, Standard or Detailed reading level.

### Screen 2 – Upload Medical Report
- Take a photo or upload a JPG, PNG or PDF.
- Maximum file size: 10 MB.
- Include photo tips, loading and error states.

### Screen 3 – Check Extracted Values
- Display extracted test names, values, units and printed reference ranges.
- Allow users to correct values or enter missing information.
- Include loading, empty and error states.

### Screen 4 – Report Explanation
- Display individual result explanation cards.
- Use Normal, Borderline and Needs Attention labels.
- Include medicine explanations based on the written prescription.
- Include loading and error states.

### Screen 5 – Red-Flag Alerts
- Display high-contrast alerts when predefined critical thresholds are breached.
- Provide doctor contact and nearby hospital actions.
- Include a no-alert state and deterministic backend fallback.

### Screen 6 – Doctor Questions
- Display 3–6 questions for discussion with a doctor.
- Allow selection and copying of questions.
- Include WhatsApp sharing and an empty state.

### Screen 7 – Share / Save Summary
- Preview the report summary.
- Provide PDF download and WhatsApp sharing.
- Include success and error states.

## 4. Visual Design Guidelines
- Mobile-first design for low-cost Android devices.
- Minimum body text size: 16px.
- Dark-blue and white theme with teal accents.
- Large, touch-friendly buttons.
- Readable typography and generous spacing.
- One primary action per screen.
- Status must use both colour and written labels.

## 5. Status Indicators
- Green – Normal.
- Amber – Borderline.
- Red – Needs Attention.

Classifications must use the reference ranges printed on the user's report and must not imply a diagnosis.

## 6. Screen State Requirements

| Screen | Required states |
|---|---|
| Language selection | Default |
| Upload report | Default, Loading, Error |
| Check values | Default, Loading, Empty, Error |
| Report explanation | Default, Loading, Error |
| Red-flag alerts | Alert, No-alert, Fallback |
| Doctor questions | Default, Empty |
| Share/save summary | Default, Success, Error |

## 7. Safety Requirements

Display this disclaimer on every screen:

"This explains your report. It does not replace your doctor."

- No diagnosis or treatment recommendations.
- No medicine dose modification.
- No recommendation to stop prescribed medicines.
- Do not invent medical reference ranges.
- Red-flag detection must use deterministic backend rules, independent of AI.
- Doctor review of anonymized sample explanations is required before production release.

## 8. MVP Sharing Options
- WhatsApp sharing through a link.
- PDF summary download.
- Phone call link.
- Google Maps search link.

Advanced integrations such as bots, medicine reminders, report history and ABHA/ABDM integration are outside the current MVP scope.

## 9. Design Deliverables
- Seven main screen designs in Google Stitch.
- UI design guidelines.
- Screen state matrix.
- Accessibility and medical safety requirements.

## 10. Stage 4 Status

The seven main screen designs have been generated in Google Stitch. This document records their intended functionality, visual guidelines, screen states and safety requirements.

Final team review is required before implementation.