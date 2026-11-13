import React from 'react';
import { SupportedLanguage, ReadingLevel } from '../../../shared/types';

interface Props {
  selectedLanguage: SupportedLanguage;
  selectedLevel: ReadingLevel;
  onLanguageChange: (lang: SupportedLanguage) => void;
  onLevelChange: (level: ReadingLevel) => void;
  onNext: () => void;
}

const LANGUAGES = [
  { id: 'en', label: 'English', sub: 'Default' },
  { id: 'hi', label: 'हिन्दी (Hindi)', sub: 'सरल भाषा' },
  { id: 'kn', label: 'ಕನ್ನಡ (Kannada)', sub: 'ಸುಲಭ ಭಾಷೆ' },
];

const LEVELS = [
  { id: 'simple', label: 'Simple', desc: 'Everyday words with zero complex medical jargon.' },
  { id: 'standard', label: 'Standard', desc: 'Balanced explanation with common clinical terms.' },
  { id: 'detailed', label: 'Detailed', desc: 'In-depth breakdown of physiological markers.' },
];

export const LanguageSelector: React.FC<Props> = ({
  selectedLanguage,
  selectedLevel,
  onLanguageChange,
  onLevelChange,
  onNext,
}) => {
  return (
    <div className="card">
      <h2 style={{ fontSize: '1.25rem', marginBottom: '1rem', color: 'var(--primary)' }}>
        1. Choose Language & Reading Level
      </h2>

      <div style={{ marginBottom: '1.5rem' }}>
        <label style={{ display: 'block', fontWeight: 600, marginBottom: '0.5rem' }}>
          Preferred Language
        </label>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: '0.75rem' }}>
          {LANGUAGES.map((lang) => (
            <button
              key={lang.id}
              type="button"
              onClick={() => onLanguageChange(lang.id as SupportedLanguage)}
              style={{
                padding: '0.85rem',
                border: selectedLanguage === lang.id ? '2px solid var(--primary)' : '1px solid var(--border)',
                backgroundColor: selectedLanguage === lang.id ? '#eff6ff' : 'white',
                color: selectedLanguage === lang.id ? 'var(--primary)' : 'var(--text-main)',
                textAlign: 'left',
              }}
            >
              <div style={{ fontWeight: 700 }}>{lang.label}</div>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{lang.sub}</div>
            </button>
          ))}
        </div>
      </div>

      <div style={{ marginBottom: '1.75rem' }}>
        <label style={{ display: 'block', fontWeight: 600, marginBottom: '0.5rem' }}>
          Explanation Depth
        </label>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {LEVELS.map((lvl) => (
            <button
              key={lvl.id}
              type="button"
              onClick={() => onLevelChange(lvl.id as ReadingLevel)}
              style={{
                padding: '0.85rem',
                border: selectedLevel === lvl.id ? '2px solid var(--primary)' : '1px solid var(--border)',
                backgroundColor: selectedLevel === lvl.id ? '#eff6ff' : 'white',
                textAlign: 'left',
              }}
            >
              <div style={{ fontWeight: 700, color: 'var(--primary)' }}>{lvl.label}</div>
              <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>{lvl.desc}</div>
            </button>
          ))}
        </div>
      </div>

      <button className="btn-primary" onClick={onNext}>
        Continue to Upload Report →
      </button>
    </div>
  );
};
