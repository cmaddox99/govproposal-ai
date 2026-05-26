'use client';

import { Building2, Landmark } from 'lucide-react';

import { useMarket, type Market } from '@/lib/useMarket';

const OPTIONS: { value: Market; label: string; sub: string; Icon: typeof Landmark }[] = [
  { value: 'federal', label: 'Federal', sub: 'SAM.gov + eBuy', Icon: Landmark },
  { value: 'sled', label: 'SLED', sub: 'txsmartbuy.gov', Icon: Building2 },
];

export default function MarketSwitcher() {
  const [market, setMarket] = useMarket();
  return (
    <div className="inline-flex items-center bg-white/[0.04] border border-white/[0.08] rounded-lg p-1 gap-1">
      {OPTIONS.map(({ value, label, sub, Icon }) => {
        const active = market === value;
        return (
          <button
            key={value}
            type="button"
            onClick={() => setMarket(value)}
            title={sub}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-colors ${
              active
                ? 'bg-gradient-to-r from-emerald-500 to-blue-500 text-white shadow'
                : 'text-gray-400 hover:text-white hover:bg-white/[0.04]'
            }`}
          >
            <Icon className="w-3.5 h-3.5" />
            {label}
          </button>
        );
      })}
    </div>
  );
}
