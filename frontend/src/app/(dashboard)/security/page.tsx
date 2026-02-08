'use client';

import { Lock, Shield, Key, UserCheck, Clock } from 'lucide-react';

export default function SecurityPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Security</h1>
        <p className="text-gray-400 mt-1">Manage security settings and access controls</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <div className="flex items-center gap-3 mb-6">
            <Shield className="w-6 h-6 text-blue-500" />
            <h2 className="text-lg font-semibold text-white">Two-Factor Authentication</h2>
          </div>
          <p className="text-gray-400 mb-4">Add an extra layer of security to your account</p>
          <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            Enable 2FA
          </button>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <div className="flex items-center gap-3 mb-6">
            <Key className="w-6 h-6 text-purple-500" />
            <h2 className="text-lg font-semibold text-white">API Keys</h2>
          </div>
          <p className="text-gray-400 mb-4">Manage API keys for integrations</p>
          <button className="px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600">
            Manage Keys
          </button>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <div className="flex items-center gap-3 mb-6">
            <UserCheck className="w-6 h-6 text-green-500" />
            <h2 className="text-lg font-semibold text-white">Active Sessions</h2>
          </div>
          <p className="text-gray-400 mb-4">View and manage your active sessions</p>
          <div className="text-sm text-gray-500">1 active session</div>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <div className="flex items-center gap-3 mb-6">
            <Clock className="w-6 h-6 text-orange-500" />
            <h2 className="text-lg font-semibold text-white">Login History</h2>
          </div>
          <p className="text-gray-400 mb-4">Review recent login activity</p>
          <button className="px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600">
            View History
          </button>
        </div>
      </div>
    </div>
  );
}
