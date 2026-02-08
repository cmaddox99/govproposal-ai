'use client';

import { Shield, CheckCircle, AlertTriangle, XCircle } from 'lucide-react';

export default function CompliancePage() {
  const complianceItems = [
    { name: 'SAM.gov Registration', status: 'complete', description: 'Active registration verified' },
    { name: 'CAGE Code', status: 'complete', description: 'Valid CAGE code on file' },
    { name: 'DUNS Number', status: 'complete', description: 'UEI number verified' },
    { name: 'GSA Schedule', status: 'warning', description: 'Expires in 45 days' },
    { name: 'Security Clearance', status: 'incomplete', description: 'Facility clearance pending' },
  ];

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'complete':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'warning':
        return <AlertTriangle className="w-5 h-5 text-yellow-500" />;
      default:
        return <XCircle className="w-5 h-5 text-red-500" />;
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Compliance</h1>
        <p className="text-gray-400 mt-1">Track your compliance requirements and certifications</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 text-center">
          <div className="text-4xl font-bold text-green-500 mb-2">85%</div>
          <div className="text-gray-400">Overall Compliance</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 text-center">
          <div className="text-4xl font-bold text-white mb-2">3</div>
          <div className="text-gray-400">Items Complete</div>
        </div>
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 text-center">
          <div className="text-4xl font-bold text-yellow-500 mb-2">2</div>
          <div className="text-gray-400">Action Required</div>
        </div>
      </div>

      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h2 className="text-lg font-semibold text-white mb-6">Compliance Checklist</h2>
        <div className="space-y-4">
          {complianceItems.map((item) => (
            <div key={item.name} className="flex items-center gap-4 p-4 bg-gray-800/50 rounded-lg">
              {getStatusIcon(item.status)}
              <div className="flex-1">
                <div className="text-white font-medium">{item.name}</div>
                <div className="text-gray-500 text-sm">{item.description}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
