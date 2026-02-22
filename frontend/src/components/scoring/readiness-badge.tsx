'use client';

import { CheckCircle, AlertTriangle, XCircle, Clock } from 'lucide-react';

interface ReadinessBadgeProps {
  level: string;
  teamType?: string;
  size?: 'sm' | 'md' | 'lg';
}

const levelConfig = {
  ready: {
    icon: CheckCircle,
    label: 'Ready',
    bgColor: 'bg-green-900/40',
    textColor: 'text-green-400',
    borderColor: 'border-green-800',
  },
  needs_work: {
    icon: AlertTriangle,
    label: 'Needs Work',
    bgColor: 'bg-yellow-900/40',
    textColor: 'text-yellow-400',
    borderColor: 'border-yellow-800',
  },
  not_ready: {
    icon: XCircle,
    label: 'Not Ready',
    bgColor: 'bg-red-900/40',
    textColor: 'text-red-400',
    borderColor: 'border-red-800',
  },
  pending: {
    icon: Clock,
    label: 'Pending',
    bgColor: 'bg-gray-800',
    textColor: 'text-gray-400',
    borderColor: 'border-gray-700',
  },
};

const teamLabels: Record<string, string> = {
  pink_team: 'Pink Team',
  red_team: 'Red Team',
  gold_team: 'Gold Team',
  submission: 'Submission',
};

export function ReadinessBadge({ level, teamType, size = 'md' }: ReadinessBadgeProps) {
  const config = levelConfig[level as keyof typeof levelConfig] || levelConfig.pending;
  const Icon = config.icon;

  const sizeClasses = {
    sm: 'text-xs px-2 py-0.5',
    md: 'text-sm px-3 py-1',
    lg: 'text-base px-4 py-1.5',
  };

  const iconSizes = {
    sm: 'w-3 h-3',
    md: 'w-4 h-4',
    lg: 'w-5 h-5',
  };

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border font-medium ${config.bgColor} ${config.textColor} ${config.borderColor} ${sizeClasses[size]}`}
    >
      <Icon className={iconSizes[size]} />
      {teamType && <span>{teamLabels[teamType] || teamType}:</span>}
      {config.label}
    </span>
  );
}
