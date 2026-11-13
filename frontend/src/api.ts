/**
 * ReportSaathi - Frontend API Client
 * Connects to FastAPI backend with strict offline/empty safety checks.
 * Medical Safety Rule: Never display mock lab values for arbitrary custom image uploads.
 */

import { ReportResult, UserCorrectionPayload } from '../../shared/types';
import sampleReport from '../../shared/sample-report.json';

const API_BASE = (import.meta as any).env?.VITE_API_URL || 'http://127.0.0.1:8000';

export async function checkBackendHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/api/health`, { method: 'GET' });
    return res.ok;
  } catch {
    return false;
  }
}

export async function uploadReportFile(
  file: File,
  language: string,
  readingLevel: string
): Promise<{ document_id: string; status: string; is_sample?: boolean }> {
  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('language', language);
    formData.append('reading_level', readingLevel);

    const res = await fetch(`${API_BASE}/api/upload`, {
      method: 'POST',
      body: formData,
    });

    if (res.ok) {
      const data = await res.json();
      return data.data;
    } else {
      const errJson = await res.json().catch(() => ({}));
      throw new Error(errJson.message || `Server error: ${res.status}`);
    }
  } catch (err: any) {
    if (err.message && !err.message.includes('Failed to fetch') && !err.message.includes('NetworkError')) {
      throw err;
    }
    // Medical Safety: Backend is offline. Do NOT pretend we extracted data from this file!
    throw new Error(
      'The backend API server (http://127.0.0.1:8000) is currently offline. Real OCR processing on custom files requires the backend. To preview the interface, click "Test with verified sample report".'
    );
  }
}

export async function fetchReportResults(documentId: string): Promise<ReportResult> {
  // If explicitly requesting the verified sample report
  if (documentId === 'sample-demo-report') {
    return sampleReport as unknown as ReportResult;
  }

  try {
    const res = await fetch(`${API_BASE}/api/reports/${documentId}`);
    if (res.ok) {
      const json = await res.json();
      return json.data || json;
    }
    throw new Error(`Failed to retrieve report data (${res.status})`);
  } catch (err: any) {
    throw new Error(
      err.message || 'Could not connect to backend to fetch processed report data.'
    );
  }
}

export async function submitCorrections(
  documentId: string,
  corrections: UserCorrectionPayload[]
): Promise<boolean> {
  if (documentId === 'sample-demo-report') {
    return true;
  }

  try {
    const res = await fetch(`${API_BASE}/api/extract/${documentId}/corrections`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ corrections }),
    });
    return res.ok;
  } catch (err) {
    return false;
  }
}
