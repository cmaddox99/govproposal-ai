'use client';

import { useCallback, useEffect, useRef, useState } from 'react';
import {
  AlertCircle,
  Download,
  FileText,
  Loader2,
  Paperclip,
  Trash2,
  Upload,
  X,
} from 'lucide-react';

import { opportunityDocumentsApi } from '@/lib/api';

interface OpportunityDocument {
  id: string;
  organization_id: string;
  opportunity_id: string;
  filename: string;
  content_type: string | null;
  size_bytes: number;
  description: string | null;
  uploaded_by: string | null;
  uploaded_at: string;
}

interface Props {
  orgId: string;
  opportunityId: string;
  opportunityTitle: string;
  onClose: () => void;
}

function formatBytes(bytes: number) {
  if (!bytes) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB'];
  let value = bytes;
  let unit = 0;
  while (value >= 1024 && unit < units.length - 1) {
    value /= 1024;
    unit += 1;
  }
  return `${value.toFixed(value >= 10 || unit === 0 ? 0 : 1)} ${units[unit]}`;
}

function formatDate(value: string) {
  return new Date(value).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  });
}

const ALLOWED_HINT = 'PDF, Word, Excel, text, CSV, or image — up to 25 MB';

export default function OpportunityDocumentsModal({
  orgId,
  opportunityId,
  opportunityTitle,
  onClose,
}: Props) {
  const [docs, setDocs] = useState<OpportunityDocument[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [description, setDescription] = useState('');
  const [dragOver, setDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const fetchDocs = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const res = await opportunityDocumentsApi.list(orgId, opportunityId);
      setDocs(res.data.items || []);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load documents');
    } finally {
      setLoading(false);
    }
  }, [orgId, opportunityId]);

  useEffect(() => {
    fetchDocs();
  }, [fetchDocs]);

  const handleFileChosen = (file: File | null) => {
    if (!file) return;
    if (file.size > 25 * 1024 * 1024) {
      setError('File exceeds 25 MB limit');
      return;
    }
    setError('');
    setSelectedFile(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    setUploading(true);
    setError('');
    try {
      await opportunityDocumentsApi.upload(
        orgId,
        opportunityId,
        selectedFile,
        description.trim() || undefined,
      );
      setSelectedFile(null);
      setDescription('');
      if (fileInputRef.current) fileInputRef.current.value = '';
      await fetchDocs();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Upload failed');
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (doc: OpportunityDocument) => {
    if (!window.confirm(`Remove ${doc.filename}?`)) return;
    setError('');
    try {
      await opportunityDocumentsApi.remove(orgId, opportunityId, doc.id);
      setDocs((prev) => prev.filter((d) => d.id !== doc.id));
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Delete failed');
    }
  };

  const handleDownload = (doc: OpportunityDocument) => {
    const url = opportunityDocumentsApi.downloadUrl(orgId, opportunityId, doc.id);
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    // The backend FileResponse requires an Authorization header, which a plain
    // <a> tag can't supply. Fetch as a blob then trigger a download.
    fetch(url, { headers: token ? { Authorization: `Bearer ${token}` } : undefined })
      .then(async (response) => {
        if (!response.ok) throw new Error('Download failed');
        const blob = await response.blob();
        const objectUrl = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = objectUrl;
        link.download = doc.filename;
        document.body.appendChild(link);
        link.click();
        link.remove();
        URL.revokeObjectURL(objectUrl);
      })
      .catch((err) => setError(err.message || 'Download failed'));
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div className="w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col bg-[#0f1115] border border-white/[0.08] rounded-xl shadow-2xl">
        <div className="flex items-start justify-between gap-4 px-6 py-4 border-b border-white/[0.06]">
          <div className="min-w-0">
            <div className="flex items-center gap-2 text-emerald-400 text-xs font-medium uppercase tracking-wide mb-1">
              <Paperclip className="w-3.5 h-3.5" />
              Opportunity documents
            </div>
            <h2 className="text-lg font-semibold text-white truncate" title={opportunityTitle}>
              {opportunityTitle}
            </h2>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white p-1 -m-1"
            aria-label="Close"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-6 py-5 space-y-5">
          {error && (
            <div className="flex items-start gap-2 text-red-300 bg-red-900/20 border border-red-800/60 p-3 rounded-lg text-sm">
              <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
              {error}
            </div>
          )}

          <div
            onDragOver={(e) => {
              e.preventDefault();
              setDragOver(true);
            }}
            onDragLeave={() => setDragOver(false)}
            onDrop={(e) => {
              e.preventDefault();
              setDragOver(false);
              const file = e.dataTransfer.files?.[0];
              if (file) handleFileChosen(file);
            }}
            className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors ${
              dragOver
                ? 'border-emerald-400 bg-emerald-500/5'
                : 'border-white/[0.12] hover:border-white/[0.18] bg-white/[0.02]'
            }`}
          >
            <Upload className="w-8 h-8 text-gray-500 mx-auto mb-3" />
            <p className="text-sm text-gray-300 mb-1">
              Drop a file here, or{' '}
              <button
                type="button"
                className="text-emerald-400 hover:text-emerald-300 underline"
                onClick={() => fileInputRef.current?.click()}
              >
                browse
              </button>
            </p>
            <p className="text-xs text-gray-500">{ALLOWED_HINT}</p>
            <input
              ref={fileInputRef}
              type="file"
              className="hidden"
              accept=".pdf,.doc,.docx,.xls,.xlsx,.txt,.csv,.png,.jpg,.jpeg"
              onChange={(e) => handleFileChosen(e.target.files?.[0] ?? null)}
            />
          </div>

          {selectedFile && (
            <div className="bg-white/[0.04] border border-white/[0.08] rounded-lg p-4 space-y-3">
              <div className="flex items-center justify-between gap-3">
                <div className="flex items-center gap-2 min-w-0">
                  <FileText className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                  <span className="text-sm text-white truncate" title={selectedFile.name}>
                    {selectedFile.name}
                  </span>
                  <span className="text-xs text-gray-500 flex-shrink-0">
                    {formatBytes(selectedFile.size)}
                  </span>
                </div>
                <button
                  onClick={() => {
                    setSelectedFile(null);
                    if (fileInputRef.current) fileInputRef.current.value = '';
                  }}
                  className="text-gray-400 hover:text-white text-xs"
                  disabled={uploading}
                >
                  Remove
                </button>
              </div>
              <input
                type="text"
                placeholder="Description (optional)"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded text-sm text-white placeholder-gray-500 focus:ring-1 focus:ring-emerald-500 focus:border-transparent"
                disabled={uploading}
              />
              <button
                onClick={handleUpload}
                disabled={uploading}
                className="flex items-center justify-center gap-2 w-full px-4 py-2 bg-gradient-to-r from-emerald-500 to-blue-500 text-white text-sm font-medium rounded-lg hover:from-emerald-600 hover:to-blue-600 disabled:opacity-50"
              >
                {uploading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    Uploading…
                  </>
                ) : (
                  <>
                    <Upload className="w-4 h-4" />
                    Upload
                  </>
                )}
              </button>
            </div>
          )}

          <div>
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium text-gray-300">Attached documents</h3>
              <span className="text-xs text-gray-500">{docs.length}</span>
            </div>
            {loading ? (
              <div className="text-center py-8 text-gray-500 text-sm">
                <Loader2 className="w-5 h-5 animate-spin mx-auto mb-2" />
                Loading…
              </div>
            ) : docs.length === 0 ? (
              <div className="text-center py-8 text-gray-500 text-sm border border-dashed border-white/[0.06] rounded-lg">
                No documents yet. Upload an RFP, attachment, or supporting file.
              </div>
            ) : (
              <ul className="space-y-2">
                {docs.map((doc) => (
                  <li
                    key={doc.id}
                    className="flex items-center justify-between gap-3 px-3 py-2.5 bg-white/[0.03] border border-white/[0.06] rounded-lg"
                  >
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-2 min-w-0">
                        <FileText className="w-4 h-4 text-gray-400 flex-shrink-0" />
                        <span
                          className="text-sm text-white truncate"
                          title={doc.filename}
                        >
                          {doc.filename}
                        </span>
                      </div>
                      <div className="text-xs text-gray-500 mt-0.5 ml-6">
                        {formatBytes(doc.size_bytes)} · uploaded {formatDate(doc.uploaded_at)}
                      </div>
                      {doc.description && (
                        <div className="text-xs text-gray-400 mt-0.5 ml-6 italic">
                          {doc.description}
                        </div>
                      )}
                    </div>
                    <div className="flex items-center gap-1 flex-shrink-0">
                      <button
                        onClick={() => handleDownload(doc)}
                        className="text-gray-400 hover:text-white p-1.5 rounded hover:bg-white/[0.06]"
                        title="Download"
                      >
                        <Download className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDelete(doc)}
                        className="text-gray-400 hover:text-red-400 p-1.5 rounded hover:bg-white/[0.06]"
                        title="Delete"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        <div className="px-6 py-4 border-t border-white/[0.06] bg-white/[0.02] flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-white/[0.06] hover:bg-white/[0.1] text-gray-200 text-sm rounded-lg"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
}
