'use client';

import { useState } from 'react';
import { Shield, Key } from 'lucide-react';
import { authApi } from '@/lib/api';
import { TokenResponse } from '@/types';

interface MfaChallengeProps {
  mfaToken: string;
  onSuccess: (tokens: TokenResponse) => void;
  onCancel: () => void;
}

export function MfaChallenge({ mfaToken, onSuccess, onCancel }: MfaChallengeProps) {
  const [mode, setMode] = useState<'code' | 'recovery'>('code');
  const [code, setCode] = useState('');
  const [recoveryCode, setRecoveryCode] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleCodeSubmit = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await authApi.mfaChallenge(mfaToken, code);
      onSuccess(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail?.message || 'Invalid code');
    } finally {
      setLoading(false);
    }
  };

  const handleRecoverySubmit = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await authApi.useRecoveryCode(mfaToken, recoveryCode);
      onSuccess(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail?.message || 'Invalid recovery code');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-md mx-auto">
      <div className="flex items-center gap-3 mb-6">
        <Shield className="w-8 h-8 text-blue-600" />
        <h2 className="text-xl font-semibold">Two-Factor Authentication</h2>
      </div>

      <div className="flex border-b mb-4">
        <button
          onClick={() => setMode('code')}
          className={`flex-1 py-2 text-sm font-medium border-b-2 ${
            mode === 'code'
              ? 'border-blue-600 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          Authenticator Code
        </button>
        <button
          onClick={() => setMode('recovery')}
          className={`flex-1 py-2 text-sm font-medium border-b-2 ${
            mode === 'recovery'
              ? 'border-blue-600 text-blue-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          Recovery Code
        </button>
      </div>

      {mode === 'code' ? (
        <div className="space-y-4">
          <p className="text-gray-600 text-sm">
            Enter the 6-digit code from your authenticator app.
          </p>
          <div>
            <input
              type="text"
              value={code}
              onChange={(e) => setCode(e.target.value.replace(/\D/g, ''))}
              placeholder="000000"
              maxLength={6}
              className="w-full px-4 py-3 text-center text-2xl tracking-widest border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              autoFocus
            />
          </div>

          {error && <p className="text-red-600 text-sm">{error}</p>}

          <button
            onClick={handleCodeSubmit}
            disabled={loading || code.length !== 6}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Verifying...' : 'Verify'}
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          <p className="text-gray-600 text-sm">
            Enter one of your recovery codes. Each code can only be used once.
          </p>
          <div>
            <input
              type="text"
              value={recoveryCode}
              onChange={(e) => setRecoveryCode(e.target.value.toUpperCase())}
              placeholder="XXXX-XXXX"
              maxLength={9}
              className="w-full px-4 py-3 text-center text-xl tracking-wider border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent font-mono"
              autoFocus
            />
          </div>

          {error && <p className="text-red-600 text-sm">{error}</p>}

          <button
            onClick={handleRecoverySubmit}
            disabled={loading || recoveryCode.length < 8}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? 'Verifying...' : 'Use Recovery Code'}
          </button>
        </div>
      )}

      <button
        onClick={onCancel}
        className="w-full mt-4 py-2 text-gray-600 hover:text-gray-800"
      >
        Back to login
      </button>
    </div>
  );
}
