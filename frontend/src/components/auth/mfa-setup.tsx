'use client';

import { useState } from 'react';
import { Shield, Copy, Check } from 'lucide-react';
import { authApi } from '../../lib/api';
import { MfaSetupResponse, MfaCompleteResponse } from '../../types';

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
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-md mx-auto">
      <div className="flex items-center gap-3 mb-6">
        <Shield className="w-8 h-8 text-blue-600" />
        <h2 className="text-xl font-semibold">Set Up Two-Factor Authentication</h2>
      </div>

      {step === 'setup' && (
        <div className="space-y-4">
          <p className="text-gray-600">
            Add an extra layer of security to your account by enabling two-factor
            authentication using an authenticator app.
          </p>
          <div className="flex gap-3">
            <button
              onClick={startSetup}
              disabled={loading}
              className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Setting up...' : 'Get Started'}
            </button>
            <button
              onClick={onCancel}
              className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {step === 'verify' && setupData && (
        <div className="space-y-4">
          <p className="text-gray-600">
            Scan this QR code with your authenticator app (Google Authenticator,
            Authy, etc.), then enter the code below.
          </p>

          <div className="bg-gray-100 p-4 rounded-lg text-center">
            <div className="bg-white p-4 inline-block rounded">
              {/* QR code placeholder - in production, use a QR library */}
              <div className="w-48 h-48 bg-gray-200 flex items-center justify-center text-gray-500 text-sm">
                QR Code
                <br />
                (Use URI below)
              </div>
            </div>
            <p className="mt-2 text-xs text-gray-500 break-all">
              {setupData.provisioning_uri}
            </p>
          </div>

          <div className="text-sm text-gray-600">
            <p className="font-medium">Manual entry code:</p>
            <code className="bg-gray-100 px-2 py-1 rounded">{setupData.secret}</code>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Enter verification code
            </label>
            <input
              type="text"
              value={code}
              onChange={(e) => setCode(e.target.value)}
              placeholder="000000"
              maxLength={6}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {error && (
            <p className="text-red-600 text-sm">{error}</p>
          )}

          <div className="flex gap-3">
            <button
              onClick={verifyCode}
              disabled={loading || code.length !== 6}
              className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Verifying...' : 'Verify & Enable'}
            </button>
            <button
              onClick={onCancel}
              className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {step === 'codes' && (
        <div className="space-y-4">
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <p className="text-green-800 font-medium">
              Two-factor authentication enabled!
            </p>
          </div>

          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <p className="text-yellow-800 font-medium mb-2">
              Save your recovery codes
            </p>
            <p className="text-yellow-700 text-sm">
              Store these codes in a safe place. You can use them to access your
              account if you lose your authenticator device.
            </p>
          </div>

          <div className="bg-gray-100 p-4 rounded-lg">
            <div className="grid grid-cols-2 gap-2 font-mono text-sm">
              {recoveryCodes.map((code, index) => (
                <div key={index} className="bg-white px-2 py-1 rounded">
                  {code}
                </div>
              ))}
            </div>
            <button
              onClick={copyRecoveryCodes}
              className="mt-3 flex items-center gap-2 text-blue-600 hover:text-blue-700"
            >
              {copied ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
              {copied ? 'Copied!' : 'Copy all codes'}
            </button>
          </div>

          <button
            onClick={handleComplete}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700"
          >
            I've saved my codes
          </button>
        </div>
      )}
    </div>
  );
}
