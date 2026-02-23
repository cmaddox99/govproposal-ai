'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';
import {
  Search,
  Filter,
  RefreshCw,
  Calendar,
  Building2,
  DollarSign,
  ExternalLink,
  FileText,
  AlertCircle,
  CheckCircle,
  X
} from 'lucide-react';

interface Opportunity {
  id: string;
  notice_id: string;
  solicitation_number: string | null;
  title: string;
  description: string | null;
  department: string | null;
  agency: string | null;
  notice_type: string;
  naics_code: string | null;
  set_aside_type: string | null;
  posted_date: string | null;
  response_deadline: string | null;
  primary_contact_name: string | null;
  primary_contact_email: string | null;
  sam_url: string | null;
  estimated_value: number | null;
  source: string;
}

const SET_ASIDE_OPTIONS = [
  { value: 'sba', label: 'SBA' },
  { value: 'sbsa', label: 'SBSA' },
  { value: 'wosb', label: 'WOSB' },
  { value: 'edwosb', label: 'EDWOSB' },
  { value: 'sdvosb', label: 'SDVOSB' },
  { value: 'hubzone', label: 'HUBZone' },
  { value: '8a', label: '8(a)' },
];

export default function OpportunitiesPage() {
  const router = useRouter();
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [syncingEbuy, setSyncingEbuy] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedOpp, setSelectedOpp] = useState<Opportunity | null>(null);
  const [creatingProposal, setCreatingProposal] = useState(false);

  // Filter state
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    set_aside_type: [] as string[],
    value_min: '',
    value_max: '',
    posted_from: '',
    posted_to: '',
    source: '' as '' | 'sam_gov' | 'gsa_ebuy',
  });

  const activeFilterCount = [
    filters.set_aside_type.length > 0,
    filters.value_min !== '',
    filters.value_max !== '',
    filters.posted_from !== '',
    filters.posted_to !== '',
    filters.source !== '',
  ].filter(Boolean).length;

  const extractError = (detail: any, fallback: string): string => {
    if (!detail) return fallback;
    if (typeof detail === 'string') return detail;
    if (detail.message) return detail.message;
    return fallback;
  };

  const fetchOpportunities = async (currentFilters?: typeof filters) => {
    const f = currentFilters ?? filters;
    setLoading(true);
    setError('');

    try {
      const token = localStorage.getItem('token');
      const orgId = localStorage.getItem('currentOrgId');

      if (!orgId) {
        setError('No organization selected');
        return;
      }

      const params = new URLSearchParams({ org_id: orgId });

      if (f.set_aside_type.length > 0) {
        params.set('set_aside_type', f.set_aside_type.join(','));
      }
      if (f.value_min) params.set('value_min', f.value_min);
      if (f.value_max) params.set('value_max', f.value_max);
      if (f.posted_from) params.set('posted_from', f.posted_from);
      if (f.posted_to) params.set('posted_to', f.posted_to);
      if (f.source) params.set('source', f.source);

      const response = await fetch(`/api/opportunities?${params.toString()}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(extractError(data.detail, 'Failed to fetch opportunities'));
      }

      const data = await response.json();
      setOpportunities(data.opportunities || []);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const syncOpportunities = async () => {
    setSyncing(true);
    setError('');
    setSuccessMessage('');

    try {
      const token = localStorage.getItem('token');
      const orgId = localStorage.getItem('currentOrgId');

      if (!orgId) {
        setError('No organization selected');
        return;
      }

      const response = await fetch(`/api/opportunities/sync?org_id=${orgId}`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(extractError(data.detail, 'Failed to sync opportunities'));
      }

      const data = await response.json();
      if (data.synced === 0) {
        setSuccessMessage(
          'SAM.gov sync completed — no new opportunities found. This can happen if the API daily quota has been reached (resets at midnight UTC) or all opportunities are already synced.'
        );
      } else {
        setSuccessMessage(data.message);
      }
      await fetchOpportunities();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSyncing(false);
    }
  };

  const syncEbuyOpportunities = async () => {
    setSyncingEbuy(true);
    setError('');
    setSuccessMessage('');

    try {
      const token = localStorage.getItem('token');
      const orgId = localStorage.getItem('currentOrgId');

      if (!orgId) {
        setError('No organization selected');
        return;
      }

      const response = await fetch(`/api/opportunities/sync-ebuy?org_id=${orgId}`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(extractError(data.detail, 'Failed to sync eBuy opportunities'));
      }

      const data = await response.json();
      if (data.synced === 0) {
        setSuccessMessage(
          'GSA eBuy sync completed — no new opportunities found. This can happen if the SAM.gov API daily quota has been reached (resets at midnight UTC) or there are no new GSA solicitations.'
        );
      } else {
        setSuccessMessage(data.message);
      }
      await fetchOpportunities();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSyncingEbuy(false);
    }
  };

  const createProposalFromOpportunity = async (opportunity: Opportunity) => {
    setCreatingProposal(true);
    setError('');

    try {
      const token = localStorage.getItem('token');
      const orgId = localStorage.getItem('currentOrgId');

      if (!orgId) {
        setError('No organization selected');
        return;
      }

      const response = await fetch('/api/proposals/from-opportunity', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          opportunity_id: opportunity.id,
          organization_id: orgId,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(extractError(data.detail, 'Failed to create proposal'));
      }

      const data = await response.json();
      router.push(`/proposals/${data.id}/scoring`);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setCreatingProposal(false);
    }
  };

  const clearFilters = () => {
    setFilters({
      set_aside_type: [],
      value_min: '',
      value_max: '',
      posted_from: '',
      posted_to: '',
      source: '',
    });
  };

  const toggleSetAside = (value: string) => {
    setFilters(prev => ({
      ...prev,
      set_aside_type: prev.set_aside_type.includes(value)
        ? prev.set_aside_type.filter(v => v !== value)
        : [...prev.set_aside_type, value],
    }));
  };

  // Initial fetch
  const isFirstRender = useRef(true);
  useEffect(() => {
    fetchOpportunities();
    isFirstRender.current = false;
  }, []);

  // Refetch when filters change (skip initial render)
  useEffect(() => {
    if (isFirstRender.current) return;
    fetchOpportunities(filters);
  }, [
    filters.set_aside_type.join(','),
    filters.value_min,
    filters.value_max,
    filters.posted_from,
    filters.posted_to,
    filters.source,
  ]);

  const filteredOpportunities = opportunities.filter(opp =>
    !searchQuery ||
    opp.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    opp.agency?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    opp.naics_code?.includes(searchQuery)
  );

  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return 'N/A';
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const formatCurrency = (value: number | null) => {
    if (!value) return 'N/A';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value);
  };

  const getDaysRemaining = (deadline: string | null) => {
    if (!deadline) return null;
    const days = Math.ceil((new Date(deadline).getTime() - Date.now()) / (1000 * 60 * 60 * 24));
    return days;
  };

  const getSourceBadge = (source: string) => {
    if (source === 'gsa_ebuy') {
      return (
        <span className="px-2 py-0.5 bg-blue-600/20 text-blue-300 text-xs font-medium rounded">
          GSA eBuy
        </span>
      );
    }
    return (
      <span className="px-2 py-0.5 bg-cyan-600/20 text-cyan-300 text-xs font-medium rounded">
        SAM.gov
      </span>
    );
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Opportunities</h1>
          <p className="text-gray-400 mt-1">Discover and track government contract opportunities from SAM.gov and GSA eBuy</p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={syncOpportunities}
            disabled={syncing}
            className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-emerald-500 to-blue-500 text-white rounded-lg hover:from-emerald-600 hover:to-blue-600 disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 ${syncing ? 'animate-spin' : ''}`} />
            {syncing ? 'Syncing...' : 'Sync from SAM.gov'}
          </button>
          <button
            onClick={syncEbuyOpportunities}
            disabled={syncingEbuy}
            className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-lg hover:from-blue-600 hover:to-purple-600 disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 ${syncingEbuy ? 'animate-spin' : ''}`} />
            {syncingEbuy ? 'Syncing...' : 'Sync from GSA eBuy'}
          </button>
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
        <div className="flex gap-4 mb-6">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
            <input
              type="text"
              placeholder="Search opportunities by keyword, NAICS, agency..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-3 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            />
          </div>
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`flex items-center gap-2 px-4 py-3 border rounded-lg transition-colors ${
              showFilters || activeFilterCount > 0
                ? 'bg-emerald-500/20 border-emerald-500/40 text-emerald-300'
                : 'bg-white/[0.05] border-white/[0.08] text-gray-300 hover:bg-white/[0.08]'
            }`}
          >
            <Filter className="w-5 h-5" />
            Filters
            {activeFilterCount > 0 && (
              <span className="ml-1 px-1.5 py-0.5 bg-emerald-500 text-white text-xs rounded-full">
                {activeFilterCount}
              </span>
            )}
          </button>
        </div>

        {showFilters && (
          <div className="mb-6 p-4 bg-white/[0.03] border border-white/[0.08] rounded-lg space-y-4">
            {/* Row 1: Date and Value filters */}
            <div className="grid grid-cols-4 gap-4">
              <div>
                <label className="block text-xs font-medium text-gray-400 mb-1">Posted From</label>
                <input
                  type="date"
                  value={filters.posted_from}
                  onChange={(e) => setFilters(prev => ({ ...prev, posted_from: e.target.value }))}
                  className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white text-sm focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-400 mb-1">Posted To</label>
                <input
                  type="date"
                  value={filters.posted_to}
                  onChange={(e) => setFilters(prev => ({ ...prev, posted_to: e.target.value }))}
                  className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white text-sm focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-400 mb-1">Min Value ($)</label>
                <input
                  type="number"
                  placeholder="0"
                  value={filters.value_min}
                  onChange={(e) => setFilters(prev => ({ ...prev, value_min: e.target.value }))}
                  className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white text-sm focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-400 mb-1">Max Value ($)</label>
                <input
                  type="number"
                  placeholder="No limit"
                  value={filters.value_max}
                  onChange={(e) => setFilters(prev => ({ ...prev, value_max: e.target.value }))}
                  className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white text-sm focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Row 2: Set-Aside Type and Source */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-gray-400 mb-2">Set-Aside Type</label>
                <div className="flex flex-wrap gap-2">
                  {SET_ASIDE_OPTIONS.map(opt => (
                    <button
                      key={opt.value}
                      onClick={() => toggleSetAside(opt.value)}
                      className={`px-3 py-1 text-xs font-medium rounded-full border transition-colors ${
                        filters.set_aside_type.includes(opt.value)
                          ? 'bg-emerald-500/20 border-emerald-500/40 text-emerald-300'
                          : 'bg-white/[0.05] border-white/[0.08] text-gray-400 hover:bg-white/[0.08]'
                      }`}
                    >
                      {opt.label}
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-400 mb-2">Source</label>
                <div className="flex gap-3">
                  {[
                    { value: '', label: 'All' },
                    { value: 'sam_gov', label: 'SAM.gov' },
                    { value: 'gsa_ebuy', label: 'GSA eBuy' },
                  ].map(opt => (
                    <label key={opt.value} className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="radio"
                        name="source"
                        checked={filters.source === opt.value}
                        onChange={() => setFilters(prev => ({ ...prev, source: opt.value as '' | 'sam_gov' | 'gsa_ebuy' }))}
                        className="text-emerald-500 focus:ring-emerald-500"
                      />
                      <span className="text-sm text-gray-300">{opt.label}</span>
                    </label>
                  ))}
                </div>
              </div>
            </div>

            {/* Clear filters */}
            {activeFilterCount > 0 && (
              <div className="flex justify-end">
                <button
                  onClick={clearFilters}
                  className="flex items-center gap-1 text-sm text-gray-400 hover:text-white transition-colors"
                >
                  <X className="w-4 h-4" />
                  Clear all filters
                </button>
              </div>
            )}
          </div>
        )}

        {loading ? (
          <div className="text-center py-12">
            <RefreshCw className="w-8 h-8 text-gray-500 mx-auto mb-4 animate-spin" />
            <p className="text-gray-400">Loading opportunities...</p>
          </div>
        ) : filteredOpportunities.length === 0 ? (
          <div className="text-center py-12">
            <Search className="w-12 h-12 text-gray-600 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-white mb-2">No Opportunities Found</h3>
            <p className="text-gray-500 max-w-md mx-auto">
              {opportunities.length === 0 && activeFilterCount === 0
                ? "Click 'Sync from SAM.gov' or 'Sync from GSA eBuy' to fetch opportunities matching your organization's NAICS codes. Make sure you've added NAICS codes in your organization settings."
                : activeFilterCount > 0
                ? "No opportunities match your current filters. Try adjusting your date range (most opportunities are posted in the past, not the future) or clearing filters."
                : "No opportunities match your search criteria."}
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredOpportunities.map((opp) => {
              const daysRemaining = getDaysRemaining(opp.response_deadline);
              const isUrgent = daysRemaining !== null && daysRemaining <= 7;

              return (
                <div
                  key={opp.id}
                  className="bg-white/[0.03] border border-white/[0.08] rounded-lg p-5 hover:border-white/[0.12] transition-colors"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-2">
                        {getSourceBadge(opp.source)}
                        <span className="px-2 py-0.5 bg-emerald-600/20 text-emerald-300 text-xs font-medium rounded">
                          {opp.notice_type.replace(/_/g, ' ').toUpperCase()}
                        </span>
                        {opp.set_aside_type && (
                          <span className="px-2 py-0.5 bg-purple-600/20 text-purple-400 text-xs font-medium rounded">
                            {opp.set_aside_type.toUpperCase()}
                          </span>
                        )}
                        {isUrgent && (
                          <span className="px-2 py-0.5 bg-red-600/20 text-red-400 text-xs font-medium rounded">
                            {daysRemaining} days left
                          </span>
                        )}
                      </div>

                      <h3 className="text-white font-medium text-lg mb-1 line-clamp-2">
                        {opp.title}
                      </h3>

                      <div className="flex flex-wrap items-center gap-4 text-sm text-gray-400 mb-3">
                        {opp.agency && (
                          <span className="flex items-center gap-1">
                            <Building2 className="w-4 h-4" />
                            {opp.agency}
                          </span>
                        )}
                        {opp.naics_code && (
                          <span>NAICS: {opp.naics_code}</span>
                        )}
                        {opp.solicitation_number && (
                          <span>Sol#: {opp.solicitation_number}</span>
                        )}
                      </div>

                      <div className="flex flex-wrap items-center gap-4 text-sm">
                        <span className="flex items-center gap-1 text-gray-400">
                          <Calendar className="w-4 h-4" />
                          Due: {formatDate(opp.response_deadline)}
                        </span>
                        {opp.estimated_value && (
                          <span className="flex items-center gap-1 text-green-400">
                            <DollarSign className="w-4 h-4" />
                            {formatCurrency(opp.estimated_value)}
                          </span>
                        )}
                      </div>
                    </div>

                    <div className="flex flex-col gap-2">
                      <button
                        onClick={() => createProposalFromOpportunity(opp)}
                        disabled={creatingProposal}
                        className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-emerald-500 to-blue-500 text-white text-sm rounded-lg hover:from-emerald-600 hover:to-blue-600 disabled:opacity-50 whitespace-nowrap"
                      >
                        <FileText className="w-4 h-4" />
                        Create Proposal
                      </button>
                      {opp.sam_url && (
                        <a
                          href={opp.sam_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-2 px-4 py-2 bg-white/[0.08] text-gray-300 text-sm rounded-lg hover:bg-white/[0.12] whitespace-nowrap"
                        >
                          <ExternalLink className="w-4 h-4" />
                          {opp.source === 'gsa_ebuy' ? 'View on eBuy' : 'View on SAM.gov'}
                        </a>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
