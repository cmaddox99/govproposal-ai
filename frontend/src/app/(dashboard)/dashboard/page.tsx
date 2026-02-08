'use client';

import { useEffect, useState } from 'react';
import { BarChart3, FileText, Users, TrendingUp } from 'lucide-react';

export default function DashboardPage() {
  const [stats, setStats] = useState({
    proposals: 0,
    avgScore: 0,
    teamMembers: 0,
    improvement: 0,
  });

  return (
    <div className="p-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-500 mt-1">Welcome to GovProposalAI</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-3 bg-blue-100 rounded-lg">
              <FileText className="w-6 h-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-500">Total Proposals</p>
              <p className="text-2xl font-semibold">{stats.proposals}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-3 bg-green-100 rounded-lg">
              <BarChart3 className="w-6 h-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-500">Average Score</p>
              <p className="text-2xl font-semibold">{stats.avgScore}%</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-3 bg-purple-100 rounded-lg">
              <Users className="w-6 h-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-500">Team Members</p>
              <p className="text-2xl font-semibold">{stats.teamMembers}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="p-3 bg-orange-100 rounded-lg">
              <TrendingUp className="w-6 h-6 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm text-gray-500">Improvement</p>
              <p className="text-2xl font-semibold">+{stats.improvement}%</p>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <a
            href="/proposals"
            className="flex items-center p-4 border rounded-lg hover:bg-gray-50 transition"
          >
            <FileText className="w-5 h-5 text-blue-600 mr-3" />
            <span>View Proposals</span>
          </a>
          <a
            href="/settings/users"
            className="flex items-center p-4 border rounded-lg hover:bg-gray-50 transition"
          >
            <Users className="w-5 h-5 text-purple-600 mr-3" />
            <span>Manage Team</span>
          </a>
          <a
            href="/settings/audit"
            className="flex items-center p-4 border rounded-lg hover:bg-gray-50 transition"
          >
            <BarChart3 className="w-5 h-5 text-green-600 mr-3" />
            <span>View Audit Logs</span>
          </a>
        </div>
      </div>
    </div>
  );
}
