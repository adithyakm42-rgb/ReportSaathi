/**
 * ReportSaathi - Shared Type Contracts
 * Synchronizes frontend and backend data structures without drift.
 * Grounded in: docs/06c-api-contracts.md, docs/04-design.md, docs/06b-safety-rules.md
 */

export type SupportedLanguage = "en" | "hi" | "kn" | "English" | "Hindi" | "Kannada";

export type ReadingLevel = "simple" | "standard" | "detailed" | "Simple" | "Standard" | "Detailed";

export type ClinicalStatus =
  | "normal"
  | "borderline"
  | "needs_attention"
  | "no_range_on_report"
  | "critical_low"
  | "critical_high"
  | "unclear";

export type RedFlagSeverity = "CRITICAL_LOW" | "CRITICAL_HIGH" | "EMERGENCY";

export interface RedFlagAlert {
  test_name: string;
  value: number | string;
  unit: string;
  severity: RedFlagSeverity;
  clinical_concern: string;
  action_required: string;
}

export interface EmergencyActions {
  call_emergency: string;
  call_ambulance: string;
  find_hospital_url: string;
}

export interface BiomarkerValue {
  test: string;
  value: number | string | null;
  unit: string | null;
  range_on_report: string | null;
  range_low?: number | null;
  range_high?: number | null;
  status: ClinicalStatus;
  is_red_flag: boolean;
  explanation?: string;
  requires_user_correction?: boolean;
}

export interface PrescriptionMedicine {
  name: string;
  purpose: string;
  timing_as_written: string;
  watch_for: string[];
}

export interface ReportResult {
  report_id: string;
  status: "processing" | "ready" | "failed";
  language: SupportedLanguage;
  reading_level: ReadingLevel;
  is_red_flag: boolean;
  red_flags: RedFlagAlert[];
  values: BiomarkerValue[];
  medicines: PrescriptionMedicine[];
  doctor_questions: string[];
  disclaimer: string;
  emergency_actions?: EmergencyActions;
  emergency_message?: string;
}

export interface UserCorrectionPayload {
  test_name: string;
  corrected_value: number | string;
  corrected_range_low?: number;
  corrected_range_high?: number;
  corrected_range_on_report?: string;
}

export interface ApiSuccessResponse<T> {
  success: boolean;
  message?: string;
  data: T;
}

export interface ApiErrorResponse {
  success: false;
  message: string;
  error_code: string;
}
