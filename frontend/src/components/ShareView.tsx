import React, { useState } from 'react';
import { ReportResult } from '../../../shared/types';

interface Props {
  report: ReportResult;
  onRestart: () => void;
}

export const ShareView: React.FC<Props> = ({ report, onRestart }) => {
  const [downloadSuccess, setDownloadSuccess] = useState(false);

  const handleWhatsAppShare = () => {
    const summaryLines = [
      `*ReportSaathi Medical Summary* (Language: ${report.language})`,
      `----------------------------------------`,
      ...report.values.map(
        (v) => `• ${v.test}: ${v.value ?? '—'} ${v.unit || ''} [${v.status.replace('_', ' ').toUpperCase()}]`
      ),
      `----------------------------------------`,
      `*Questions for Doctor:*`,
      ...report.doctor_questions.map((q, i) => `${i + 1}. ${q}`),
      `----------------------------------------`,
      `_${report.disclaimer}_`,
    ];

    const shareText = encodeURIComponent(summaryLines.join('\n'));
    window.open(`https://wa.me/?text=${shareText}`, '_blank');
  };

  const handleDownloadPDF = () => {
    // Generate readable print view
    window.print();
    setDownloadSuccess(true);
    setTimeout(() => setDownloadSuccess(false), 3000);
  };

  return (
    <div className="card">
      <h2 style={{ fontSize: '1.25rem', color: 'var(--primary)', marginBottom: '0.5rem' }}>
        6. Share or Save Summary
      </h2>
      <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '1.5rem' }}>
        Take your plain-language explanation with you or share it with family and caregivers.
      </p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '2rem' }}>
        {/* WhatsApp Share Button */}
        <button
          onClick={handleWhatsAppShare}
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '0.5rem',
            backgroundColor: '#25d366',
            color: 'white',
            padding: '1rem',
            fontSize: '1rem',
            borderRadius: '8px',
          }}
        >
          <span style={{ fontSize: '1.25rem' }}>💬</span> Share via WhatsApp (Pre-filled)
        </button>

        {/* Download PDF / Print Button */}
        <button
          onClick={handleDownloadPDF}
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '0.5rem',
            backgroundColor: 'var(--primary)',
            color: 'white',
            padding: '1rem',
            fontSize: '1rem',
            borderRadius: '8px',
          }}
        >
          <span style={{ fontSize: '1.25rem' }}>📥</span> Download Summary as PDF
        </button>

        {downloadSuccess && (
          <div style={{ textAlign: 'center', color: '#15803d', fontSize: '0.9rem', fontWeight: 600 }}>
            ✓ Print/Save dialog opened successfully!
          </div>
        )}
      </div>

      <div style={{ borderTop: '1px solid var(--border)', paddingTop: '1.25rem', textAlign: 'center' }}>
        <button className="btn-secondary" onClick={onRestart}>
          Upload Another Report
        </button>
      </div>
    </div>
  );
};
