'use client';

import { useState } from 'react';
import { UserPlus, X } from 'lucide-react';
import { orgAdminApi } from '@/lib/api';

interface UserInviteFormProps {
  orgId: string;
  onSuccess: () => void;
  onCancel: () => void;
}

export function UserInviteForm({ orgId, onSuccess, onCancel }: UserInviteFormProps) {
  const [email, setEmail] = useState('');
  const [role, setRole] = useState('member');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await orgAdminApi.inviteUser(orgId, email, role);
      onSuccess();
    } catch (err: any) {
      setError(err.response?.data?.detail?.message || 'Failed to invite user');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-800 border border-white/[0.12] rounded-lg shadow-lg p-6 max-w-md">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <UserPlus className="w-5 h-5 text-emerald-400" />
          <h3 className="font-semibold text-white">Invite User</h3>
        </div>
        <button
          onClick={onCancel}
          className="p-1 hover:bg-white/[0.08] rounded"
        >
          <X className="w-5 h-5 text-gray-500" />
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            Email address
          </label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="user@example.com"
            required
            className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] text-white rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent placeholder-gray-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1">
            Role
          </label>
          <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
            className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] text-white rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
          >
            <option value="member">Member</option>
            <option value="admin">Administrator</option>
          </select>
          <p className="mt-1 text-xs text-gray-500">
            {role === 'member'
              ? 'Can view/edit assigned proposals and run analyses'
              : 'Can manage users, configure templates, and view audit logs'}
          </p>
        </div>

        {error && (
          <p className="text-red-400 text-sm">{error}</p>
        )}

        <div className="flex gap-3">
          <button
            type="submit"
            disabled={loading}
            className="flex-1 bg-gradient-to-r from-emerald-500 to-blue-500 text-white py-2 px-4 rounded-lg hover:from-emerald-600 hover:to-blue-600 disabled:opacity-50"
          >
            {loading ? 'Sending invite...' : 'Send Invite'}
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="px-4 py-2 border border-white/[0.08] text-gray-300 rounded-lg hover:bg-white/[0.08]"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}
