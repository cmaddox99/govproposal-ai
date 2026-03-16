'use client';

import { useEffect, useState } from 'react';
import {
  FileText,
  Search,
  TrendingUp,
  Clock,
  ArrowUpRight,
  ArrowDownRight,
  AlertCircle,
  CheckCircle,
  Loader2,
} from 'lucide-react';
import Link from 'next/link';
import { dashboardApi } from '@/lib/api';

interface PipelineStage {
  status: string;
  count: number;
}

interface RecentProposal {
  id: string;
  title: string;
  agency: string | null;
  status: string;
  estimated_value: number | null;
  due_date: string | null;
  updated_at: string;
}

interface DashboardData {
  active_proposals: number;
  new_opportunities: number;
  win_rate: number;
  pending_deadlines: number;
  pipeline: PipelineStage[];
  recent_proposals: RecentProposal[];
}

const DEFAULT_DATA: DashboardData = {
  active_proposals: 0,
  new_opportunities: 0,
  win_rate: 0,
  pending_deadlines: 0,
  pipeline: [],
  recent_proposals: [],
};

export default function DashboardPage() {
  const [orgName, setOrgName] = useState('');
  const [data, setData] = useState<DashboardData>(DEFAULT_DATA);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedOrgName = localStorage.getItem('currentOrgName');
    const orgId = localStorage.getItem('currentOrgId');
    if (storedOrgName) setOrgName(storedOrgName);

    if (orgId) {
      dashboardApi.getDashboard(orgId)
        .then((res) => setData(res.data))
        .catch(() => {})
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const getStageColor = (status: string) => {
    const colors: Record<string, string> = {
      draft: 'bg-gray-600',
      in_progress: 'bg-blue-600',
      review: 'bg-yellow-600',
      submitted: 'bg-purple-600',
      awarded: 'bg-green-600',
      not_awarded: 'bg-red-600',
      cancelled: 'bg-gray-400',
    };
    return colors[status] || 'bg-gray-600';
  };

  const getStageLabel = (status: string) => {
    const labels: Record<string, string> = {
      draft: 'Draft',
      in_progress: 'In Progress',
      review: 'Review',
      submitted: 'Submitted',
      awarded: 'Awarded',
      not_awarded: 'Not Awarded',
      cancelled: 'Cancelled',
    };
    return labels[status] || status;
  };

  const formatCurrency = (value: number | null) => {
    if (!value) return 'N/A';
    if (value >= 1_000_000) return `$${(value / 1_000_000).toFixed(1)}M`;
    if (value >= 1_000) return `$${(value / 1_000).toFixed(0)}K`;
    return `$${value.toFixed(0)}`;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-gray-400" />
      </div>
    );
  }

  const metrics = [
    { label: 'Active Proposals', value: data.active_proposals, icon: FileText, color: 'blue' },
    { label: 'New Opportunities', value: data.new_opportunities, icon: Search, color: 'green' },
    { label: 'Win Rate', value: `${data.win_rate}%`, icon: TrendingUp, color: 'purple' },
    { label: 'Pending Deadlines', value: data.pending_deadlines, icon: Clock, color: 'orange' },
  ];

  const maxPipelineCount = data.pipeline.length > 0 ? Math.max(...data.pipeline.map(s => s.count), 1) : 1;

  return (
    <div className="space-y-8">
      {/* Welcome Header */}
      <div>
        <h1 className="text-3xl font-bold text-white">Welcome back!</h1>
        <p className="text-gray-400 mt-1">
          {orgName ? `${orgName} Dashboard` : 'Here\'s what\'s happening with your proposals'}
        </p>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {metrics.map((metric) => (
          <div
            key={metric.label}
            className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6"
          >
            <div className="flex items-center justify-between mb-4">
              <div className={`p-3 rounded-lg bg-${metric.color}-600/20`}>
                <metric.icon className={`w-6 h-6 text-${metric.color}-500`} />
              </div>
            </div>
            <div className="text-3xl font-bold text-white mb-1">{metric.value}</div>
            <div className="text-gray-500 text-sm">{metric.label}</div>
          </div>
        ))}
      </div>

      {/* Pipeline and Alerts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Pipeline Overview */}
        <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
          <h2 className="text-lg font-semibold text-white mb-6">Pipeline Overview</h2>
          {data.pipeline.length === 0 ? (
            <p className="text-gray-500">No proposals in pipeline yet</p>
          ) : (
            <div className="space-y-4">
              {data.pipeline.map((stage) => (
                <div key={stage.status} className="flex items-center gap-4">
                  <div className="w-28 text-sm text-gray-400">{getStageLabel(stage.status)}</div>
                  <div className="flex-1 bg-white/[0.05] rounded-full h-4 overflow-hidden">
                    <div
                      className={`h-full ${getStageColor(stage.status)} rounded-full`}
                      style={{ width: `${(stage.count / maxPipelineCount) * 100}%` }}
                    />
                  </div>
                  <div className="w-8 text-sm text-white font-medium">{stage.count}</div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent Alerts placeholder */}
        <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
          <h2 className="text-lg font-semibold text-white mb-6">Recent Alerts</h2>
          <div className="space-y-4">
            <div className="flex items-start gap-3 p-3 bg-white/[0.03] rounded-lg">
              <AlertCircle className="w-5 h-5 text-blue-500" />
              <div className="flex-1 min-w-0">
                <p className="text-sm text-white">Welcome to GovProposalAI</p>
                <p className="text-xs text-gray-500 mt-1">Get started by creating a proposal</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Proposals */}
      <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold text-white">Recent Proposals</h2>
          <Link href="/proposals" className="text-sm text-emerald-400 hover:text-emerald-300">
            View all
          </Link>
        </div>
        {data.recent_proposals.length === 0 ? (
          <p className="text-gray-500">No proposals yet. Create your first proposal to get started.</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-white/[0.08]">
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-400">Title</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-400">Agency</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-400">Value</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-400">Status</th>
                  <th className="text-left py-3 px-4 text-sm font-medium text-gray-400">Due Date</th>
                </tr>
              </thead>
              <tbody>
                {data.recent_proposals.map((proposal) => (
                  <tr key={proposal.id} className="border-b border-white/[0.08]/50 hover:bg-white/[0.02]">
                    <td className="py-4 px-4">
                      <Link href={`/proposals/${proposal.id}/scoring`} className="text-white hover:text-blue-400">
                        {proposal.title}
                      </Link>
                    </td>
                    <td className="py-4 px-4 text-gray-400">{proposal.agency || 'N/A'}</td>
                    <td className="py-4 px-4 text-white font-medium">{formatCurrency(proposal.estimated_value)}</td>
                    <td className="py-4 px-4">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStageColor(proposal.status)} text-white`}>
                        {getStageLabel(proposal.status)}
                      </span>
                    </td>
                    <td className="py-4 px-4 text-gray-400">
                      {proposal.due_date ? new Date(proposal.due_date).toLocaleDateString() : 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
