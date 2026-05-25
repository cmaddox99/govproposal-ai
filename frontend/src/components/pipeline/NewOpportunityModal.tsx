'use client';

import { useRef, useState } from 'react';
import {
  AlertCircle,
  FileText,
  Loader2,
  Save,
  Sparkles,
  Upload,
  X,
} from 'lucide-react';

import { opportunitiesApi, pipelineApi } from '@/lib/api';

interface Props {
  orgId: string;
  market: 'federal' | 'sled';
  mode: 'manual' | 'smart';
  onClose: () => void;
  onCreated: () => void; // refresh callback for the parent list
}

interface FormState {
  title: string;
  solicitation_number: string;
  agency: string;
  department: string;
  office: string;
  naics_code: string;
  set_aside_type: string;
  notice_type: string;
  response_deadline: string; // datetime-local
  posted_date: string; // date
  estimated_value: string;
  place_of_performance_city: string;
  place_of_performance_state: string;
  primary_contact_name: string;
  primary_contact_email: string;
  primary_contact_phone: string;
  description: string;
  sam_url: string;
}

const EMPTY: FormState = {
  title: '',
  solicitation_number: '',
  agency: '',
  department: '',
  office: '',
  naics_code: '',
  set_aside_type: '',
  notice_type: 'solicitation',
  response_deadline: '',
  posted_date: '',
  estimated_value: '',
  place_of_performance_city: '',
  place_of_performance_state: '',
  primary_contact_name: '',
  primary_contact_email: '',
  primary_contact_phone: '',
  description: '',
  sam_url: '',
};

function toDateTimeLocal(iso: string | null | undefined): string {
  if (!iso) return '';
  // datetime-local wants "YYYY-MM-DDTHH:MM"
  const d = new Date(iso);
  if (isNaN(d.getTime())) return '';
  const pad = (n: number) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

function toDateOnly(iso: string | null | undefined): string {
  if (!iso) return '';
  const d = new Date(iso);
  if (isNaN(d.getTime())) return '';
  const pad = (n: number) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

const SET_ASIDE_OPTIONS = [
  { value: '', label: 'Full and open (no set-aside)' },
  { value: 'sba', label: 'Small Business (SBA)' },
  { value: 'sbsa', label: 'Partial Small Business' },
  { value: 'wosb', label: 'Women-Owned Small Business' },
  { value: 'edwosb', label: 'Economically Disadvantaged WOSB' },
  { value: 'sdvosb', label: 'Service-Disabled Veteran-Owned' },
  { value: 'hubzone', label: 'HUBZone' },
  { value: '8a', label: '8(a)' },
];

const NOTICE_TYPE_OPTIONS = [
  { value: 'solicitation', label: 'Solicitation' },
  { value: 'presolicitation', label: 'Presolicitation' },
  { value: 'combined_synopsis', label: 'Combined Synopsis / Solicitation' },
  { value: 'sources_sought', label: 'Sources Sought' },
  { value: 'special_notice', label: 'Special Notice' },
];

export default function NewOpportunityModal({ orgId, market, mode, onClose, onCreated }: Props) {
  const [form, setForm] = useState<FormState>(EMPTY);
  const [extracting, setExtracting] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [extractionBanner, setExtractionBanner] = useState<string | null>(null);
  const [stage, setStage] = useState<'pick' | 'form'>(mode === 'manual' ? 'form' : 'pick');
  const [sourceDocument, setSourceDocument] = useState<{
    path: string;
    filename: string;
    content_type: string | null;
  } | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const set = <K extends keyof FormState>(key: K, value: FormState[K]) =>
    setForm((prev) => ({ ...prev, [key]: value }));

  const handleFile = async (file: File | null) => {
    if (!file) return;
    if (file.size > 25 * 1024 * 1024) {
      setError('File exceeds 25 MB limit');
      return;
    }
    setError('');
    setExtracting(true);
    try {
      const res = await opportunitiesApi.extract(orgId, file);
      const data = res.data;
      const ex = data.extracted || {};
      setForm({
        title: ex.title || '',
        solicitation_number: ex.solicitation_number || '',
        agency: ex.agency || '',
        department: ex.department || '',
        office: ex.office || '',
        naics_code: ex.naics_code || '',
        set_aside_type: ex.set_aside_type || '',
        notice_type: ex.notice_type || 'solicitation',
        response_deadline: toDateTimeLocal(ex.response_deadline),
        posted_date: toDateOnly(ex.posted_date),
        estimated_value: ex.estimated_value != null ? String(ex.estimated_value) : '',
        place_of_performance_city: ex.place_of_performance_city || '',
        place_of_performance_state: ex.place_of_performance_state || '',
        primary_contact_name: ex.primary_contact_name || '',
        primary_contact_email: ex.primary_contact_email || '',
        primary_contact_phone: ex.primary_contact_phone || '',
        description: ex.description || '',
        sam_url: ex.sam_url || '',
      });
      setSourceDocument({
        path: data.source_document_path,
        filename: data.source_document_filename,
        content_type: data.source_document_content_type ?? null,
      });
      if (data.extraction_available) {
        const filled = Object.values(ex).filter((v) => v != null && v !== '').length;
        setExtractionBanner(`Extracted ${filled} field${filled === 1 ? '' : 's'} from ${data.source_document_filename}. Review and edit before saving.`);
      } else {
        setExtractionBanner(`Couldn't read content from ${data.source_document_filename}. The doc is attached — fill in the fields manually below.`);
      }
      setStage('form');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to extract from document');
    } finally {
      setExtracting(false);
    }
  };

  const handleSave = async () => {
    if (!form.title.trim()) {
      setError('Title is required');
      return;
    }
    setSaving(true);
    setError('');
    try {
      const payload: Record<string, any> = {
        organization_id: orgId,
        market,
        title: form.title.trim(),
        notice_type: form.notice_type || 'solicitation',
      };
      // Optional fields
      const optional: Array<[keyof FormState, string]> = [
        ['solicitation_number', 'solicitation_number'],
        ['agency', 'agency'],
        ['department', 'department'],
        ['office', 'office'],
        ['naics_code', 'naics_code'],
        ['set_aside_type', 'set_aside_type'],
        ['place_of_performance_city', 'place_of_performance_city'],
        ['place_of_performance_state', 'place_of_performance_state'],
        ['primary_contact_name', 'primary_contact_name'],
        ['primary_contact_email', 'primary_contact_email'],
        ['primary_contact_phone', 'primary_contact_phone'],
        ['description', 'description'],
        ['sam_url', 'sam_url'],
      ];
      for (const [k, apiKey] of optional) {
        if (form[k]) payload[apiKey] = form[k];
      }
      if (form.response_deadline) {
        payload.response_deadline = new Date(form.response_deadline).toISOString();
      }
      if (form.posted_date) {
        payload.posted_date = new Date(form.posted_date).toISOString();
      }
      if (form.estimated_value) {
        const n = Number(form.estimated_value);
        if (!isNaN(n)) payload.estimated_value = n;
      }
      if (sourceDocument) {
        payload.source_document_path = sourceDocument.path;
        payload.source_document_filename = sourceDocument.filename;
        payload.source_document_content_type = sourceDocument.content_type;
      }

      const oppRes = await opportunitiesApi.create(payload);
      const oppId = oppRes.data.id;

      await pipelineApi.add({
        organization_id: orgId,
        opportunity_id: oppId,
      });

      onCreated();
      onClose();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save opportunity');
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div className="w-full max-w-3xl max-h-[90vh] overflow-hidden flex flex-col bg-[#0f1115] border border-white/[0.08] rounded-xl shadow-2xl">
        <div className="flex items-start justify-between gap-4 px-6 py-4 border-b border-white/[0.06]">
          <div>
            <div className="flex items-center gap-2 text-emerald-400 text-xs font-medium uppercase tracking-wide mb-1">
              {mode === 'smart' ? <Sparkles className="w-3.5 h-3.5" /> : <FileText className="w-3.5 h-3.5" />}
              {mode === 'smart' ? 'Smart Upload' : 'Add Opportunity Manually'}
            </div>
            <h2 className="text-lg font-semibold text-white">
              {stage === 'pick' ? 'Upload a solicitation document' : 'Review opportunity details'}
            </h2>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-white p-1 -m-1" aria-label="Close">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto px-6 py-5 space-y-4">
          {error && (
            <div className="flex items-start gap-2 text-red-300 bg-red-900/20 border border-red-800/60 p-3 rounded-lg text-sm">
              <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
              {error}
            </div>
          )}

          {stage === 'pick' && (
            <div
              className="border-2 border-dashed border-white/[0.12] hover:border-white/[0.18] bg-white/[0.02] rounded-lg p-8 text-center"
            >
              <Upload className="w-10 h-10 text-gray-500 mx-auto mb-3" />
              <p className="text-sm text-gray-300 mb-1">
                Drop an RFP / solicitation here, or{' '}
                <button
                  type="button"
                  className="text-emerald-400 hover:text-emerald-300 underline"
                  onClick={() => fileInputRef.current?.click()}
                  disabled={extracting}
                >
                  browse
                </button>
              </p>
              <p className="text-xs text-gray-500">PDF, Word, or text — up to 25 MB. Claude will extract title, agency, NAICS, deadline, and more.</p>
              <input
                ref={fileInputRef}
                type="file"
                className="hidden"
                accept=".pdf,.doc,.docx,.txt,.csv"
                onChange={(e) => handleFile(e.target.files?.[0] ?? null)}
              />
              {extracting && (
                <div className="flex items-center justify-center gap-2 mt-4 text-sm text-emerald-300">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  Extracting fields…
                </div>
              )}
              <div className="mt-6 pt-4 border-t border-white/[0.06]">
                <button
                  type="button"
                  onClick={() => setStage('form')}
                  className="text-xs text-gray-400 hover:text-white underline"
                >
                  Skip and fill in manually
                </button>
              </div>
            </div>
          )}

          {stage === 'form' && (
            <>
              {extractionBanner && (
                <div className="flex items-start gap-2 text-emerald-200 bg-emerald-900/20 border border-emerald-800/60 p-3 rounded-lg text-xs">
                  <Sparkles className="w-4 h-4 flex-shrink-0 mt-0.5 text-emerald-400" />
                  <div className="flex-1">
                    {extractionBanner}
                    {sourceDocument && (
                      <button
                        type="button"
                        className="ml-2 text-emerald-400 hover:text-emerald-300 underline"
                        onClick={() => {
                          setSourceDocument(null);
                          setExtractionBanner('Source document detached. It will not be saved with the opportunity.');
                        }}
                      >
                        Detach source doc
                      </button>
                    )}
                  </div>
                </div>
              )}

              <div className="grid grid-cols-1 gap-3">
                <Field label="Title *" required>
                  <input type="text" value={form.title} onChange={(e) => set('title', e.target.value)} className={inputCls} placeholder="e.g. Cybersecurity Operations Support Services" />
                </Field>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <Field label="Solicitation number">
                  <input type="text" value={form.solicitation_number} onChange={(e) => set('solicitation_number', e.target.value)} className={inputCls} />
                </Field>
                <Field label="NAICS code">
                  <input type="text" value={form.naics_code} onChange={(e) => set('naics_code', e.target.value)} className={inputCls} placeholder="e.g. 541512" />
                </Field>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <Field label="Agency">
                  <input type="text" value={form.agency} onChange={(e) => set('agency', e.target.value)} className={inputCls} />
                </Field>
                <Field label="Office">
                  <input type="text" value={form.office} onChange={(e) => set('office', e.target.value)} className={inputCls} />
                </Field>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <Field label="Notice type">
                  <select value={form.notice_type} onChange={(e) => set('notice_type', e.target.value)} className={inputCls}>
                    {NOTICE_TYPE_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
                  </select>
                </Field>
                <Field label="Set-aside">
                  <select value={form.set_aside_type} onChange={(e) => set('set_aside_type', e.target.value)} className={inputCls}>
                    {SET_ASIDE_OPTIONS.map((o) => <option key={o.value} value={o.value}>{o.label}</option>)}
                  </select>
                </Field>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <Field label="Response deadline">
                  <input type="datetime-local" value={form.response_deadline} onChange={(e) => set('response_deadline', e.target.value)} className={inputCls} />
                </Field>
                <Field label="Estimated value (USD)">
                  <input type="number" value={form.estimated_value} onChange={(e) => set('estimated_value', e.target.value)} className={inputCls} placeholder="e.g. 500000" />
                </Field>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <Field label="Place of performance: city">
                  <input type="text" value={form.place_of_performance_city} onChange={(e) => set('place_of_performance_city', e.target.value)} className={inputCls} />
                </Field>
                <Field label="State">
                  <input type="text" value={form.place_of_performance_state} onChange={(e) => set('place_of_performance_state', e.target.value)} className={inputCls} />
                </Field>
              </div>

              <div className="grid grid-cols-1 gap-3">
                <Field label="Contact name">
                  <input type="text" value={form.primary_contact_name} onChange={(e) => set('primary_contact_name', e.target.value)} className={inputCls} />
                </Field>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <Field label="Contact email">
                  <input type="email" value={form.primary_contact_email} onChange={(e) => set('primary_contact_email', e.target.value)} className={inputCls} />
                </Field>
                <Field label="Contact phone">
                  <input type="tel" value={form.primary_contact_phone} onChange={(e) => set('primary_contact_phone', e.target.value)} className={inputCls} />
                </Field>
              </div>

              <Field label="SAM.gov URL (optional)">
                <input type="url" value={form.sam_url} onChange={(e) => set('sam_url', e.target.value)} className={inputCls} placeholder="https://sam.gov/opp/..." />
              </Field>

              <Field label="Description">
                <textarea value={form.description} onChange={(e) => set('description', e.target.value)} className={`${inputCls} min-h-[100px]`} placeholder="Scope of work, key requirements, evaluation factors…" />
              </Field>
            </>
          )}
        </div>

        {stage === 'form' && (
          <div className="px-6 py-4 border-t border-white/[0.06] bg-white/[0.02] flex justify-between gap-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 bg-white/[0.06] hover:bg-white/[0.1] text-gray-200 text-sm rounded-lg"
              disabled={saving}
            >
              Cancel
            </button>
            <button
              type="button"
              onClick={handleSave}
              disabled={saving || !form.title.trim()}
              className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-emerald-500 to-blue-500 text-white text-sm font-medium rounded-lg hover:from-emerald-600 hover:to-blue-600 disabled:opacity-50"
            >
              {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
              {saving ? 'Saving…' : 'Save & add to pipeline'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

const inputCls =
  'w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded text-sm text-white placeholder-gray-500 focus:ring-1 focus:ring-emerald-500 focus:border-transparent';

function Field({
  label,
  required,
  children,
}: {
  label: string;
  required?: boolean;
  children: React.ReactNode;
}) {
  return (
    <label className="block">
      <span className={`block text-xs mb-1 ${required ? 'text-white' : 'text-gray-400'}`}>{label}</span>
      {children}
    </label>
  );
}
