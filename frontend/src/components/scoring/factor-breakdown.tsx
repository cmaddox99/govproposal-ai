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

// Criteria sourced from backend/src/govproposal/scoring/templates.py — keep in sync
const factorCriteria: Record<string, string[]> = {
  completeness: [
    'All expected sections present (Executive Summary, Technical, Management, etc.)',
    'Each section contains substantive content, not placeholder text',
    'Appropriate word counts for each section type',
    'No obvious gaps, "TBD" markers, or incomplete areas',
    'Required attachments and exhibits referenced',
  ],
  technical_depth: [
    'Specific technical approaches, not generic statements',
    'Concrete methodologies, tools, and processes named explicitly',
    'Evidence of deep understanding of the problem domain',
    'Appropriate use of technical terminology',
    'Clear connection between approach and requirements',
    'No vague language like "best practices" or "industry standard"',
  ],
  section_l_compliance: [
    'Format requirements met (page limits, margins, fonts)',
    'All required elements from Section L addressed',
    'Proper organization as specified in solicitation instructions',
    'Required certifications and representations included',
    'Submission requirements understood and followed',
  ],
  section_m_alignment: [
    'Each evaluation factor explicitly addressed',
    'Content organized to highlight evaluation criteria',
    'Discriminators clearly presented',
    'Win themes aligned with evaluation priorities',
    'Relative emphasis matches stated factor weights',
  ],
  sow_coverage: [
    'Statement of Work requirements fully addressed',
    'Deliverables mapped to SOW line items',
    'Performance standards referenced',
    'All task areas covered',
  ],
  pp_mapping: [
    'Past performance contracts relevant to current work',
    'Outcomes and ratings documented with specifics',
    'Clear relevance connections to current opportunity',
    'Contact information provided for verification',
  ],
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
              <span className="text-gray-300 relative group cursor-help inline-flex items-center gap-1">
                {factorLabels[factor.factor_type] || factor.factor_type}
                <span className="text-gray-500 text-xs">&#9432;</span>
                {factorCriteria[factor.factor_type] && (
                  <div className="absolute left-0 bottom-full mb-2 w-72 p-3 bg-gray-800 border border-gray-600 rounded-lg shadow-xl text-xs text-gray-200 hidden group-hover:block z-50">
                    <p className="font-semibold text-white mb-1.5">
                      {factorLabels[factor.factor_type]} Criteria:
                    </p>
                    <ul className="space-y-1 list-disc list-inside">
                      {factorCriteria[factor.factor_type].map((criterion, i) => (
                        <li key={i}>{criterion}</li>
                      ))}
                    </ul>
                  </div>
                )}
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
