'use client';

import { useEffect, useState } from 'react';
import { BarChart3, TrendingUp, PieChart, Loader2, Award, Building2 } from 'lucide-react';
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

interface TrendPoint {
  month: string;
  proposals_created: number;
  proposals_submitted: number;
  proposals_awarded: number;
  avg_score: number | null;
}

interface ScoreTrend {
  proposal_id: string;
  title: string;
  scores: Array<{ score: number; date: string }>;
}

interface TrendsData {
  monthly_activity: TrendPoint[];
  score_trends: ScoreTrend[];
  top_agencies: Array<{ agency: string; count: number; awarded: number }>;
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
  const [trends, setTrends] = useState<TrendsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const orgId = localStorage.getItem('currentOrgId');
    if (!orgId) {
      setLoading(false);
      return;
    }

    Promise.all([
      dashboardApi.getAnalytics(orgId),
      dashboardApi.getTrends(orgId).catch(() => null),
    ])
      .then(([analyticsRes, trendsRes]) => {
        setData(analyticsRes.data);
        if (trendsRes) setTrends(trendsRes.data);
      })
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

  const getStageColor = (status: string) => {
    const colors: Record<string, string> = {
      draft: 'bg-gray-500', in_progress: 'bg-blue-500', review: 'bg-yellow-500',
      submitted: 'bg-purple-500', awarded: 'bg-green-500', not_awarded: 'bg-red-500',
    };
    return colors[status] || 'bg-gray-500';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-gray-400" />
      </div>
    );
  }

  const maxMonthlyCount = trends?.monthly_activity.length
    ? Math.max(...trends.monthly_activity.map(m => m.proposals_created), 1)
    : 1;

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
                <div className={`w-3 h-3 rounded-full ${getStageColor(stage.status)} mx-auto mb-2`} />
                <div className="text-2xl font-bold text-white">{stage.count}</div>
                <div className="text-gray-400 text-sm mt-1">{getStageLabel(stage.status)}</div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Monthly Activity */}
        <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
          <h2 className="text-lg font-semibold text-white mb-6">Monthly Activity</h2>
          {!trends?.monthly_activity.length ? (
            <div className="h-48 flex items-center justify-center text-gray-500 text-sm">
              No activity data yet. Create proposals to see trends.
            </div>
          ) : (
            <div className="space-y-3">
              {trends.monthly_activity.map((month) => (
                <div key={month.month}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm text-gray-400">{month.month}</span>
                    <div className="flex items-center gap-3 text-xs">
                      <span className="text-blue-400">{month.proposals_created} created</span>
                      <span className="text-purple-400">{month.proposals_submitted} submitted</span>
                      <span className="text-green-400">{month.proposals_awarded} won</span>
                    </div>
                  </div>
                  <div className="flex gap-1 h-4">
                    <div
                      className="bg-blue-500/60 rounded-sm"
                      style={{ width: `${(month.proposals_created / maxMonthlyCount) * 100}%` }}
                      title={`${month.proposals_created} created`}
                    />
                    {month.proposals_submitted > 0 && (
                      <div
                        className="bg-purple-500/60 rounded-sm"
                        style={{ width: `${(month.proposals_submitted / maxMonthlyCount) * 100}%` }}
                        title={`${month.proposals_submitted} submitted`}
                      />
                    )}
                    {month.proposals_awarded > 0 && (
                      <div
                        className="bg-green-500/60 rounded-sm"
                        style={{ width: `${(month.proposals_awarded / maxMonthlyCount) * 100}%` }}
                        title={`${month.proposals_awarded} awarded`}
                      />
                    )}
                  </div>
                  {month.avg_score !== null && (
                    <div className="text-xs text-gray-500 mt-0.5">Avg score: {month.avg_score}</div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Top Agencies */}
        <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
          <div className="flex items-center gap-2 mb-6">
            <Building2 className="w-5 h-5 text-gray-400" />
            <h2 className="text-lg font-semibold text-white">Top Agencies</h2>
          </div>
          {!trends?.top_agencies.length ? (
            <div className="h-48 flex items-center justify-center text-gray-500 text-sm">
              No agency data yet. Create proposals with agency info.
            </div>
          ) : (
            <div className="space-y-4">
              {trends.top_agencies.map((agency, i) => {
                const maxCount = trends.top_agencies[0].count;
                return (
                  <div key={i}>
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm text-white truncate max-w-[60%]">{agency.agency}</span>
                      <div className="flex items-center gap-2 text-xs">
                        <span className="text-gray-400">{agency.count} proposals</span>
                        {agency.awarded > 0 && (
                          <span className="text-green-400">{agency.awarded} won</span>
                        )}
                      </div>
                    </div>
                    <div className="bg-white/[0.05] rounded-full h-2.5 overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-emerald-500 to-blue-500 rounded-full"
                        style={{ width: `${(agency.count / maxCount) * 100}%` }}
                      />
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>

      {/* Score Trends */}
      <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
        <h2 className="text-lg font-semibold text-white mb-6">Score History</h2>
        {!trends?.score_trends.length ? (
          <div className="h-32 flex items-center justify-center text-gray-500 text-sm">
            Score proposals to see score trends over time.
          </div>
        ) : (
          <div className="space-y-4">
            {trends.score_trends.map((trend) => (
              <div key={trend.proposal_id} className="p-4 bg-white/[0.03] rounded-lg">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-white font-medium text-sm truncate max-w-[70%]">{trend.title}</span>
                  <span className="text-emerald-400 font-bold">
                    {trend.scores[trend.scores.length - 1]?.score ?? 'N/A'}
                  </span>
                </div>
                <div className="flex items-end gap-1 h-12">
                  {trend.scores.map((s, i) => (
                    <div
                      key={i}
                      className="flex-1 bg-gradient-to-t from-emerald-500/40 to-blue-500/40 rounded-t-sm relative group"
                      style={{ height: `${s.score}%` }}
                      title={`Score: ${s.score} — ${new Date(s.date).toLocaleDateString()}`}
                    >
                      <div className="absolute -top-5 left-1/2 -translate-x-1/2 text-[10px] text-gray-500 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                        {s.score}
                      </div>
                    </div>
                  ))}
                </div>
                <div className="flex justify-between mt-1">
                  <span className="text-[10px] text-gray-600">
                    {trend.scores.length > 0 && new Date(trend.scores[0].date).toLocaleDateString()}
                  </span>
                  <span className="text-[10px] text-gray-600">
                    {trend.scores.length > 1 && new Date(trend.scores[trend.scores.length - 1].date).toLocaleDateString()}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
