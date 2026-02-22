'use client';

import { ScoreFactor } from '@/types';

interface FactorBreakdownProps {
  factors: ScoreFactor[];
}

const factorLabels: Record<string, string> = {
  completeness: 'Completeness',
  technical_depth: 'Technical Depth',
  section_l_compliance: 'Section L Compliance',
  section_m_alignment: 'Section M Alignment',
  sow_coverage: 'SOW Coverage',
  pp_mapping: 'Past Performance',
};

const getBarColor = (score: number) => {
  if (score >= 80) return 'bg-green-500';
  if (score >= 60) return 'bg-yellow-500';
  if (score >= 40) return 'bg-orange-500';
  return 'bg-red-500';
};

export function FactorBreakdown({ factors }: FactorBreakdownProps) {
  return (
    <div className="space-y-4">
      <h3 className="font-medium text-white">Score Breakdown</h3>

      <div className="space-y-3">
        {factors.map((factor) => (
          <div key={factor.id} className="space-y-1">
            <div className="flex justify-between text-sm">
              <span className="text-gray-300">
                {factorLabels[factor.factor_type] || factor.factor_type}
              </span>
              <span className="font-medium text-white">
                {factor.raw_score}
                <span className="text-gray-500 text-xs ml-1">
                  ({(factor.factor_weight * 100).toFixed(0)}%)
                </span>
              </span>
            </div>

            <div className="w-full bg-gray-700 rounded-full h-2">
              <div
                className={`h-2 rounded-full transition-all duration-500 ${getBarColor(factor.raw_score)}`}
                style={{ width: `${factor.raw_score}%` }}
              />
            </div>

            {factor.evidence_summary && (
              <p className="text-xs text-gray-500 mt-1">
                {factor.evidence_summary}
              </p>
            )}
          </div>
        ))}
      </div>

      <div className="pt-3 border-t border-gray-700">
        <div className="flex justify-between text-sm">
          <span className="text-gray-400">Weighted Average</span>
          <span className="font-semibold text-white">
            {factors.reduce((sum, f) => sum + f.weighted_score, 0).toFixed(0)}
          </span>
        </div>
      </div>
    </div>
  );
}
