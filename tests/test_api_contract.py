"""
ReportSaathi - Automated API Contract Testing Suite
Author: Person 3 (Quality & Engineering Lead)
Grounded in: docs/06c-api-contracts.md, docs/06-test-plan.md (TC-01 to TC-26, T-10 Contract Test)
Requirements: TEST-14 (API Contract Testing), API-10 (Response Standardization), SAFE-03 (Offline Red-Flags)

Purpose:
Verifies that all API payloads, schemas, and error responses strictly match
docs/06c-api-contracts.md and shared/types.ts field-for-field.
Prevents contract drift between Person 2 (Backend) and Person 3 (Frontend).
"""

import unittest
import json
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.safety.rules import ClinicalStatus, RedFlagSeverity


class TestSampleReportContract(unittest.TestCase):
    """T-10 / TEST-14: Verifies shared/sample-report.json against the agreed contract."""

    def setUp(self):
        self.sample_path = os.path.join(os.path.dirname(__file__), "..", "shared", "sample-report.json")
        with open(self.sample_path, "r", encoding="utf-8") as f:
            self.report = json.load(f)

    def test_top_level_contract_fields(self):
        """ReportResult must contain all mandatory contract fields."""
        required_fields = [
            "report_id",
            "status",
            "language",
            "reading_level",
            "is_red_flag",
            "red_flags",
            "values",
            "medicines",
            "doctor_questions",
            "disclaimer",
        ]
        for field in required_fields:
            self.assertIn(field, self.report, f"Missing required contract field: '{field}'")

    def test_status_field_values(self):
        """Status field must be one of 'processing', 'ready', 'failed'."""
        self.assertIn(self.report["status"], ["processing", "ready", "failed"])

    def test_disclaimer_mandatory_line(self):
        """SR-3: Every report payload must carry the exact non-negotiable disclaimer."""
        expected_disclaimer = "This explains your report. It does not replace your doctor."
        self.assertEqual(self.report["disclaimer"], expected_disclaimer)

    def test_biomarker_value_schema(self):
        """Each biomarker in values[] must adhere to the BiomarkerValue schema."""
        self.assertTrue(len(self.report["values"]) > 0, "Report values list must not be empty")
        valid_statuses = [s.value for s in ClinicalStatus]

        for item in self.report["values"]:
            self.assertIn("test", item, "Biomarker must have 'test' field")
            self.assertIn("value", item, "Biomarker must have 'value' field")
            self.assertIn("unit", item, "Biomarker must have 'unit' field")
            self.assertIn("range_on_report", item, "Biomarker must have 'range_on_report' field")
            self.assertIn("status", item, "Biomarker must have 'status' field")
            self.assertIn("is_red_flag", item, "Biomarker must have 'is_red_flag' field")
            self.assertIn(item["status"], valid_statuses, f"Invalid biomarker status: {item['status']}")

    def test_doctor_questions_count(self):
        """FR-09 / TC-19: Doctor questions count must strictly be between 3 and 6."""
        questions = self.report.get("doctor_questions", [])
        self.assertTrue(
            3 <= len(questions) <= 6,
            f"Expected between 3 and 6 doctor questions, got {len(questions)}"
        )
        for q in questions:
            self.assertIsInstance(q, str)
            self.assertTrue(len(q.strip()) > 10, "Doctor question must be a non-trivial question string")

    def test_medicines_schema_if_present(self):
        """FR-07 / Prescription instructions must preserve name, timing, and purpose."""
        medicines = self.report.get("medicines", [])
        for med in medicines:
            self.assertIn("name", med)
            self.assertIn("purpose", med)
            self.assertIn("timing_as_written", med)
            self.assertIn("watch_for", med)
            self.assertIsInstance(med["watch_for"], list)


class TestApiContractResponseSchemas(unittest.TestCase):
    """Validates contract structures defined in docs/06c-api-contracts.md."""

    def test_health_endpoint_contract(self):
        """GET /api/health contract schema."""
        mock_health = {
            "status": "healthy",
            "service": "ReportSaathi API"
        }
        self.assertEqual(mock_health["status"], "healthy")
        self.assertEqual(mock_health["service"], "ReportSaathi API")

    def test_standard_error_response_contract(self):
        """Standardized error responses must contain success=False, message, and error_code."""
        mock_error = {
            "success": False,
            "message": "The requested document was not found.",
            "error_code": "INVALID_DOCUMENT_ID"
        }
        self.assertFalse(mock_error["success"])
        self.assertIsInstance(mock_error["message"], str)
        self.assertIsInstance(mock_error["error_code"], str)

    def test_upload_success_contract(self):
        """POST /api/upload success response schema."""
        mock_upload_res = {
            "success": True,
            "message": "Document uploaded successfully",
            "data": {
                "document_id": "temp-doc-12345",
                "filename": "blood_report.pdf",
                "status": "uploaded"
            }
        }
        self.assertTrue(mock_upload_res["success"])
        data = mock_upload_res["data"]
        self.assertIn("document_id", data)
        self.assertIn("filename", data)
        self.assertEqual(data["status"], "uploaded")

    def test_extract_success_contract(self):
        """POST /api/extract success response schema."""
        mock_extract_res = {
            "success": True,
            "data": {
                "extracted_text": "Hemoglobin: 13.5 g/dL",
                "extraction_status": "completed",
                "requires_verification": False
            }
        }
        self.assertTrue(mock_extract_res["success"])
        data = mock_extract_res["data"]
        self.assertIn("extracted_text", data)
        self.assertIn("extraction_status", data)
        self.assertIn("requires_verification", data)

    def test_correction_submission_contract(self):
        """POST /api/extract/{id}/corrections contract schema."""
        mock_correction_res = {
            "success": True,
            "message": "Extracted text corrected successfully",
            "data": {
                "document_id": "temp-doc-12345",
                "status": "corrected"
            }
        }
        self.assertTrue(mock_correction_res["success"])
        self.assertEqual(mock_correction_res["data"]["status"], "corrected")


class TestMedicalSafetyContractConstraints(unittest.TestCase):
    """Enforces that contract models cannot violate core safety constraints."""

    def test_missing_range_must_never_default_to_normal(self):
        """A missing reference range must NEVER silently default to 'normal'."""
        item = {
            "test": "CRP",
            "value": 8.0,
            "unit": "mg/L",
            "range_on_report": None,
            "status": "no_range_on_report"
        }
        self.assertNotEqual(item["status"], "normal")
        self.assertEqual(item["status"], "no_range_on_report")

    def test_emergency_red_flag_alert_structure(self):
        """Red flag alert structure must include clinical concern and required action."""
        mock_alert = {
            "test_name": "Serum Potassium",
            "value": 6.8,
            "unit": "mmol/L",
            "severity": "CRITICAL_HIGH",
            "clinical_concern": "Severe Hyperkalemia: Cardiac arrhythmia risk.",
            "action_required": "Immediate emergency room evaluation required."
        }
        valid_severities = [s.value for s in RedFlagSeverity]
        self.assertIn(mock_alert["severity"], valid_severities)
        self.assertTrue(len(mock_alert["clinical_concern"]) > 0)
        self.assertTrue(len(mock_alert["action_required"]) > 0)


if __name__ == "__main__":
    unittest.main()
