'use client';

import { useEffect, useState } from 'react';
import {
  Shield, Key, UserCheck, Clock, Loader2, CheckCircle, XCircle,
  AlertTriangle, Plus, X, FileWarning, ClipboardList,
} from 'lucide-react';
import { authApi, securityApi } from '@/lib/api';
import { MfaSetup } from '@/components/auth/mfa-setup';

interface UserInfo {
  id: string;
  email: string;
  mfa_enabled: boolean;
  created_at: string;
}

interface Incident {
  id: string;
  incident_number: string;
  title: string;
  description: string;
  severity: string;
  status: string;
  category: string;
  detected_at: string;
  created_at: string;
}

interface POAMItem {
  id: string;
  poam_id: string;
  weakness_name: string;
  weakness_description: string;
  control_identifier: string;
  status: string;
  risk_level: string;
  scheduled_completion: string | null;
  point_of_contact: string | null;
}

type Tab = 'settings' | 'incidents' | 'poam';

export default function SecurityPage() {
  const [tab, setTab] = useState<Tab>('settings');
  const [user, setUser] = useState<UserInfo | null>(null);
  const [loading, setLoading] = useState(true);
  const [showMfaSetup, setShowMfaSetup] = useState(false);
  const [showRecoveryCodes, setShowRecoveryCodes] = useState(false);
  const [recoveryCodes, setRecoveryCodes] = useState<string[]>([]);
  const [disabling, setDisabling] = useState(false);
  const [showDisableConfirm, setShowDisableConfirm] = useState(false);
  const [disablePassword, setDisablePassword] = useState('');
  const [disableError, setDisableError] = useState('');
  const [regenerating, setRegenerating] = useState(false);
  const [changePasswordForm, setChangePasswordForm] = useState(false);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordError, setPasswordError] = useState('');
  const [passwordSuccess, setPasswordSuccess] = useState('');
  const [changingPassword, setChangingPassword] = useState(false);

  // Incidents state
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [showAddIncident, setShowAddIncident] = useState(false);
  const [newIncident, setNewIncident] = useState({ title: '', description: '', severity: 'medium', category: 'general' });
  const [saving, setSaving] = useState(false);

  // POAM state
  const [poamItems, setPoamItems] = useState<POAMItem[]>([]);
  const [showAddPoam, setShowAddPoam] = useState(false);
  const [newPoam, setNewPoam] = useState({
    weakness_name: '', weakness_description: '', control_identifier: '',
    risk_level: 'medium', scheduled_completion: '', point_of_contact: '',
  });

  const orgId = typeof window !== 'undefined' ? localStorage.getItem('currentOrgId') : null;

  const fetchUser = async () => {
    try {
      const res = await authApi.me();
      setUser(res.data);
    } catch {
      // handled by interceptor
    } finally {
      setLoading(false);
    }
  };

  const fetchIncidents = async () => {
    if (!orgId) return;
    try {
      const res = await securityApi.listIncidents(orgId);
      setIncidents(res.data.items || []);
    } catch { /* admin only */ }
  };

  const fetchPoam = async () => {
    if (!orgId) return;
    try {
      const res = await securityApi.listPOAM(orgId);
      setPoamItems(res.data.items || []);
    } catch { /* admin only */ }
  };

  useEffect(() => {
    fetchUser();
    fetchIncidents();
    fetchPoam();
  }, []);

  const handleMfaComplete = (codes: string[]) => {
    setRecoveryCodes(codes);
    setShowMfaSetup(false);
    setShowRecoveryCodes(true);
    fetchUser();
  };

  const handleDisableMfa = async () => {
    setDisabling(true);
    setDisableError('');
    try {
      await authApi.disableMfa(disablePassword);
      setShowDisableConfirm(false);
      setDisablePassword('');
      fetchUser();
    } catch (err: any) {
      setDisableError(err.response?.data?.detail?.message || err.response?.data?.detail || 'Failed to disable MFA');
    } finally {
      setDisabling(false);
    }
  };

  const handleRegenerateCodes = async () => {
    setRegenerating(true);
    try {
      const res = await authApi.regenerateRecoveryCodes();
      setRecoveryCodes(res.data.recovery_codes);
      setShowRecoveryCodes(true);
    } catch { }
    finally { setRegenerating(false); }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setPasswordError('');
    setPasswordSuccess('');
    if (newPassword !== confirmPassword) { setPasswordError('Passwords do not match'); return; }
    if (newPassword.length < 8) { setPasswordError('Password must be at least 8 characters'); return; }
    setChangingPassword(true);
    try {
      await authApi.changePassword(currentPassword, newPassword);
      setPasswordSuccess('Password changed successfully');
      setCurrentPassword(''); setNewPassword(''); setConfirmPassword('');
      setChangePasswordForm(false);
    } catch (err: any) {
      setPasswordError(err.response?.data?.detail?.message || err.response?.data?.detail || 'Failed to change password');
    } finally { setChangingPassword(false); }
  };

  const handleCreateIncident = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!orgId) return;
    setSaving(true);
    try {
      await securityApi.createIncident(orgId, newIncident);
      setShowAddIncident(false);
      setNewIncident({ title: '', description: '', severity: 'medium', category: 'general' });
      fetchIncidents();
    } catch { }
    finally { setSaving(false); }
  };

  const handleCreatePoam = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!orgId) return;
    setSaving(true);
    try {
      await securityApi.createPOAM(orgId, {
        ...newPoam,
        scheduled_completion: newPoam.scheduled_completion || null,
        point_of_contact: newPoam.point_of_contact || null,
      });
      setShowAddPoam(false);
      setNewPoam({ weakness_name: '', weakness_description: '', control_identifier: '', risk_level: 'medium', scheduled_completion: '', point_of_contact: '' });
      fetchPoam();
    } catch { }
    finally { setSaving(false); }
  };

  const getSeverityColor = (severity: string) => {
    const colors: Record<string, string> = {
      critical: 'text-red-500 bg-red-500/10', high: 'text-orange-500 bg-orange-500/10',
      medium: 'text-yellow-500 bg-yellow-500/10', low: 'text-blue-500 bg-blue-500/10',
    };
    return colors[severity] || 'text-gray-500 bg-gray-500/10';
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      open: 'text-red-400', investigating: 'text-orange-400', contained: 'text-yellow-400',
      resolved: 'text-green-400', closed: 'text-gray-400', in_progress: 'text-blue-400',
      completed: 'text-green-400', delayed: 'text-orange-400', accepted_risk: 'text-purple-400',
    };
    return colors[status] || 'text-gray-400';
  };

  if (loading) {
    return <div className="flex items-center justify-center h-64"><Loader2 className="w-8 h-8 animate-spin text-gray-400" /></div>;
  }

  if (showMfaSetup) {
    return <div className="max-w-lg mx-auto mt-8"><MfaSetup onComplete={handleMfaComplete} onCancel={() => setShowMfaSetup(false)} /></div>;
  }

  if (showRecoveryCodes) {
    return (
      <div className="space-y-6 max-w-lg mx-auto mt-8">
        <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
          <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-4 mb-4">
            <p className="text-green-400 font-medium">Recovery codes generated</p>
            <p className="text-green-400/70 text-sm mt-1">Save these codes in a safe place. Each can only be used once.</p>
          </div>
          <div className="grid grid-cols-2 gap-2 mb-4">
            {recoveryCodes.map((code, i) => (
              <div key={i} className="bg-white/[0.05] px-3 py-2 rounded font-mono text-sm text-white text-center">{code}</div>
            ))}
          </div>
          <div className="flex gap-3">
            <button onClick={() => navigator.clipboard.writeText(recoveryCodes.join('\n'))} className="flex-1 px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 text-sm">Copy All Codes</button>
            <button onClick={() => setShowRecoveryCodes(false)} className="flex-1 px-4 py-2 bg-gradient-to-r from-emerald-500 to-blue-500 text-white rounded-lg hover:from-emerald-600 hover:to-blue-600 text-sm">I've Saved My Codes</button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Security</h1>
        <p className="text-gray-400 mt-1">Manage security settings, incidents, and action plans</p>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 border-b border-white/[0.08]">
        {([
          { id: 'settings' as Tab, label: 'Account Security', icon: Shield },
          { id: 'incidents' as Tab, label: 'Incidents', icon: FileWarning },
          { id: 'poam' as Tab, label: 'POA&M', icon: ClipboardList },
        ]).map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
              tab === t.id
                ? 'border-emerald-500 text-emerald-400'
                : 'border-transparent text-gray-400 hover:text-white'
            }`}
          >
            <t.icon className="w-4 h-4" />
            {t.label}
          </button>
        ))}
      </div>

      {passwordSuccess && (
        <div className="flex items-center gap-2 text-green-400 bg-green-500/10 border border-green-500/20 p-4 rounded-lg">
          <CheckCircle className="w-5 h-5" />{passwordSuccess}
        </div>
      )}

      {/* Settings Tab */}
      {tab === 'settings' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* 2FA */}
          <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
            <div className="flex items-center gap-3 mb-4">
              <Shield className="w-6 h-6 text-emerald-400" />
              <h2 className="text-lg font-semibold text-white">Two-Factor Authentication</h2>
            </div>
            <div className="flex items-center gap-2 mb-4">
              {user?.mfa_enabled
                ? <><CheckCircle className="w-5 h-5 text-green-500" /><span className="text-green-400 font-medium">Enabled</span></>
                : <><XCircle className="w-5 h-5 text-red-500" /><span className="text-red-400 font-medium">Disabled</span></>}
            </div>
            <p className="text-gray-400 text-sm mb-4">
              {user?.mfa_enabled ? 'Your account is protected with TOTP-based 2FA.' : 'Add an extra layer of security with TOTP-based 2FA.'}
            </p>
            {user?.mfa_enabled ? (
              <div className="space-y-3">
                <button onClick={handleRegenerateCodes} disabled={regenerating} className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 disabled:opacity-50 text-sm">
                  {regenerating ? 'Generating...' : 'Regenerate Recovery Codes'}
                </button>
                <button onClick={() => setShowDisableConfirm(true)} className="w-full px-4 py-2 bg-red-600/20 text-red-400 border border-red-500/30 rounded-lg hover:bg-red-600/30 text-sm">Disable 2FA</button>
              </div>
            ) : (
              <button onClick={() => setShowMfaSetup(true)} className="px-4 py-2 bg-gradient-to-r from-emerald-500 to-blue-500 text-white rounded-lg hover:from-emerald-600 hover:to-blue-600">Enable 2FA</button>
            )}
          </div>

          {/* Password */}
          <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
            <div className="flex items-center gap-3 mb-4">
              <Key className="w-6 h-6 text-purple-500" />
              <h2 className="text-lg font-semibold text-white">Password</h2>
            </div>
            <p className="text-gray-400 text-sm mb-4">Change your account password</p>
            {changePasswordForm ? (
              <form onSubmit={handleChangePassword} className="space-y-3">
                <input type="password" value={currentPassword} onChange={(e) => setCurrentPassword(e.target.value)} placeholder="Current password" required className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 text-sm" />
                <input type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} placeholder="New password" required className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 text-sm" />
                <input type="password" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} placeholder="Confirm new password" required className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 text-sm" />
                {passwordError && <p className="text-red-400 text-sm">{passwordError}</p>}
                <div className="flex gap-2">
                  <button type="submit" disabled={changingPassword} className="flex-1 px-4 py-2 bg-gradient-to-r from-emerald-500 to-blue-500 text-white rounded-lg disabled:opacity-50 text-sm">{changingPassword ? 'Changing...' : 'Change Password'}</button>
                  <button type="button" onClick={() => { setChangePasswordForm(false); setPasswordError(''); }} className="px-4 py-2 bg-gray-700 text-white rounded-lg text-sm">Cancel</button>
                </div>
              </form>
            ) : (
              <button onClick={() => setChangePasswordForm(true)} className="px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600">Change Password</button>
            )}
          </div>

          {/* Account Info */}
          <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
            <div className="flex items-center gap-3 mb-4">
              <UserCheck className="w-6 h-6 text-green-500" />
              <h2 className="text-lg font-semibold text-white">Account Info</h2>
            </div>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between"><span className="text-gray-400">Email</span><span className="text-white">{user?.email}</span></div>
              <div className="flex justify-between"><span className="text-gray-400">Account Created</span><span className="text-white">{user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}</span></div>
              <div className="flex justify-between"><span className="text-gray-400">MFA Status</span><span className={user?.mfa_enabled ? 'text-green-400' : 'text-red-400'}>{user?.mfa_enabled ? 'Enabled' : 'Disabled'}</span></div>
            </div>
          </div>

          {/* Security Recommendations */}
          <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
            <div className="flex items-center gap-3 mb-4">
              <AlertTriangle className="w-6 h-6 text-yellow-500" />
              <h2 className="text-lg font-semibold text-white">Security Recommendations</h2>
            </div>
            <div className="space-y-3">
              <div className={`flex items-center gap-3 p-3 rounded-lg ${user?.mfa_enabled ? 'bg-green-500/10' : 'bg-yellow-500/10'}`}>
                {user?.mfa_enabled ? <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" /> : <AlertTriangle className="w-5 h-5 text-yellow-500 flex-shrink-0" />}
                <span className={`text-sm ${user?.mfa_enabled ? 'text-green-400' : 'text-yellow-400'}`}>
                  {user?.mfa_enabled ? '2FA is enabled' : 'Enable 2FA for better security'}
                </span>
              </div>
              <div className="flex items-center gap-3 p-3 bg-white/[0.03] rounded-lg">
                <Clock className="w-5 h-5 text-gray-500 flex-shrink-0" />
                <span className="text-sm text-gray-400">Change your password regularly</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Incidents Tab */}
      {tab === 'incidents' && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-white">Security Incidents</h2>
            <button onClick={() => setShowAddIncident(true)} className="flex items-center gap-2 px-3 py-2 bg-gradient-to-r from-emerald-500 to-blue-500 text-white rounded-lg text-sm">
              <Plus className="w-4 h-4" />Report Incident
            </button>
          </div>

          {showAddIncident && (
            <form onSubmit={handleCreateIncident} className="bg-white/[0.03] border border-white/[0.08] rounded-xl p-6 space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="text-white font-medium">New Incident</h3>
                <button type="button" onClick={() => setShowAddIncident(false)} className="text-gray-400 hover:text-white"><X className="w-5 h-5" /></button>
              </div>
              <input type="text" value={newIncident.title} onChange={(e) => setNewIncident({ ...newIncident, title: e.target.value })} placeholder="Incident title" required className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 text-sm" />
              <textarea value={newIncident.description} onChange={(e) => setNewIncident({ ...newIncident, description: e.target.value })} placeholder="Description of the incident..." rows={3} required className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 text-sm" />
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs text-gray-400 mb-1">Severity</label>
                  <select value={newIncident.severity} onChange={(e) => setNewIncident({ ...newIncident, severity: e.target.value })} className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white text-sm">
                    <option value="low">Low</option><option value="medium">Medium</option><option value="high">High</option><option value="critical">Critical</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs text-gray-400 mb-1">Category</label>
                  <select value={newIncident.category} onChange={(e) => setNewIncident({ ...newIncident, category: e.target.value })} className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white text-sm">
                    <option value="general">General</option><option value="unauthorized_access">Unauthorized Access</option><option value="data_breach">Data Breach</option><option value="malware">Malware</option><option value="phishing">Phishing</option><option value="policy_violation">Policy Violation</option>
                  </select>
                </div>
              </div>
              <button type="submit" disabled={saving} className="px-4 py-2 bg-gradient-to-r from-emerald-500 to-blue-500 text-white rounded-lg disabled:opacity-50 text-sm">{saving ? 'Creating...' : 'Create Incident'}</button>
            </form>
          )}

          {incidents.length === 0 ? (
            <div className="bg-white/[0.03] border border-white/[0.08] rounded-xl p-8 text-center text-gray-500">No security incidents recorded</div>
          ) : (
            <div className="space-y-3">
              {incidents.map((incident) => (
                <div key={incident.id} className="bg-white/[0.03] border border-white/[0.08] rounded-xl p-4">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-1">
                        <span className="text-gray-500 text-xs font-mono">{incident.incident_number}</span>
                        <span className={`px-2 py-0.5 rounded text-xs font-medium ${getSeverityColor(incident.severity)}`}>{incident.severity}</span>
                        <span className={`text-xs font-medium ${getStatusColor(incident.status)}`}>{incident.status.replace('_', ' ')}</span>
                      </div>
                      <h3 className="text-white font-medium">{incident.title}</h3>
                      <p className="text-gray-500 text-sm mt-1 line-clamp-2">{incident.description}</p>
                    </div>
                    <div className="text-xs text-gray-500 whitespace-nowrap">
                      {new Date(incident.detected_at).toLocaleDateString()}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* POAM Tab */}
      {tab === 'poam' && (
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-white">Plan of Action & Milestones</h2>
            <button onClick={() => setShowAddPoam(true)} className="flex items-center gap-2 px-3 py-2 bg-gradient-to-r from-emerald-500 to-blue-500 text-white rounded-lg text-sm">
              <Plus className="w-4 h-4" />Add Item
            </button>
          </div>

          {showAddPoam && (
            <form onSubmit={handleCreatePoam} className="bg-white/[0.03] border border-white/[0.08] rounded-xl p-6 space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="text-white font-medium">New POA&M Item</h3>
                <button type="button" onClick={() => setShowAddPoam(false)} className="text-gray-400 hover:text-white"><X className="w-5 h-5" /></button>
              </div>
              <input type="text" value={newPoam.weakness_name} onChange={(e) => setNewPoam({ ...newPoam, weakness_name: e.target.value })} placeholder="Weakness name" required className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 text-sm" />
              <textarea value={newPoam.weakness_description} onChange={(e) => setNewPoam({ ...newPoam, weakness_description: e.target.value })} placeholder="Weakness description..." rows={2} required className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 text-sm" />
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs text-gray-400 mb-1">Control Identifier</label>
                  <input type="text" value={newPoam.control_identifier} onChange={(e) => setNewPoam({ ...newPoam, control_identifier: e.target.value })} placeholder="e.g., AC-2" required className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 text-sm" />
                </div>
                <div>
                  <label className="block text-xs text-gray-400 mb-1">Risk Level</label>
                  <select value={newPoam.risk_level} onChange={(e) => setNewPoam({ ...newPoam, risk_level: e.target.value })} className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white text-sm">
                    <option value="low">Low</option><option value="medium">Medium</option><option value="high">High</option><option value="critical">Critical</option>
                  </select>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs text-gray-400 mb-1">Scheduled Completion</label>
                  <input type="date" value={newPoam.scheduled_completion} onChange={(e) => setNewPoam({ ...newPoam, scheduled_completion: e.target.value })} className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white text-sm" />
                </div>
                <div>
                  <label className="block text-xs text-gray-400 mb-1">Point of Contact</label>
                  <input type="text" value={newPoam.point_of_contact} onChange={(e) => setNewPoam({ ...newPoam, point_of_contact: e.target.value })} placeholder="Name or email" className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 text-sm" />
                </div>
              </div>
              <button type="submit" disabled={saving} className="px-4 py-2 bg-gradient-to-r from-emerald-500 to-blue-500 text-white rounded-lg disabled:opacity-50 text-sm">{saving ? 'Creating...' : 'Add POA&M Item'}</button>
            </form>
          )}

          {poamItems.length === 0 ? (
            <div className="bg-white/[0.03] border border-white/[0.08] rounded-xl p-8 text-center text-gray-500">No POA&M items tracked</div>
          ) : (
            <div className="space-y-3">
              {poamItems.map((item) => (
                <div key={item.id} className="bg-white/[0.03] border border-white/[0.08] rounded-xl p-4">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-1">
                        <span className="text-gray-500 text-xs font-mono">{item.poam_id}</span>
                        <span className={`px-2 py-0.5 rounded text-xs font-medium ${getSeverityColor(item.risk_level)}`}>{item.risk_level}</span>
                        <span className={`text-xs font-medium ${getStatusColor(item.status)}`}>{item.status.replace('_', ' ')}</span>
                      </div>
                      <h3 className="text-white font-medium">{item.weakness_name}</h3>
                      <p className="text-gray-500 text-sm mt-1">{item.weakness_description}</p>
                      <div className="flex gap-4 mt-2 text-xs text-gray-500">
                        <span>Control: {item.control_identifier}</span>
                        {item.point_of_contact && <span>POC: {item.point_of_contact}</span>}
                      </div>
                    </div>
                    {item.scheduled_completion && (
                      <div className="text-xs text-gray-500 whitespace-nowrap">
                        Due: {new Date(item.scheduled_completion).toLocaleDateString()}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Disable MFA Modal */}
      {showDisableConfirm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-[#1a1a2e] border border-white/[0.08] rounded-xl p-6 max-w-md w-full">
            <h3 className="text-lg font-semibold text-white mb-2">Disable Two-Factor Authentication</h3>
            <p className="text-gray-400 text-sm mb-4">Enter your password to confirm.</p>
            <input type="password" value={disablePassword} onChange={(e) => setDisablePassword(e.target.value)} placeholder="Enter your password" className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 mb-3" />
            {disableError && <p className="text-red-400 text-sm mb-3">{disableError}</p>}
            <div className="flex gap-3">
              <button onClick={handleDisableMfa} disabled={disabling || !disablePassword} className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg disabled:opacity-50">{disabling ? 'Disabling...' : 'Disable 2FA'}</button>
              <button onClick={() => { setShowDisableConfirm(false); setDisablePassword(''); setDisableError(''); }} className="px-4 py-2 bg-gray-700 text-white rounded-lg">Cancel</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
