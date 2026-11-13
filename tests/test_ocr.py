"""
OCR Text Extraction & Biomarker Parser Test Suite
Author: Person 3 (Quality & Engineering Lead)
Grounded in: docs/06-test-plan.md (TC-08, TC-09, TC-10), docs/06b-safety-rules.md, docs/06c-api-contracts.md
Requirements: OCR-06, OCR-07, OCR-08, OCR-09, SAFE-05
"""

import unittest
import sys
import os
import json

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.integrations.ocr import (
    parse_biomarkers_from_text,
    assess_text_clarity,
    apply_user_corrections,
)
from backend.safety.rules import ClinicalStatus, check_red_flags


class TestBiomarkerTextParser(unittest.TestCase):
    """TC-08 & OCR-08: Parsing structured biomarkers, units, and printed reference ranges."""

    def setUp(self):
        self.fixtures_dir = os.path.join(os.path.dirname(__file__), "fixtures")

    def test_parse_normal_cbc_fixture(self):
        """TC-08: Parse standard CBC text and extract values with units and printed ranges."""
        with open(os.path.join(self.fixtures_dir, "01-normal-report.json"), "r") as f:
            fixture = json.load(f)

        raw_text = fixture["raw_text"]
        extracted = parse_biomarkers_from_text(raw_text)

        self.assertTrue(len(extracted) >= 4, f"Expected at least 4 tests, got {len(extracted)}")

        # Check Hemoglobin
        hb = next((x for x in extracted if "hemoglobin" in x.test_name.lower()), None)
        self.assertIsNotNone(hb, "Hemoglobin not found in extracted biomarkers")
        self.assertEqual(hb.value, 13.5)
        self.assertEqual(hb.unit, "g/dL")
        self.assertEqual(hb.range_low, 12.0)
        self.assertEqual(hb.range_high, 15.5)
        self.assertEqual(hb.status, ClinicalStatus.NORMAL)

        # Check Platelets
        plt = next((x for x in extracted if "platelet" in x.test_name.lower()), None)
        self.assertIsNotNone(plt, "Platelets not found in extracted biomarkers")
        self.assertEqual(plt.value, 240000)
        self.assertEqual(plt.range_low, 150000)
        self.assertEqual(plt.range_high, 450000)
        self.assertEqual(plt.status, ClinicalStatus.NORMAL)

    def test_parse_report_with_missing_ranges(self):
        """TC-13 / OCR-08: When a row has no printed reference range, status must be no_range_on_report."""
        with open(os.path.join(self.fixtures_dir, "04-missing-ranges.json"), "r") as f:
            fixture = json.load(f)

        raw_text = fixture["raw_text"]
        extracted = parse_biomarkers_from_text(raw_text)

        # ESR has printed range
        esr = next((x for x in extracted if "esr" in x.test_name.lower() or "erythrocyte" in x.test_name.lower()), None)
        self.assertIsNotNone(esr)
        self.assertEqual(esr.value, 28.0)
        self.assertEqual(esr.status, ClinicalStatus.NEEDS_ATTENTION)

        # CRP has NO printed range
        crp = next((x for x in extracted if "c-reactive" in x.test_name.lower() or "crp" in x.test_name.lower()), None)
        self.assertIsNotNone(crp)
        self.assertEqual(crp.value, 7.4)
        self.assertIsNone(crp.range_on_report)
        self.assertEqual(crp.status, ClinicalStatus.NO_RANGE_ON_REPORT)


class TestTextClarityAndUncertaintyDetection(unittest.TestCase):
    """TC-09 & OCR-07: Unclear text triggers manual verification requirement."""

    def test_blurry_noisy_text_triggers_verification(self):
        """Noisy text with artifacts must return requires_verification=True."""
        noisy_text = "C11N1CAL L4B... Hb / H3m0gl0b1n: 1?.2 ?? W.B.C.: 7,??? Pl4te1et: [UNREADABLE]"
        clarity = assess_text_clarity(noisy_text)
        self.assertTrue(clarity["requires_verification"])
        self.assertEqual(clarity["extraction_status"], "unclear")
        self.assertIn("verify", clarity["fallback_message"].lower())

    def test_clean_text_passes_verification(self):
        """Clean medical text does not require forced manual verification."""
        clean_text = (
            "Hemoglobin: 13.5 g/dL (Ref Range: 12.0 - 15.5)\n"
            "Total WBC Count: 6800 /cumm (Ref Range: 4000 - 11000)\n"
            "Platelet Count: 240000 /cumm (Ref Range: 150000 - 450000)"
        )
        clarity = assess_text_clarity(clean_text)
        self.assertFalse(clarity["requires_verification"])
        self.assertEqual(clarity["extraction_status"], "completed")


class TestManualCorrectionAndRevalidation(unittest.TestCase):
    """TC-10 / OCR-09: User can correct misread values and the backend revalidates them."""

    def test_correction_revalidates_and_clears_red_flag(self):
        """
        Scenario:
        OCR misreads Potassium as 6.8 (triggering red flag).
        User inspects report and corrects Potassium to 4.2.
        Backend revalidates: status becomes normal and red flag is cleared.
        """
        with open(os.path.join(os.path.dirname(__file__), "fixtures", "10-red-flag-case.json"), "r") as f:
            fixture = json.load(f)

        raw_text = fixture["raw_text"]
        extracted = parse_biomarkers_from_text(raw_text)

        # Before correction: red flag exists
        initial_flags = check_red_flags(extracted)
        self.assertTrue(len(initial_flags) > 0)

        # User submits corrections
        corrections = [
            {
                "test_name": "Serum Potassium",
                "corrected_value": 4.2
            },
            {
                "test_name": "Platelet Count",
                "corrected_value": 250000
            }
        ]

        updated = apply_user_corrections(extracted, corrections)

        # Find corrected Potassium
        potassium = next(x for x in updated if "potassium" in x.test_name.lower())
        self.assertEqual(potassium.value, 4.2)
        self.assertEqual(potassium.status, ClinicalStatus.NORMAL)
        self.assertFalse(potassium.is_red_flag)

        # Find corrected Platelets
        plt = next(x for x in updated if "platelet" in x.test_name.lower())
        self.assertEqual(plt.value, 250000)
        self.assertEqual(plt.status, ClinicalStatus.NORMAL)

        # Re-check red flags: all cleared!
        updated_flags = check_red_flags(updated)
        self.assertEqual(len(updated_flags), 0)


if __name__ == "__main__":
    unittest.main()
