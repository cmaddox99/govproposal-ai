'use client';

import { BarChart3, TrendingUp, PieChart, Calendar } from 'lucide-react';

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Analytics</h1>
        <p className="text-gray-400 mt-1">Insights and performance metrics for your proposals</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <TrendingUp className="w-8 h-8 text-green-500 mb-4" />
          <div className="text-3xl font-bold text-white mb-1">68%</div>
          <div className="text-gray-400 text-sm">Win Rate</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <BarChart3 className="w-8 h-8 text-blue-500 mb-4" />
          <div className="text-3xl font-bold text-white mb-1">$12.4M</div>
          <div className="text-gray-400 text-sm">Total Contract Value</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <PieChart className="w-8 h-8 text-purple-500 mb-4" />
          <div className="text-3xl font-bold text-white mb-1">47</div>
          <div className="text-gray-400 text-sm">Proposals Submitted</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <Calendar className="w-8 h-8 text-orange-500 mb-4" />
          <div className="text-3xl font-bold text-white mb-1">15</div>
          <div className="text-gray-400 text-sm">Avg Days to Complete</div>
        </div>
      </div>

      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h2 className="text-lg font-semibold text-white mb-6">Performance Trends</h2>
        <div className="h-64 flex items-center justify-center text-gray-500">
          <div className="text-center">
            <BarChart3 className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <p>Charts and detailed analytics coming soon</p>
          </div>
        </div>
      </div>
    </div>
  );
}
