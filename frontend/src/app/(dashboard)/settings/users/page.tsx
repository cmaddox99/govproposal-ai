'use client';

import { useEffect, useState } from 'react';
import { Users, UserPlus, MoreVertical, Shield, ShieldOff } from 'lucide-react';
import { orgAdminApi } from '@/lib/api';
import { OrgUser } from '@/types';
import { RoleBadge } from '@/components/admin/role-badge';
import { UserInviteForm } from '@/components/admin/user-invite-form';

export default function UsersPage() {
  const [users, setUsers] = useState<OrgUser[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showInvite, setShowInvite] = useState(false);
  const [selectedUser, setSelectedUser] = useState<string | null>(null);
  const [orgId, setOrgId] = useState<string | null>(null);

  useEffect(() => {
    const storedOrgId = localStorage.getItem('currentOrgId');
    setOrgId(storedOrgId);
  }, []);

  const fetchUsers = async () => {
    if (!orgId) return;
    setLoading(true);
    try {
      const response = await orgAdminApi.listUsers(orgId);
      setUsers(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail?.message || 'Failed to load users');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (orgId) {
      fetchUsers();
    }
  }, [orgId]);

  const handleRoleChange = async (userId: string, newRole: string) => {
    try {
      await orgAdminApi.changeRole(orgId, userId, newRole);
      await fetchUsers();
    } catch (err: any) {
      alert(err.response?.data?.detail?.message || 'Failed to change role');
    }
    setSelectedUser(null);
  };

  const handleRemoveUser = async (userId: string) => {
    if (!confirm('Are you sure you want to remove this user?')) return;

    try {
      await orgAdminApi.removeUser(orgId, userId);
      await fetchUsers();
    } catch (err: any) {
      alert(err.response?.data?.detail?.message || 'Failed to remove user');
    }
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <Users className="w-6 h-6 text-gray-400" />
          <h1 className="text-2xl font-semibold text-white">User Management</h1>
        </div>
        <button
          onClick={() => setShowInvite(true)}
          className="flex items-center gap-2 bg-gradient-to-r from-emerald-500 to-blue-500 text-white px-4 py-2 rounded-lg hover:from-emerald-600 hover:to-blue-600"
        >
          <UserPlus className="w-4 h-4" />
          Invite User
        </button>
      </div>

      {error && (
        <div className="bg-red-900/20 border border-red-800 text-red-400 px-4 py-3 rounded-lg mb-4">
          {error}
        </div>
      )}

      {loading ? (
        <div className="text-center py-12 text-gray-500">Loading users...</div>
      ) : (
        <div className="bg-white/[0.03] border border-white/[0.08] rounded-lg overflow-hidden">
          <table className="w-full">
            <thead className="bg-white/[0.05] border-b border-white/[0.08]">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">
                  User
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">
                  Role
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">
                  MFA
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase">
                  Joined
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-gray-400 uppercase">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/[0.08]">
              {users.map((user) => (
                <tr key={user.id} className="hover:bg-white/[0.05]">
                  <td className="px-6 py-4">
                    <div className="text-sm font-medium text-white">
                      {user.email}
                    </div>
                    <div className="text-xs text-gray-500">
                      ID: {user.user_id.slice(0, 8)}...
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <RoleBadge role={user.role} size="sm" />
                  </td>
                  <td className="px-6 py-4">
                    {user.mfa_enabled ? (
                      <span className="flex items-center gap-1 text-green-400 text-sm">
                        <Shield className="w-4 h-4" />
                        Enabled
                      </span>
                    ) : (
                      <span className="flex items-center gap-1 text-gray-500 text-sm">
                        <ShieldOff className="w-4 h-4" />
                        Disabled
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4">
                    <span
                      className={`px-2 py-1 text-xs rounded-full ${
                        user.is_active
                          ? 'bg-green-900/30 text-green-400'
                          : 'bg-gray-800 text-gray-500'
                      }`}
                    >
                      {user.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-500">
                    {user.joined_at
                      ? new Date(user.joined_at).toLocaleDateString()
                      : 'Pending invite'}
                  </td>
                  <td className="px-6 py-4 text-right relative">
                    <button
                      onClick={() =>
                        setSelectedUser(selectedUser === user.id ? null : user.id)
                      }
                      className="p-1 hover:bg-white/[0.08] rounded"
                    >
                      <MoreVertical className="w-4 h-4 text-gray-500" />
                    </button>

                    {selectedUser === user.id && (
                      <div className="absolute right-0 mt-1 w-48 bg-gray-800 border border-white/[0.12] rounded-lg shadow-lg z-10">
                        <div className="py-1">
                          {user.role !== 'owner' && (
                            <>
                              <button
                                onClick={() => handleRoleChange(user.user_id, 'admin')}
                                disabled={user.role === 'admin'}
                                className="w-full text-left px-4 py-2 text-sm text-gray-300 hover:bg-white/[0.08] disabled:opacity-50"
                              >
                                Make Admin
                              </button>
                              <button
                                onClick={() => handleRoleChange(user.user_id, 'member')}
                                disabled={user.role === 'member'}
                                className="w-full text-left px-4 py-2 text-sm text-gray-300 hover:bg-white/[0.08] disabled:opacity-50"
                              >
                                Make Member
                              </button>
                              <hr className="my-1 border-white/[0.08]" />
                              <button
                                onClick={() => handleRemoveUser(user.user_id)}
                                className="w-full text-left px-4 py-2 text-sm text-red-400 hover:bg-red-900/30"
                              >
                                Remove User
                              </button>
                            </>
                          )}
                          {user.role === 'owner' && (
                            <p className="px-4 py-2 text-sm text-gray-500">
                              Cannot modify owner
                            </p>
                          )}
                        </div>
                      </div>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showInvite && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <UserInviteForm
            orgId={orgId}
            onSuccess={() => {
              setShowInvite(false);
              fetchUsers();
            }}
            onCancel={() => setShowInvite(false)}
          />
        </div>
      )}
    </div>
  );
}
