'use client';

import { useEffect, useState } from 'react';
import { Building2, Settings, ToggleLeft, ToggleRight, RefreshCw } from 'lucide-react';
import { platformApi } from '@/lib/api';
import { Tenant, FeatureToggle } from '@/types';

export default function PlatformPage() {
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [features, setFeatures] = useState<FeatureToggle[]>([]);
  const [activeTab, setActiveTab] = useState<'tenants' | 'features'>('tenants');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      const [tenantsRes, featuresRes] = await Promise.all([
        platformApi.listTenants(),
        platformApi.getFeatures(),
      ]);
      setTenants(tenantsRes.data);
      setFeatures(featuresRes.data.features);
    } catch (err: any) {
      if (err.response?.status === 403) {
        setError('Super user access required');
      } else {
        setError(err.response?.data?.detail?.message || 'Failed to load data');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const toggleTenantStatus = async (orgId: string, currentStatus: boolean) => {
    try {
      await platformApi.updateTenantStatus(orgId, !currentStatus);
      await fetchData();
    } catch (err: any) {
      alert(err.response?.data?.detail?.message || 'Failed to update status');
    }
  };

  const toggleFeature = async (feature: string, currentEnabled: boolean) => {
    try {
      await platformApi.updateFeature(feature, !currentEnabled);
      await fetchData();
    } catch (err: any) {
      alert(err.response?.data?.detail?.message || 'Failed to update feature');
    }
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <Settings className="w-6 h-6 text-purple-600" />
          <div>
            <h1 className="text-2xl font-semibold">Platform Administration</h1>
            <p className="text-sm text-gray-500">Super user access only</p>
          </div>
        </div>
        <button
          onClick={fetchData}
          className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
        >
          <RefreshCw className="w-4 h-4" />
          Refresh
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
          {error}
        </div>
      )}

      {/* Tabs */}
      <div className="flex border-b mb-6">
        <button
          onClick={() => setActiveTab('tenants')}
          className={`px-4 py-2 text-sm font-medium border-b-2 ${
            activeTab === 'tenants'
              ? 'border-purple-600 text-purple-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          <Building2 className="w-4 h-4 inline mr-2" />
          Tenants ({tenants.length})
        </button>
        <button
          onClick={() => setActiveTab('features')}
          className={`px-4 py-2 text-sm font-medium border-b-2 ${
            activeTab === 'features'
              ? 'border-purple-600 text-purple-600'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          }`}
        >
          <ToggleLeft className="w-4 h-4 inline mr-2" />
          Feature Toggles
        </button>
      </div>

      {loading ? (
        <div className="text-center py-12 text-gray-500">Loading...</div>
      ) : (
        <>
          {/* Tenants Tab */}
          {activeTab === 'tenants' && (
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-50 border-b">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                      Organization
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                      Slug
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                      Members
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                      Created
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                      Status
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {tenants.map((tenant) => (
                    <tr key={tenant.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4">
                        <div className="text-sm font-medium text-gray-900">
                          {tenant.name}
                        </div>
                        <div className="text-xs text-gray-500">
                          ID: {tenant.id.slice(0, 8)}...
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {tenant.slug}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {tenant.member_count}
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-500">
                        {new Date(tenant.created_at).toLocaleDateString()}
                      </td>
                      <td className="px-6 py-4">
                        <button
                          onClick={() => toggleTenantStatus(tenant.id, tenant.is_active)}
                          className={`px-3 py-1 text-sm rounded-full ${
                            tenant.is_active
                              ? 'bg-green-100 text-green-700 hover:bg-green-200'
                              : 'bg-red-100 text-red-700 hover:bg-red-200'
                          }`}
                        >
                          {tenant.is_active ? 'Active' : 'Disabled'}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Features Tab */}
          {activeTab === 'features' && (
            <div className="space-y-4">
              {features.map((feature) => (
                <div
                  key={feature.feature}
                  className="bg-white rounded-lg shadow p-4 flex items-center justify-between"
                >
                  <div>
                    <h3 className="font-medium text-gray-900">
                      {feature.feature.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())}
                    </h3>
                    {feature.description && (
                      <p className="text-sm text-gray-500">{feature.description}</p>
                    )}
                  </div>
                  <button
                    onClick={() => toggleFeature(feature.feature, feature.enabled)}
                    className={`flex items-center gap-2 px-4 py-2 rounded-lg ${
                      feature.enabled
                        ? 'bg-green-100 text-green-700'
                        : 'bg-gray-100 text-gray-600'
                    }`}
                  >
                    {feature.enabled ? (
                      <>
                        <ToggleRight className="w-5 h-5" />
                        Enabled
                      </>
                    ) : (
                      <>
                        <ToggleLeft className="w-5 h-5" />
                        Disabled
                      </>
                    )}
                  </button>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
