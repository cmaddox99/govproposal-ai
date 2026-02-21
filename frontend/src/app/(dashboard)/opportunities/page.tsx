'use client';

import { useState, useEffect } from 'react';
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
  CheckCircle
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
}

export default function OpportunitiesPage() {
  const router = useRouter();
  const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedOpp, setSelectedOpp] = useState<Opportunity | null>(null);
  const [creatingProposal, setCreatingProposal] = useState(false);

  const extractError = (detail: any, fallback: string): string => {
    if (!detail) return fallback;
    if (typeof detail === 'string') return detail;
    if (detail.message) return detail.message;
    return fallback;
  };

  const fetchOpportunities = async () => {
    setLoading(true);
    setError('');

    try {
      const token = localStorage.getItem('token');
      const orgId = localStorage.getItem('currentOrgId');

      if (!orgId) {
        setError('No organization selected');
        return;
      }

      const response = await fetch(`/api/opportunities?org_id=${orgId}`, {
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
      setSuccessMessage(data.message);
      await fetchOpportunities();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSyncing(false);
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

  useEffect(() => {
    fetchOpportunities();
  }, []);

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

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Opportunities</h1>
          <p className="text-gray-400 mt-1">Discover and track government contract opportunities from SAM.gov</p>
        </div>
        <button
          onClick={syncOpportunities}
          disabled={syncing}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${syncing ? 'animate-spin' : ''}`} />
          {syncing ? 'Syncing...' : 'Sync from SAM.gov'}
        </button>
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

      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <div className="flex gap-4 mb-6">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
            <input
              type="text"
              placeholder="Search opportunities by keyword, NAICS, agency..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button className="flex items-center gap-2 px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 hover:bg-gray-700">
            <Filter className="w-5 h-5" />
            Filters
          </button>
        </div>

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
              {opportunities.length === 0
                ? "Click 'Sync from SAM.gov' to fetch opportunities matching your organization's NAICS codes. Make sure you've added NAICS codes in your organization settings."
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
                  className="bg-gray-800/50 border border-gray-700 rounded-lg p-5 hover:border-gray-600 transition-colors"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="px-2 py-0.5 bg-blue-600/20 text-blue-400 text-xs font-medium rounded">
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
                        className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 disabled:opacity-50 whitespace-nowrap"
                      >
                        <FileText className="w-4 h-4" />
                        Create Proposal
                      </button>
                      {opp.sam_url && (
                        <a
                          href={opp.sam_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-2 px-4 py-2 bg-gray-700 text-gray-300 text-sm rounded-lg hover:bg-gray-600 whitespace-nowrap"
                        >
                          <ExternalLink className="w-4 h-4" />
                          View on SAM.gov
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
