import React, { useState } from 'react';

interface Props {
  questions: string[];
  onNext: () => void;
  onBack: () => void;
}

export const DoctorQuestionsView: React.FC<Props> = ({ questions, onNext, onBack }) => {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const copyQuestion = (q: string, idx: number) => {
    navigator.clipboard.writeText(q);
    setCopiedIndex(idx);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const copyAll = () => {
    const text = questions.map((q, i) => `${i + 1}. ${q}`).join('\n');
    navigator.clipboard.writeText(text);
    setCopiedIndex(999);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h2 style={{ fontSize: '1.25rem', color: 'var(--primary)' }}>
          5. Questions for Your Doctor
        </h2>
        <button
          type="button"
          onClick={copyAll}
          style={{
            fontSize: '0.85rem',
            padding: '0.35rem 0.65rem',
            backgroundColor: copiedIndex === 999 ? '#dcfce7' : '#f1f5f9',
            color: copiedIndex === 999 ? '#15803d' : 'var(--text-main)',
            border: '1px solid var(--border)',
          }}
        >
          {copiedIndex === 999 ? '✓ Copied All' : '📋 Copy All'}
        </button>
      </div>

      <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '1.25rem' }}>
        These tailored questions help you have an informed discussion during your next medical appointment:
      </p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', marginBottom: '1.5rem' }}>
        {questions.map((q, idx) => (
          <div
            key={idx}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              backgroundColor: '#f8fafc',
              border: '1px solid var(--border)',
              borderRadius: '8px',
              padding: '0.85rem',
              gap: '0.75rem',
            }}
          >
            <div style={{ fontSize: '0.95rem', color: 'var(--text-main)', lineHeight: 1.4 }}>
              <strong style={{ color: 'var(--primary)', marginRight: '0.35rem' }}>{idx + 1}.</strong>
              {q}
            </div>
            <button
              type="button"
              onClick={() => copyQuestion(q, idx)}
              style={{
                fontSize: '0.8rem',
                padding: '0.3rem 0.5rem',
                backgroundColor: copiedIndex === idx ? '#dcfce7' : 'white',
                color: copiedIndex === idx ? '#15803d' : 'var(--text-muted)',
                border: '1px solid var(--border)',
                flexShrink: 0,
              }}
            >
              {copiedIndex === idx ? '✓' : 'Copy'}
            </button>
          </div>
        ))}
      </div>

      <div style={{ display: 'flex', gap: '0.75rem' }}>
        <button className="btn-secondary" onClick={onBack} style={{ width: '35%' }}>
          ← Back
        </button>
        <button className="btn-primary" onClick={onNext} style={{ width: '65%' }}>
          Share or Download Summary →
        </button>
      </div>
    </div>
  );
};
