'use client';

import { useEffect, useState } from 'react';
import { Shield, Key, UserCheck, Clock, Loader2, CheckCircle, XCircle, AlertTriangle } from 'lucide-react';
import { authApi } from '@/lib/api';
import { MfaSetup } from '@/components/auth/mfa-setup';
// RecoveryCodes component used inline below

interface UserInfo {
  id: string;
  email: string;
  mfa_enabled: boolean;
  created_at: string;
}

export default function SecurityPage() {
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

  useEffect(() => {
    fetchUser();
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
    } catch {
      // error handling
    } finally {
      setRegenerating(false);
    }
  };

  const handleChangePassword = async (e: React.FormEvent) => {
    e.preventDefault();
    setPasswordError('');
    setPasswordSuccess('');

    if (newPassword !== confirmPassword) {
      setPasswordError('Passwords do not match');
      return;
    }
    if (newPassword.length < 8) {
      setPasswordError('Password must be at least 8 characters');
      return;
    }

    setChangingPassword(true);
    try {
      await authApi.changePassword(currentPassword, newPassword);
      setPasswordSuccess('Password changed successfully');
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
      setChangePasswordForm(false);
    } catch (err: any) {
      setPasswordError(err.response?.data?.detail?.message || err.response?.data?.detail || 'Failed to change password');
    } finally {
      setChangingPassword(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-gray-400" />
      </div>
    );
  }

  if (showMfaSetup) {
    return (
      <div className="max-w-lg mx-auto mt-8">
        <MfaSetup
          onComplete={handleMfaComplete}
          onCancel={() => setShowMfaSetup(false)}
        />
      </div>
    );
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
              <div key={i} className="bg-white/[0.05] px-3 py-2 rounded font-mono text-sm text-white text-center">
                {code}
              </div>
            ))}
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => {
                navigator.clipboard.writeText(recoveryCodes.join('\n'));
              }}
              className="flex-1 px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 text-sm"
            >
              Copy All Codes
            </button>
            <button
              onClick={() => setShowRecoveryCodes(false)}
              className="flex-1 px-4 py-2 bg-gradient-to-r from-emerald-500 to-blue-500 text-white rounded-lg hover:from-emerald-600 hover:to-blue-600 text-sm"
            >
              I've Saved My Codes
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Security</h1>
        <p className="text-gray-400 mt-1">Manage security settings and access controls</p>
      </div>

      {passwordSuccess && (
        <div className="flex items-center gap-2 text-green-400 bg-green-500/10 border border-green-500/20 p-4 rounded-lg">
          <CheckCircle className="w-5 h-5" />
          {passwordSuccess}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Two-Factor Authentication */}
        <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <Shield className="w-6 h-6 text-emerald-400" />
            <h2 className="text-lg font-semibold text-white">Two-Factor Authentication</h2>
          </div>

          <div className="flex items-center gap-2 mb-4">
            {user?.mfa_enabled ? (
              <>
                <CheckCircle className="w-5 h-5 text-green-500" />
                <span className="text-green-400 font-medium">Enabled</span>
              </>
            ) : (
              <>
                <XCircle className="w-5 h-5 text-red-500" />
                <span className="text-red-400 font-medium">Disabled</span>
              </>
            )}
          </div>

          <p className="text-gray-400 text-sm mb-4">
            {user?.mfa_enabled
              ? 'Your account is protected with two-factor authentication using an authenticator app.'
              : 'Add an extra layer of security to your account with TOTP-based two-factor authentication.'}
          </p>

          {user?.mfa_enabled ? (
            <div className="space-y-3">
              <button
                onClick={handleRegenerateCodes}
                disabled={regenerating}
                className="w-full px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 disabled:opacity-50 text-sm"
              >
                {regenerating ? 'Generating...' : 'Regenerate Recovery Codes'}
              </button>
              <button
                onClick={() => setShowDisableConfirm(true)}
                className="w-full px-4 py-2 bg-red-600/20 text-red-400 border border-red-500/30 rounded-lg hover:bg-red-600/30 text-sm"
              >
                Disable 2FA
              </button>
            </div>
          ) : (
            <button
              onClick={() => setShowMfaSetup(true)}
              className="px-4 py-2 bg-gradient-to-r from-emerald-500 to-blue-500 text-white rounded-lg hover:from-emerald-600 hover:to-blue-600"
            >
              Enable 2FA
            </button>
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
              <input
                type="password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                placeholder="Current password"
                required
                className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 text-sm focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              />
              <input
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder="New password"
                required
                className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 text-sm focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              />
              <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirm new password"
                required
                className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 text-sm focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              />
              {passwordError && (
                <p className="text-red-400 text-sm">{passwordError}</p>
              )}
              <div className="flex gap-2">
                <button
                  type="submit"
                  disabled={changingPassword}
                  className="flex-1 px-4 py-2 bg-gradient-to-r from-emerald-500 to-blue-500 text-white rounded-lg hover:from-emerald-600 hover:to-blue-600 disabled:opacity-50 text-sm"
                >
                  {changingPassword ? 'Changing...' : 'Change Password'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setChangePasswordForm(false);
                    setPasswordError('');
                  }}
                  className="px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 text-sm"
                >
                  Cancel
                </button>
              </div>
            </form>
          ) : (
            <button
              onClick={() => setChangePasswordForm(true)}
              className="px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600"
            >
              Change Password
            </button>
          )}
        </div>

        {/* Account Info */}
        <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <UserCheck className="w-6 h-6 text-green-500" />
            <h2 className="text-lg font-semibold text-white">Account Info</h2>
          </div>
          <div className="space-y-3 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">Email</span>
              <span className="text-white">{user?.email}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Account Created</span>
              <span className="text-white">
                {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">MFA Status</span>
              <span className={user?.mfa_enabled ? 'text-green-400' : 'text-red-400'}>
                {user?.mfa_enabled ? 'Enabled' : 'Disabled'}
              </span>
            </div>
          </div>
        </div>

        {/* Security Tips */}
        <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <AlertTriangle className="w-6 h-6 text-yellow-500" />
            <h2 className="text-lg font-semibold text-white">Security Recommendations</h2>
          </div>
          <div className="space-y-3">
            <div className={`flex items-center gap-3 p-3 rounded-lg ${user?.mfa_enabled ? 'bg-green-500/10' : 'bg-yellow-500/10'}`}>
              {user?.mfa_enabled ? (
                <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
              ) : (
                <AlertTriangle className="w-5 h-5 text-yellow-500 flex-shrink-0" />
              )}
              <span className={`text-sm ${user?.mfa_enabled ? 'text-green-400' : 'text-yellow-400'}`}>
                {user?.mfa_enabled ? 'Two-factor authentication is enabled' : 'Enable two-factor authentication for better security'}
              </span>
            </div>
            <div className="flex items-center gap-3 p-3 bg-white/[0.03] rounded-lg">
              <Clock className="w-5 h-5 text-gray-500 flex-shrink-0" />
              <span className="text-sm text-gray-400">
                Change your password regularly and use a strong, unique password
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Disable MFA Confirmation Modal */}
      {showDisableConfirm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-[#1a1a2e] border border-white/[0.08] rounded-xl p-6 max-w-md w-full">
            <h3 className="text-lg font-semibold text-white mb-2">Disable Two-Factor Authentication</h3>
            <p className="text-gray-400 text-sm mb-4">
              This will remove the extra security layer from your account. Enter your password to confirm.
            </p>
            <input
              type="password"
              value={disablePassword}
              onChange={(e) => setDisablePassword(e.target.value)}
              placeholder="Enter your password"
              className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 mb-3 focus:ring-2 focus:ring-red-500 focus:border-transparent"
            />
            {disableError && (
              <p className="text-red-400 text-sm mb-3">{disableError}</p>
            )}
            <div className="flex gap-3">
              <button
                onClick={handleDisableMfa}
                disabled={disabling || !disablePassword}
                className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50"
              >
                {disabling ? 'Disabling...' : 'Disable 2FA'}
              </button>
              <button
                onClick={() => {
                  setShowDisableConfirm(false);
                  setDisablePassword('');
                  setDisableError('');
                }}
                className="px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
