'use client';

import { Crown, Shield, User } from 'lucide-react';

interface RoleBadgeProps {
  role: string;
  size?: 'sm' | 'md';
}

const roleConfig = {
  owner: {
    label: 'Owner',
    icon: Crown,
    bgColor: 'bg-purple-900/30',
    textColor: 'text-purple-300',
    borderColor: 'border-purple-700/50',
  },
  admin: {
    label: 'Admin',
    icon: Shield,
    bgColor: 'bg-blue-900/30',
    textColor: 'text-blue-300',
    borderColor: 'border-blue-700/50',
  },
  member: {
    label: 'Member',
    icon: User,
    bgColor: 'bg-gray-800',
    textColor: 'text-gray-300',
    borderColor: 'border-gray-700',
  },
  super_user: {
    label: 'Super User',
    icon: Crown,
    bgColor: 'bg-yellow-900/30',
    textColor: 'text-yellow-300',
    borderColor: 'border-yellow-700/50',
  },
};

export function RoleBadge({ role, size = 'md' }: RoleBadgeProps) {
  const config = roleConfig[role as keyof typeof roleConfig] || roleConfig.member;
  const Icon = config.icon;

  const sizeClasses = size === 'sm'
    ? 'text-xs px-2 py-0.5'
    : 'text-sm px-2.5 py-1';

  const iconSize = size === 'sm' ? 'w-3 h-3' : 'w-4 h-4';

  return (
    <span
      className={`inline-flex items-center gap-1 rounded-full border font-medium ${config.bgColor} ${config.textColor} ${config.borderColor} ${sizeClasses}`}
    >
      <Icon className={iconSize} />
      {config.label}
    </span>
  );
}
