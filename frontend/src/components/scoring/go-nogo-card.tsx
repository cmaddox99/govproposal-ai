'use client';

import {
  CheckCircle,
  AlertTriangle,
  XCircle,
  TrendingUp,
  AlertOctagon,
  ArrowRight
} from 'lucide-react';
import { GoNoGoSummary } from '@/types';

interface GoNoGoCardProps {
  summary: GoNoGoSummary;
}

const recommendationConfig = {
  Proceed: {
    icon: CheckCircle,
    bgColor: 'bg-green-900/20',
    borderColor: 'border-green-800',
    textColor: 'text-green-400',
    iconColor: 'text-green-500',
  },
  'Proceed with caution': {
    icon: AlertTriangle,
    bgColor: 'bg-yellow-900/20',
    borderColor: 'border-yellow-800',
    textColor: 'text-yellow-400',
    iconColor: 'text-yellow-500',
  },
  'Do not proceed': {
    icon: XCircle,
    bgColor: 'bg-red-900/20',
    borderColor: 'border-red-800',
    textColor: 'text-red-400',
    iconColor: 'text-red-500',
  },
};

export function GoNoGoCard({ summary }: GoNoGoCardProps) {
  const config = recommendationConfig[summary.recommendation as keyof typeof recommendationConfig]
    || recommendationConfig['Proceed with caution'];
  const Icon = config.icon;

  return (
    <div className={`rounded-lg border ${config.borderColor} ${config.bgColor} p-6`}>
      {/* Header */}
      <div className="flex items-center gap-3 mb-4">
        <Icon className={`w-8 h-8 ${config.iconColor}`} />
        <div>
          <h3 className={`text-lg font-semibold ${config.textColor}`}>
            {summary.recommendation}
          </h3>
          <p className="text-sm text-gray-400">
            Overall Score: {summary.overall_score}/100 |
            Readiness: {summary.readiness_level.replace('_', ' ')}
          </p>
        </div>
      </div>

      {/* Key Strengths */}
      {summary.key_strengths.length > 0 && (
        <div className="mb-4">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="w-4 h-4 text-green-400" />
            <h4 className="text-sm font-medium text-gray-300">Key Strengths</h4>
          </div>
          <ul className="space-y-1">
            {summary.key_strengths.map((strength, index) => (
              <li key={index} className="text-sm text-gray-400 flex items-start gap-2">
                <span className="text-green-500 mt-1">+</span>
                {strength}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Key Risks */}
      {summary.key_risks.length > 0 && (
        <div className="mb-4">
          <div className="flex items-center gap-2 mb-2">
            <AlertOctagon className="w-4 h-4 text-red-400" />
            <h4 className="text-sm font-medium text-gray-300">Key Risks</h4>
          </div>
          <ul className="space-y-1">
            {summary.key_risks.map((risk, index) => (
              <li key={index} className="text-sm text-gray-400 flex items-start gap-2">
                <span className="text-red-500 mt-1">!</span>
                {risk}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Next Steps */}
      {summary.next_steps.length > 0 && (
        <div className="pt-4 border-t border-gray-700">
          <div className="flex items-center gap-2 mb-2">
            <ArrowRight className="w-4 h-4 text-blue-400" />
            <h4 className="text-sm font-medium text-gray-300">Recommended Next Steps</h4>
          </div>
          <ul className="space-y-1">
            {summary.next_steps.map((step, index) => (
              <li key={index} className="text-sm text-gray-400 flex items-start gap-2">
                <span className="text-blue-400 font-medium">{index + 1}.</span>
                {step}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
