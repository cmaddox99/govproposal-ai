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
    bgColor: 'bg-purple-100',
    textColor: 'text-purple-800',
    borderColor: 'border-purple-200',
  },
  admin: {
    label: 'Admin',
    icon: Shield,
    bgColor: 'bg-blue-100',
    textColor: 'text-blue-800',
    borderColor: 'border-blue-200',
  },
  member: {
    label: 'Member',
    icon: User,
    bgColor: 'bg-gray-100',
    textColor: 'text-gray-700',
    borderColor: 'border-gray-200',
  },
  super_user: {
    label: 'Super User',
    icon: Crown,
    bgColor: 'bg-yellow-100',
    textColor: 'text-yellow-800',
    borderColor: 'border-yellow-200',
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
