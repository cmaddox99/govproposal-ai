'use client';

import { useState } from 'react';
import { Shield } from 'lucide-react';
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
    <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6 max-w-md mx-auto">
      <div className="flex items-center gap-3 mb-6">
        <Shield className="w-8 h-8 text-emerald-400" />
        <h2 className="text-xl font-semibold text-white">Two-Factor Authentication</h2>
      </div>

      <div className="flex border-b border-white/[0.08] mb-4">
        <button
          onClick={() => setMode('code')}
          className={`flex-1 py-2 text-sm font-medium border-b-2 ${
            mode === 'code'
              ? 'border-emerald-500 text-emerald-400'
              : 'border-transparent text-gray-500 hover:text-gray-300'
          }`}
        >
          Authenticator Code
        </button>
        <button
          onClick={() => setMode('recovery')}
          className={`flex-1 py-2 text-sm font-medium border-b-2 ${
            mode === 'recovery'
              ? 'border-emerald-500 text-emerald-400'
              : 'border-transparent text-gray-500 hover:text-gray-300'
          }`}
        >
          Recovery Code
        </button>
      </div>

      {mode === 'code' ? (
        <div className="space-y-4">
          <p className="text-gray-400 text-sm">
            Enter the 6-digit code from your authenticator app.
          </p>
          <input
            type="text"
            value={code}
            onChange={(e) => setCode(e.target.value.replace(/\D/g, ''))}
            placeholder="000000"
            maxLength={6}
            className="w-full px-4 py-3 text-center text-2xl tracking-widest bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-600 focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            autoFocus
          />
          {error && <p className="text-red-400 text-sm">{error}</p>}
          <button
            onClick={handleCodeSubmit}
            disabled={loading || code.length !== 6}
            className="w-full bg-gradient-to-r from-emerald-500 to-blue-500 text-white py-2 px-4 rounded-lg hover:from-emerald-600 hover:to-blue-600 disabled:opacity-50"
          >
            {loading ? 'Verifying...' : 'Verify'}
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          <p className="text-gray-400 text-sm">
            Enter one of your recovery codes. Each code can only be used once.
          </p>
          <input
            type="text"
            value={recoveryCode}
            onChange={(e) => setRecoveryCode(e.target.value.toUpperCase())}
            placeholder="XXXX-XXXX"
            maxLength={9}
            className="w-full px-4 py-3 text-center text-xl tracking-wider bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-600 font-mono focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            autoFocus
          />
          {error && <p className="text-red-400 text-sm">{error}</p>}
          <button
            onClick={handleRecoverySubmit}
            disabled={loading || recoveryCode.length < 8}
            className="w-full bg-gradient-to-r from-emerald-500 to-blue-500 text-white py-2 px-4 rounded-lg hover:from-emerald-600 hover:to-blue-600 disabled:opacity-50"
          >
            {loading ? 'Verifying...' : 'Use Recovery Code'}
          </button>
        </div>
      )}

      <button
        onClick={onCancel}
        className="w-full mt-4 py-2 text-gray-500 hover:text-gray-300"
      >
        Back to login
      </button>
    </div>
  );
}
