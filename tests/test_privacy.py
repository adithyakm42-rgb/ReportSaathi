"""
ReportSaathi — Privacy, Logging & Ephemeral Lifecycle Test Suite
Author: Person 3 (Quality & Engineering Lead)
Grounded in: docs/06-test-plan.md (TC-25, TC-26), docs/06b-safety-rules.md (Sec 9), docs/07-task-breakdown.md (SAFE-07, SAFE-08, OCR-10, TEST-13)
"""

import unittest
import os
import sys
import tempfile
import time
import logging
import io

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.safety.privacy import (
    sanitize_log_message,
    sanitize_payload_for_logging,
    PrivacyPreservingLogFilter,
    EphemeralStorageManager,
)


class TestPrivacyLogSanitization(unittest.TestCase):
    """TC-25 & SAFE-08: Medical report contents and PHI must never appear in application logs."""

    def test_sanitize_log_message_redacts_lab_values(self):
        """Medical biomarkers with numerical values and units must be redacted."""
        raw_msg = "Processing report for Hemoglobin: 13.5 g/dL and Platelet: 240000 /cumm"
        sanitized = sanitize_log_message(raw_msg)
        self.assertNotIn("13.5", sanitized)
        self.assertNotIn("240000", sanitized)
        self.assertIn("[REDACTED_MEDICAL_DATA]", sanitized)

    def test_sanitize_log_message_redacts_critical_values(self):
        """Red-flag biomarkers such as Potassium 6.8 mmol/L must not be logged in cleartext."""
        raw_msg = "Potassium: 6.8 mmol/L triggered critical alert"
        sanitized = sanitize_log_message(raw_msg)
        self.assertNotIn("6.8 mmol/L", sanitized)
        self.assertIn("[REDACTED_MEDICAL_DATA]", sanitized)

    def test_sanitize_log_message_preserves_operational_metadata(self):
        """Non-sensitive operational identifiers like doc_id and status codes must remain readable."""
        raw_msg = "Document doc-12345678 processed successfully with status 200 in 45ms"
        sanitized = sanitize_log_message(raw_msg)
        self.assertIn("doc-12345678", sanitized)
        self.assertIn("status 200", sanitized)
        self.assertIn("45ms", sanitized)

    def test_privacy_preserving_log_filter(self):
        """The logging filter automatically intercepts and sanitizes standard logger output."""
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.addFilter(PrivacyPreservingLogFilter())

        logger = logging.getLogger("reportsaathi_test_logger")
        logger.setLevel(logging.INFO)
        logger.handlers = [handler]

        logger.info("Extracted Hemoglobin: 8.5 g/dL from specimen")
        output = log_stream.getvalue()

        self.assertNotIn("8.5 g/dL", output)
        self.assertIn("[REDACTED_MEDICAL_DATA]", output)

    def test_sanitize_payload_for_logging(self):
        """Dict payloads containing raw_text, extracted_text, or biomarkers are redacted for logging."""
        payload = {
            "document_id": "doc-abcdef12",
            "language": "hi",
            "reading_level": "simple",
            "raw_text": "CBC Report: Hemoglobin 12.0 g/dL, Platelets 200000 /uL",
            "patient_name": "Test Patient",
            "biomarkers": [
                {"name": "Hemoglobin", "value": 12.0}
            ]
        }
        sanitized = sanitize_payload_for_logging(payload)

        # Operational metadata preserved
        self.assertEqual(sanitized["document_id"], "doc-abcdef12")
        self.assertEqual(sanitized["language"], "hi")
        self.assertEqual(sanitized["reading_level"], "simple")

        # Medical and PHI fields redacted
        self.assertEqual(sanitized["raw_text"], "[REDACTED_MEDICAL_DATA]")
        self.assertEqual(sanitized["patient_name"], "[REDACTED_MEDICAL_DATA]")
        self.assertNotIn("CBC Report", str(sanitized))


class TestEphemeralStorageLifecycle(unittest.TestCase):
    """TC-26, OCR-10 & SAFE-07: Temporary document storage, deletion, and path safety."""

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="rs_test_ephemeral_")
        self.manager = EphemeralStorageManager(base_dir=self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            import shutil
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_save_and_retrieve_ephemeral_file(self):
        """Uploaded document file can be saved in an isolated document session."""
        doc_id = "doc-test-12345678"
        content = b"%PDF-1.4 Mock lab report binary content"
        saved_path = self.manager.save_ephemeral_file(doc_id, "report.pdf", content)

        self.assertTrue(os.path.exists(saved_path))
        with open(saved_path, "rb") as f:
            self.assertEqual(f.read(), content)

    def test_cleanup_document_deletes_files_completely(self):
        """TC-26: cleanup_document permanently wipes the file and directory."""
        doc_id = "doc-cleanup-1234"
        saved_path = self.manager.save_ephemeral_file(doc_id, "blood_test.png", b"image bytes")
        self.assertTrue(os.path.exists(saved_path))

        # Perform cleanup
        result = self.manager.cleanup_document(doc_id)
        self.assertTrue(result)
        self.assertFalse(os.path.exists(saved_path))
        self.assertFalse(os.path.exists(os.path.dirname(saved_path)))

    def test_path_traversal_prevention_on_document_id(self):
        """SAFE-07: Directory traversal attempts via document_id must raise ValueError."""
        malicious_ids = [
            "../../etc/passwd",
            "..\\..\\windows\\system32",
            "doc/subfolder",
            "doc\\subfolder",
            "doc\0nullbyte",
            "short",  # under 8 chars
            "doc with spaces and symbols!@#$",
        ]

        for bad_id in malicious_ids:
            with self.subTest(bad_id=bad_id):
                with self.assertRaises(ValueError):
                    self.manager.get_document_path(bad_id)

    def test_cleanup_expired_documents(self):
        """OCR-10: Files exceeding TTL are purged by cleanup_expired()."""
        doc_id = "doc-expired-1234"
        saved_path = self.manager.save_ephemeral_file(doc_id, "scan.jpg", b"old scan data")
        doc_dir = os.path.dirname(saved_path)

        # Set mtime to 2 hours ago
        past_time = time.time() - 7200
        os.utime(doc_dir, (past_time, past_time))

        # Cleanup documents older than 1 hour (3600s)
        purged = self.manager.cleanup_expired(max_age_seconds=3600)
        self.assertEqual(purged, 1)
        self.assertFalse(os.path.exists(doc_dir))


if __name__ == "__main__":
    unittest.main()
