import React from 'react';
import { ReportResult } from '../../../shared/types';

interface Props {
  report: ReportResult;
  onNext: () => void;
  onRestart: () => void;
}

export const ResultsView: React.FC<Props> = ({ report, onNext, onRestart }) => {
  const getBadgeClass = (status: string) => {
    switch (status) {
      case 'normal':
        return 'badge-normal';
      case 'borderline':
        return 'badge-borderline';
      case 'needs_attention':
        return 'badge-attention';
      case 'no_range_on_report':
      default:
        return 'badge-norange';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'normal':
        return '🟢 Normal';
      case 'borderline':
        return '🟡 Borderline';
      case 'needs_attention':
        return '🔴 Needs Attention';
      case 'no_range_on_report':
        return '⚪ No Range on Report';
      default:
        return status;
    }
  };

  return (
    <div>
      {/* Screen 5: Emergency Red-Flag Alert Banner (Rendered deterministically) */}
      {report.is_red_flag && (
        <div className="red-flag-banner">
          <h3>⚠️ Urgent Clinical Alert Detected</h3>
          <p style={{ marginBottom: '0.75rem', fontSize: '0.95rem' }}>
            {report.emergency_message || 'Your report contains values outside safe limits that warrant prompt medical evaluation.'}
          </p>
          {report.red_flags.map((rf, idx) => (
            <div key={idx} style={{ backgroundColor: 'white', padding: '0.75rem', borderRadius: '6px', marginBottom: '0.5rem', borderLeft: '4px solid var(--red-flag)' }}>
              <strong>{rf.test_name} ({rf.value} {rf.unit}):</strong> {rf.clinical_concern}
            </div>
          ))}
          <div style={{ display: 'flex', gap: '0.5rem', marginTop: '1rem' }}>
            <a
              href="tel:112"
              className="btn-primary"
              style={{ textAlign: 'center', textDecoration: 'none', backgroundColor: '#991b1b', padding: '0.65rem 1rem' }}
            >
              📞 Call Emergency (112)
            </a>
            <a
              href="https://www.google.com/maps/search/?api=1&query=hospital+near+me"
              target="_blank"
              rel="noreferrer"
              className="btn-secondary"
              style={{ textAlign: 'center', textDecoration: 'none', padding: '0.65rem 1rem' }}
            >
              🏥 Find Nearby Hospital
            </a>
          </div>
        </div>
      )}

      {/* Screen 4: Explanation Cards */}
      <div className="card">
        <h2 style={{ fontSize: '1.25rem', color: 'var(--primary)', marginBottom: '1rem' }}>
          4. Plain-Language Explanation
        </h2>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '1.5rem' }}>
          {report.values.map((v, i) => (
            <div
              key={i}
              style={{
                border: '1px solid var(--border)',
                borderRadius: '8px',
                padding: '1rem',
                backgroundColor: '#ffffff',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.4rem' }}>
                <div>
                  <span style={{ fontWeight: 700, fontSize: '1.05rem', color: 'var(--text-main)' }}>
                    {v.test}
                  </span>
                  <div style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                    Observed: <strong>{v.value ?? '—'} {v.unit}</strong>{' '}
                    {v.range_on_report ? `(Range: ${v.range_on_report})` : '(No range printed)'}
                  </div>
                </div>
                <span className={`badge ${getBadgeClass(v.status)}`}>
                  {getStatusLabel(v.status)}
                </span>
              </div>
              <p style={{ fontSize: '0.95rem', color: '#334155', marginTop: '0.5rem' }}>
                {v.explanation || 'Result evaluated against your printed reference range.'}
              </p>
            </div>
          ))}
        </div>

        {/* Medicines Section */}
        {report.medicines && report.medicines.length > 0 && (
          <div style={{ marginTop: '1.5rem', marginBottom: '1.5rem', borderTop: '1px solid var(--border)', paddingTop: '1.25rem' }}>
            <h3 style={{ fontSize: '1.1rem', color: 'var(--primary)', marginBottom: '0.75rem' }}>
              💊 Prescription Instructions
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {report.medicines.map((m, idx) => (
                <div key={idx} style={{ backgroundColor: '#f8fafc', padding: '0.85rem', borderRadius: '8px', border: '1px solid var(--border)' }}>
                  <div style={{ fontWeight: 700 }}>{m.name}</div>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '0.35rem' }}>
                    Timing as written: <strong>{m.timing_as_written}</strong>
                  </div>
                  <p style={{ fontSize: '0.9rem', marginBottom: '0.35rem' }}>{m.purpose}</p>
                  {m.watch_for && m.watch_for.length > 0 && (
                    <div style={{ fontSize: '0.85rem', color: '#475569' }}>
                      <em>Note:</em> {m.watch_for.join('. ')}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <button className="btn-secondary" onClick={onRestart} style={{ width: '35%' }}>
            Start Over
          </button>
          <button className="btn-primary" onClick={onNext} style={{ width: '65%' }}>
            View Doctor Questions →
          </button>
        </div>
      </div>
    </div>
  );
};
