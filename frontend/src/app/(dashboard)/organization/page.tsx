'use client';

import { useEffect, useState } from 'react';
import { Building2, Users, Settings, Mail, Phone, MapPin } from 'lucide-react';

export default function OrganizationPage() {
  const [orgName, setOrgName] = useState('');

  useEffect(() => {
    const storedOrgName = localStorage.getItem('currentOrgName');
    if (storedOrgName) {
      setOrgName(storedOrgName);
    }
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Organization</h1>
        <p className="text-gray-400 mt-1">Manage your organization profile and settings</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Organization Info */}
        <div className="lg:col-span-2 bg-gray-900 border border-gray-800 rounded-xl p-6">
          <div className="flex items-center gap-3 mb-6">
            <Building2 className="w-6 h-6 text-blue-500" />
            <h2 className="text-lg font-semibold text-white">Organization Details</h2>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                Organization Name
              </label>
              <input
                type="text"
                value={orgName}
                onChange={(e) => setOrgName(e.target.value)}
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">
                  <Mail className="w-4 h-4 inline mr-2" />
                  Contact Email
                </label>
                <input
                  type="email"
                  placeholder="contact@company.com"
                  className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">
                  <Phone className="w-4 h-4 inline mr-2" />
                  Phone Number
                </label>
                <input
                  type="tel"
                  placeholder="(555) 123-4567"
                  className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                <MapPin className="w-4 h-4 inline mr-2" />
                Address
              </label>
              <textarea
                placeholder="Enter your organization address"
                rows={3}
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div className="pt-4">
              <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                Save Changes
              </button>
            </div>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="space-y-6">
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
            <div className="flex items-center gap-3 mb-4">
              <Users className="w-6 h-6 text-green-500" />
              <h2 className="text-lg font-semibold text-white">Team Members</h2>
            </div>
            <div className="text-4xl font-bold text-white mb-2">5</div>
            <p className="text-gray-400 text-sm">Active users in your organization</p>
            <button className="mt-4 text-sm text-blue-500 hover:text-blue-400">
              Manage Team →
            </button>
          </div>

          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
            <div className="flex items-center gap-3 mb-4">
              <Settings className="w-6 h-6 text-purple-500" />
              <h2 className="text-lg font-semibold text-white">Subscription</h2>
            </div>
            <div className="text-xl font-bold text-white mb-2">Professional</div>
            <p className="text-gray-400 text-sm">Current plan</p>
            <button className="mt-4 text-sm text-blue-500 hover:text-blue-400">
              Upgrade Plan →
            </button>
          </div>
        </div>
      </div>

      {/* Government Credentials */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h2 className="text-lg font-semibold text-white mb-6">Government Credentials</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">
              UEI Number
            </label>
            <input
              type="text"
              placeholder="Enter UEI"
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">
              CAGE Code
            </label>
            <input
              type="text"
              placeholder="Enter CAGE Code"
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">
              Primary NAICS
            </label>
            <input
              type="text"
              placeholder="Enter NAICS Code"
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>
    </div>
  );
}
