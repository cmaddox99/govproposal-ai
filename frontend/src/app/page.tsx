'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { FileText } from 'lucide-react';

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }
    router.push('/dashboard');
  }, [router]);

  return (
    <div className="min-h-screen bg-[#0a0a0f] flex items-center justify-center">
      <div className="text-center">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-emerald-500/20 to-blue-500/20 rounded-full mb-4">
          <FileText className="w-8 h-8 text-emerald-400" />
        </div>
        <h1 className="text-2xl font-bold text-white">GovProposalAI</h1>
        <p className="text-gray-500 mt-2">Loading...</p>
      </div>
    </div>
  );
}
