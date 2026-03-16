'use client';

import { useEffect, useState } from 'react';
import { Shield, CheckCircle, AlertTriangle, XCircle, Loader2, Clock } from 'lucide-react';
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

export default function CompliancePage() {
  const [summary, setSummary] = useState<ComplianceSummary>(DEFAULT_SUMMARY);
  const [items, setItems] = useState<ComplianceItem[]>([]);
  const [certifications, setCertifications] = useState<Certification[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const orgId = localStorage.getItem('currentOrgId');
    if (!orgId) {
      setLoading(false);
      return;
    }

    Promise.all([
      complianceApi.getSummary(orgId),
      complianceApi.listItems(orgId),
      complianceApi.listCertifications(orgId),
    ])
      .then(([summaryRes, itemsRes, certsRes]) => {
        setSummary(summaryRes.data);
        setItems(itemsRes.data.items);
        setCertifications(certsRes.data.items);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

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
    const labels: Record<string, string> = {
      sam: 'SAM.gov Registration',
      cage: 'CAGE Code',
      uei: 'UEI Number',
      gsa: 'GSA Schedule',
      cmmc: 'CMMC Certification',
      sba_8a: 'SBA 8(a)',
      hubzone: 'HUBZone',
      sdvosb: 'SDVOSB',
      wosb: 'WOSB',
    };
    return labels[type] || type;
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
        <h2 className="text-lg font-semibold text-white mb-6">Compliance Checklist</h2>
        {items.length === 0 ? (
          <p className="text-gray-500">No compliance items tracked yet</p>
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
        <h2 className="text-lg font-semibold text-white mb-6">Certifications</h2>
        {certifications.length === 0 ? (
          <p className="text-gray-500">No certifications tracked yet</p>
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
