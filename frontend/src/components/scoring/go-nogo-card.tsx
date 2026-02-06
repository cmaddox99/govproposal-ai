'use client';

import {
  CheckCircle,
  AlertTriangle,
  XCircle,
  TrendingUp,
  AlertOctagon,
  ArrowRight
} from 'lucide-react';
import { GoNoGoSummary } from '../../types';

interface GoNoGoCardProps {
  summary: GoNoGoSummary;
}

const recommendationConfig = {
  Proceed: {
    icon: CheckCircle,
    bgColor: 'bg-green-50',
    borderColor: 'border-green-200',
    textColor: 'text-green-800',
    iconColor: 'text-green-600',
  },
  'Proceed with caution': {
    icon: AlertTriangle,
    bgColor: 'bg-yellow-50',
    borderColor: 'border-yellow-200',
    textColor: 'text-yellow-800',
    iconColor: 'text-yellow-600',
  },
  'Do not proceed': {
    icon: XCircle,
    bgColor: 'bg-red-50',
    borderColor: 'border-red-200',
    textColor: 'text-red-800',
    iconColor: 'text-red-600',
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
          <p className="text-sm text-gray-600">
            Overall Score: {summary.overall_score}/100 |
            Readiness: {summary.readiness_level.replace('_', ' ')}
          </p>
        </div>
      </div>

      {/* Key Strengths */}
      {summary.key_strengths.length > 0 && (
        <div className="mb-4">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="w-4 h-4 text-green-600" />
            <h4 className="text-sm font-medium text-gray-700">Key Strengths</h4>
          </div>
          <ul className="space-y-1">
            {summary.key_strengths.map((strength, index) => (
              <li key={index} className="text-sm text-gray-600 flex items-start gap-2">
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
            <AlertOctagon className="w-4 h-4 text-red-600" />
            <h4 className="text-sm font-medium text-gray-700">Key Risks</h4>
          </div>
          <ul className="space-y-1">
            {summary.key_risks.map((risk, index) => (
              <li key={index} className="text-sm text-gray-600 flex items-start gap-2">
                <span className="text-red-500 mt-1">!</span>
                {risk}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Next Steps */}
      {summary.next_steps.length > 0 && (
        <div className="pt-4 border-t border-gray-200">
          <div className="flex items-center gap-2 mb-2">
            <ArrowRight className="w-4 h-4 text-blue-600" />
            <h4 className="text-sm font-medium text-gray-700">Recommended Next Steps</h4>
          </div>
          <ul className="space-y-1">
            {summary.next_steps.map((step, index) => (
              <li key={index} className="text-sm text-gray-600 flex items-start gap-2">
                <span className="text-blue-500 font-medium">{index + 1}.</span>
                {step}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
