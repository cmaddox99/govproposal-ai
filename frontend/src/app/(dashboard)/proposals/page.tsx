'use client';

import { useState } from 'react';
import { FileText, Plus, Search, Filter } from 'lucide-react';
import Link from 'next/link';

interface Proposal {
  id: string;
  title: string;
  status: 'draft' | 'in_progress' | 'submitted' | 'awarded' | 'not_awarded';
  score: number | null;
  dueDate: string;
  updatedAt: string;
}

const statusColors = {
  draft: 'bg-gray-100 text-gray-700',
  in_progress: 'bg-blue-100 text-blue-700',
  submitted: 'bg-green-100 text-green-700',
  awarded: 'bg-emerald-100 text-emerald-700',
  not_awarded: 'bg-red-100 text-red-700',
};

const statusLabels = {
  draft: 'Draft',
  in_progress: 'In Progress',
  submitted: 'Submitted',
  awarded: 'Awarded',
  not_awarded: 'Not Awarded',
};

export default function ProposalsPage() {
  const [proposals, setProposals] = useState<Proposal[]>([]);
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Proposals</h1>
          <p className="text-gray-500 mt-1">Manage your government proposals</p>
        </div>
        <button className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
          <Plus className="w-4 h-4" />
          New Proposal
        </button>
      </div>

      {/* Search and Filter */}
      <div className="bg-white rounded-lg shadow p-4 mb-6">
        <div className="flex gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder="Search proposals..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
            <Filter className="w-4 h-4" />
            Filter
          </button>
        </div>
      </div>

      {/* Proposals List */}
      {proposals.length === 0 ? (
        <div className="bg-white rounded-lg shadow p-12 text-center">
          <FileText className="w-12 h-12 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No proposals yet</h3>
          <p className="text-gray-500 mb-4">
            Get started by creating your first proposal
          </p>
          <button className="inline-flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
            <Plus className="w-4 h-4" />
            Create Proposal
          </button>
        </div>
      ) : (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="w-full">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Title
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Score
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Due Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Last Updated
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {proposals.map((proposal) => (
                <tr key={proposal.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4">
                    <Link
                      href={`/proposals/${proposal.id}/scoring`}
                      className="text-blue-600 hover:underline font-medium"
                    >
                      {proposal.title}
                    </Link>
                  </td>
                  <td className="px-6 py-4">
                    <span
                      className={`px-2 py-1 text-xs rounded-full ${
                        statusColors[proposal.status]
                      }`}
                    >
                      {statusLabels[proposal.status]}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    {proposal.score !== null ? (
                      <span className="font-medium">{proposal.score}%</span>
                    ) : (
                      <span className="text-gray-400">-</span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-gray-500">
                    {new Date(proposal.dueDate).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 text-gray-500">
                    {new Date(proposal.updatedAt).toLocaleDateString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
