'use client';

import { useState } from 'react';
import { Key, Copy, Check, RefreshCw, AlertTriangle } from 'lucide-react';
import { authApi } from '@/lib/api';

interface RecoveryCodesProps {
  codes: string[];
  onRegenerate?: (newCodes: string[]) => void;
}

export function RecoveryCodes({ codes, onRegenerate }: RecoveryCodesProps) {
  const [copied, setCopied] = useState(false);
  const [regenerating, setRegenerating] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  const copyAll = () => {
    navigator.clipboard.writeText(codes.join('\n'));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleRegenerate = async () => {
    setRegenerating(true);
    try {
      const response = await authApi.regenerateRecoveryCodes();
      if (onRegenerate) {
        onRegenerate(response.data.recovery_codes);
      }
      setShowConfirm(false);
    } catch (error) {
      console.error('Failed to regenerate codes:', error);
    } finally {
      setRegenerating(false);
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <Key className="w-5 h-5 text-gray-600" />
        <h3 className="font-medium">Recovery Codes</h3>
      </div>

      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <p className="text-sm text-gray-600 mb-3">
          Use these codes to access your account if you lose your authenticator
          device. Each code can only be used once.
        </p>

        <div className="grid grid-cols-2 gap-2 mb-3">
          {codes.map((code, index) => (
            <div
              key={index}
              className="bg-white border border-gray-200 px-3 py-2 rounded font-mono text-sm"
            >
              {code}
            </div>
          ))}
        </div>

        <div className="flex gap-2">
          <button
            onClick={copyAll}
            className="flex items-center gap-2 px-3 py-1.5 text-sm text-blue-600 hover:bg-blue-50 rounded"
          >
            {copied ? (
              <>
                <Check className="w-4 h-4" />
                Copied!
              </>
            ) : (
              <>
                <Copy className="w-4 h-4" />
                Copy all
              </>
            )}
          </button>

          {onRegenerate && (
            <button
              onClick={() => setShowConfirm(true)}
              className="flex items-center gap-2 px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-100 rounded"
            >
              <RefreshCw className="w-4 h-4" />
              Regenerate
            </button>
          )}
        </div>
      </div>

      {showConfirm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-sm mx-4">
            <div className="flex items-center gap-2 text-yellow-600 mb-4">
              <AlertTriangle className="w-5 h-5" />
              <h4 className="font-medium">Regenerate Recovery Codes?</h4>
            </div>
            <p className="text-gray-600 text-sm mb-4">
              This will invalidate all your existing recovery codes. Make sure to
              save the new codes in a safe place.
            </p>
            <div className="flex gap-3">
              <button
                onClick={handleRegenerate}
                disabled={regenerating}
                className="flex-1 bg-yellow-600 text-white py-2 px-4 rounded hover:bg-yellow-700 disabled:opacity-50"
              >
                {regenerating ? 'Regenerating...' : 'Regenerate'}
              </button>
              <button
                onClick={() => setShowConfirm(false)}
                className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-50"
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
