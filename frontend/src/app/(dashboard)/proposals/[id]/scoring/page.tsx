'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { BarChart3, RefreshCw, History, TrendingUp, FileCheck } from 'lucide-react';
import { scoringApi } from '@/lib/api';
import { ProposalScore, ImprovementList, GoNoGoSummary, ColorTeamType } from '@/types';
import { ScoreGauge } from '@/components/scoring/score-gauge';
import { FactorBreakdown } from '@/components/scoring/factor-breakdown';
import { ImprovementList as ImprovementListComponent } from '@/components/scoring/improvement-list';
import { ReadinessBadge } from '@/components/scoring/readiness-badge';
import { GoNoGoCard } from '@/components/scoring/go-nogo-card';

const colorTeams: ColorTeamType[] = ['pink_team', 'red_team', 'gold_team', 'submission'];

export default function ScoringPage() {
  const params = useParams();
  const proposalId = params.id as string;

  const [score, setScore] = useState<ProposalScore | null>(null);
  const [improvements, setImprovements] = useState<ImprovementList | null>(null);
  const [goNoGo, setGoNoGo] = useState<GoNoGoSummary | null>(null);
  const [readinessStates, setReadinessStates] = useState<Record<string, string>>({});
  const [activeTab, setActiveTab] = useState<'score' | 'improvements' | 'readiness'>('score');
  const [loading, setLoading] = useState(true);
  const [calculating, setCalculating] = useState(false);
  const [error, setError] = useState('');

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      const [scoreRes, improvementsRes, goNoGoRes] = await Promise.all([
        scoringApi.getScore(proposalId).catch(() => ({ data: null })),
        scoringApi.getImprovements(proposalId).catch(() => ({ data: null })),
        scoringApi.getGoNoGo(proposalId).catch(() => ({ data: null })),
      ]);

      setScore(scoreRes.data);
      setImprovements(improvementsRes.data);
      setGoNoGo(goNoGoRes.data);

      // Fetch readiness for each team type
      const readiness: Record<string, string> = {};
      for (const team of colorTeams) {
        try {
          const res = await scoringApi.getReadiness(proposalId, team);
          if (res.data) {
            readiness[team] = res.data.readiness_level;
          }
        } catch {
          // No readiness data for this team
        }
      }
      setReadinessStates(readiness);
    } catch (err: any) {
      setError(err.response?.data?.detail?.message || 'Failed to load scoring data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (proposalId) {
      fetchData();
    }
  }, [proposalId]);

  const handleCalculateScore = async () => {
    setCalculating(true);
    try {
      const response = await scoringApi.calculateScore(proposalId, true);
      setScore(response.data);
      // Refresh improvements and go/no-go
      const [improvementsRes, goNoGoRes] = await Promise.all([
        scoringApi.getImprovements(proposalId),
        scoringApi.getGoNoGo(proposalId),
      ]);
      setImprovements(improvementsRes.data);
      setGoNoGo(goNoGoRes.data);
    } catch (err: any) {
      alert(err.response?.data?.detail?.message || 'Failed to calculate score');
    } finally {
      setCalculating(false);
    }
  };

  const handleCheckReadiness = async (teamType: ColorTeamType) => {
    try {
      const response = await scoringApi.checkReadiness(proposalId, teamType, true);
      setReadinessStates((prev) => ({
        ...prev,
        [teamType]: response.data.readiness_level,
      }));
    } catch (err: any) {
      alert(err.response?.data?.detail?.message || 'Failed to check readiness');
    }
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <BarChart3 className="w-6 h-6 text-blue-400" />
          <div>
            <h1 className="text-2xl font-semibold text-white">Proposal Scoring</h1>
            <p className="text-sm text-gray-400">
              Proposal ID: {proposalId.slice(0, 8)}...
            </p>
          </div>
        </div>
        <button
          onClick={handleCalculateScore}
          disabled={calculating}
          className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${calculating ? 'animate-spin' : ''}`} />
          {calculating ? 'Calculating...' : 'Calculate Score'}
        </button>
      </div>

      {error && (
        <div className="bg-red-900/30 border border-red-800 text-red-400 px-4 py-3 rounded-lg mb-4">
          {error}
        </div>
      )}

      {/* Tabs */}
      <div className="flex border-b border-gray-700 mb-6">
        <button
          onClick={() => setActiveTab('score')}
          className={`px-4 py-2 text-sm font-medium border-b-2 ${
            activeTab === 'score'
              ? 'border-blue-500 text-blue-400'
              : 'border-transparent text-gray-400 hover:text-gray-200'
          }`}
        >
          <BarChart3 className="w-4 h-4 inline mr-2" />
          Score Overview
        </button>
        <button
          onClick={() => setActiveTab('improvements')}
          className={`px-4 py-2 text-sm font-medium border-b-2 ${
            activeTab === 'improvements'
              ? 'border-blue-500 text-blue-400'
              : 'border-transparent text-gray-400 hover:text-gray-200'
          }`}
        >
          <TrendingUp className="w-4 h-4 inline mr-2" />
          Improvements
        </button>
        <button
          onClick={() => setActiveTab('readiness')}
          className={`px-4 py-2 text-sm font-medium border-b-2 ${
            activeTab === 'readiness'
              ? 'border-blue-500 text-blue-400'
              : 'border-transparent text-gray-400 hover:text-gray-200'
          }`}
        >
          <FileCheck className="w-4 h-4 inline mr-2" />
          Readiness
        </button>
      </div>

      {loading ? (
        <div className="text-center py-12 text-gray-400">Loading...</div>
      ) : (
        <>
          {/* Score Overview Tab */}
          {activeTab === 'score' && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Score Gauge */}
              <div className="bg-gray-800 rounded-lg border border-gray-700 p-6 flex flex-col items-center">
                {score ? (
                  <ScoreGauge
                    score={score.overall_score}
                    size="lg"
                    confidence={score.confidence_level}
                  />
                ) : (
                  <div className="text-center py-8 text-gray-400">
                    <p>No score calculated yet</p>
                    <button
                      onClick={handleCalculateScore}
                      className="mt-2 text-blue-400 hover:underline"
                    >
                      Calculate now
                    </button>
                  </div>
                )}
                {score && (
                  <p className="text-xs text-gray-500 mt-4">
                    Last scored: {new Date(score.score_date).toLocaleString()}
                  </p>
                )}
              </div>

              {/* Factor Breakdown */}
              <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
                {score ? (
                  <FactorBreakdown factors={score.factors} />
                ) : (
                  <div className="text-center py-8 text-gray-400">
                    Calculate a score to see breakdown
                  </div>
                )}
              </div>

              {/* Go/No-Go Summary */}
              <div className="lg:col-span-1">
                {goNoGo ? (
                  <GoNoGoCard summary={goNoGo} />
                ) : (
                  <div className="bg-gray-800 rounded-lg border border-gray-700 p-6 text-center text-gray-400">
                    <p>No go/no-go summary available</p>
                    <p className="text-sm">Calculate a score first</p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Improvements Tab */}
          {activeTab === 'improvements' && (
            <div className="bg-gray-800 rounded-lg border border-gray-700 p-6">
              {improvements ? (
                <ImprovementListComponent
                  improvements={improvements.improvements}
                  currentScore={improvements.current_score}
                />
              ) : (
                <div className="text-center py-8 text-gray-400">
                  Calculate a score to see improvement recommendations
                </div>
              )}
            </div>
          )}

          {/* Readiness Tab */}
          {activeTab === 'readiness' && (
            <div className="space-y-4">
              {colorTeams.map((team) => (
                <div
                  key={team}
                  className="bg-gray-800 rounded-lg border border-gray-700 p-4 flex items-center justify-between"
                >
                  <div className="flex items-center gap-4">
                    <span className="font-medium text-white w-32">
                      {team.replace('_', ' ').replace(/\b\w/g, (c) => c.toUpperCase())}
                    </span>
                    {readinessStates[team] ? (
                      <ReadinessBadge level={readinessStates[team]} />
                    ) : (
                      <span className="text-gray-500 text-sm">Not checked</span>
                    )}
                  </div>
                  <button
                    onClick={() => handleCheckReadiness(team)}
                    className="px-4 py-2 text-sm border border-gray-600 text-gray-300 rounded-lg hover:bg-gray-700"
                  >
                    Check Readiness
                  </button>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
