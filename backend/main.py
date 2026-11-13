"""
ReportSaathi — FastAPI Backend Application
Technical Coordination: Person 2 (Systems & DevOps Lead) & Person 3 (Quality & Engineering Lead)
Grounded in: docs/06c-api-contracts.md, docs/06b-safety-rules.md, docs/07-task-breakdown.md
"""

import os
import uuid
import logging
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, field_validator

from backend.safety.rules import (
    ClinicalStatus,
    BiomarkerValue,
    check_red_flags,
    evaluate_biomarker,
)
from backend.safety.banned_phrases import sanitize_ai_output
from backend.safety.privacy import (
    EphemeralStorageManager,
    PrivacyPreservingLogFilter,
    sanitize_log_message,
)
from backend.integrations.ocr import (
    run_tesseract,
    parse_biomarkers_from_text,
    assess_text_clarity,
    apply_user_corrections,
)

# Setup privacy-preserving logging
logger = logging.getLogger("reportsaathi")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.addFilter(PrivacyPreservingLogFilter())
logger.addHandler(handler)

# Initialize FastAPI application
app = FastAPI(
    title="ReportSaathi API",
    description="Plain-Language Medical Report Explainer Backend",
    version="1.0.0",
)

# CORS Middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production config will bind to approved origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ephemeral document storage manager
storage_manager = EphemeralStorageManager()

# In-memory session cache for verified document OCR texts & biomarkers (ephemeral)
_DOCUMENT_CACHE: Dict[str, Dict[str, Any]] = {}

MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB limit (OCR-02)
SUPPORTED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png"}

MANDATORY_DISCLAIMER = "This explains your report. It does not replace your doctor."

# ---------------------------------------------------------------------------
# Pydantic Schemas (docs/06c-api-contracts.md)
# ---------------------------------------------------------------------------

class ExtractRequest(BaseModel):
    document_id: str = Field(..., description="Temporary document identifier")

class CorrectionRequest(BaseModel):
    corrected_text: str = Field(..., description="User-verified or corrected report text")

    @field_validator("corrected_text")
    @classmethod
    def validate_non_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Corrected text must not be empty.")
        return v.strip()

class ExplainRequest(BaseModel):
    document_id: str
    language: str = "English"
    reading_level: str = "Simple"

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        valid_langs = {"english", "hindi", "kannada", "en", "hi", "kn"}
        if v.lower() not in valid_langs:
            raise ValueError("Supported languages are English, Hindi, and Kannada.")
        return v

    @field_validator("reading_level")
    @classmethod
    def validate_reading_level(cls, v: str) -> str:
        valid_levels = {"simple", "standard", "detailed"}
        if v.lower() not in valid_levels:
            raise ValueError("Supported reading levels are Simple, Standard, and Detailed.")
        return v

class TranslateRequest(BaseModel):
    text: str
    target_language: str

class QuestionsRequest(BaseModel):
    explanation: Optional[str] = None
    document_id: Optional[str] = None

class FeedbackRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="User rating between 1 and 5")
    feedback: Optional[str] = None


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------

@app.get("/api/health")
def health_check():
    """API-01: Health check endpoint."""
    return {"status": "healthy", "service": "ReportSaathi API"}


@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    API-02 / OCR-01 to OCR-04:
    Accepts PDF, JPG, JPEG, PNG <= 10MB for ephemeral processing.
    """
    filename = file.filename or "uploaded_document"
    _, ext = os.path.splitext(filename.lower())

    # Format validation
    if ext not in SUPPORTED_EXTENSIONS:
        return JSONResponse(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            content={
                "success": False,
                "message": f"Unsupported file format '{ext}'. Allowed: PDF, JPG, JPEG, PNG.",
                "error_code": "UNSUPPORTED_FORMAT",
            },
        )

    # Read content
    content = await file.read()

    # Empty file check
    if not content or len(content) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "success": False,
                "message": "Uploaded file is empty.",
                "error_code": "EMPTY_FILE",
            },
        )

    # Size validation (10 MB limit)
    if len(content) > MAX_UPLOAD_BYTES:
        return JSONResponse(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            content={
                "success": False,
                "message": f"File size exceeds the 10 MB maximum upload limit.",
                "error_code": "FILE_TOO_LARGE",
            },
        )

    # Generate temporary document ID
    document_id = f"doc-{uuid.uuid4().hex[:16]}"
    file_path = storage_manager.save_ephemeral_file(document_id, filename, content)

    # Initialize cache record
    _DOCUMENT_CACHE[document_id] = {
        "filename": filename,
        "file_path": file_path,
        "raw_text": "",
        "corrected_text": "",
        "biomarkers": [],
    }

    logger.info(f"Document {document_id} uploaded successfully.")

    return {
        "success": True,
        "message": "Document uploaded successfully",
        "data": {
            "document_id": document_id,
            "filename": filename,
            "status": "uploaded",
        },
    }


@app.post("/api/extract")
def extract_text(request: ExtractRequest):
    """
    API-03 / OCR-06: Extract text using OCR and assess clarity.
    """
    doc_id = request.document_id
    if doc_id not in _DOCUMENT_CACHE:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "The requested document was not found or has expired.",
                "error_code": "INVALID_DOCUMENT_ID",
            },
        )

    doc_info = _DOCUMENT_CACHE[doc_id]
    file_path = doc_info["file_path"]

    # Run Tesseract extraction
    try:
        extracted_text = run_tesseract(file_path)
    except Exception as e:
        logger.warning(f"Tesseract extraction notice: {sanitize_log_message(str(e))}")
        extracted_text = ""

    # Assess clarity
    clarity = assess_text_clarity(extracted_text)

    # Parse initial biomarkers
    biomarkers = parse_biomarkers_from_text(extracted_text)

    doc_info["raw_text"] = extracted_text
    doc_info["corrected_text"] = extracted_text
    doc_info["biomarkers"] = biomarkers

    return {
        "success": True,
        "data": {
            "extracted_text": extracted_text,
            "extraction_status": clarity["extraction_status"],
            "requires_verification": clarity["requires_verification"],
            "biomarkers_detected": len(biomarkers),
        },
    }


@app.post("/api/extract/{document_id}/corrections")
def correct_ocr_text(document_id: str, request: CorrectionRequest):
    """
    API-04 / OCR-09: Apply user-corrected OCR text.
    """
    if document_id not in _DOCUMENT_CACHE:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "The requested document was not found or has expired.",
                "error_code": "INVALID_DOCUMENT_ID",
            },
        )

    # Re-parse biomarkers from verified text
    revalidated = apply_user_corrections(request.corrected_text)

    doc_info = _DOCUMENT_CACHE[document_id]
    doc_info["corrected_text"] = request.corrected_text
    doc_info["biomarkers"] = revalidated["biomarkers"]

    return {
        "success": True,
        "message": "Extracted text corrected successfully",
        "data": {
            "document_id": document_id,
            "status": "corrected",
            "biomarkers_count": len(revalidated["biomarkers"]),
        },
    }


@app.post("/api/explain")
def explain_report(request: ExplainRequest):
    """
    API-05 / AI-03 / SAFE-01 / SAFE-04:
    Executes deterministic red-flag safety checks before plain-language educational explanation.
    """
    doc_id = request.document_id
    if doc_id not in _DOCUMENT_CACHE:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "The requested document was not found or has expired.",
                "error_code": "INVALID_DOCUMENT_ID",
            },
        )

    doc_info = _DOCUMENT_CACHE[doc_id]
    biomarkers: List[BiomarkerValue] = doc_info.get("biomarkers", [])

    # Deterministic red-flag safety check (SAFE-01)
    red_flags = check_red_flags(biomarkers)

    # Build plain-language explanation
    lang = request.language.lower()
    level = request.reading_level.lower()

    # Rule-grounded educational summary generator
    explanations = []
    if red_flags:
        for rf in red_flags:
            explanations.append(f"⚠️ URGENT: {rf['message']}. Action needed: {rf['action_required']}")

    for bm in biomarkers:
        if bm.status == ClinicalStatus.NORMAL:
            explanations.append(f"• {bm.test_name}: {bm.value} {bm.unit} is within the laboratory's printed reference range ({bm.range_low} - {bm.range_high} {bm.unit}).")
        elif bm.status == ClinicalStatus.NEEDS_ATTENTION:
            explanations.append(f"• {bm.test_name}: {bm.value} {bm.unit} is outside the printed reference range ({bm.range_low} - {bm.range_high} {bm.unit}). Discuss this result with your doctor.")
        elif bm.status == ClinicalStatus.BORDERLINE:
            explanations.append(f"• {bm.test_name}: {bm.value} {bm.unit} is close to the reference boundary ({bm.range_low} - {bm.range_high} {bm.unit}).")
        elif bm.status == ClinicalStatus.NO_RANGE_ON_REPORT:
            explanations.append(f"• {bm.test_name}: {bm.value} {bm.unit} was recorded, but no reference range was printed on this report.")

    if not explanations:
        raw_text = doc_info.get("corrected_text", "")
        if raw_text.strip():
            explanations.append("The document text was reviewed. Please consult your physician regarding the specific details of your report.")
        else:
            explanations.append("No medical values were detected on the uploaded page.")

    full_explanation = "\n\n".join(explanations)

    # Safety validation: Sanitize AI/generated text against prohibited diagnostic or dose alterations
    safe_explanation = sanitize_ai_output(full_explanation)

    # Map biomarkers to serializable JSON format
    values_json = [
        {
            "test_name": b.test_name,
            "value": b.value,
            "unit": b.unit,
            "range_on_report": f"{b.range_low} - {b.range_high}" if b.range_low is not None and b.range_high is not None else None,
            "status": b.status.value,
            "explanation": f"Your {b.test_name} is {b.value} {b.unit}."
        }
        for b in biomarkers
    ]

    return {
        "success": True,
        "data": {
            "document_id": doc_id,
            "explanation": safe_explanation,
            "language": request.language,
            "reading_level": request.reading_level,
            "disclaimer": MANDATORY_DISCLAIMER,
            "requires_medical_review": len(red_flags) > 0,
            "red_flags": red_flags,
            "values": values_json,
        },
    }


@app.post("/api/questions")
def generate_questions(request: QuestionsRequest):
    """
    API-07 / AI-10 / TC-19:
    Generates 3 to 6 educational doctor consultation questions.
    """
    default_questions = [
        "What do these laboratory results mean in the context of my current health?",
        "Are there any specific lifestyle or dietary habits I should adjust based on these values?",
        "Do any of the tests outside the reference range require a repeat test or follow-up?",
        "Are there any further diagnostic tests you would recommend to investigate these results?",
    ]

    # If specific biomarkers were flagged, append a tailored inquiry
    if request.document_id and request.document_id in _DOCUMENT_CACHE:
        biomarkers = _DOCUMENT_CACHE[request.document_id].get("biomarkers", [])
        abnormal = [b.test_name for b in biomarkers if b.status in (ClinicalStatus.NEEDS_ATTENTION, ClinicalStatus.BORDERLINE)]
        if abnormal:
            default_questions.append(f"Could you explain what may have caused my {', '.join(abnormal[:2])} to be outside the reference range?")

    # Enforce strictly 3 to 6 questions
    selected_questions = default_questions[:5]

    return {
        "success": True,
        "data": {
            "questions": selected_questions,
        },
    }


@app.post("/api/feedback")
def submit_feedback(request: FeedbackRequest):
    """
    API-08 / TC-23: Optional user feedback collection.
    """
    # Privacy rule: Do not log or store any medical content
    logger.info(f"Feedback received with rating: {request.rating}")
    return {
        "success": True,
        "message": "Feedback submitted successfully",
    }
