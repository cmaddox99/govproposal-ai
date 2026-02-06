'use client';

import { ArrowUp, AlertCircle } from 'lucide-react';
import { ScoreImprovement } from '../../types';

interface ImprovementListProps {
  improvements: ScoreImprovement[];
  currentScore: number;
}

const getPriorityBadge = (priority: number) => {
  if (priority <= 3) {
    return (
      <span className="px-2 py-0.5 text-xs font-medium bg-red-100 text-red-700 rounded">
        High
      </span>
    );
  }
  if (priority <= 6) {
    return (
      <span className="px-2 py-0.5 text-xs font-medium bg-yellow-100 text-yellow-700 rounded">
        Medium
      </span>
    );
  }
  return (
    <span className="px-2 py-0.5 text-xs font-medium bg-gray-100 text-gray-700 rounded">
      Low
    </span>
  );
};

const factorLabels: Record<string, string> = {
  completeness: 'Completeness',
  technical_depth: 'Technical Depth',
  section_l_compliance: 'Compliance',
  section_m_alignment: 'Alignment',
};

export function ImprovementList({ improvements, currentScore }: ImprovementListProps) {
  if (improvements.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        <AlertCircle className="w-8 h-8 mx-auto mb-2 opacity-50" />
        <p>No improvement suggestions available.</p>
        <p className="text-sm">Calculate a score first to see recommendations.</p>
      </div>
    );
  }

  const totalPotentialGain = improvements.reduce((sum, i) => sum + i.potential_gain, 0);
  const potentialScore = Math.min(100, currentScore + totalPotentialGain);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="font-medium text-gray-900">Improvement Opportunities</h3>
        <div className="flex items-center gap-2 text-sm">
          <ArrowUp className="w-4 h-4 text-green-600" />
          <span className="text-green-600 font-medium">
            Up to {potentialScore} potential
          </span>
        </div>
      </div>

      <div className="space-y-3">
        {improvements.map((improvement, index) => (
          <div
            key={index}
            className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-sm font-medium text-gray-900">
                    {improvement.action}
                  </span>
                  {getPriorityBadge(improvement.priority)}
                </div>
                <p className="text-sm text-gray-600">{improvement.details}</p>
                <div className="mt-2 flex items-center gap-4 text-xs text-gray-500">
                  <span>
                    {factorLabels[improvement.factor] || improvement.factor}
                  </span>
                  <span>Current: {improvement.current_score}/100</span>
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm font-medium text-green-600">
                  +{improvement.potential_gain}
                </div>
                <div className="text-xs text-gray-400">points</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
