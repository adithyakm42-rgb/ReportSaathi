"""
ReportSaathi — Privacy, PHI Sanitization & Ephemeral Storage Engine
Author: Person 3 (Quality & Engineering Lead)
Grounded in: docs/06b-safety-rules.md (Sec 9), docs/06-test-plan.md (TC-25, TC-26), docs/07-task-breakdown.md (SAFE-08, OCR-10)

Key Guarantees:
1. SAFE-08 / TC-25: No patient health information (PHI), raw medical text, or lab biomarkers in application logs.
2. OCR-10 / TC-26: Ephemeral storage lifecycle with deterministic file deletion and TTL-based expiry.
3. SAFE-07: Strict path-traversal prevention for document identifiers.
"""

import os
import re
import logging
import time
import shutil
import tempfile
from typing import Optional, List, Dict, Any


# Regex pattern to identify sensitive medical report contents, biomarker values, and prescription text
_SENSITIVE_PATTERNS = [
    # Laboratory test with numerical result and unit (e.g. Hemoglobin: 13.5 g/dL)
    re.compile(r"(?i)\b(hemoglobin|hb|platelet|wbc|rbc|potassium|creatinine|glucose|sugar|cholesterol|bilirubin|tsh|esr|crp)\s*[:=-]?\s*\d+(\.\d+)?\s*(g/dl|mg/dl|mmol/l|/cumm|/ul|%|u/l|ng/ml|mm/hr)?\b"),
    # Diagnostic or medication phrases
    re.compile(r"(?i)\b(rx|tablet|capsule|mg|dosage|prescription|patient|dr\.|doctor|mrs?\.|mr\.)\s+([A-Za-z0-9_ -]+)"),
    # Raw multi-word medical report extraction snippets
    re.compile(r"(?i)\b(report|specimen|serum|plasma|urine|blood count|lipid profile|liver function|renal function)\b.*"),
]

# Sensitive keys in JSON/dict payloads that must never be logged in cleartext
SENSITIVE_LOG_KEYS = {
    "raw_text",
    "extracted_text",
    "corrected_text",
    "report_text",
    "biomarkers",
    "values",
    "patient_name",
    "patient_id",
    "authorization",
    "api_key",
    "gemini_api_key",
}


def sanitize_log_message(msg: str) -> str:
    """
    TC-25 / SAFE-08: Redacts medical content, lab values, and personal identifiers
    from log messages before outputting to streams or operational logs.
    """
    if not isinstance(msg, str):
        msg = str(msg)

    sanitized = msg
    for pattern in _SENSITIVE_PATTERNS:
        sanitized = pattern.sub("[REDACTED_MEDICAL_DATA]", sanitized)
    
    return sanitized


class PrivacyPreservingLogFilter(logging.Filter):
    """
    Logging filter that sanitizes all log records to prevent medical data leak in application logs.
    """
    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = sanitize_log_message(record.msg)
        return True


def sanitize_payload_for_logging(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Safely redacts dict/JSON structures for audit logging.
    Leaves operational metadata (document_id, language, status) intact.
    """
    safe_copy = {}
    for k, v in payload.items():
        if k.lower() in SENSITIVE_LOG_KEYS:
            safe_copy[k] = "[REDACTED_MEDICAL_DATA]"
        elif isinstance(v, dict):
            safe_copy[k] = sanitize_payload_for_logging(v)
        elif isinstance(v, list):
            safe_copy[k] = [
                sanitize_payload_for_logging(item) if isinstance(item, dict) else "[REDACTED_ITEM]"
                for item in v
            ]
        else:
            safe_copy[k] = v
    return safe_copy


class EphemeralStorageManager:
    """
    TC-26 / OCR-10 / SAFE-07: Manages the lifecycle of temporary uploaded documents.
    Enforces strict path sanitization and automatic cleanup.
    """

    def __init__(self, base_dir: Optional[str] = None):
        if base_dir:
            self.base_dir = os.path.abspath(base_dir)
        else:
            self.base_dir = os.path.join(tempfile.gettempdir(), "reportsaathi_ephemeral")
        os.makedirs(self.base_dir, exist_ok=True)

    def _validate_document_id(self, document_id: str) -> str:
        """
        SAFE-07: Prevents directory traversal attacks.
        Document IDs must be alphanumeric or UUIDs with hyphens only.
        """
        if not document_id or not isinstance(document_id, str):
            raise ValueError("Document ID must be a non-empty string.")
        
        # Disallow path separators, dot-dot traversal, and special characters
        if "/" in document_id or "\\" in document_id or ".." in document_id or "\0" in document_id:
            raise ValueError(f"Invalid document_id (potential path traversal detected): {document_id}")

        # Strict regex: alphanumeric and hyphens/underscores only
        if not re.match(r"^[A-Za-z0-9_-]{8,64}$", document_id):
            raise ValueError(f"Document ID does not match valid format: {document_id}")

        return document_id

    def get_document_path(self, document_id: str, filename: Optional[str] = None) -> str:
        """Returns the canonical path for a document, verifying it stays within base_dir."""
        valid_id = self._validate_document_id(document_id)
        doc_dir = os.path.join(self.base_dir, valid_id)

        if filename:
            # Strip path elements from filename
            safe_filename = os.path.basename(filename)
            target_path = os.path.join(doc_dir, safe_filename)
        else:
            target_path = doc_dir

        canonical = os.path.abspath(target_path)
        if not canonical.startswith(self.base_dir):
            raise ValueError(f"Path traversal blocked: {target_path}")

        return canonical

    def save_ephemeral_file(self, document_id: str, filename: str, content: bytes) -> str:
        """Saves a temporary file for OCR processing."""
        doc_dir = self.get_document_path(document_id)
        os.makedirs(doc_dir, exist_ok=True)

        file_path = self.get_document_path(document_id, filename)
        with open(file_path, "wb") as f:
            f.write(content)

        return file_path

    def cleanup_document(self, document_id: str) -> bool:
        """
        OCR-10 / TC-26: Deletes a temporary document folder and its contents completely.
        Returns True if deleted, False if already absent.
        """
        try:
            doc_dir = self.get_document_path(document_id)
            if os.path.exists(doc_dir):
                shutil.rmtree(doc_dir)
                return True
            return False
        except Exception as e:
            logging.error(f"Error deleting ephemeral document {document_id}: {sanitize_log_message(str(e))}")
            return False

    def cleanup_expired(self, max_age_seconds: int = 3600) -> int:
        """
        OCR-10 / TC-26: Deletes temporary documents older than max_age_seconds (TTL).
        Returns the count of purged document sessions.
        """
        now = time.time()
        purged_count = 0

        if not os.path.exists(self.base_dir):
            return 0

        for entry in os.listdir(self.base_dir):
            entry_path = os.path.join(self.base_dir, entry)
            if os.path.isdir(entry_path):
                try:
                    stat = os.stat(entry_path)
                    age = now - stat.st_mtime
                    if age > max_age_seconds:
                        shutil.rmtree(entry_path)
                        purged_count += 1
                except Exception:
                    continue

        return purged_count
