'use client';

import { useEffect, useState } from 'react';
import { BarChart3, TrendingUp, PieChart, Loader2, Award } from 'lucide-react';
import { dashboardApi } from '@/lib/api';

interface AnalyticsData {
  active_proposals: number;
  new_opportunities: number;
  win_rate: number;
  pending_deadlines: number;
  total_contract_value: number;
  total_submitted: number;
  average_score: number;
  pipeline: Array<{ status: string; count: number }>;
  recent_proposals: Array<{
    id: string;
    title: string;
    agency: string | null;
    status: string;
    estimated_value: number | null;
  }>;
}

const DEFAULT_DATA: AnalyticsData = {
  active_proposals: 0,
  new_opportunities: 0,
  win_rate: 0,
  pending_deadlines: 0,
  total_contract_value: 0,
  total_submitted: 0,
  average_score: 0,
  pipeline: [],
  recent_proposals: [],
};

export default function AnalyticsPage() {
  const [data, setData] = useState<AnalyticsData>(DEFAULT_DATA);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const orgId = localStorage.getItem('currentOrgId');
    if (!orgId) {
      setLoading(false);
      return;
    }

    dashboardApi.getAnalytics(orgId)
      .then((res) => setData(res.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const formatCurrency = (value: number) => {
    if (value >= 1_000_000) return `$${(value / 1_000_000).toFixed(1)}M`;
    if (value >= 1_000) return `$${(value / 1_000).toFixed(0)}K`;
    if (value === 0) return '$0';
    return `$${value.toFixed(0)}`;
  };

  const getStageLabel = (status: string) => {
    const labels: Record<string, string> = {
      draft: 'Draft', in_progress: 'In Progress', review: 'Review',
      submitted: 'Submitted', awarded: 'Awarded', not_awarded: 'Not Awarded',
    };
    return labels[status] || status;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-gray-400" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Analytics</h1>
        <p className="text-gray-400 mt-1">Insights and performance metrics for your proposals</p>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
          <TrendingUp className="w-8 h-8 text-green-500 mb-4" />
          <div className="text-3xl font-bold text-white mb-1">{data.win_rate}%</div>
          <div className="text-gray-400 text-sm">Win Rate</div>
        </div>
        <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
          <BarChart3 className="w-8 h-8 text-emerald-400 mb-4" />
          <div className="text-3xl font-bold text-white mb-1">{formatCurrency(data.total_contract_value)}</div>
          <div className="text-gray-400 text-sm">Total Contract Value</div>
        </div>
        <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
          <PieChart className="w-8 h-8 text-purple-500 mb-4" />
          <div className="text-3xl font-bold text-white mb-1">{data.total_submitted}</div>
          <div className="text-gray-400 text-sm">Proposals Submitted</div>
        </div>
        <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
          <Award className="w-8 h-8 text-orange-500 mb-4" />
          <div className="text-3xl font-bold text-white mb-1">{data.average_score}</div>
          <div className="text-gray-400 text-sm">Average Score</div>
        </div>
      </div>

      {/* Pipeline Breakdown */}
      <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
        <h2 className="text-lg font-semibold text-white mb-6">Pipeline Breakdown</h2>
        {data.pipeline.length === 0 ? (
          <p className="text-gray-500">No proposals to analyze yet</p>
        ) : (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {data.pipeline.map((stage) => (
              <div key={stage.status} className="text-center p-4 bg-white/[0.03] rounded-lg">
                <div className="text-2xl font-bold text-white">{stage.count}</div>
                <div className="text-gray-400 text-sm mt-1">{getStageLabel(stage.status)}</div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Performance Trends placeholder */}
      <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
        <h2 className="text-lg font-semibold text-white mb-6">Performance Trends</h2>
        <div className="h-64 flex items-center justify-center text-gray-500">
          <div className="text-center">
            <BarChart3 className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <p>Charts and detailed analytics coming soon</p>
          </div>
        </div>
      </div>
    </div>
  );
}
