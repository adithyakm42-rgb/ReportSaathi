"""
ReportSaathi - Tesseract OCR & Biomarker Extraction Engine
Author: Person 3 (Quality & Engineering Lead)
Grounded in: docs/06-test-plan.md (TC-08, TC-09, TC-10), docs/06b-safety-rules.md, docs/06c-api-contracts.md

Features:
1. Runs Tesseract OCR directly on uploaded medical images/PDFs.
2. Assesses text clarity and automatically flags blurry/uncertain reports for user verification.
3. Parses structured biomarkers, values, units, and printed reference ranges.
4. If no reference range is printed, strictly preserves 'no_range_on_report'.
5. Supports user manual corrections and re-validates all values deterministically.
"""

import re
import os
import subprocess
from typing import List, Dict, Any, Optional, Union
from backend.safety.rules import BiomarkerValue, evaluate_biomarker, ClinicalStatus

# Ignored non-test headers
HEADER_KEYWORDS = [
    "patient name", "patient id", "date", "doctor", "laboratory",
    "investigation", "clinic", "hospital", "alert", "comment",
    "note", "verified by", "end of report", "phone", "plot"
]


def assess_text_clarity(text: str) -> Dict[str, Any]:
    """
    Assesses whether the OCR text is sufficiently legible or if it requires
    mandatory user review/correction (TC-09 / OCR-07).
    """
    if not text or len(text.strip()) < 20:
        return {
            "extraction_status": "unclear",
            "requires_verification": True,
            "fallback_message": "We could not read some information clearly. Please upload a clearer image or verify the extracted values manually."
        }

    # Count noise artifacts and question marks
    unclear_markers = len(re.findall(r"(\?{1,}|\[UNREADABLE\]|\[BLURRED\]|\?\.\?)", text, re.IGNORECASE))
    digit_count = len(re.findall(r"\d", text))
    char_count = len(text)

    # If document has severe question marks or unreadable markers
    if unclear_markers >= 2 or (digit_count == 0 and char_count > 50):
        return {
            "extraction_status": "unclear",
            "requires_verification": True,
            "fallback_message": "We could not read some information clearly. Please upload a clearer image or verify the extracted values manually."
        }

    return {
        "extraction_status": "completed",
        "requires_verification": False,
        "fallback_message": ""
    }


def parse_biomarkers_from_text(raw_text: str) -> List[BiomarkerValue]:
    """
    Extracts structured biomarker records from raw clinical text.
    Strictly preserves printed reference ranges or records None if missing.
    """
    results: List[BiomarkerValue] = []
    lines = raw_text.splitlines()

    for line in lines:
        line_clean = line.strip()
        if not line_clean or line_clean.startswith("---") or line_clean.startswith("==="):
            continue

        # Strip trailing annotations like *** CRITICAL HIGH *** or comments
        cleaned = re.sub(r"\*{3}.*?\*{3}", "", line_clean).strip()

        # Check for colon separating test name from value
        if ":" not in cleaned:
            continue

        parts = cleaned.split(":", 1)
        test_candidate = parts[0].strip()
        rest = parts[1].strip()

        # Filter out metadata lines
        if any(test_candidate.lower().startswith(h) for h in HEADER_KEYWORDS):
            continue
        if test_candidate.lower().startswith("rx") or test_candidate.lower().startswith("tab."):
            continue

        # Extract reference range in parentheses if present
        ref_match = re.search(r"\((?:Ref(?:\s*Range)?|Reference\s*Interval)?[:\s]*([^\)]+)\)", rest, re.IGNORECASE)
        raw_range: Optional[str] = ref_match.group(1).strip() if ref_match else None

        # Value part without the parentheses
        val_part = re.sub(r"\(.*?\)", "", rest).strip()

        # Extract value and optional unit
        val_match = re.match(r"^([<>]?\s*[\d\.\,]+|[A-Za-z\s\-]+?)(?:\s+([A-Za-z\/\%\_]+))?$", val_part)
        if not val_match:
            # Fallback for value and unit together
            val_match = re.search(r"([<>]?\s*[\d\.\,]+|[A-Za-z\s\-]+)\s*([A-Za-z\/\%\_]+)?", val_part)

        if not val_match:
            continue

        raw_val_str = val_match.group(1).strip()
        raw_unit = val_match.group(2).strip() if val_match.group(2) else None

        # Parse numeric value
        clean_num = raw_val_str.replace(",", "").strip()
        parsed_val: Union[float, int, str]

        if re.match(r"^[\d\.]+$", clean_num):
            try:
                parsed_val = float(clean_num) if "." in clean_num else int(clean_num)
            except ValueError:
                parsed_val = raw_val_str
        else:
            parsed_val = raw_val_str

        # Parse range boundaries if present
        range_low: Optional[float] = None
        range_high: Optional[float] = None

        if raw_range:
            range_match = re.search(r"([\d\.\,]+)\s*(?:-|to)\s*([\d\.\,]+)", raw_range)
            if range_match:
                try:
                    range_low = float(range_match.group(1).replace(",", ""))
                    range_high = float(range_match.group(2).replace(",", ""))
                except ValueError:
                    pass
            else:
                lt_match = re.search(r"<\s*([\d\.\,]+)", raw_range)
                if lt_match:
                    try:
                        range_low = 0.0
                        range_high = float(lt_match.group(1).replace(",", ""))
                    except ValueError:
                        pass

        # Construct and evaluate biomarker
        item = BiomarkerValue(
            test_name=test_candidate,
            value=parsed_val,
            unit=raw_unit,
            range_low=range_low,
            range_high=range_high,
            range_on_report=raw_range,
            raw_token=line_clean
        )

        evaluated = evaluate_biomarker(item)
        results.append(evaluated)

    return results


def apply_user_corrections(
    original_values: List[BiomarkerValue],
    corrections: List[Dict[str, Any]]
) -> List[BiomarkerValue]:
    """
    Applies user-provided corrections to extracted biomarkers and
    strictly re-evaluates clinical classification and red-flag status (TC-10 / OCR-09).
    """
    updated_list = []

    for item in original_values:
        # Check if this item has a matching correction
        match = next(
            (c for c in corrections if c.get("test_name", "").lower() in item.test_name.lower() or item.test_name.lower() in c.get("test_name", "").lower()),
            None
        )

        if match:
            # Update value
            if "corrected_value" in match:
                corr_val = match["corrected_value"]
                if isinstance(corr_val, (int, float)):
                    item.value = corr_val
                elif isinstance(corr_val, str) and re.match(r"^[\d\.\,]+$", corr_val):
                    c_clean = corr_val.replace(",", "").strip()
                    item.value = float(c_clean) if "." in c_clean else int(c_clean)
                else:
                    item.value = corr_val

            # Update range if user corrected range
            if "corrected_range_low" in match:
                item.range_low = match["corrected_range_low"]
            if "corrected_range_high" in match:
                item.range_high = match["corrected_range_high"]
            if "corrected_range_on_report" in match:
                item.range_on_report = match["corrected_range_on_report"]

            # Re-evaluate biomarker deterministically
            item.is_red_flag = False
            item = evaluate_biomarker(item)

        updated_list.append(item)

    return updated_list


def run_tesseract(
    image_path: str,
    tesseract_cmd: str = r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    lang: str = "eng"
) -> str:
    """
    Executes Tesseract OCR on a local image file.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"File not found: {image_path}")

    cmd = [tesseract_cmd, image_path, "stdout", "-l", lang]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return proc.stdout
    except Exception:
        proc = subprocess.run(["tesseract", image_path, "stdout", "-l", lang], capture_output=True, text=True, check=True)
        return proc.stdout
