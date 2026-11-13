"""
ReportSaathi - Prohibited Phrases and AI Output Safety Filter
Author: Person 3 (Quality & Engineering Lead)
Grounded in: docs/06b-safety-rules.md Section 3, 4, 8, 11

Guiding Principles:
1. Rejects any AI-generated output containing diagnoses, predictions of disease, dosage modifications, or medication stop commands.
2. Replaces prohibited text with safe, standardized medical fallback messages.
"""

import re
from typing import List, Dict

# Standardized fallback messages from docs/06b-safety-rules.md Section 11
SAFETY_FALLBACK_MESSAGES: Dict[str, str] = {
    "diagnosis_attempt": (
        "ReportSaathi cannot diagnose medical conditions. "
        "Please discuss your symptoms and report with a qualified healthcare professional."
    ),
    "prescription_alteration": (
        "We could not confidently understand this prescription instruction. "
        "Please confirm it with your doctor or pharmacist."
    ),
    "potential_emergency": (
        "Your information may indicate a potentially urgent health concern. "
        "Please seek immediate medical attention or contact your local emergency service."
    ),
    "general_disclaimer": "This explains your report. It does not replace your doctor."
}

# Regex patterns for prohibited medical phrases
PROHIBITED_PATTERNS = [
    # Prohibited Diagnosis Attempts
    (re.compile(r"\b(you have|you are suffering from|diagnosed with|confirm(s|ed)? a case of|indicates that you have|patient has)\b", re.IGNORECASE), "diagnosis_attempt"),
    (re.compile(r"\b(you likely have|you suffer from|positive for diagnosis of)\b", re.IGNORECASE), "diagnosis_attempt"),
    
    # Prohibited Medication / Dosage Alterations
    (re.compile(r"\b(stop taking|discontinue (your )?medic(ine|ation)|stop (your )?medic(ine|ation))\b", re.IGNORECASE), "prescription_alteration"),
    (re.compile(r"\b(increase your dose|decrease your dose|reduce the dosage|change your medication|replace your prescribed)\b", re.IGNORECASE), "prescription_alteration"),
    (re.compile(r"\b(take \d+\s?mg instead|take twice as much|skip your dose)\b", re.IGNORECASE), "prescription_alteration"),
    
    # Prohibited Bypassing of Healthcare Providers
    (re.compile(r"\b(you do not need a doctor|no need to see a physician|safe to ignore|no medical attention required)\b", re.IGNORECASE), "diagnosis_attempt"),
]


def scan_for_prohibited_content(text: str) -> List[str]:
    """
    Scans candidate text (from LLM or user inputs) for prohibited clinical statements.
    Returns a list of violation category tags if matches are found.
    """
    if not text:
        return []

    violations = []
    for pattern, category in PROHIBITED_PATTERNS:
        if pattern.search(text):
            violations.append(category)

    return violations


def sanitize_ai_output(text: str) -> str:
    """
    Validates AI output. If prohibited language is detected, replaces it
    with the approved safe fallback message. Otherwise returns original text.
    """
    violations = scan_for_prohibited_content(text)
    if not violations:
        return text

    # Select the most critical violation category
    if "diagnosis_attempt" in violations:
        return SAFETY_FALLBACK_MESSAGES["diagnosis_attempt"]
    if "prescription_alteration" in violations:
        return SAFETY_FALLBACK_MESSAGES["prescription_alteration"]

    return SAFETY_FALLBACK_MESSAGES["general_disclaimer"]
