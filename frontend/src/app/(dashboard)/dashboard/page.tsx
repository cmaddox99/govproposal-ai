'use client';

import { useEffect, useState } from 'react';
import {
  FileText,
  Search,
  TrendingUp,
  Clock,
  ArrowUpRight,
  ArrowDownRight,
  AlertCircle,
  CheckCircle,
} from 'lucide-react';
import Link from 'next/link';

interface Metric {
  label: string;
  value: string | number;
  change: number;
  changeLabel: string;
  icon: React.ElementType;
  color: string;
}

interface PipelineStage {
  name: string;
  count: number;
  color: string;
}

interface Alert {
  id: string;
  type: 'warning' | 'info' | 'success';
  message: string;
  time: string;
}

interface Proposal {
  id: string;
  title: string;
  agency: string;
  value: string;
  stage: string;
  dueDate: string;
}

export default function DashboardPage() {
  const [userName, setUserName] = useState('User');
  const [orgName, setOrgName] = useState('');

  useEffect(() => {
    const storedOrgName = localStorage.getItem('currentOrgName');
    if (storedOrgName) {
      setOrgName(storedOrgName);
    }
  }, []);

  const metrics: Metric[] = [
    {
      label: 'Active Proposals',
      value: 12,
      change: 2,
      changeLabel: 'from last month',
      icon: FileText,
      color: 'blue',
    },
    {
      label: 'New Opportunities',
      value: 47,
      change: 15,
      changeLabel: 'from last month',
      icon: Search,
      color: 'green',
    },
    {
      label: 'Win Rate',
      value: '68%',
      change: 5,
      changeLabel: 'from last quarter',
      icon: TrendingUp,
      color: 'purple',
    },
    {
      label: 'Pending Deadlines',
      value: 3,
      change: -1,
      changeLabel: 'from last week',
      icon: Clock,
      color: 'orange',
    },
  ];

  const pipelineStages: PipelineStage[] = [
    { name: 'Discovery', count: 8, color: 'bg-gray-600' },
    { name: 'Qualification', count: 5, color: 'bg-blue-600' },
    { name: 'Development', count: 4, color: 'bg-yellow-600' },
    { name: 'Review', count: 2, color: 'bg-purple-600' },
    { name: 'Submitted', count: 3, color: 'bg-green-600' },
  ];

  const alerts: Alert[] = [
    {
      id: '1',
      type: 'warning',
      message: 'Proposal deadline in 3 days: DOD Cybersecurity Contract',
      time: '2 hours ago',
    },
    {
      id: '2',
      type: 'info',
      message: 'New opportunity matching your criteria: GSA IT Services',
      time: '5 hours ago',
    },
    {
      id: '3',
      type: 'success',
      message: 'Compliance check passed for NASA proposal',
      time: '1 day ago',
    },
  ];

  const recentProposals: Proposal[] = [
    {
      id: '1',
      title: 'DOD Cybersecurity Enhancement',
      agency: 'Department of Defense',
      value: '$2.4M',
      stage: 'Development',
      dueDate: 'Feb 15, 2026',
    },
    {
      id: '2',
      title: 'VA Healthcare IT Modernization',
      agency: 'Veterans Affairs',
      value: '$1.8M',
      stage: 'Review',
      dueDate: 'Feb 20, 2026',
    },
    {
      id: '3',
      title: 'GSA Cloud Infrastructure',
      agency: 'General Services Admin',
      value: '$3.2M',
      stage: 'Qualification',
      dueDate: 'Mar 01, 2026',
    },
    {
      id: '4',
      title: 'NASA Data Analytics Platform',
      agency: 'NASA',
      value: '$950K',
      stage: 'Submitted',
      dueDate: 'Feb 10, 2026',
    },
  ];

  const getAlertIcon = (type: Alert['type']) => {
    switch (type) {
      case 'warning':
        return <AlertCircle className="w-5 h-5 text-yellow-500" />;
      case 'success':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      default:
        return <AlertCircle className="w-5 h-5 text-blue-500" />;
    }
  };

  const getStageColor = (stage: string) => {
    const colors: Record<string, string> = {
      Discovery: 'bg-gray-500',
      Qualification: 'bg-blue-500',
      Development: 'bg-yellow-500',
      Review: 'bg-purple-500',
      Submitted: 'bg-green-500',
    };
    return colors[stage] || 'bg-gray-500';
  };

  return (
    <div className="space-y-8">
      {/* Welcome Header */}
      <div>
        <h1 className="text-3xl font-bold text-white">Welcome back!</h1>
        <p className="text-gray-400 mt-1">
          {orgName ? `${orgName} Dashboard` : 'Here\'s what\'s happening with your proposals'}
        </p>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {metrics.map((metric) => (
          <div
            key={metric.label}
            className="bg-gray-900 border border-gray-800 rounded-xl p-6"
          >
            <div className="flex items-center justify-between mb-4">
              <div className={`p-3 rounded-lg bg-${metric.color}-600/20`}>
                <metric.icon className={`w-6 h-6 text-${metric.color}-500`} />
              </div>
              <div
                className={`flex items-center gap-1 text-sm ${
                  metric.change >= 0 ? 'text-green-500' : 'text-red-500'
                }`}
              >
                {metric.change >= 0 ? (
                  <ArrowUpRight className="w-4 h-4" />
                ) : (
                  <ArrowDownRight className="w-4 h-4" />
                )}
                {Math.abs(metric.change)}
              </div>
            </div>
            <div className="text-3xl font-bold text-white mb-1">{metric.value}</div>
            <div className="text-gray-500 text-sm">{metric.label}</div>
          </div>
        ))}
      </div>

      {/* Pipeline and Alerts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Pipeline Overview */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <h2 className="text-lg font-semibold text-white mb-6">Pipeline Overview</h2>
          <div className="space-y-4">
            {pipelineStages.map((stage) => (
              <div key={stage.name} className="flex items-center gap-4">
                <div className="w-24 text-sm text-gray-400">{stage.name}</div>
                <div className="flex-1 bg-gray-800 rounded-full h-4 overflow-hidden">
                  <div
                    className={`h-full ${stage.color} rounded-full`}
                    style={{ width: `${(stage.count / 10) * 100}%` }}
                  />
                </div>
                <div className="w-8 text-sm text-white font-medium">{stage.count}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Alerts */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <h2 className="text-lg font-semibold text-white mb-6">Recent Alerts</h2>
          <div className="space-y-4">
            {alerts.map((alert) => (
              <div
                key={alert.id}
                className="flex items-start gap-3 p-3 bg-gray-800/50 rounded-lg"
              >
                {getAlertIcon(alert.type)}
                <div className="flex-1 min-w-0">
                  <p className="text-sm text-white">{alert.message}</p>
                  <p className="text-xs text-gray-500 mt-1">{alert.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Proposals */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold text-white">Recent Proposals</h2>
          <Link
            href="/proposals"
            className="text-sm text-blue-500 hover:text-blue-400"
          >
            View all
          </Link>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-800">
                <th className="text-left py-3 px-4 text-sm font-medium text-gray-400">
                  Title
                </th>
                <th className="text-left py-3 px-4 text-sm font-medium text-gray-400">
                  Agency
                </th>
                <th className="text-left py-3 px-4 text-sm font-medium text-gray-400">
                  Value
                </th>
                <th className="text-left py-3 px-4 text-sm font-medium text-gray-400">
                  Stage
                </th>
                <th className="text-left py-3 px-4 text-sm font-medium text-gray-400">
                  Due Date
                </th>
              </tr>
            </thead>
            <tbody>
              {recentProposals.map((proposal) => (
                <tr
                  key={proposal.id}
                  className="border-b border-gray-800/50 hover:bg-gray-800/30"
                >
                  <td className="py-4 px-4">
                    <Link
                      href={`/proposals/${proposal.id}/scoring`}
                      className="text-white hover:text-blue-400"
                    >
                      {proposal.title}
                    </Link>
                  </td>
                  <td className="py-4 px-4 text-gray-400">{proposal.agency}</td>
                  <td className="py-4 px-4 text-white font-medium">{proposal.value}</td>
                  <td className="py-4 px-4">
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStageColor(
                        proposal.stage
                      )} text-white`}
                    >
                      {proposal.stage}
                    </span>
                  </td>
                  <td className="py-4 px-4 text-gray-400">{proposal.dueDate}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
