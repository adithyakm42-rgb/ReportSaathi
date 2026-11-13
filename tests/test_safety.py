"""
Medical Safety & Deterministic Classification Test Suite
Author: Person 3 (Quality & Engineering Lead)
Grounded in: docs/06b-safety-rules.md, docs/06c-api-contracts.md, docs/06-test-plan.md
Requirements: SAFE-01, SAFE-02, SAFE-03, SAFE-04, SAFE-05, SAFE-06
Test Cases: TC-12 (Range comparison), TC-13 (Missing range), TC-14 (Red flags), TC-16 (Offline red-flag), TC-17 (Banned phrases)
"""

import unittest
import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.safety.rules import (
    evaluate_biomarker,
    check_red_flags,
    BiomarkerValue,
    ClinicalStatus,
    RedFlagSeverity,
)
from backend.safety.banned_phrases import (
    scan_for_prohibited_content,
    sanitize_ai_output,
    SAFETY_FALLBACK_MESSAGES,
)


class TestDeterministicBiomarkerClassification(unittest.TestCase):
    """TC-12 & TC-13: Range comparison and missing range handling."""

    def test_normal_value_within_printed_range(self):
        """Value inside printed range must strictly classify as 'normal'."""
        item = BiomarkerValue(
            test_name="Hemoglobin",
            value=13.5,
            unit="g/dL",
            range_low=12.0,
            range_high=15.5,
            range_on_report="12.0 - 15.5",
        )
        result = evaluate_biomarker(item)
        self.assertEqual(result.status, ClinicalStatus.NORMAL)
        self.assertFalse(result.is_red_flag)

    def test_low_value_below_printed_range(self):
        """Value below printed range must classify as 'needs_attention'."""
        item = BiomarkerValue(
            test_name="Hemoglobin",
            value=9.8,
            unit="g/dL",
            range_low=12.0,
            range_high=15.5,
            range_on_report="12.0 - 15.5",
        )
        result = evaluate_biomarker(item)
        self.assertEqual(result.status, ClinicalStatus.NEEDS_ATTENTION)
        self.assertFalse(result.is_red_flag)

    def test_high_value_above_printed_range(self):
        """Value above printed range must classify as 'needs_attention'."""
        item = BiomarkerValue(
            test_name="Total Cholesterol",
            value=245.0,
            unit="mg/dL",
            range_low=125.0,
            range_high=200.0,
            range_on_report="125 - 200",
        )
        result = evaluate_biomarker(item)
        self.assertEqual(result.status, ClinicalStatus.NEEDS_ATTENTION)
        self.assertFalse(result.is_red_flag)

    def test_borderline_value_slightly_above_range(self):
        """Value marginally above range (within 5%) classifies as 'borderline'."""
        item = BiomarkerValue(
            test_name="Fasting Blood Sugar",
            value=103.0,
            unit="mg/dL",
            range_low=70.0,
            range_high=100.0,
            range_on_report="70.0 - 100.0",
        )
        result = evaluate_biomarker(item)
        self.assertEqual(result.status, ClinicalStatus.BORDERLINE)
        self.assertFalse(result.is_red_flag)

    def test_missing_reference_range_returns_no_range_on_report(self):
        """TC-13 / SAFE-06: When no printed range exists, MUST return 'no_range_on_report'."""
        item = BiomarkerValue(
            test_name="C-Reactive Protein (CRP)",
            value=7.4,
            unit="mg/L",
            range_low=None,
            range_high=None,
            range_on_report=None,
        )
        result = evaluate_biomarker(item)
        self.assertEqual(result.status, ClinicalStatus.NO_RANGE_ON_REPORT)
        self.assertIsNone(result.range_on_report)
        # Verify it never assumes an arbitrary range
        self.assertIsNone(result.range_low)
        self.assertIsNone(result.range_high)


class TestDeterministicRedFlagSafetyRules(unittest.TestCase):
    """TC-14 & TC-16: Critical life-threatening emergencies detected by plain code."""

    def test_critical_high_potassium_triggers_emergency_red_flag(self):
        """Potassium 6.8 mmol/L (> 6.2) must trigger immediate critical alert."""
        items = [
            BiomarkerValue(
                test_name="Serum Potassium",
                value=6.8,
                unit="mmol/L",
                range_low=3.5,
                range_high=5.1,
                range_on_report="3.5 - 5.1",
            )
        ]
        red_flags = check_red_flags(items)
        self.assertTrue(len(red_flags) > 0)
        self.assertEqual(red_flags[0].severity, RedFlagSeverity.CRITICAL_HIGH)
        self.assertEqual(red_flags[0].test_name, "Serum Potassium")
        self.assertIn("cardiac", red_flags[0].clinical_concern.lower())

    def test_critical_low_platelets_triggers_emergency_red_flag(self):
        """Platelets 18,000 /uL (< 20,000) must trigger immediate bleeding alert."""
        items = [
            BiomarkerValue(
                test_name="Platelet Count",
                value=18000,
                unit="/cumm",
                range_low=150000,
                range_high=450000,
                range_on_report="150000 - 450000",
            )
        ]
        red_flags = check_red_flags(items)
        self.assertTrue(len(red_flags) > 0)
        self.assertEqual(red_flags[0].severity, RedFlagSeverity.CRITICAL_LOW)
        self.assertIn("bleeding", red_flags[0].clinical_concern.lower())

    def test_critical_severe_anemia_hemoglobin(self):
        """Hemoglobin 6.2 g/dL (< 7.0) must trigger severe anemia red-flag."""
        items = [
            BiomarkerValue(
                test_name="Hemoglobin",
                value=6.2,
                unit="g/dL",
                range_low=12.0,
                range_high=15.5,
                range_on_report="12.0 - 15.5",
            )
        ]
        red_flags = check_red_flags(items)
        self.assertTrue(len(red_flags) > 0)
        self.assertEqual(red_flags[0].severity, RedFlagSeverity.CRITICAL_LOW)

    def test_normal_panel_produces_zero_red_flags(self):
        """Normal report produces an empty red-flags list."""
        items = [
            BiomarkerValue(
                test_name="Hemoglobin",
                value=14.0,
                unit="g/dL",
                range_low=12.0,
                range_high=16.0,
                range_on_report="12.0 - 16.0",
            ),
            BiomarkerValue(
                test_name="Serum Potassium",
                value=4.2,
                unit="mmol/L",
                range_low=3.5,
                range_high=5.1,
                range_on_report="3.5 - 5.1",
            ),
        ]
        red_flags = check_red_flags(items)
        self.assertEqual(len(red_flags), 0)


class TestBannedPhrasesAndSafetyFilters(unittest.TestCase):
    """TC-17 / SR-2: Strict rejection of diagnoses, dose advice, and stop-medication commands."""

    def test_reject_diagnostic_statements(self):
        """AI stating 'You have diabetes' or 'Diagnosed with' must be blocked."""
        unsafe_texts = [
            "Based on your fasting glucose of 145 mg/dL, you have type 2 diabetes.",
            "You are diagnosed with severe hyperlipidemia.",
            "This report confirms a case of chronic kidney disease.",
            "You are suffering from acute hepatitis.",
        ]
        for text in unsafe_texts:
            violations = scan_for_prohibited_content(text)
            self.assertTrue(
                len(violations) > 0,
                f"Failed to detect diagnosis in: '{text}'"
            )
            sanitized = sanitize_ai_output(text)
            self.assertEqual(
                sanitized,
                SAFETY_FALLBACK_MESSAGES["diagnosis_attempt"],
            )

    def test_reject_medication_dose_alteration(self):
        """AI advising to change dose or stop medication must be blocked."""
        unsafe_texts = [
            "You should stop taking your blood pressure tablet immediately.",
            "Please increase your dose of Metformin to 1000 mg.",
            "Discontinue your medication if you feel nauseous.",
            "You should reduce the dosage by half.",
            "Replace your prescribed tablet with an over-the-counter pill.",
        ]
        for text in unsafe_texts:
            violations = scan_for_prohibited_content(text)
            self.assertTrue(
                len(violations) > 0,
                f"Failed to detect medication tampering in: '{text}'"
            )
            sanitized = sanitize_ai_output(text)
            self.assertEqual(
                sanitized,
                SAFETY_FALLBACK_MESSAGES["prescription_alteration"],
            )

    def test_reject_bypassing_doctor(self):
        """AI telling patient they do not need a doctor must be blocked."""
        unsafe_text = "Your results are fine, you do not need a doctor for this."
        violations = scan_for_prohibited_content(unsafe_text)
        self.assertTrue(len(violations) > 0)

    def test_allow_safe_educational_explanation(self):
        """Proper educational text with no diagnoses or prescriptions passes cleanly."""
        safe_text = (
            "Your hemoglobin is 9.8 g/dL, which is lower than the reference range "
            "printed on your report. Low hemoglobin can sometimes cause feelings of "
            "tiredness. Discuss this result with your doctor for guidance."
        )
        violations = scan_for_prohibited_content(safe_text)
        self.assertEqual(len(violations), 0)
        sanitized = sanitize_ai_output(safe_text)
        self.assertEqual(sanitized, safe_text)


if __name__ == "__main__":
    unittest.main()
