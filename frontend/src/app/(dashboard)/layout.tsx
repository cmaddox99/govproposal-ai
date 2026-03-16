'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import {
  LayoutDashboard,
  Search,
  FileText,
  Shield,
  Lock,
  BarChart3,
  Bot,
  Building2,
  Settings,
  LogOut,
  ChevronDown,
  AlertCircle,
} from 'lucide-react';
import { organizationsApi } from '@/lib/api';
import { NotificationBell } from '@/components/notifications/notification-bell';

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Opportunities', href: '/opportunities', icon: Search },
  { name: 'Proposals', href: '/proposals', icon: FileText },
  { name: 'Compliance', href: '/compliance', icon: Shield },
  { name: 'Security', href: '/security', icon: Lock },
  { name: 'Analytics', href: '/analytics', icon: BarChart3 },
  { name: 'AI Assistant', href: '/assistant', icon: Bot },
];

const bottomNavigation = [
  { name: 'Organization', href: '/organization', icon: Building2 },
  { name: 'Settings', href: '/settings/users', icon: Settings },
];

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const router = useRouter();
  const [orgName, setOrgName] = useState('');
  const [orgId, setOrgId] = useState('');
  const [showCreateOrg, setShowCreateOrg] = useState(false);
  const [newOrgName, setNewOrgName] = useState('');
  const [newOrgSlug, setNewOrgSlug] = useState('');
  const [createError, setCreateError] = useState('');
  const [creating, setCreating] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const init = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        router.push('/login');
        return;
      }

      const storedOrgName = localStorage.getItem('currentOrgName');
      const storedOrgId = localStorage.getItem('currentOrgId');

      if (storedOrgName && storedOrgId) {
        setOrgName(storedOrgName);
        setOrgId(storedOrgId);
      } else {
        // Check if user already has organizations
        try {
          const response = await organizationsApi.list();
          if (response.data && response.data.length > 0) {
            const org = response.data[0];
            localStorage.setItem('currentOrgId', org.id);
            localStorage.setItem('currentOrgName', org.name);
            setOrgId(org.id);
            setOrgName(org.name);
          } else {
            setShowCreateOrg(true);
          }
        } catch {
          setShowCreateOrg(true);
        }
      }
      setIsLoading(false);
    };
    init();
  }, [router]);

  const generateSlug = (name: string) => {
    return name
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-|-$/g, '');
  };

  const handleOrgNameChange = (value: string) => {
    setNewOrgName(value);
    setNewOrgSlug(generateSlug(value));
  };

  const handleCreateOrg = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreating(true);
    setCreateError('');

    try {
      const token = localStorage.getItem('token');

      // Use local API route to bypass CORS
      const response = await fetch('/api/organizations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ name: newOrgName, slug: newOrgSlug }),
      });

      const text = await response.text();
      let data;
      try {
        data = JSON.parse(text);
      } catch {
        throw new Error(text || 'Invalid server response');
      }

      if (!response.ok) {
        throw new Error(data.detail?.message || data.detail || 'Failed to create organization');
      }

      const org = data;

      localStorage.setItem('currentOrgId', org.id);
      localStorage.setItem('currentOrgName', org.name);

      setOrgId(org.id);
      setOrgName(org.name);
      setShowCreateOrg(false);
    } catch (err: any) {
      console.error('Create org error:', err);
      setCreateError(err.message || 'Failed to create organization');
    } finally {
      setCreating(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center">
        <div className="text-gray-400">Loading...</div>
      </div>
    );
  }

  // Show create organization form if no org exists
  if (showCreateOrg) {
    return (
      <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center p-4">
        <div className="w-full max-w-md">
          <div className="bg-white/[0.03] backdrop-blur-sm border border-white/[0.08] rounded-xl p-8">
            <div className="text-center mb-8">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-emerald-500/20 to-blue-500/20 rounded-full mb-4">
                <Building2 className="w-8 h-8 text-emerald-400" />
              </div>
              <h1 className="text-2xl font-bold text-white">Create Your Organization</h1>
              <p className="text-gray-400 mt-1">Set up your team workspace to get started</p>
            </div>

            <form onSubmit={handleCreateOrg} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Organization Name
                </label>
                <input
                  type="text"
                  value={newOrgName}
                  onChange={(e) => handleOrgNameChange(e.target.value)}
                  placeholder="Acme Government Solutions"
                  required
                  className="w-full px-4 py-3 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  URL Slug
                </label>
                <input
                  type="text"
                  value={newOrgSlug}
                  onChange={(e) => setNewOrgSlug(e.target.value.toLowerCase().replace(/[^a-z0-9-]/g, ''))}
                  placeholder="acme-gov"
                  required
                  className="w-full px-4 py-3 bg-white/[0.05] border border-white/[0.08] rounded-lg text-white placeholder-gray-500 focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                />
                <p className="text-xs text-gray-500 mt-1">
                  This will be used in URLs and cannot be changed later
                </p>
              </div>

              {createError && (
                <div className="flex items-center gap-2 text-red-400 text-sm bg-red-500/10 border border-red-500/20 p-3 rounded-lg">
                  <AlertCircle className="w-4 h-4 flex-shrink-0" />
                  {createError}
                </div>
              )}

              <button
                type="submit"
                disabled={creating || !newOrgName || !newOrgSlug}
                className="w-full bg-gradient-to-r from-emerald-500 to-blue-500 text-white py-3 px-4 rounded-lg hover:from-emerald-600 hover:to-blue-600 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
              >
                {creating ? 'Creating...' : 'Create Organization'}
              </button>
            </form>
          </div>
        </div>
      </div>
    );
  }

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('currentOrgId');
    localStorage.removeItem('currentOrgName');
    router.push('/login');
  };

  return (
    <div className="min-h-screen bg-[#0a0a0f] flex">
      {/* Sidebar */}
      <div className="w-64 bg-white/[0.03] backdrop-blur-sm border-r border-white/[0.08] flex flex-col">
        {/* Logo */}
        <div className="p-6 border-b border-white/[0.08]">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-emerald-500 to-blue-500 rounded-lg flex items-center justify-center">
              <FileText className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-white font-bold text-lg">GovProposalAI</h1>
              <p className="text-gray-500 text-xs">Proposal Management</p>
            </div>
          </div>
        </div>

        {/* Main Navigation */}
        <nav className="flex-1 p-4 space-y-1">
          {navigation.map((item) => {
            const isActive = pathname?.startsWith(item.href);
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-gradient-to-r from-emerald-500/20 to-blue-500/20 text-white border border-white/[0.08]'
                    : 'text-gray-400 hover:bg-white/[0.05] hover:text-white'
                }`}
              >
                <item.icon className={`w-5 h-5 ${isActive ? 'text-emerald-400' : ''}`} />
                {item.name}
              </Link>
            );
          })}
        </nav>

        {/* Bottom Navigation */}
        <div className="p-4 border-t border-white/[0.08] space-y-1">
          {bottomNavigation.map((item) => {
            const isActive = pathname?.startsWith(item.href);
            return (
              <Link
                key={item.name}
                href={item.href}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-white/[0.05] text-white'
                    : 'text-gray-400 hover:bg-white/[0.05] hover:text-white'
                }`}
              >
                <item.icon className="w-5 h-5" />
                {item.name}
              </Link>
            );
          })}
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium text-gray-400 hover:bg-white/[0.05] hover:text-white transition-colors"
          >
            <LogOut className="w-5 h-5" />
            Logout
          </button>
        </div>

        {/* Organization Info */}
        {orgName && (
          <div className="p-4 border-t border-white/[0.08]">
            <div className="flex items-center gap-3 px-4 py-3 bg-white/[0.05] rounded-lg">
              <div className="w-8 h-8 bg-gradient-to-br from-emerald-500 to-blue-500 rounded-full flex items-center justify-center">
                <span className="text-white text-sm font-medium">
                  {orgName.charAt(0).toUpperCase()}
                </span>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-white text-sm font-medium truncate">{orgName}</p>
                <p className="text-gray-500 text-xs">Organization</p>
              </div>
              <ChevronDown className="w-4 h-4 text-gray-500" />
            </div>
          </div>
        )}
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        {/* Top Bar */}
        <div className="flex items-center justify-end px-8 py-4 border-b border-white/[0.05]">
          <NotificationBell />
        </div>
        <main className="p-8">{children}</main>
      </div>
    </div>
  );
}
