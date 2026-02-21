'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import {
  FileText,
  Plus,
  Search,
  RefreshCw,
  AlertCircle,
  ChevronLeft,
  ChevronRight,
  Calendar,
  DollarSign,
  Building2,
} from 'lucide-react';
import { proposalsApi } from '@/lib/api';
import { Proposal, ProposalStatus } from '@/types';

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

const LIMIT = 20;

export default function ProposalsPage() {
  const [proposals, setProposals] = useState<Proposal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [total, setTotal] = useState(0);
  const [offset, setOffset] = useState(0);

  const extractError = (detail: any, fallback: string): string => {
    if (!detail) return fallback;
    if (typeof detail === 'string') return detail;
    if (detail.message) return detail.message;
    return fallback;
  };

  const fetchProposals = async () => {
    setLoading(true);
    setError('');

    try {
      const orgId = localStorage.getItem('currentOrgId');
      if (!orgId) {
        setError('No organization selected');
        return;
      }

      const response = await proposalsApi.list({
        org_id: orgId,
        status_filter: statusFilter || undefined,
        limit: LIMIT,
        offset,
      });

      const data = response.data;
      setProposals(data.proposals || []);
      setTotal(data.total || 0);
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      setError(extractError(detail, err.message || 'Failed to fetch proposals'));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProposals();
  }, [statusFilter, offset]);

  const filteredProposals = proposals.filter(
    (p) =>
      !searchQuery ||
      p.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.agency?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.solicitation_number?.toLowerCase().includes(searchQuery.toLowerCase())
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

  const pageStart = offset + 1;
  const pageEnd = Math.min(offset + LIMIT, total);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Proposals</h1>
          <p className="text-gray-400 mt-1">
            Manage and track your government contract proposals
          </p>
        </div>
        <Link
          href="/proposals/new"
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          <Plus className="w-4 h-4" />
          New Proposal
        </Link>
      </div>

      {error && (
        <div className="flex items-center gap-2 text-red-400 bg-red-900/20 border border-red-800 p-4 rounded-lg">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          {error}
        </div>
      )}

      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <div className="flex gap-4 mb-6">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
            <input
              type="text"
              placeholder="Search by title, agency, or solicitation number..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <select
            value={statusFilter}
            onChange={(e) => {
              setStatusFilter(e.target.value);
              setOffset(0);
            }}
            className="px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Statuses</option>
            <option value="draft">Draft</option>
            <option value="in_progress">In Progress</option>
            <option value="review">Review</option>
            <option value="submitted">Submitted</option>
            <option value="awarded">Awarded</option>
            <option value="not_awarded">Not Awarded</option>
            <option value="cancelled">Cancelled</option>
          </select>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <RefreshCw className="w-8 h-8 text-gray-500 mx-auto mb-4 animate-spin" />
            <p className="text-gray-400">Loading proposals...</p>
          </div>
        ) : filteredProposals.length === 0 ? (
          <div className="text-center py-12">
            <FileText className="w-12 h-12 text-gray-600 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-white mb-2">
              No Proposals Found
            </h3>
            <p className="text-gray-500 max-w-md mx-auto mb-6">
              {proposals.length === 0
                ? 'Create your first proposal or generate one from an opportunity.'
                : 'No proposals match your search criteria.'}
            </p>
            {proposals.length === 0 && (
              <div className="flex items-center justify-center gap-4">
                <Link
                  href="/proposals/new"
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  <Plus className="w-4 h-4" />
                  New Proposal
                </Link>
                <Link
                  href="/opportunities"
                  className="flex items-center gap-2 px-4 py-2 bg-gray-700 text-gray-300 rounded-lg hover:bg-gray-600"
                >
                  Browse Opportunities
                </Link>
              </div>
            )}
          </div>
        ) : (
          <>
            <div className="space-y-4">
              {filteredProposals.map((proposal) => (
                <Link
                  key={proposal.id}
                  href={`/proposals/${proposal.id}`}
                  className="block bg-gray-800/50 border border-gray-700 rounded-lg p-5 hover:border-gray-600 transition-colors"
                >
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-2">
                        <span
                          className={`px-2 py-0.5 text-xs font-medium rounded ${
                            statusColors[proposal.status] || statusColors.draft
                          }`}
                        >
                          {statusLabels[proposal.status] || proposal.status}
                        </span>
                        {proposal.naics_code && (
                          <span className="px-2 py-0.5 bg-gray-700/50 text-gray-400 text-xs font-medium rounded">
                            NAICS: {proposal.naics_code}
                          </span>
                        )}
                      </div>

                      <h3 className="text-white font-medium text-lg mb-1 line-clamp-2">
                        {proposal.title}
                      </h3>

                      <div className="flex flex-wrap items-center gap-4 text-sm text-gray-400 mb-3">
                        {proposal.agency && (
                          <span className="flex items-center gap-1">
                            <Building2 className="w-4 h-4" />
                            {proposal.agency}
                          </span>
                        )}
                        {proposal.solicitation_number && (
                          <span>Sol#: {proposal.solicitation_number}</span>
                        )}
                      </div>

                      <div className="flex flex-wrap items-center gap-4 text-sm">
                        <span className="flex items-center gap-1 text-gray-400">
                          <Calendar className="w-4 h-4" />
                          Due: {formatDate(proposal.due_date)}
                        </span>
                        {proposal.estimated_value && (
                          <span className="flex items-center gap-1 text-green-400">
                            <DollarSign className="w-4 h-4" />
                            {formatCurrency(proposal.estimated_value)}
                          </span>
                        )}
                        <span className="text-gray-500 text-xs">
                          Updated: {formatDate(proposal.updated_at)}
                        </span>
                      </div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>

            {total > LIMIT && (
              <div className="flex items-center justify-between mt-6 pt-4 border-t border-gray-800">
                <p className="text-sm text-gray-400">
                  Showing {pageStart}&ndash;{pageEnd} of {total}
                </p>
                <div className="flex gap-2">
                  <button
                    onClick={() => setOffset(Math.max(0, offset - LIMIT))}
                    disabled={offset === 0}
                    className="flex items-center gap-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <ChevronLeft className="w-4 h-4" />
                    Previous
                  </button>
                  <button
                    onClick={() => setOffset(offset + LIMIT)}
                    disabled={offset + LIMIT >= total}
                    className="flex items-center gap-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Next
                    <ChevronRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
