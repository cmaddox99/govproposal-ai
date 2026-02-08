'use client';

import { useEffect, useState } from 'react';
import { ClipboardList, Filter, RefreshCw } from 'lucide-react';
import { orgAdminApi } from '@/lib/api';
import { AuditLog, AuditLogList } from '@/types';

const eventTypeLabels: Record<string, string> = {
  login_success: 'Login Success',
  login_failure: 'Login Failed',
  logout: 'Logout',
  password_change: 'Password Changed',
  mfa_setup_completed: 'MFA Enabled',
  mfa_disabled: 'MFA Disabled',
  user_invited: 'User Invited',
  user_role_changed: 'Role Changed',
  user_removed: 'User Removed',
  proposal_created: 'Proposal Created',
  proposal_updated: 'Proposal Updated',
  proposal_scored: 'Proposal Scored',
};

const outcomeColors: Record<string, string> = {
  success: 'bg-green-100 text-green-700',
  failure: 'bg-red-100 text-red-700',
};

export default function AuditPage() {
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [eventTypeFilter, setEventTypeFilter] = useState('');
  const [page, setPage] = useState(0);
  const [orgId, setOrgId] = useState<string | null>(null);
  const limit = 20;

  useEffect(() => {
    const storedOrgId = localStorage.getItem('currentOrgId');
    setOrgId(storedOrgId);
  }, []);

  const fetchLogs = async () => {
    if (!orgId) return;
    setLoading(true);
    try {
      const params: Record<string, unknown> = {
        limit,
        offset: page * limit,
      };
      if (eventTypeFilter) {
        params.event_type = eventTypeFilter;
      }

      const response = await orgAdminApi.getAuditLogs(orgId, params);
      const data: AuditLogList = response.data;
      setLogs(data.items);
      setTotal(data.total);
    } catch (err: any) {
      setError(err.response?.data?.detail?.message || 'Failed to load audit logs');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (orgId) {
      fetchLogs();
    }
  }, [page, eventTypeFilter, orgId]);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      dateStyle: 'medium',
      timeStyle: 'short',
    }).format(date);
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <ClipboardList className="w-6 h-6 text-gray-600" />
          <h1 className="text-2xl font-semibold">Audit Logs</h1>
        </div>
        <button
          onClick={fetchLogs}
          className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
        >
          <RefreshCw className="w-4 h-4" />
          Refresh
        </button>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-4 mb-4">
        <div className="flex items-center gap-4">
          <Filter className="w-4 h-4 text-gray-500" />
          <div className="flex-1">
            <select
              value={eventTypeFilter}
              onChange={(e) => {
                setEventTypeFilter(e.target.value);
                setPage(0);
              }}
              className="px-3 py-2 border border-gray-300 rounded-lg text-sm"
            >
              <option value="">All Events</option>
              {Object.entries(eventTypeLabels).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </div>
          <span className="text-sm text-gray-500">
            {total} total events
          </span>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
          {error}
        </div>
      )}

      {loading ? (
        <div className="text-center py-12 text-gray-500">Loading audit logs...</div>
      ) : logs.length === 0 ? (
        <div className="text-center py-12 text-gray-500">No audit logs found</div>
      ) : (
        <>
          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Time
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Event
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Actor
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Action
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Outcome
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    IP Address
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {logs.map((log) => (
                  <tr key={log.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 text-sm text-gray-500 whitespace-nowrap">
                      {formatDate(log.event_time)}
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm font-medium">
                        {eventTypeLabels[log.event_type] || log.event_type}
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className="text-sm text-gray-900">
                        {log.actor_email || 'System'}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600 max-w-xs truncate">
                      {log.action}
                    </td>
                    <td className="px-6 py-4">
                      <span
                        className={`px-2 py-1 text-xs rounded-full ${
                          outcomeColors[log.outcome] || 'bg-gray-100 text-gray-700'
                        }`}
                      >
                        {log.outcome}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      {log.ip_address || '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          <div className="flex items-center justify-between mt-4">
            <span className="text-sm text-gray-500">
              Showing {page * limit + 1} - {Math.min((page + 1) * limit, total)} of {total}
            </span>
            <div className="flex gap-2">
              <button
                onClick={() => setPage(Math.max(0, page - 1))}
                disabled={page === 0}
                className="px-3 py-1 border rounded hover:bg-gray-50 disabled:opacity-50"
              >
                Previous
              </button>
              <button
                onClick={() => setPage(page + 1)}
                disabled={(page + 1) * limit >= total}
                className="px-3 py-1 border rounded hover:bg-gray-50 disabled:opacity-50"
              >
                Next
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
