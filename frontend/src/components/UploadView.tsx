import React, { useState, useEffect } from 'react';
import { checkBackendHealth } from '../api';

interface Props {
  onFileUpload: (file: File) => void;
  onUseSample: () => void;
  onBack: () => void;
}

const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10 MB

export const UploadView: React.FC<Props> = ({ onFileUpload, onUseSample, onBack }) => {
  const [error, setError] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null);

  useEffect(() => {
    checkBackendHealth().then(setBackendOnline);
  }, []);

  const handleFile = (file: File) => {
    setError(null);
    if (file.size > MAX_FILE_SIZE) {
      setError('File size exceeds the 10 MB limit. Please upload a smaller file or clearer crop.');
      return;
    }
    const validTypes = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf'];
    if (!validTypes.includes(file.type) && !file.name.match(/\.(pdf|jpg|jpeg|png)$/i)) {
      setError('Unsupported file type. Please upload a PDF, JPG, or PNG report.');
      return;
    }
    onFileUpload(file);
  };

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
        <h2 style={{ fontSize: '1.25rem', color: 'var(--primary)' }}>
          2. Upload Medical Report
        </h2>
        <span
          style={{
            fontSize: '0.75rem',
            padding: '0.2rem 0.5rem',
            borderRadius: '4px',
            fontWeight: 600,
            backgroundColor: backendOnline ? '#dcfce7' : '#fef3c7',
            color: backendOnline ? '#15803d' : '#b45309',
            border: backendOnline ? '1px solid #bbf7d0' : '1px solid #fde68a',
          }}
        >
          {backendOnline === null ? 'Checking API...' : backendOnline ? '● Backend API Online' : '○ Backend Offline (Demo Mode)'}
        </span>
      </div>

      <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: '1.25rem' }}>
        Upload a clear lab report photo or PDF (max 10 MB).
      </p>

      {error && (
        <div style={{ padding: '0.85rem', backgroundColor: '#fef2f2', border: '1px solid #fecaca', borderRadius: '8px', color: '#b91c1c', marginBottom: '1rem', fontSize: '0.9rem', lineHeight: 1.4 }}>
          {error}
        </div>
      )}

      {/* Drag & Drop Area */}
      <div
        onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setIsDragging(false);
          if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
          }
        }}
        style={{
          border: isDragging ? '2px dashed var(--accent)' : '2px dashed var(--border)',
          borderRadius: '12px',
          padding: '2.5rem 1rem',
          textAlign: 'center',
          backgroundColor: isDragging ? '#f0fdfa' : '#fafafa',
          cursor: 'pointer',
          marginBottom: '1.5rem',
        }}
        onClick={() => {
          const input = document.getElementById('report-file-input') as HTMLInputElement;
          input?.click();
        }}
      >
        <div style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>📄</div>
        <div style={{ fontWeight: 600, color: 'var(--primary)', marginBottom: '0.25rem' }}>
          Click to choose or drag & drop file
        </div>
        <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
          Supports PDF, JPG, PNG (up to 10 MB)
        </div>
        <input
          id="report-file-input"
          type="file"
          accept=".pdf,.jpg,.jpeg,.png"
          style={{ display: 'none' }}
          onChange={(e) => {
            if (e.target.files && e.target.files[0]) {
              handleFile(e.target.files[0]);
            }
          }}
        />
      </div>

      {/* Distinct Sample Report Button */}
      <div style={{ backgroundColor: '#f8fafc', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border)', marginBottom: '1.5rem', textAlign: 'center' }}>
        <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
          Want to test the full explanation & doctor questions without a real report?
        </div>
        <button
          type="button"
          onClick={onUseSample}
          className="btn-secondary"
          style={{ width: '100%', borderColor: 'var(--accent)', color: 'var(--accent)', fontWeight: 600 }}
        >
          🧪 Test with Verified Sample CBC Report →
        </button>
      </div>

      <div style={{ display: 'flex', gap: '0.75rem' }}>
        <button className="btn-secondary" onClick={onBack} style={{ width: '40%' }}>
          ← Back
        </button>
      </div>
    </div>
  );
};
