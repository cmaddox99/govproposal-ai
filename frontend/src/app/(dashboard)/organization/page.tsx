'use client';

import { useEffect, useState } from 'react';
import { Building2, Users, Settings, Mail, Phone, MapPin, Save, Plus, X, AlertCircle, CheckCircle, Briefcase, Award, Trash2, Edit3 } from 'lucide-react';
import { pastPerformanceApi } from '@/lib/api';

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
  capabilities_summary: string | null;
  capabilities: Array<{ name: string; description: string }> | null;
}

interface PastPerformanceRecord {
  id: string;
  organization_id: string;
  contract_name: string;
  agency: string | null;
  contract_number: string | null;
  contract_value: number | null;
  period_of_performance_start: string | null;
  period_of_performance_end: string | null;
  description: string | null;
  relevance_tags: string[] | null;
  contact_name: string | null;
  contact_email: string | null;
  contact_phone: string | null;
  performance_rating: string | null;
  created_at: string;
  updated_at: string;
}

const EMPTY_PP: Omit<PastPerformanceRecord, 'id' | 'organization_id' | 'created_at' | 'updated_at'> = {
  contract_name: '',
  agency: '',
  contract_number: '',
  contract_value: null,
  period_of_performance_start: null,
  period_of_performance_end: null,
  description: '',
  relevance_tags: [],
  contact_name: '',
  contact_email: '',
  contact_phone: '',
  performance_rating: '',
};

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

  // Capabilities
  const [capabilitiesSummary, setCapabilitiesSummary] = useState('');
  const [capabilities, setCapabilities] = useState<Array<{ name: string; description: string }>>([]);

  // Past Performance
  const [ppRecords, setPpRecords] = useState<PastPerformanceRecord[]>([]);
  const [ppLoading, setPpLoading] = useState(false);
  const [showPpForm, setShowPpForm] = useState(false);
  const [editingPpId, setEditingPpId] = useState<string | null>(null);
  const [ppForm, setPpForm] = useState(EMPTY_PP);
  const [newTag, setNewTag] = useState('');

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
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!response.ok) throw new Error('Failed to fetch organization');

      const data = await response.json();
      setOrg(data);
      setName(data.name || '');
      setContactEmail(data.contact_email || '');
      setPhone(data.phone || '');
      setAddress(data.address || '');
      setUeiNumber(data.uei_number || '');
      setCageCode(data.cage_code || '');
      setDunsNumber(data.duns_number || '');
      setNaicsCodes(data.naics_codes || []);
      setCapabilitiesSummary(data.capabilities_summary || '');
      setCapabilities(data.capabilities || []);

      // Fetch past performance
      fetchPastPerformance(orgId);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchPastPerformance = async (orgId: string) => {
    setPpLoading(true);
    try {
      const res = await pastPerformanceApi.list(orgId);
      setPpRecords(res.data);
    } catch {
      // silently fail — PP section just shows empty
    } finally {
      setPpLoading(false);
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
          capabilities_summary: capabilitiesSummary || null,
          capabilities: capabilities.length > 0 ? capabilities : null,
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

  // Capabilities handlers
  const addCapability = () => {
    setCapabilities([...capabilities, { name: '', description: '' }]);
  };

  const updateCapability = (index: number, field: 'name' | 'description', value: string) => {
    const updated = [...capabilities];
    updated[index] = { ...updated[index], [field]: value };
    setCapabilities(updated);
  };

  const removeCapability = (index: number) => {
    setCapabilities(capabilities.filter((_, i) => i !== index));
  };

  // Past Performance handlers
  const handleSavePp = async () => {
    const orgId = localStorage.getItem('currentOrgId');
    if (!orgId || !ppForm.contract_name) return;

    try {
      const payload = {
        ...ppForm,
        contract_value: ppForm.contract_value || null,
        relevance_tags: ppForm.relevance_tags && ppForm.relevance_tags.length > 0 ? ppForm.relevance_tags : null,
      };

      if (editingPpId) {
        await pastPerformanceApi.update(orgId, editingPpId, payload);
      } else {
        await pastPerformanceApi.create(orgId, payload);
      }

      setShowPpForm(false);
      setEditingPpId(null);
      setPpForm(EMPTY_PP);
      fetchPastPerformance(orgId);
      setSuccessMessage(editingPpId ? 'Past performance updated' : 'Past performance added');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to save past performance');
    }
  };

  const handleEditPp = (record: PastPerformanceRecord) => {
    setEditingPpId(record.id);
    setPpForm({
      contract_name: record.contract_name,
      agency: record.agency || '',
      contract_number: record.contract_number || '',
      contract_value: record.contract_value,
      period_of_performance_start: record.period_of_performance_start ? record.period_of_performance_start.split('T')[0] : null,
      period_of_performance_end: record.period_of_performance_end ? record.period_of_performance_end.split('T')[0] : null,
      description: record.description || '',
      relevance_tags: record.relevance_tags || [],
      contact_name: record.contact_name || '',
      contact_email: record.contact_email || '',
      contact_phone: record.contact_phone || '',
      performance_rating: record.performance_rating || '',
    });
    setShowPpForm(true);
  };

  const handleDeletePp = async (ppId: string) => {
    if (!window.confirm('Delete this past performance record?')) return;
    const orgId = localStorage.getItem('currentOrgId');
    if (!orgId) return;

    try {
      await pastPerformanceApi.delete(orgId, ppId);
      fetchPastPerformance(orgId);
      setSuccessMessage('Past performance deleted');
    } catch (err: any) {
      setError('Failed to delete past performance');
    }
  };

  const addPpTag = () => {
    if (newTag && !(ppForm.relevance_tags || []).includes(newTag)) {
      setPpForm({ ...ppForm, relevance_tags: [...(ppForm.relevance_tags || []), newTag] });
      setNewTag('');
    }
  };

  const removePpTag = (tag: string) => {
    setPpForm({ ...ppForm, relevance_tags: (ppForm.relevance_tags || []).filter(t => t !== tag) });
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
        <p className="text-gray-400 mt-1">Manage your organization profile, capabilities, and past performance</p>
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
              <label className="block text-sm font-medium text-gray-400 mb-2">Organization Name</label>
              <input type="text" value={name} onChange={(e) => setName(e.target.value)}
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">
                  <Mail className="w-4 h-4 inline mr-2" />Contact Email
                </label>
                <input type="email" value={contactEmail} onChange={(e) => setContactEmail(e.target.value)}
                  placeholder="contact@company.com"
                  className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">
                  <Phone className="w-4 h-4 inline mr-2" />Phone Number
                </label>
                <input type="tel" value={phone} onChange={(e) => setPhone(e.target.value)}
                  placeholder="(555) 123-4567"
                  className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">
                <MapPin className="w-4 h-4 inline mr-2" />Address
              </label>
              <textarea value={address} onChange={(e) => setAddress(e.target.value)}
                placeholder="Enter your organization address" rows={3}
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
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
            <label className="block text-sm font-medium text-gray-400 mb-2">UEI Number</label>
            <input type="text" value={ueiNumber} onChange={(e) => setUeiNumber(e.target.value)}
              placeholder="Enter UEI"
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">CAGE Code</label>
            <input type="text" value={cageCode} onChange={(e) => setCageCode(e.target.value)}
              placeholder="Enter CAGE Code"
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">DUNS Number</label>
            <input type="text" value={dunsNumber} onChange={(e) => setDunsNumber(e.target.value)}
              placeholder="Enter DUNS Number"
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
          </div>
        </div>
      </div>

      {/* NAICS Codes */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h2 className="text-lg font-semibold text-white mb-2">NAICS Codes</h2>
        <p className="text-gray-400 text-sm mb-6">Add your NAICS codes to automatically match with relevant opportunities from SAM.gov</p>

        <div className="flex gap-2 mb-4">
          <input type="text" value={newNaicsCode}
            onChange={(e) => setNewNaicsCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
            placeholder="Enter NAICS code (e.g., 541512)"
            className="flex-1 px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            onKeyDown={(e) => e.key === 'Enter' && addNaicsCode()} />
          <button onClick={addNaicsCode}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            <Plus className="w-4 h-4" /> Add
          </button>
        </div>

        <div className="flex flex-wrap gap-2">
          {naicsCodes.map((code) => (
            <span key={code} className="flex items-center gap-2 px-3 py-1.5 bg-blue-600/20 text-blue-400 rounded-lg">
              {code}
              <button onClick={() => removeNaicsCode(code)} className="hover:text-blue-200"><X className="w-4 h-4" /></button>
            </span>
          ))}
          {naicsCodes.length === 0 && <span className="text-gray-500 text-sm">No NAICS codes added yet</span>}
        </div>
      </div>

      {/* Capabilities */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <div className="flex items-center gap-3 mb-2">
          <Briefcase className="w-6 h-6 text-purple-500" />
          <h2 className="text-lg font-semibold text-white">Company Capabilities</h2>
        </div>
        <p className="text-gray-400 text-sm mb-6">Describe your company&apos;s capabilities. This information is used by AI to generate tailored proposal content.</p>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">Capabilities Summary</label>
            <textarea value={capabilitiesSummary} onChange={(e) => setCapabilitiesSummary(e.target.value)}
              placeholder="Describe your company's core competencies, strategic advantages, and areas of expertise..."
              rows={4}
              className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
          </div>

          <div>
            <div className="flex items-center justify-between mb-3">
              <label className="block text-sm font-medium text-gray-400">Key Capabilities</label>
              <button onClick={addCapability}
                className="flex items-center gap-1 px-3 py-1 text-sm bg-purple-600 text-white rounded-lg hover:bg-purple-700">
                <Plus className="w-3 h-3" /> Add
              </button>
            </div>

            <div className="space-y-3">
              {capabilities.map((cap, index) => (
                <div key={index} className="flex gap-3 items-start">
                  <input type="text" value={cap.name}
                    onChange={(e) => updateCapability(index, 'name', e.target.value)}
                    placeholder="Capability name"
                    className="w-1/3 px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 text-sm focus:ring-2 focus:ring-blue-500" />
                  <input type="text" value={cap.description}
                    onChange={(e) => updateCapability(index, 'description', e.target.value)}
                    placeholder="Brief description"
                    className="flex-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 text-sm focus:ring-2 focus:ring-blue-500" />
                  <button onClick={() => removeCapability(index)}
                    className="p-2 text-gray-400 hover:text-red-400">
                    <X className="w-4 h-4" />
                  </button>
                </div>
              ))}
              {capabilities.length === 0 && <p className="text-gray-500 text-sm">No capabilities added yet</p>}
            </div>
          </div>
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end">
        <button onClick={handleSave} disabled={saving}
          className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50">
          <Save className="w-5 h-5" />
          {saving ? 'Saving...' : 'Save Changes'}
        </button>
      </div>

      {/* Past Performance */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <Award className="w-6 h-6 text-yellow-500" />
            <div>
              <h2 className="text-lg font-semibold text-white">Past Performance</h2>
              <p className="text-gray-400 text-sm">Track your contract history for AI-powered proposal generation</p>
            </div>
          </div>
          <button onClick={() => { setShowPpForm(true); setEditingPpId(null); setPpForm(EMPTY_PP); }}
            className="flex items-center gap-2 px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 text-sm">
            <Plus className="w-4 h-4" /> Add Record
          </button>
        </div>

        {/* PP Form */}
        {showPpForm && (
          <div className="mb-6 p-4 bg-gray-800 border border-gray-700 rounded-lg space-y-4">
            <h3 className="text-white font-medium">{editingPpId ? 'Edit' : 'New'} Past Performance Record</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm text-gray-400 mb-1">Contract Name *</label>
                <input type="text" value={ppForm.contract_name}
                  onChange={(e) => setPpForm({ ...ppForm, contract_name: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white text-sm" />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Agency</label>
                <input type="text" value={ppForm.agency || ''}
                  onChange={(e) => setPpForm({ ...ppForm, agency: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white text-sm" />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Contract Number</label>
                <input type="text" value={ppForm.contract_number || ''}
                  onChange={(e) => setPpForm({ ...ppForm, contract_number: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white text-sm" />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Contract Value ($)</label>
                <input type="number" value={ppForm.contract_value || ''}
                  onChange={(e) => setPpForm({ ...ppForm, contract_value: e.target.value ? parseFloat(e.target.value) : null })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white text-sm" />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Period Start</label>
                <input type="date" value={ppForm.period_of_performance_start || ''}
                  onChange={(e) => setPpForm({ ...ppForm, period_of_performance_start: e.target.value || null })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white text-sm" />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Period End</label>
                <input type="date" value={ppForm.period_of_performance_end || ''}
                  onChange={(e) => setPpForm({ ...ppForm, period_of_performance_end: e.target.value || null })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white text-sm" />
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Performance Rating</label>
                <select value={ppForm.performance_rating || ''}
                  onChange={(e) => setPpForm({ ...ppForm, performance_rating: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white text-sm">
                  <option value="">Select rating</option>
                  <option value="Exceptional">Exceptional</option>
                  <option value="Very Good">Very Good</option>
                  <option value="Satisfactory">Satisfactory</option>
                  <option value="Marginal">Marginal</option>
                  <option value="Unsatisfactory">Unsatisfactory</option>
                </select>
              </div>
              <div>
                <label className="block text-sm text-gray-400 mb-1">Client Contact Name</label>
                <input type="text" value={ppForm.contact_name || ''}
                  onChange={(e) => setPpForm({ ...ppForm, contact_name: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white text-sm" />
              </div>
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Description</label>
              <textarea value={ppForm.description || ''}
                onChange={(e) => setPpForm({ ...ppForm, description: e.target.value })}
                rows={3}
                className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white text-sm" />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Relevance Tags</label>
              <div className="flex gap-2 mb-2">
                <input type="text" value={newTag}
                  onChange={(e) => setNewTag(e.target.value)}
                  placeholder="e.g., IT, Cybersecurity, Cloud"
                  onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addPpTag())}
                  className="flex-1 px-3 py-2 bg-gray-700 border border-gray-600 rounded-lg text-white text-sm" />
                <button onClick={addPpTag} className="px-3 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700">Add</button>
              </div>
              <div className="flex flex-wrap gap-2">
                {(ppForm.relevance_tags || []).map((tag) => (
                  <span key={tag} className="flex items-center gap-1 px-2 py-1 bg-yellow-600/20 text-yellow-400 rounded text-sm">
                    {tag}
                    <button onClick={() => removePpTag(tag)} className="hover:text-yellow-200"><X className="w-3 h-3" /></button>
                  </span>
                ))}
              </div>
            </div>
            <div className="flex gap-3">
              <button onClick={handleSavePp} disabled={!ppForm.contract_name}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm disabled:opacity-50">
                {editingPpId ? 'Update' : 'Save'} Record
              </button>
              <button onClick={() => { setShowPpForm(false); setEditingPpId(null); setPpForm(EMPTY_PP); }}
                className="px-4 py-2 bg-gray-700 text-gray-300 rounded-lg hover:bg-gray-600 text-sm">
                Cancel
              </button>
            </div>
          </div>
        )}

        {/* PP List */}
        {ppLoading ? (
          <p className="text-gray-400 text-sm">Loading past performance...</p>
        ) : ppRecords.length === 0 ? (
          <p className="text-gray-500 text-sm">No past performance records yet. Add your contract history to help AI generate better proposals.</p>
        ) : (
          <div className="space-y-4">
            {ppRecords.map((record) => (
              <div key={record.id} className="p-4 bg-gray-800 border border-gray-700 rounded-lg">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="text-white font-medium">{record.contract_name}</h3>
                    <div className="flex flex-wrap gap-x-4 gap-y-1 mt-1 text-sm text-gray-400">
                      {record.agency && <span>{record.agency}</span>}
                      {record.contract_number && <span>#{record.contract_number}</span>}
                      {record.contract_value && <span>${record.contract_value.toLocaleString()}</span>}
                      {record.period_of_performance_start && record.period_of_performance_end && (
                        <span>
                          {new Date(record.period_of_performance_start).toLocaleDateString()} — {new Date(record.period_of_performance_end).toLocaleDateString()}
                        </span>
                      )}
                    </div>
                    {record.description && <p className="text-gray-400 text-sm mt-2 line-clamp-2">{record.description}</p>}
                    <div className="flex flex-wrap gap-2 mt-2">
                      {record.performance_rating && (
                        <span className="px-2 py-0.5 bg-green-600/20 text-green-400 rounded text-xs">{record.performance_rating}</span>
                      )}
                      {(record.relevance_tags || []).map((tag) => (
                        <span key={tag} className="px-2 py-0.5 bg-yellow-600/20 text-yellow-400 rounded text-xs">{tag}</span>
                      ))}
                    </div>
                  </div>
                  <div className="flex gap-2 ml-4">
                    <button onClick={() => handleEditPp(record)} className="p-1.5 text-gray-400 hover:text-blue-400">
                      <Edit3 className="w-4 h-4" />
                    </button>
                    <button onClick={() => handleDeletePp(record.id)} className="p-1.5 text-gray-400 hover:text-red-400">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
