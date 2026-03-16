'use client';

import { useState } from 'react';
import { Shield, Copy, Check } from 'lucide-react';
import { authApi } from '@/lib/api';
import { MfaSetupResponse, MfaCompleteResponse } from '@/types';

interface MfaSetupProps {
  onComplete: (recoveryCodes: string[]) => void;
  onCancel: () => void;
}

export function MfaSetup({ onComplete, onCancel }: MfaSetupProps) {
  const [step, setStep] = useState<'setup' | 'verify' | 'codes'>('setup');
  const [setupData, setSetupData] = useState<MfaSetupResponse | null>(null);
  const [code, setCode] = useState('');
  const [recoveryCodes, setRecoveryCodes] = useState<string[]>([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const startSetup = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await authApi.setupMfa();
      setSetupData(response.data);
      setStep('verify');
    } catch (err: any) {
      setError(err.response?.data?.detail?.message || 'Failed to start MFA setup');
    } finally {
      setLoading(false);
    }
  };

  const verifyCode = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await authApi.verifyMfaSetup(code);
      const data: MfaCompleteResponse = response.data;
      setRecoveryCodes(data.recovery_codes);
      setStep('codes');
    } catch (err: any) {
      setError(err.response?.data?.detail?.message || 'Invalid code');
    } finally {
      setLoading(false);
    }
  };

  const copyRecoveryCodes = () => {
    navigator.clipboard.writeText(recoveryCodes.join('\n'));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleComplete = () => {
    onComplete(recoveryCodes);
  };

  return (
    <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6 max-w-md mx-auto">
      <div className="flex items-center gap-3 mb-6">
        <Shield className="w-8 h-8 text-emerald-400" />
        <h2 className="text-xl font-semibold text-white">Set Up Two-Factor Authentication</h2>
      </div>

      {step === 'setup' && (
        <div className="space-y-4">
          <p className="text-gray-400">
            Add an extra layer of security to your account by enabling two-factor
            authentication using an authenticator app.
          </p>
          <div className="flex gap-3">
            <button
              onClick={startSetup}
              disabled={loading}
              className="flex-1 bg-gradient-to-r from-emerald-500 to-blue-500 text-white py-2 px-4 rounded-lg hover:from-emerald-600 hover:to-blue-600 disabled:opacity-50"
            >
              {loading ? 'Setting up...' : 'Get Started'}
            </button>
            <button
              onClick={onCancel}
              className="px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {step === 'verify' && setupData && (
        <div className="space-y-4">
          <p className="text-gray-400">
            Scan this QR code with your authenticator app (Google Authenticator,
            Authy, etc.), then enter the code below.
          </p>

          <div className="bg-white/[0.05] p-4 rounded-lg text-center">
            <div className="bg-white p-4 inline-block rounded">
              <div className="w-48 h-48 bg-gray-100 flex items-center justify-center text-gray-500 text-sm">
                QR Code
                <br />
                (Use URI below)
              </div>
            </div>
            <p className="mt-2 text-xs text-gray-500 break-all">
              {setupData.provisioning_uri}
            </p>
          </div>

          <div className="text-sm text-gray-400">
            <p className="font-medium text-gray-300">Manual entry code:</p>
            <code className="bg-white/[0.05] px-2 py-1 rounded text-emerald-400">{setupData.secret}</code>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-1">
              Enter verification code
            </label>
            <input
              type="text"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="000000"
              maxLength={6}
              className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            />
          </div>

          {error && <p className="text-red-400 text-sm">{error}</p>}

          <div className="flex gap-3">
            <button
              onClick={verifyCode}
              disabled={loading || code.length !== 6}
              className="flex-1 bg-gradient-to-r from-emerald-500 to-blue-500 text-white py-2 px-4 rounded-lg hover:from-emerald-600 hover:to-blue-600 disabled:opacity-50"
            >
              {loading ? 'Verifying...' : 'Verify & Enable'}
            </button>
            <button
              onClick={onCancel}
              className="px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {step === 'codes' && (
        <div className="space-y-4">
          <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-4">
            <p className="text-green-400 font-medium">
              Two-factor authentication enabled!
            </p>
          </div>

          <div className="bg-yellow-500/10 border border-yellow-500/20 rounded-lg p-4">
            <p className="text-yellow-400 font-medium mb-2">Save your recovery codes</p>
            <p className="text-yellow-400/70 text-sm">
              Store these codes in a safe place. You can use them to access your
              account if you lose your authenticator device.
            </p>
          </div>

          <div className="bg-white/[0.05] p-4 rounded-lg">
            <div className="grid grid-cols-2 gap-2 font-mono text-sm">
              {recoveryCodes.map((code, index) => (
                <div key={index} className="bg-white/[0.05] px-2 py-1 rounded text-white text-center">
                  {code}
                </div>
              ))}
            </div>
            <button
              onClick={copyRecoveryCodes}
              className="mt-3 flex items-center gap-2 text-emerald-400 hover:text-emerald-300"
            >
              {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
              {copied ? 'Copied!' : 'Copy all codes'}
            </button>
          </div>

          <button
            onClick={handleComplete}
            className="w-full bg-gradient-to-r from-emerald-500 to-blue-500 text-white py-2 px-4 rounded-lg hover:from-emerald-600 hover:to-blue-600"
          >
            I've saved my codes
          </button>
        </div>
      )}
    </div>
  );
}
