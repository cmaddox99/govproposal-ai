'use client';

import { useEffect, useState } from 'react';
import { Shield, CheckCircle, AlertTriangle, XCircle, Loader2, Clock, Plus, X } from 'lucide-react';
import { complianceApi } from '@/lib/api';

interface ComplianceSummary {
  overall_compliance_percentage: number;
  total_items: number;
  compliant_items: number;
  partial_items: number;
  non_compliant_items: number;
  action_required: number;
  total_certifications: number;
  active_certifications: number;
}

interface ComplianceItem {
  id: string;
  framework: string;
  clause_number: string;
  title: string;
  status: string;
  evidence_notes: string | null;
  due_date: string | null;
}

interface Certification {
  id: string;
  certification_type: string;
  identifier: string | null;
  status: string;
  expiry_date: string | null;
  notes: string | null;
}

const DEFAULT_SUMMARY: ComplianceSummary = {
  overall_compliance_percentage: 0,
  total_items: 0,
  compliant_items: 0,
  partial_items: 0,
  non_compliant_items: 0,
  action_required: 0,
  total_certifications: 0,
  active_certifications: 0,
};

const FRAMEWORKS = [
  { value: 'far', label: 'FAR' },
  { value: 'dfars', label: 'DFARS' },
  { value: 'nist_800_171', label: 'NIST 800-171' },
  { value: 'cmmc', label: 'CMMC' },
  { value: 'itar', label: 'ITAR' },
  { value: 'ear', label: 'EAR' },
  { value: 'other', label: 'Other' },
];

const STATUSES = [
  { value: 'compliant', label: 'Compliant' },
  { value: 'non_compliant', label: 'Non-Compliant' },
  { value: 'partial', label: 'Partial' },
  { value: 'pending_review', label: 'Pending Review' },
  { value: 'not_applicable', label: 'Not Applicable' },
];

const CERT_TYPES = [
  { value: 'sam', label: 'SAM.gov Registration' },
  { value: 'cage', label: 'CAGE Code' },
  { value: 'uei', label: 'UEI Number' },
  { value: 'gsa', label: 'GSA Schedule' },
  { value: 'cmmc', label: 'CMMC Certification' },
  { value: 'sba_8a', label: 'SBA 8(a)' },
  { value: 'hubzone', label: 'HUBZone' },
  { value: 'sdvosb', label: 'SDVOSB' },
  { value: 'wosb', label: 'WOSB' },
];

export default function CompliancePage() {
  const [summary, setSummary] = useState<ComplianceSummary>(DEFAULT_SUMMARY);
  const [items, setItems] = useState<ComplianceItem[]>([]);
  const [certifications, setCertifications] = useState<Certification[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddItem, setShowAddItem] = useState(false);
  const [showAddCert, setShowAddCert] = useState(false);
  const [saving, setSaving] = useState(false);

  // New item form
  const [newItem, setNewItem] = useState({
    framework: 'far',
    clause_number: '',
    title: '',
    status: 'pending_review',
    evidence_notes: '',
    due_date: '',
  });

  // New certification form
  const [newCert, setNewCert] = useState({
    certification_type: 'sam',
    identifier: '',
    status: 'pending_review',
    expiry_date: '',
    notes: '',
  });

  const orgId = typeof window !== 'undefined' ? localStorage.getItem('currentOrgId') : null;

  const fetchData = async () => {
    if (!orgId) {
      setLoading(false);
      return;
    }

    try {
      const [summaryRes, itemsRes, certsRes] = await Promise.all([
        complianceApi.getSummary(orgId),
        complianceApi.listItems(orgId),
        complianceApi.listCertifications(orgId),
      ]);
      setSummary(summaryRes.data);
      setItems(itemsRes.data.items || itemsRes.data);
      setCertifications(certsRes.data.items || certsRes.data);
    } catch {
      // Endpoints may not exist yet - show empty state
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleAddItem = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!orgId) return;
    setSaving(true);
    try {
      await complianceApi.createItem(orgId, {
        ...newItem,
        due_date: newItem.due_date || null,
        evidence_notes: newItem.evidence_notes || null,
      });
      setShowAddItem(false);
      setNewItem({ framework: 'far', clause_number: '', title: '', status: 'pending_review', evidence_notes: '', due_date: '' });
      fetchData();
    } catch {
      // error handling
    } finally {
      setSaving(false);
    }
  };

  const handleAddCert = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!orgId) return;
    setSaving(true);
    try {
      await complianceApi.createCertification(orgId, {
        ...newCert,
        identifier: newCert.identifier || null,
        expiry_date: newCert.expiry_date || null,
        notes: newCert.notes || null,
      });
      setShowAddCert(false);
      setNewCert({ certification_type: 'sam', identifier: '', status: 'pending_review', expiry_date: '', notes: '' });
      fetchData();
    } catch {
      // error handling
    } finally {
      setSaving(false);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'compliant':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'partial':
        return <AlertTriangle className="w-5 h-5 text-yellow-500" />;
      case 'pending_review':
        return <Clock className="w-5 h-5 text-blue-500" />;
      default:
        return <XCircle className="w-5 h-5 text-red-500" />;
    }
  };

  const getCertLabel = (type: string) => {
    return CERT_TYPES.find(t => t.value === type)?.label || type;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-8 h-8 animate-spin text-gray-400" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Compliance</h1>
        <p className="text-gray-400 mt-1">Track your compliance requirements and certifications</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6 text-center">
          <div className={`text-4xl font-bold mb-2 ${summary.overall_compliance_percentage >= 80 ? 'text-green-500' : summary.overall_compliance_percentage >= 50 ? 'text-yellow-500' : 'text-red-500'}`}>
            {summary.overall_compliance_percentage}%
          </div>
          <div className="text-gray-400">Overall Compliance</div>
        </div>
        <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6 text-center">
          <div className="text-4xl font-bold text-white mb-2">{summary.compliant_items}</div>
          <div className="text-gray-400">Items Compliant</div>
        </div>
        <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6 text-center">
          <div className="text-4xl font-bold text-yellow-500 mb-2">{summary.action_required}</div>
          <div className="text-gray-400">Action Required</div>
        </div>
      </div>

      {/* Compliance Items */}
      <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold text-white">Compliance Checklist</h2>
          <button
            onClick={() => setShowAddItem(true)}
            className="flex items-center gap-2 px-3 py-2 bg-gradient-to-r from-emerald-500 to-blue-500 text-white rounded-lg hover:from-emerald-600 hover:to-blue-600 text-sm"
          >
            <Plus className="w-4 h-4" />
            Add Item
          </button>
        </div>

        {showAddItem && (
          <form onSubmit={handleAddItem} className="mb-6 p-4 bg-white/[0.03] border border-white/[0.08] rounded-lg space-y-3">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-white font-medium">New Compliance Item</h3>
              <button type="button" onClick={() => setShowAddItem(false)} className="text-gray-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs text-gray-400 mb-1">Framework</label>
                <select
                  value={newItem.framework}
                  onChange={(e) => setNewItem({ ...newItem, framework: e.target.value })}
                  className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white text-sm"
                >
                  {FRAMEWORKS.map(f => (
                    <option key={f.value} value={f.value}>{f.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-xs text-gray-400 mb-1">Clause Number</label>
                <input
                  type="text"
                  value={newItem.clause_number}
                  onChange={(e) => setNewItem({ ...newItem, clause_number: e.target.value })}
                  placeholder="e.g., 52.204-21"
                  required
                  className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 text-sm"
                />
              </div>
            </div>
            <div>
              <label className="block text-xs text-gray-400 mb-1">Title</label>
              <input
                type="text"
                value={newItem.title}
                onChange={(e) => setNewItem({ ...newItem, title: e.target.value })}
                placeholder="e.g., Basic Safeguarding of Covered Contractor Information"
                required
                className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 text-sm"
              />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs text-gray-400 mb-1">Status</label>
                <select
                  value={newItem.status}
                  onChange={(e) => setNewItem({ ...newItem, status: e.target.value })}
                  className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white text-sm"
                >
                  {STATUSES.map(s => (
                    <option key={s.value} value={s.value}>{s.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-xs text-gray-400 mb-1">Due Date</label>
                <input
                  type="date"
                  value={newItem.due_date}
                  onChange={(e) => setNewItem({ ...newItem, due_date: e.target.value })}
                  className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white text-sm"
                />
              </div>
            </div>
            <div>
              <label className="block text-xs text-gray-400 mb-1">Evidence / Notes</label>
              <textarea
                value={newItem.evidence_notes}
                onChange={(e) => setNewItem({ ...newItem, evidence_notes: e.target.value })}
                placeholder="Documentation or evidence notes..."
                rows={2}
                className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 text-sm"
              />
            </div>
            <button
              type="submit"
              disabled={saving}
              className="px-4 py-2 bg-gradient-to-r from-emerald-500 to-blue-500 text-white rounded-lg hover:from-emerald-600 hover:to-blue-600 disabled:opacity-50 text-sm"
            >
              {saving ? 'Saving...' : 'Add Compliance Item'}
            </button>
          </form>
        )}

        {items.length === 0 && !showAddItem ? (
          <p className="text-gray-500">No compliance items tracked yet. Add your first item to get started.</p>
        ) : (
          <div className="space-y-4">
            {items.map((item) => (
              <div key={item.id} className="flex items-center gap-4 p-4 bg-white/[0.03] rounded-lg">
                {getStatusIcon(item.status)}
                <div className="flex-1">
                  <div className="text-white font-medium">{item.title}</div>
                  <div className="text-gray-500 text-sm">
                    {item.framework.toUpperCase()} {item.clause_number}
                    {item.evidence_notes && ` — ${item.evidence_notes}`}
                  </div>
                </div>
                {item.due_date && (
                  <div className="text-gray-500 text-sm">Due: {new Date(item.due_date).toLocaleDateString()}</div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Certifications */}
      <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold text-white">Certifications</h2>
          <button
            onClick={() => setShowAddCert(true)}
            className="flex items-center gap-2 px-3 py-2 bg-gradient-to-r from-emerald-500 to-blue-500 text-white rounded-lg hover:from-emerald-600 hover:to-blue-600 text-sm"
          >
            <Plus className="w-4 h-4" />
            Add Certification
          </button>
        </div>

        {showAddCert && (
          <form onSubmit={handleAddCert} className="mb-6 p-4 bg-white/[0.03] border border-white/[0.08] rounded-lg space-y-3">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-white font-medium">New Certification</h3>
              <button type="button" onClick={() => setShowAddCert(false)} className="text-gray-400 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs text-gray-400 mb-1">Certification Type</label>
                <select
                  value={newCert.certification_type}
                  onChange={(e) => setNewCert({ ...newCert, certification_type: e.target.value })}
                  className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white text-sm"
                >
                  {CERT_TYPES.map(c => (
                    <option key={c.value} value={c.value}>{c.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-xs text-gray-400 mb-1">Status</label>
                <select
                  value={newCert.status}
                  onChange={(e) => setNewCert({ ...newCert, status: e.target.value })}
                  className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white text-sm"
                >
                  {STATUSES.map(s => (
                    <option key={s.value} value={s.value}>{s.label}</option>
                  ))}
                </select>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs text-gray-400 mb-1">Identifier / ID Number</label>
                <input
                  type="text"
                  value={newCert.identifier}
                  onChange={(e) => setNewCert({ ...newCert, identifier: e.target.value })}
                  placeholder="e.g., 1234567890"
                  className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 text-sm"
                />
              </div>
              <div>
                <label className="block text-xs text-gray-400 mb-1">Expiry Date</label>
                <input
                  type="date"
                  value={newCert.expiry_date}
                  onChange={(e) => setNewCert({ ...newCert, expiry_date: e.target.value })}
                  className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white text-sm"
                />
              </div>
            </div>
            <div>
              <label className="block text-xs text-gray-400 mb-1">Notes</label>
              <textarea
                value={newCert.notes}
                onChange={(e) => setNewCert({ ...newCert, notes: e.target.value })}
                placeholder="Additional notes..."
                rows={2}
                className="w-full px-3 py-2 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 text-sm"
              />
            </div>
            <button
              type="submit"
              disabled={saving}
              className="px-4 py-2 bg-gradient-to-r from-emerald-500 to-blue-500 text-white rounded-lg hover:from-emerald-600 hover:to-blue-600 disabled:opacity-50 text-sm"
            >
              {saving ? 'Saving...' : 'Add Certification'}
            </button>
          </form>
        )}

        {certifications.length === 0 && !showAddCert ? (
          <p className="text-gray-500">No certifications tracked yet. Add your certifications to maintain compliance visibility.</p>
        ) : (
          <div className="space-y-4">
            {certifications.map((cert) => (
              <div key={cert.id} className="flex items-center gap-4 p-4 bg-white/[0.03] rounded-lg">
                {getStatusIcon(cert.status)}
                <div className="flex-1">
                  <div className="text-white font-medium">{getCertLabel(cert.certification_type)}</div>
                  <div className="text-gray-500 text-sm">
                    {cert.identifier && `ID: ${cert.identifier}`}
                    {cert.notes && ` — ${cert.notes}`}
                  </div>
                </div>
                {cert.expiry_date && (
                  <div className="text-gray-500 text-sm">
                    Expires: {new Date(cert.expiry_date).toLocaleDateString()}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
