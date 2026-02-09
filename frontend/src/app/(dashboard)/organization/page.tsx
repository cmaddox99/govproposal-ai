'use client';

import { useEffect, useState } from 'react';
import { Building2, Users, Settings, Mail, Phone, MapPin, Save, Plus, X, AlertCircle, CheckCircle } from 'lucide-react';

interface Organization {
  id: string;
  name: string;
  slug: string;
  contact_email: string | null;
  phone: string | null;
  address: string | null;
  uei_number: string | null;
  cage_code: string | null;
  duns_number: string | null;
  naics_codes: string[] | null;
}

export default function OrganizationPage() {
  const [org, setOrg] = useState<Organization | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  // Form fields
  const [name, setName] = useState('');
  const [contactEmail, setContactEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [address, setAddress] = useState('');
  const [ueiNumber, setUeiNumber] = useState('');
  const [cageCode, setCageCode] = useState('');
  const [dunsNumber, setDunsNumber] = useState('');
  const [naicsCodes, setNaicsCodes] = useState<string[]>([]);
  const [newNaicsCode, setNewNaicsCode] = useState('');

  useEffect(() => {
    fetchOrganization();
  }, []);

  const fetchOrganization = async () => {
    try {
      const token = localStorage.getItem('token');
      const orgId = localStorage.getItem('currentOrgId');

      if (!orgId) {
        setError('No organization selected');
        return;
      }

      const response = await fetch(`/api/organizations/${orgId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch organization');
      }

      const data = await response.json();
      setOrg(data);

      // Set form fields
      setName(data.name || '');
      setContactEmail(data.contact_email || '');
      setPhone(data.phone || '');
      setAddress(data.address || '');
      setUeiNumber(data.uei_number || '');
      setCageCode(data.cage_code || '');
      setDunsNumber(data.duns_number || '');
      setNaicsCodes(data.naics_codes || []);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    setError('');
    setSuccessMessage('');

    try {
      const token = localStorage.getItem('token');
      const orgId = localStorage.getItem('currentOrgId');

      const response = await fetch(`/api/organizations/${orgId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          name,
          contact_email: contactEmail || null,
          phone: phone || null,
          address: address || null,
          uei_number: ueiNumber || null,
          cage_code: cageCode || null,
          duns_number: dunsNumber || null,
          naics_codes: naicsCodes.length > 0 ? naicsCodes : null,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to save organization');
      }

      const data = await response.json();
      setOrg(data);
      localStorage.setItem('currentOrgName', data.name);
      setSuccessMessage('Organization saved successfully');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  const addNaicsCode = () => {
    if (newNaicsCode && !naicsCodes.includes(newNaicsCode)) {
      setNaicsCodes([...naicsCodes, newNaicsCode]);
      setNewNaicsCode('');
    }
  };

  const removeNaicsCode = (code: string) => {
    setNaicsCodes(naicsCodes.filter((c) => c !== code));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-gray-400">Loading...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Organization</h1>
        <p className="text-gray-400 mt-1">Manage your organization profile and government credentials</p>
      </div>

      {error && (
        <div className="flex items-center gap-2 text-red-400 bg-red-900/20 border border-red-800 p-4 rounded-lg">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          {error}
        </div>
      )}

      {successMessage && (
        <div className="flex items-center gap-2 text-green-400 bg-green-900/20 border border-green-800 p-4 rounded-lg">
          <CheckCircle className="w-5 h-5 flex-shrink-0" />
          {successMessage}
        </div>
      )}

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
                value={name}
                onChange={(e) => setName(e.target.value)}
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
                  value={contactEmail}
                  onChange={(e) => setContactEmail(e.target.value)}
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
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
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
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                placeholder="Enter your organization address"
                rows={3}
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
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
            <div className="text-4xl font-bold text-white mb-2">-</div>
            <p className="text-gray-400 text-sm">Active users in your organization</p>
            <a href="/settings/users" className="mt-4 text-sm text-blue-500 hover:text-blue-400 block">
              Manage Team →
            </a>
          </div>

          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
            <div className="flex items-center gap-3 mb-4">
              <Settings className="w-6 h-6 text-purple-500" />
              <h2 className="text-lg font-semibold text-white">Subscription</h2>
            </div>
            <div className="text-xl font-bold text-white mb-2">Professional</div>
            <p className="text-gray-400 text-sm">Current plan</p>
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
              value={ueiNumber}
              onChange={(e) => setUeiNumber(e.target.value)}
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
              value={cageCode}
              onChange={(e) => setCageCode(e.target.value)}
              placeholder="Enter CAGE Code"
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">
              DUNS Number
            </label>
            <input
              type="text"
              value={dunsNumber}
              onChange={(e) => setDunsNumber(e.target.value)}
              placeholder="Enter DUNS Number"
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>

      {/* NAICS Codes */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h2 className="text-lg font-semibold text-white mb-2">NAICS Codes</h2>
        <p className="text-gray-400 text-sm mb-6">
          Add your NAICS codes to automatically match with relevant opportunities from SAM.gov
        </p>

        <div className="flex gap-2 mb-4">
          <input
            type="text"
            value={newNaicsCode}
            onChange={(e) => setNewNaicsCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
            placeholder="Enter NAICS code (e.g., 541512)"
            className="flex-1 px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            onKeyDown={(e) => e.key === 'Enter' && addNaicsCode()}
          />
          <button
            onClick={addNaicsCode}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            <Plus className="w-4 h-4" />
            Add
          </button>
        </div>

        <div className="flex flex-wrap gap-2">
          {naicsCodes.map((code) => (
            <span
              key={code}
              className="flex items-center gap-2 px-3 py-1.5 bg-blue-600/20 text-blue-400 rounded-lg"
            >
              {code}
              <button
                onClick={() => removeNaicsCode(code)}
                className="hover:text-blue-200"
              >
                <X className="w-4 h-4" />
              </button>
            </span>
          ))}
          {naicsCodes.length === 0 && (
            <span className="text-gray-500 text-sm">No NAICS codes added yet</span>
          )}
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end">
        <button
          onClick={handleSave}
          disabled={saving}
          className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          <Save className="w-5 h-5" />
          {saving ? 'Saving...' : 'Save Changes'}
        </button>
      </div>
    </div>
  );
}
