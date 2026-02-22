'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import {
  ArrowLeft,
  Save,
  Trash2,
  AlertCircle,
  CheckCircle,
  BarChart3,
  FileText,
  Settings,
  Sparkles,
  Download,
  Loader2,
  RefreshCw,
} from 'lucide-react';
import { proposalsApi } from '@/lib/api';
import { Proposal, ProposalStatus } from '@/types';

type SectionKey = 'executive_summary' | 'technical_approach' | 'management_approach' | 'past_performance' | 'pricing_summary';

const sectionConfig: { key: SectionKey; label: string; placeholder: string; rows: number }[] = [
  { key: 'executive_summary', label: 'Executive Summary', placeholder: 'Write the executive summary for your proposal...', rows: 10 },
  { key: 'technical_approach', label: 'Technical Approach', placeholder: 'Describe the technical approach and methodology...', rows: 10 },
  { key: 'management_approach', label: 'Management Approach', placeholder: 'Outline the management structure and staffing plan...', rows: 10 },
  { key: 'past_performance', label: 'Past Performance', placeholder: 'Detail relevant past performance and references...', rows: 10 },
  { key: 'pricing_summary', label: 'Pricing Summary', placeholder: 'Provide the pricing breakdown and cost justification...', rows: 10 },
];

const statusColors: Record<ProposalStatus, string> = {
  draft: 'bg-gray-600/20 text-gray-400',
  in_progress: 'bg-blue-600/20 text-blue-400',
  review: 'bg-purple-600/20 text-purple-400',
  submitted: 'bg-green-600/20 text-green-400',
  awarded: 'bg-emerald-600/20 text-emerald-400',
  not_awarded: 'bg-red-600/20 text-red-400',
  cancelled: 'bg-yellow-600/20 text-yellow-400',
};

const statusLabels: Record<ProposalStatus, string> = {
  draft: 'Draft',
  in_progress: 'In Progress',
  review: 'Review',
  submitted: 'Submitted',
  awarded: 'Awarded',
  not_awarded: 'Not Awarded',
  cancelled: 'Cancelled',
};

const allStatuses: ProposalStatus[] = [
  'draft',
  'in_progress',
  'review',
  'submitted',
  'awarded',
  'not_awarded',
  'cancelled',
];

export default function ProposalDetailPage() {
  const params = useParams();
  const router = useRouter();
  const proposalId = params.id as string;

  const [proposal, setProposal] = useState<Proposal | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [activeTab, setActiveTab] = useState<'overview' | 'content'>('overview');

  // Overview form fields
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [agency, setAgency] = useState('');
  const [solicitationNumber, setSolicitationNumber] = useState('');
  const [naicsCode, setNaicsCode] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [estimatedValue, setEstimatedValue] = useState('');
  const [proposedValue, setProposedValue] = useState('');

  // Content form fields
  const [executiveSummary, setExecutiveSummary] = useState('');
  const [technicalApproach, setTechnicalApproach] = useState('');
  const [managementApproach, setManagementApproach] = useState('');
  const [pastPerformance, setPastPerformance] = useState('');
  const [pricingSummary, setPricingSummary] = useState('');

  // AI generation state
  const [generatingAll, setGeneratingAll] = useState(false);
  const [generatingSection, setGeneratingSection] = useState<SectionKey | null>(null);
  const [exportingDocx, setExportingDocx] = useState(false);

  const sectionSetters: Record<SectionKey, (v: string) => void> = {
    executive_summary: setExecutiveSummary,
    technical_approach: setTechnicalApproach,
    management_approach: setManagementApproach,
    past_performance: setPastPerformance,
    pricing_summary: setPricingSummary,
  };

  const sectionValues: Record<SectionKey, string> = {
    executive_summary: executiveSummary,
    technical_approach: technicalApproach,
    management_approach: managementApproach,
    past_performance: pastPerformance,
    pricing_summary: pricingSummary,
  };

  const extractError = (detail: any, fallback: string): string => {
    if (!detail) return fallback;
    if (typeof detail === 'string') return detail;
    if (detail.message) return detail.message;
    return fallback;
  };

  const formatDateForInput = (dateStr: string | null) => {
    if (!dateStr) return '';
    return dateStr.substring(0, 10);
  };

  const fetchProposal = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await proposalsApi.get(proposalId);
      const p = response.data;
      setProposal(p);

      // Populate form fields
      setTitle(p.title || '');
      setDescription(p.description || '');
      setAgency(p.agency || '');
      setSolicitationNumber(p.solicitation_number || '');
      setNaicsCode(p.naics_code || '');
      setDueDate(formatDateForInput(p.due_date));
      setEstimatedValue(p.estimated_value?.toString() || '');
      setProposedValue(p.proposed_value?.toString() || '');
      setExecutiveSummary(p.executive_summary || '');
      setTechnicalApproach(p.technical_approach || '');
      setManagementApproach(p.management_approach || '');
      setPastPerformance(p.past_performance || '');
      setPricingSummary(p.pricing_summary || '');
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      setError(extractError(detail, err.message || 'Failed to fetch proposal'));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (proposalId) fetchProposal();
  }, [proposalId]);

  const handleStatusChange = async (newStatus: ProposalStatus) => {
    setError('');
    setSuccessMessage('');

    try {
      const payload: any = { status: newStatus };
      if (newStatus === 'submitted') {
        payload.submitted_at = new Date().toISOString();
      }

      await proposalsApi.update(proposalId, payload);
      setProposal((prev) => prev ? { ...prev, status: newStatus } : prev);
      setSuccessMessage(`Status changed to ${statusLabels[newStatus]}`);
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      setError(extractError(detail, 'Failed to update status'));
    }
  };

  const handleSaveOverview = async () => {
    setSaving(true);
    setError('');
    setSuccessMessage('');

    try {
      const payload: any = {
        title,
        description: description || null,
        agency: agency || null,
        solicitation_number: solicitationNumber || null,
        naics_code: naicsCode || null,
        due_date: dueDate ? new Date(dueDate).toISOString() : null,
        estimated_value: estimatedValue ? parseFloat(estimatedValue) : null,
        proposed_value: proposedValue ? parseFloat(proposedValue) : null,
      };

      const response = await proposalsApi.update(proposalId, payload);
      setProposal(response.data);
      setSuccessMessage('Proposal details saved');
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      setError(extractError(detail, 'Failed to save proposal'));
    } finally {
      setSaving(false);
    }
  };

  const handleSaveContent = async () => {
    setSaving(true);
    setError('');
    setSuccessMessage('');

    try {
      const payload = {
        executive_summary: executiveSummary || null,
        technical_approach: technicalApproach || null,
        management_approach: managementApproach || null,
        past_performance: pastPerformance || null,
        pricing_summary: pricingSummary || null,
      };

      const response = await proposalsApi.update(proposalId, payload);
      setProposal(response.data);
      setSuccessMessage('Content saved');
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      setError(extractError(detail, 'Failed to save content'));
    } finally {
      setSaving(false);
    }
  };

  const handleGenerateAll = async () => {
    const hasContent = Object.values(sectionValues).some((v) => v.trim());
    if (hasContent) {
      if (!window.confirm('This will overwrite all existing section content with AI-generated content. Continue?')) {
        return;
      }
    }

    setGeneratingAll(true);
    setError('');
    setSuccessMessage('');

    try {
      const response = await proposalsApi.generateContent(proposalId);
      const data = response.data;

      // Update local state with generated content
      if (data.executive_summary) setExecutiveSummary(data.executive_summary);
      if (data.technical_approach) setTechnicalApproach(data.technical_approach);
      if (data.management_approach) setManagementApproach(data.management_approach);
      if (data.past_performance) setPastPerformance(data.past_performance);
      if (data.pricing_summary) setPricingSummary(data.pricing_summary);

      // Update ai_generated_content tracking
      if (data.ai_generated_content) {
        setProposal((prev) => prev ? { ...prev, ai_generated_content: data.ai_generated_content } : prev);
      }

      setSuccessMessage('All sections generated with AI');
      setTimeout(() => setSuccessMessage(''), 5000);
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      setError(extractError(detail, 'Failed to generate content. Please try again.'));
    } finally {
      setGeneratingAll(false);
    }
  };

  const handleGenerateSection = async (sectionKey: SectionKey) => {
    const currentValue = sectionValues[sectionKey];
    if (currentValue.trim()) {
      if (!window.confirm(`This will overwrite the existing ${sectionConfig.find(s => s.key === sectionKey)?.label} content. Continue?`)) {
        return;
      }
    }

    setGeneratingSection(sectionKey);
    setError('');
    setSuccessMessage('');

    try {
      const response = await proposalsApi.generateContent(proposalId, [sectionKey]);
      const data = response.data;

      if (data[sectionKey]) {
        sectionSetters[sectionKey](data[sectionKey]);
      }

      if (data.ai_generated_content) {
        setProposal((prev) => prev ? { ...prev, ai_generated_content: data.ai_generated_content } : prev);
      }

      const label = sectionConfig.find(s => s.key === sectionKey)?.label || sectionKey;
      setSuccessMessage(`${label} generated with AI`);
      setTimeout(() => setSuccessMessage(''), 5000);
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      setError(extractError(detail, `Failed to generate ${sectionKey}. Please try again.`));
    } finally {
      setGeneratingSection(null);
    }
  };

  const handleExportDocx = async () => {
    setExportingDocx(true);
    setError('');

    try {
      const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
      const response = await fetch(`/api/proposals/${proposalId}/export?format=docx`, {
        headers: {
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
      });

      if (!response.ok) {
        const errData = await response.json().catch(() => null);
        throw new Error(errData?.detail || 'Export failed');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const disposition = response.headers.get('content-disposition');
      const filenameMatch = disposition?.match(/filename="?(.+?)"?$/);
      a.download = filenameMatch ? filenameMatch[1] : `${proposal?.title || 'proposal'}.docx`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      window.URL.revokeObjectURL(url);

      setSuccessMessage('Document exported successfully');
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (err: any) {
      setError(err.message || 'Failed to export document');
    } finally {
      setExportingDocx(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this proposal? This action cannot be undone.')) {
      return;
    }

    setDeleting(true);
    setError('');

    try {
      await proposalsApi.delete(proposalId);
      router.push('/proposals');
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      if (err.response?.status === 403) {
        setError('Only organization admins or owners can delete proposals');
      } else {
        setError(extractError(detail, 'Failed to delete proposal'));
      }
    } finally {
      setDeleting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="text-gray-400">Loading proposal...</div>
      </div>
    );
  }

  if (!proposal) {
    return (
      <div className="space-y-6">
        <Link
          href="/proposals"
          className="inline-flex items-center gap-2 text-gray-400 hover:text-white"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Proposals
        </Link>
        <div className="flex items-center gap-2 text-red-400 bg-red-900/20 border border-red-800 p-4 rounded-lg">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          {error || 'Proposal not found'}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-start gap-4">
          <Link
            href="/proposals"
            className="mt-1 p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-white">{proposal.title}</h1>
            <div className="flex items-center gap-3 mt-2">
              <span
                className={`px-2 py-0.5 text-xs font-medium rounded ${
                  statusColors[proposal.status]
                }`}
              >
                {statusLabels[proposal.status]}
              </span>
              {proposal.agency && (
                <span className="text-gray-400 text-sm">{proposal.agency}</span>
              )}
              {proposal.solicitation_number && (
                <span className="text-gray-500 text-sm">
                  Sol#: {proposal.solicitation_number}
                </span>
              )}
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <select
            value={proposal.status}
            onChange={(e) => handleStatusChange(e.target.value as ProposalStatus)}
            className="px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            {allStatuses.map((s) => (
              <option key={s} value={s}>
                {statusLabels[s]}
              </option>
            ))}
          </select>

          <button
            onClick={handleExportDocx}
            disabled={exportingDocx}
            className="flex items-center gap-2 px-4 py-2 bg-emerald-600 text-white text-sm rounded-lg hover:bg-emerald-700 disabled:opacity-50"
          >
            {exportingDocx ? (
              <Loader2 className="w-4 h-4 animate-spin" />
            ) : (
              <Download className="w-4 h-4" />
            )}
            {exportingDocx ? 'Exporting...' : 'Export DOCX'}
          </button>

          <Link
            href={`/proposals/${proposalId}/scoring`}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700"
          >
            <BarChart3 className="w-4 h-4" />
            Scoring
          </Link>

          <button
            onClick={handleDelete}
            disabled={deleting}
            className="flex items-center gap-2 px-4 py-2 bg-red-600/20 text-red-400 text-sm rounded-lg hover:bg-red-600/30 disabled:opacity-50 border border-red-800"
          >
            <Trash2 className="w-4 h-4" />
            {deleting ? 'Deleting...' : 'Delete'}
          </button>
        </div>
      </div>

      {/* Messages */}
      {error && (
        <div className="flex items-center gap-2 text-red-400 bg-red-900/20 border border-red-800 p-4 rounded-lg">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          {error}
        </div>
      )}

      {successMessage && (
        <div className="flex items-center gap-2 text-green-400 bg-green-900/20 border border-green-800 p-4 rounded-lg">
          <CheckCircle className="w-5 h-5 flex-shrink-0" />
          {successMessage}
        </div>
      )}

      {/* Tabs */}
      <div className="border-b border-gray-800">
        <div className="flex gap-1">
          <button
            onClick={() => setActiveTab('overview')}
            className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
              activeTab === 'overview'
                ? 'border-blue-500 text-blue-400'
                : 'border-transparent text-gray-400 hover:text-white'
            }`}
          >
            <Settings className="w-4 h-4" />
            Overview
          </button>
          <button
            onClick={() => setActiveTab('content')}
            className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
              activeTab === 'content'
                ? 'border-blue-500 text-blue-400'
                : 'border-transparent text-gray-400 hover:text-white'
            }`}
          >
            <FileText className="w-4 h-4" />
            Content
          </button>
        </div>
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && (
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Title
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Description
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={3}
              className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Agency
              </label>
              <input
                type="text"
                value={agency}
                onChange={(e) => setAgency(e.target.value)}
                className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Solicitation Number
              </label>
              <input
                type="text"
                value={solicitationNumber}
                onChange={(e) => setSolicitationNumber(e.target.value)}
                className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                NAICS Code
              </label>
              <input
                type="text"
                value={naicsCode}
                onChange={(e) => setNaicsCode(e.target.value)}
                className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Due Date
              </label>
              <input
                type="date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Estimated Value ($)
              </label>
              <input
                type="number"
                value={estimatedValue}
                onChange={(e) => setEstimatedValue(e.target.value)}
                min="0"
                step="1000"
                className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Proposed Value ($)
              </label>
              <input
                type="number"
                value={proposedValue}
                onChange={(e) => setProposedValue(e.target.value)}
                min="0"
                step="1000"
                className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <div className="pt-4">
            <button
              onClick={handleSaveOverview}
              disabled={saving || !title}
              className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              <Save className="w-4 h-4" />
              {saving ? 'Saving...' : 'Save Details'}
            </button>
          </div>
        </div>
      )}

      {/* Content Tab */}
      {activeTab === 'content' && (
        <div className="space-y-6">
          {/* Generate All Sections Button */}
          <div className="bg-purple-900/20 border border-purple-800 rounded-xl p-4 flex items-center justify-between">
            <div>
              <h3 className="text-purple-300 font-medium">AI Content Generation</h3>
              <p className="text-purple-400/70 text-sm mt-1">
                Generate all proposal sections using AI based on the solicitation details and your organization&apos;s capabilities.
              </p>
            </div>
            <button
              onClick={handleGenerateAll}
              disabled={generatingAll || generatingSection !== null}
              className="flex items-center gap-2 px-5 py-2.5 bg-purple-600 text-white text-sm rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap font-medium"
            >
              {generatingAll ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Sparkles className="w-4 h-4" />
              )}
              {generatingAll ? 'Generating All Sections...' : 'Generate All Sections with AI'}
            </button>
          </div>

          {/* Section editors */}
          {sectionConfig.map((section) => {
            const isGenerating = generatingSection === section.key || generatingAll;
            const isAiGenerated = proposal?.ai_generated_content?.[section.key];

            return (
              <div key={section.key} className="bg-gray-900 border border-gray-800 rounded-xl p-6">
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <label className="block text-sm font-medium text-gray-300">
                      {section.label}
                    </label>
                    {isAiGenerated && (
                      <span className="px-2 py-0.5 text-xs font-medium bg-purple-600/20 text-purple-400 rounded border border-purple-800">
                        AI Generated
                      </span>
                    )}
                  </div>
                  <button
                    onClick={() => handleGenerateSection(section.key)}
                    disabled={isGenerating}
                    className="flex items-center gap-1.5 px-3 py-1.5 text-xs bg-purple-600/20 text-purple-400 rounded-lg hover:bg-purple-600/30 disabled:opacity-50 disabled:cursor-not-allowed border border-purple-800"
                  >
                    {generatingSection === section.key ? (
                      <Loader2 className="w-3 h-3 animate-spin" />
                    ) : (
                      <RefreshCw className="w-3 h-3" />
                    )}
                    {generatingSection === section.key ? 'Generating...' : 'Generate'}
                  </button>
                </div>
                <textarea
                  value={sectionValues[section.key]}
                  onChange={(e) => sectionSetters[section.key](e.target.value)}
                  rows={section.rows}
                  placeholder={section.placeholder}
                  disabled={isGenerating}
                  className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono text-sm disabled:opacity-50"
                />
              </div>
            );
          })}

          <div>
            <button
              onClick={handleSaveContent}
              disabled={saving || generatingAll || generatingSection !== null}
              className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              <Save className="w-4 h-4" />
              {saving ? 'Saving...' : 'Save Content'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
