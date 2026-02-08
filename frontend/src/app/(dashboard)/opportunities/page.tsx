'use client';

import { Search, Filter, ExternalLink } from 'lucide-react';

export default function OpportunitiesPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Opportunities</h1>
        <p className="text-gray-400 mt-1">Discover and track government contract opportunities</p>
      </div>

      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <div className="flex gap-4 mb-6">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
            <input
              type="text"
              placeholder="Search opportunities by keyword, NAICS, agency..."
              className="w-full pl-10 pr-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button className="flex items-center gap-2 px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-gray-300 hover:bg-gray-700">
            <Filter className="w-5 h-5" />
            Filters
          </button>
        </div>

        <div className="text-center py-12">
          <Search className="w-12 h-12 text-gray-600 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-white mb-2">Search for Opportunities</h3>
          <p className="text-gray-500 max-w-md mx-auto">
            Use the search bar above to find government contract opportunities from SAM.gov,
            or connect your SAM.gov API key in settings to enable automated opportunity matching.
          </p>
        </div>
      </div>
    </div>
  );
}
