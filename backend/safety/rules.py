"""
ReportSaathi - Deterministic Medical Safety Rules
Author: Person 3 (Quality & Engineering Lead)
Grounded in: docs/06b-safety-rules.md, docs/06c-api-contracts.md, docs/06-test-plan.md

Guiding Principles:
1. Deterministic code classifies biomarkers and triggers red flags before AI runs.
2. Only reference ranges printed on the report are used. If missing, return 'no_range_on_report'.
3. Critical thresholds trigger immediate emergency guidance independently of LLM availability.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Union


class ClinicalStatus(str, Enum):
    NORMAL = "normal"
    BORDERLINE = "borderline"
    NEEDS_ATTENTION = "needs_attention"
    NO_RANGE_ON_REPORT = "no_range_on_report"
    CRITICAL_LOW = "critical_low"
    CRITICAL_HIGH = "critical_high"
    UNCLEAR = "unclear"


class RedFlagSeverity(str, Enum):
    CRITICAL_LOW = "CRITICAL_LOW"
    CRITICAL_HIGH = "CRITICAL_HIGH"
    EMERGENCY = "EMERGENCY"


@dataclass
class BiomarkerValue:
    test_name: str
    value: Optional[Union[float, int, str]]
    unit: Optional[str] = None
    range_low: Optional[float] = None
    range_high: Optional[float] = None
    range_on_report: Optional[str] = None
    status: Optional[ClinicalStatus] = None
    is_red_flag: bool = False
    raw_token: Optional[str] = None
    explanation: Optional[str] = None


@dataclass
class RedFlagAlert:
    test_name: str
    value: Union[float, int, str]
    unit: str
    severity: RedFlagSeverity
    clinical_concern: str
    action_required: str


# Baseline Emergency Critical Thresholds
CRITICAL_THRESHOLDS = {
    "potassium": {
        "critical_low": 2.8,
        "critical_high": 6.2,
        "unit": "mmol/L",
        "low_concern": "Severe Hypokalemia: Urgent risk of cardiac arrhythmia and muscle paralysis.",
        "high_concern": "Severe Hyperkalemia (Potassium > 6.2 mmol/L): Urgent risk of fatal cardiac arrhythmia.",
        "action": "Immediate emergency room evaluation required."
    },
    "platelet": {
        "critical_low": 20000,
        "unit": "/cumm",
        "low_concern": "Severe Thrombocytopenia (Platelets < 20,000 /cumm): High risk of spontaneous internal bleeding.",
        "action": "Avoid injury or anti-platelet medications. Seek immediate hospital care."
    },
    "hemoglobin": {
        "critical_low": 7.0,
        "unit": "g/dL",
        "low_concern": "Critical Severe Anemia (Hemoglobin < 7.0 g/dL): Risk of tissue hypoxia and cardiovascular strain.",
        "action": "Urgent medical assessment and transfusion evaluation required."
    },
    "glucose": {
        "critical_low": 50.0,
        "critical_high": 350.0,
        "unit": "mg/dL",
        "low_concern": "Severe Hypoglycemia: Risk of loss of consciousness, seizure, and neuroglycopenia.",
        "high_concern": "Severe Hyperglycemia (> 350 mg/dL): Risk of Diabetic Ketoacidosis (DKA) or Hyperosmolar Hyperglycemic State (HHS).",
        "action": "Seek prompt emergency medical care."
    },
    "creatinine": {
        "critical_high": 5.0,
        "unit": "mg/dL",
        "high_concern": "Critical Acute Renal Impairment (Creatinine > 5.0 mg/dL): Risk of uremic emergency.",
        "action": "Immediate nephrology evaluation and emergency hospital care required."
    }
}


def evaluate_biomarker(item: BiomarkerValue) -> BiomarkerValue:
    """
    Classifies a biomarker using only the printed reference range on the report.
    If no reference range is printed, sets status to 'no_range_on_report'.
    """
    # Safety Rule: If no reference range is provided, never invent or assume one.
    if item.range_on_report is None or (item.range_low is None and item.range_high is None):
        item.status = ClinicalStatus.NO_RANGE_ON_REPORT
        item.range_low = None
        item.range_high = None
        item.is_red_flag = False
        return item

    # If the value is not numeric (e.g., "Negative", "Reactive", "Unclear")
    if not isinstance(item.value, (int, float)):
        item.status = ClinicalStatus.NORMAL if str(item.value).lower() in ["negative", "non-reactive", "normal"] else ClinicalStatus.NEEDS_ATTENTION
        return item

    val = float(item.value)

    # Check Low
    if item.range_low is not None and val < item.range_low:
        # Borderline check: within 5% of lower limit
        margin = item.range_low * 0.05
        if (item.range_low - val) <= margin:
            item.status = ClinicalStatus.BORDERLINE
        else:
            item.status = ClinicalStatus.NEEDS_ATTENTION
        return item

    # Check High
    if item.range_high is not None and val > item.range_high:
        # Borderline check: within 5% of upper limit
        margin = item.range_high * 0.05
        if (val - item.range_high) <= margin:
            item.status = ClinicalStatus.BORDERLINE
        else:
            item.status = ClinicalStatus.NEEDS_ATTENTION
        return item

    # In range
    item.status = ClinicalStatus.NORMAL
    item.is_red_flag = False
    return item


def _normalize_name(name: str) -> str:
    return name.lower().replace("_", " ").replace("-", " ")


def check_red_flags(items: List[BiomarkerValue]) -> List[RedFlagAlert]:
    """
    Deterministic rule-based check for emergency red-flag thresholds.
    Executes in plain Python without any external API or LLM dependency.
    """
    alerts: List[RedFlagAlert] = []

    for item in items:
        if item.value is None or not isinstance(item.value, (int, float)):
            continue

        val = float(item.value)
        name = _normalize_name(item.test_name)

        # Potassium
        if "potassium" in name or name == "k+":
            rule = CRITICAL_THRESHOLDS["potassium"]
            if val >= rule["critical_high"]:
                item.is_red_flag = True
                item.status = ClinicalStatus.CRITICAL_HIGH
                alerts.append(RedFlagAlert(
                    test_name=item.test_name,
                    value=item.value,
                    unit=item.unit or rule["unit"],
                    severity=RedFlagSeverity.CRITICAL_HIGH,
                    clinical_concern=rule["high_concern"],
                    action_required=rule["action"]
                ))
            elif val <= rule["critical_low"]:
                item.is_red_flag = True
                item.status = ClinicalStatus.CRITICAL_LOW
                alerts.append(RedFlagAlert(
                    test_name=item.test_name,
                    value=item.value,
                    unit=item.unit or rule["unit"],
                    severity=RedFlagSeverity.CRITICAL_LOW,
                    clinical_concern=rule["low_concern"],
                    action_required=rule["action"]
                ))

        # Platelets
        elif "platelet" in name or name == "plt":
            rule = CRITICAL_THRESHOLDS["platelet"]
            if val <= rule["critical_low"]:
                item.is_red_flag = True
                item.status = ClinicalStatus.CRITICAL_LOW
                alerts.append(RedFlagAlert(
                    test_name=item.test_name,
                    value=item.value,
                    unit=item.unit or rule["unit"],
                    severity=RedFlagSeverity.CRITICAL_LOW,
                    clinical_concern=rule["low_concern"],
                    action_required=rule["action"]
                ))

        # Hemoglobin
        elif "hemoglobin" in name or name == "hb":
            rule = CRITICAL_THRESHOLDS["hemoglobin"]
            if val <= rule["critical_low"]:
                item.is_red_flag = True
                item.status = ClinicalStatus.CRITICAL_LOW
                alerts.append(RedFlagAlert(
                    test_name=item.test_name,
                    value=item.value,
                    unit=item.unit or rule["unit"],
                    severity=RedFlagSeverity.CRITICAL_LOW,
                    clinical_concern=rule["low_concern"],
                    action_required=rule["action"]
                ))

        # Blood Glucose
        elif any(k in name for k in ["glucose", "blood sugar", "fbs", "rbs"]):
            rule = CRITICAL_THRESHOLDS["glucose"]
            if val <= rule["critical_low"]:
                item.is_red_flag = True
                item.status = ClinicalStatus.CRITICAL_LOW
                alerts.append(RedFlagAlert(
                    test_name=item.test_name,
                    value=item.value,
                    unit=item.unit or rule["unit"],
                    severity=RedFlagSeverity.CRITICAL_LOW,
                    clinical_concern=rule["low_concern"],
                    action_required=rule["action"]
                ))
            elif val >= rule["critical_high"]:
                item.is_red_flag = True
                item.status = ClinicalStatus.CRITICAL_HIGH
                alerts.append(RedFlagAlert(
                    test_name=item.test_name,
                    value=item.value,
                    unit=item.unit or rule["unit"],
                    severity=RedFlagSeverity.CRITICAL_HIGH,
                    clinical_concern=rule["high_concern"],
                    action_required=rule["action"]
                ))

        # Creatinine
        elif "creatinine" in name:
            rule = CRITICAL_THRESHOLDS["creatinine"]
            if val >= rule["critical_high"]:
                item.is_red_flag = True
                item.status = ClinicalStatus.CRITICAL_HIGH
                alerts.append(RedFlagAlert(
                    test_name=item.test_name,
                    value=item.value,
                    unit=item.unit or rule["unit"],
                    severity=RedFlagSeverity.CRITICAL_HIGH,
                    clinical_concern=rule["high_concern"],
                    action_required=rule["action"]
                ))

    return alerts
