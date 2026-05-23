'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import {
  Target,
  RefreshCw,
  Search,
  Calendar,
  DollarSign,
  ExternalLink,
  FileText,
  AlertCircle,
  CheckCircle,
  Building2,
  Mail,
  TrendingUp,
  Archive,
  XCircle,
  Activity,
  Loader2,
  Check,
  Square,
  X,
  Paperclip,
} from 'lucide-react';
import OpportunityDocumentsModal from '@/components/pipeline/OpportunityDocumentsModal';
import { useOrgId } from '@/lib/useOrgId';

type PipelineStatus = 'active' | 'archived' | 'no_bid';
type MatchTier = 'red' | 'yellow' | 'green';

interface OpportunitySummary {
  id: string;
  title: string;
  solicitation_number: string | null;
  agency: string | null;
  naics_code: string | null;
  set_aside_type: string | null;
  response_deadline: string | null;
  estimated_value: number | null;
  primary_contact_name: string | null;
  primary_contact_email: string | null;
  sam_url: string | null;
  source: string;
}

interface PipelineItem {
  id: string;
  organization_id: string;
  opportunity_id: string;
  proposal_id: string | null;
  status: PipelineStatus;
  dollar_value_text: string | null;
  questions_due_date: string | null;
  proposal_due_date_override: string | null;
  contact_name_override: string | null;
  contact_email_override: string | null;
  has_rfp: boolean;
  has_ppqs: boolean;
  has_resume: boolean;
  has_price: boolean;
  has_details: boolean;
  archive_status: string | null;
  no_bid_reason: string | null;
  match_score: number | null;
  match_tier: MatchTier | null;
  match_breakdown: string | null;
  notes: string | null;
  opportunity: OpportunitySummary | null;
}

const STATUS_TABS: { value: PipelineStatus; label: string; icon: any }[] = [
  { value: 'active', label: 'Active', icon: Activity },
  { value: 'archived', label: 'Archive', icon: Archive },
  { value: 'no_bid', label: 'No Bid', icon: XCircle },
];

const CHECKMARK_FIELDS: { key: keyof PipelineItem; label: string }[] = [
  { key: 'has_rfp', label: 'RFP' },
  { key: 'has_ppqs', label: 'PPQs' },
  { key: 'has_resume', label: 'Resume' },
  { key: 'has_price', label: 'Price' },
  { key: 'has_details', label: 'Details' },
];

function formatDate(dateStr: string | null) {
  if (!dateStr) return 'N/A';
  return new Date(dateStr).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

function formatCurrency(value: number | null, fallback: string | null) {
  if (fallback) return fallback;
  if (!value) return 'N/A';
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(value);
}

function tierStyle(tier: MatchTier | null) {
  switch (tier) {
    case 'green':
      return { bg: 'bg-emerald-500/15', text: 'text-emerald-400', border: 'border-emerald-500/30', dot: 'bg-emerald-400', label: 'Good' };
    case 'yellow':
      return { bg: 'bg-yellow-500/15', text: 'text-yellow-300', border: 'border-yellow-500/30', dot: 'bg-yellow-400', label: 'Low' };
    case 'red':
      return { bg: 'bg-red-500/15', text: 'text-red-400', border: 'border-red-500/30', dot: 'bg-red-400', label: 'No Bid' };
    default:
      return { bg: 'bg-gray-500/15', text: 'text-gray-400', border: 'border-gray-500/30', dot: 'bg-gray-400', label: 'Unscored' };
  }
}

export default function PipelinePage() {
  const router = useRouter();
  const orgId = useOrgId();
  const [items, setItems] = useState<PipelineItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [statusFilter, setStatusFilter] = useState<PipelineStatus>('active');
  const [searchQuery, setSearchQuery] = useState('');
  const [creatingProposalFor, setCreatingProposalFor] = useState<string | null>(null);
  const [showBreakdownFor, setShowBreakdownFor] = useState<string | null>(null);
  const [documentsModalFor, setDocumentsModalFor] = useState<PipelineItem | null>(null);

  const fetchPipeline = useCallback(async () => {
    if (!orgId) return;
    setLoading(true);
    setError('');
    try {
      const token = localStorage.getItem('token');
      const params = new URLSearchParams({ org_id: orgId, status: statusFilter });
      const response = await fetch(`/api/pipeline?${params.toString()}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to load pipeline');
      }
      const data = await response.json();
      setItems(data.items || []);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [orgId, statusFilter]);

  useEffect(() => {
    fetchPipeline();
  }, [fetchPipeline]);

  const updateItem = async (id: string, patch: Record<string, any>, optimistic = true) => {
    if (optimistic) {
      setItems((prev) => prev.map((it) => (it.id === id ? { ...it, ...patch } : it)));
    }
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/pipeline/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify(patch),
      });
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Update failed');
      }
      if (!optimistic) {
        const data = await response.json();
        setItems((prev) => prev.map((it) => (it.id === id ? { ...it, ...data } : it)));
      }
    } catch (err: any) {
      setError(err.message);
      fetchPipeline();
    }
  };

  const toggleCheckmark = (id: string, key: keyof PipelineItem, current: boolean) => {
    updateItem(id, { [key]: !current });
  };

  const moveToStatus = async (id: string, status: PipelineStatus) => {
    const patch: Record<string, any> = { status };
    if (status === 'no_bid') {
      const reason = window.prompt('Reason for no-bid?');
      if (reason === null) return;
      patch.no_bid_reason = reason || 'No reason provided';
    }
    await updateItem(id, patch, false);
    setSuccessMessage(`Moved to ${status.replace('_', ' ')}`);
    setTimeout(() => setSuccessMessage(''), 2500);
    fetchPipeline();
  };

  const removeItem = async (id: string) => {
    if (!window.confirm('Remove this item from the pipeline? The underlying opportunity is not deleted.')) return;
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/pipeline/${id}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Delete failed');
      }
      setItems((prev) => prev.filter((it) => it.id !== id));
      setSuccessMessage('Removed from pipeline');
      setTimeout(() => setSuccessMessage(''), 2500);
    } catch (err: any) {
      setError(err.message);
    }
  };

  const rescore = async (id: string) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/pipeline/${id}/rescore`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Rescore failed');
      }
      const data = await response.json();
      setItems((prev) => prev.map((it) => (it.id === id ? { ...it, ...data } : it)));
    } catch (err: any) {
      setError(err.message);
    }
  };

  const createProposal = async (item: PipelineItem) => {
    setCreatingProposalFor(item.id);
    setError('');
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/pipeline/${item.id}/create-proposal`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to create proposal');
      }
      const data = await response.json();
      router.push(`/proposals/${data.id}`);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setCreatingProposalFor(null);
    }
  };

  const filteredItems = items.filter((it) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    const opp = it.opportunity;
    return (
      opp?.title?.toLowerCase().includes(q) ||
      opp?.agency?.toLowerCase().includes(q) ||
      opp?.solicitation_number?.toLowerCase().includes(q)
    );
  });

  const counts = {
    active: items.filter((i) => i.status === 'active').length,
    archived: items.filter((i) => i.status === 'archived').length,
    no_bid: items.filter((i) => i.status === 'no_bid').length,
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <Target className="w-7 h-7 text-emerald-400" />
            Pipeline
          </h1>
          <p className="text-gray-400 mt-1">
            Opportunities you&apos;re actively pursuing — scored by past-performance fit
          </p>
        </div>
      </div>

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

      <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
        {/* Status tabs */}
        <div className="flex items-center gap-2 mb-6 border-b border-white/[0.06] pb-3">
          {STATUS_TABS.map((tab) => {
            const isActive = statusFilter === tab.value;
            const Icon = tab.icon;
            return (
              <button
                key={tab.value}
                onClick={() => setStatusFilter(tab.value)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-gradient-to-r from-emerald-500/20 to-blue-500/20 text-white border border-white/[0.08]'
                    : 'text-gray-400 hover:bg-white/[0.05] hover:text-white'
                }`}
              >
                <Icon className="w-4 h-4" />
                {tab.label}
                <span className="ml-1 px-1.5 py-0.5 bg-white/[0.08] text-xs rounded-full">
                  {counts[tab.value]}
                </span>
              </button>
            );
          })}
        </div>

        {/* Search */}
        <div className="mb-6 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
          <input
            type="text"
            placeholder="Search by title, agency, solicitation #..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-3 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
          />
        </div>

        {loading ? (
          <div className="text-center py-12">
            <RefreshCw className="w-8 h-8 text-gray-500 mx-auto mb-4 animate-spin" />
            <p className="text-gray-400">Loading pipeline...</p>
          </div>
        ) : filteredItems.length === 0 ? (
          <div className="text-center py-12">
            <Target className="w-12 h-12 text-gray-600 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-white mb-2">No items in this section</h3>
            <p className="text-gray-500 max-w-md mx-auto">
              {statusFilter === 'active'
                ? 'Go to Opportunities and click "Add to Pipeline" to start pursuing one.'
                : statusFilter === 'archived'
                ? 'Archived items will appear here once you mark proposals as submitted, awarded, or lost.'
                : 'Items you decide not to pursue will appear here with your no-bid reason.'}
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredItems.map((item) => {
              const opp = item.opportunity;
              const tier = tierStyle(item.match_tier);
              const isActive = item.status === 'active';
              return (
                <div
                  key={item.id}
                  className="bg-white/[0.03] border border-white/[0.08] rounded-lg p-5 hover:border-white/[0.12] transition-colors"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      {/* Top row: tags */}
                      <div className="flex items-center gap-2 mb-2 flex-wrap">
                        {item.match_tier && (
                          <span className={`flex items-center gap-1.5 px-2 py-0.5 ${tier.bg} ${tier.text} ${tier.border} border text-xs font-medium rounded`}>
                            <span className={`w-2 h-2 rounded-full ${tier.dot}`} />
                            {item.match_score ?? 0}% {tier.label}
                          </span>
                        )}
                        {opp?.set_aside_type && (
                          <span className="px-2 py-0.5 bg-purple-600/20 text-purple-400 text-xs font-medium rounded">
                            {opp.set_aside_type.toUpperCase()}
                          </span>
                        )}
                        {opp?.source === 'gsa_ebuy' ? (
                          <span className="px-2 py-0.5 bg-blue-600/20 text-blue-300 text-xs font-medium rounded">GSA eBuy</span>
                        ) : (
                          <span className="px-2 py-0.5 bg-cyan-600/20 text-cyan-300 text-xs font-medium rounded">SAM.gov</span>
                        )}
                        {item.archive_status && (
                          <span className="px-2 py-0.5 bg-gray-600/20 text-gray-300 text-xs font-medium rounded uppercase">
                            {item.archive_status}
                          </span>
                        )}
                      </div>

                      <h3 className="text-white font-medium text-lg mb-2 line-clamp-2">
                        {opp?.title || '(opportunity removed)'}
                      </h3>

                      {/* Spreadsheet-style metadata grid */}
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-x-4 gap-y-2 text-sm mb-3">
                        {opp?.solicitation_number && (
                          <div>
                            <div className="text-gray-500 text-xs">Solicitation</div>
                            <div className="text-gray-300">{opp.solicitation_number}</div>
                          </div>
                        )}
                        <div>
                          <div className="text-gray-500 text-xs">Dollar Value</div>
                          <div className="text-emerald-400 flex items-center gap-1">
                            <DollarSign className="w-3.5 h-3.5" />
                            {formatCurrency(opp?.estimated_value ?? null, item.dollar_value_text)}
                          </div>
                        </div>
                        <div>
                          <div className="text-gray-500 text-xs">Questions Due</div>
                          <div className="text-gray-300 flex items-center gap-1">
                            <Calendar className="w-3.5 h-3.5" />
                            {formatDate(item.questions_due_date)}
                          </div>
                        </div>
                        <div>
                          <div className="text-gray-500 text-xs">Proposal Due</div>
                          <div className="text-gray-300 flex items-center gap-1">
                            <Calendar className="w-3.5 h-3.5" />
                            {formatDate(item.proposal_due_date_override || opp?.response_deadline || null)}
                          </div>
                        </div>
                        {opp?.agency && (
                          <div>
                            <div className="text-gray-500 text-xs">Agency</div>
                            <div className="text-gray-300 flex items-center gap-1">
                              <Building2 className="w-3.5 h-3.5" />
                              {opp.agency}
                            </div>
                          </div>
                        )}
                        {(item.contact_name_override || opp?.primary_contact_name) && (
                          <div>
                            <div className="text-gray-500 text-xs">Contact</div>
                            <div className="text-gray-300">
                              {item.contact_name_override || opp?.primary_contact_name}
                            </div>
                          </div>
                        )}
                        {(item.contact_email_override || opp?.primary_contact_email) && (
                          <div className="col-span-2">
                            <div className="text-gray-500 text-xs">Email</div>
                            <a
                              href={`mailto:${item.contact_email_override || opp?.primary_contact_email}`}
                              className="text-blue-400 hover:text-blue-300 flex items-center gap-1 truncate"
                            >
                              <Mail className="w-3.5 h-3.5 flex-shrink-0" />
                              {item.contact_email_override || opp?.primary_contact_email}
                            </a>
                          </div>
                        )}
                      </div>

                      {/* Checkmarks for active items */}
                      {isActive && (
                        <div className="flex flex-wrap gap-2 mb-2">
                          {CHECKMARK_FIELDS.map(({ key, label }) => {
                            const checked = Boolean(item[key]);
                            return (
                              <button
                                key={key}
                                onClick={() => toggleCheckmark(item.id, key, checked)}
                                className={`flex items-center gap-1.5 px-2.5 py-1 text-xs rounded border transition-colors ${
                                  checked
                                    ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30'
                                    : 'bg-white/[0.03] text-gray-400 border-white/[0.08] hover:bg-white/[0.06]'
                                }`}
                              >
                                {checked ? <Check className="w-3 h-3" /> : <Square className="w-3 h-3" />}
                                {label}
                              </button>
                            );
                          })}
                        </div>
                      )}

                      {item.no_bid_reason && (
                        <div className="mt-2 text-sm text-gray-400 italic">
                          <span className="text-gray-500">No-bid reason:</span> {item.no_bid_reason}
                        </div>
                      )}

                      {showBreakdownFor === item.id && item.match_breakdown && (
                        <MatchBreakdownPanel raw={item.match_breakdown} />
                      )}
                    </div>

                    {/* Right column: actions */}
                    <div className="flex flex-col gap-2 w-44 flex-shrink-0">
                      {isActive && (
                        <button
                          onClick={() => createProposal(item)}
                          disabled={creatingProposalFor === item.id}
                          className="flex items-center justify-center gap-2 px-3 py-2 bg-gradient-to-r from-emerald-500 to-blue-500 text-white text-sm rounded-lg hover:from-emerald-600 hover:to-blue-600 disabled:opacity-50 whitespace-nowrap"
                        >
                          {creatingProposalFor === item.id ? (
                            <Loader2 className="w-4 h-4 animate-spin" />
                          ) : (
                            <FileText className="w-4 h-4" />
                          )}
                          {item.proposal_id ? 'Open Proposal' : 'Create Proposal'}
                        </button>
                      )}
                      {opp?.sam_url && (
                        <a
                          href={opp.sam_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center justify-center gap-2 px-3 py-2 bg-white/[0.08] text-gray-300 text-sm rounded-lg hover:bg-white/[0.12] whitespace-nowrap"
                        >
                          <ExternalLink className="w-4 h-4" />
                          View Source
                        </a>
                      )}
                      <button
                        onClick={() => setShowBreakdownFor(showBreakdownFor === item.id ? null : item.id)}
                        className="flex items-center justify-center gap-2 px-3 py-2 bg-white/[0.05] text-gray-300 text-sm rounded-lg hover:bg-white/[0.08]"
                      >
                        <TrendingUp className="w-4 h-4" />
                        {showBreakdownFor === item.id ? 'Hide' : 'Why this score'}
                      </button>
                      <button
                        onClick={() => setDocumentsModalFor(item)}
                        className="flex items-center justify-center gap-2 px-3 py-2 bg-white/[0.05] text-gray-300 text-sm rounded-lg hover:bg-white/[0.08]"
                      >
                        <Paperclip className="w-4 h-4" />
                        Documents
                      </button>
                      <button
                        onClick={() => rescore(item.id)}
                        className="flex items-center justify-center gap-2 px-3 py-2 bg-white/[0.05] text-gray-300 text-xs rounded-lg hover:bg-white/[0.08]"
                      >
                        <RefreshCw className="w-3.5 h-3.5" />
                        Recalculate score
                      </button>

                      <div className="border-t border-white/[0.06] pt-2 mt-1 flex flex-col gap-1">
                        {isActive && (
                          <>
                            <button
                              onClick={() => moveToStatus(item.id, 'archived')}
                              className="text-xs text-gray-400 hover:text-white text-left"
                            >
                              Move to Archive
                            </button>
                            <button
                              onClick={() => moveToStatus(item.id, 'no_bid')}
                              className="text-xs text-gray-400 hover:text-white text-left"
                            >
                              Mark as No Bid
                            </button>
                          </>
                        )}
                        {!isActive && (
                          <button
                            onClick={() => moveToStatus(item.id, 'active')}
                            className="text-xs text-gray-400 hover:text-white text-left"
                          >
                            Move back to Active
                          </button>
                        )}
                        <button
                          onClick={() => removeItem(item.id)}
                          className="text-xs text-red-400 hover:text-red-300 text-left flex items-center gap-1"
                        >
                          <X className="w-3 h-3" /> Remove
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {documentsModalFor && documentsModalFor.opportunity && (
        <OpportunityDocumentsModal
          orgId={documentsModalFor.organization_id}
          opportunityId={documentsModalFor.opportunity_id}
          opportunityTitle={documentsModalFor.opportunity.title}
          onClose={() => setDocumentsModalFor(null)}
        />
      )}
    </div>
  );
}

interface ScoreImprovement {
  factor: string;
  action: string;
  potential_gain: number;
  effort: 'low' | 'medium' | 'high';
}

const EFFORT_STYLE: Record<string, { bg: string; text: string }> = {
  low: { bg: 'bg-emerald-500/15', text: 'text-emerald-300' },
  medium: { bg: 'bg-yellow-500/15', text: 'text-yellow-300' },
  high: { bg: 'bg-red-500/15', text: 'text-red-300' },
};

const FACTOR_LABEL: Record<string, string> = {
  naics: 'NAICS',
  past_performance: 'Past performance',
  set_aside: 'Set-aside',
  value_fit: 'Value fit',
};

function MatchBreakdownPanel({ raw }: { raw: string }) {
  let parsed: any;
  try {
    parsed = JSON.parse(raw);
  } catch {
    return null;
  }
  const rows: { label: string; score: number; max: number }[] = [
    { label: 'NAICS match', score: parsed.naics_score ?? 0, max: 30 },
    { label: 'Past performance', score: parsed.past_performance_score ?? 0, max: 40 },
    { label: 'Set-aside fit', score: parsed.set_aside_score ?? 0, max: 15 },
    { label: 'Value fit', score: parsed.value_fit_score ?? 0, max: 15 },
  ];
  const improvements: ScoreImprovement[] = Array.isArray(parsed.improvements)
    ? parsed.improvements
    : [];
  const total: number = parsed.total ?? 0;
  const potential: number = parsed.potential_total ?? total;
  const gain = Math.max(0, potential - total);

  return (
    <div className="mt-3 p-3 bg-white/[0.03] border border-white/[0.06] rounded-lg">
      <div className="text-xs text-gray-400 mb-2 font-medium">Score breakdown</div>
      <div className="space-y-1.5">
        {rows.map((r) => (
          <div key={r.label} className="flex items-center gap-3 text-xs">
            <div className="w-32 text-gray-400">{r.label}</div>
            <div className="flex-1 h-1.5 bg-white/[0.05] rounded-full overflow-hidden">
              <div
                className="h-full bg-gradient-to-r from-emerald-500 to-blue-500"
                style={{ width: `${(r.score / r.max) * 100}%` }}
              />
            </div>
            <div className="text-gray-300 w-12 text-right">
              {r.score}/{r.max}
            </div>
          </div>
        ))}
      </div>
      {parsed.notes && Array.isArray(parsed.notes) && parsed.notes.length > 0 && (
        <ul className="mt-3 space-y-1">
          {parsed.notes.map((note: string, i: number) => (
            <li key={i} className="text-xs text-gray-400 flex gap-1.5">
              <span className="text-gray-600">•</span>
              {note}
            </li>
          ))}
        </ul>
      )}
      {improvements.length > 0 && (
        <div className="mt-4 pt-3 border-t border-white/[0.06]">
          <div className="flex items-center justify-between mb-2">
            <div className="text-xs text-gray-400 font-medium">
              How to improve this score
            </div>
            {gain > 0 && (
              <div className="text-xs text-emerald-300">
                +{gain} pts possible · could reach {potential}/100
              </div>
            )}
          </div>
          <ul className="space-y-2">
            {improvements.map((imp, i) => {
              const effort = EFFORT_STYLE[imp.effort] || EFFORT_STYLE.medium;
              return (
                <li
                  key={i}
                  className="flex items-start gap-3 text-xs bg-white/[0.02] border border-white/[0.05] rounded p-2.5"
                >
                  <div className="flex flex-col items-center gap-1 flex-shrink-0 w-14">
                    <span className="text-emerald-300 font-semibold text-sm">
                      +{imp.potential_gain}
                    </span>
                    <span className={`px-1.5 py-0.5 rounded ${effort.bg} ${effort.text} uppercase tracking-wide`}>
                      {imp.effort}
                    </span>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-gray-500 text-[10px] uppercase tracking-wide mb-0.5">
                      {FACTOR_LABEL[imp.factor] || imp.factor}
                    </div>
                    <div className="text-gray-200 leading-relaxed">{imp.action}</div>
                  </div>
                </li>
              );
            })}
          </ul>
        </div>
      )}
    </div>
  );
}
