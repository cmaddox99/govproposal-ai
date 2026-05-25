'use client';

import { useEffect, useState } from 'react';

export type Market = 'federal' | 'sled';

const STORAGE_KEY = 'currentMarket';
const EVENT_NAME = 'currentMarketChanged';

function read(): Market {
  if (typeof window === 'undefined') return 'federal';
  const raw = localStorage.getItem(STORAGE_KEY);
  return raw === 'sled' ? 'sled' : 'federal';
}

/**
 * Hook for the global Federal / SLED view switcher.
 *
 * Reads from localStorage on mount, listens for cross-component updates via a
 * window-level custom event so flipping the switch in the header re-renders
 * every page that depends on it without prop-drilling.
 */
export function useMarket(): [Market, (m: Market) => void] {
  const [market, setMarketState] = useState<Market>(() => read());

  useEffect(() => {
    const handler = () => setMarketState(read());
    window.addEventListener(EVENT_NAME, handler);
    window.addEventListener('storage', handler);
    return () => {
      window.removeEventListener(EVENT_NAME, handler);
      window.removeEventListener('storage', handler);
    };
  }, []);

  const setMarket = (m: Market) => {
    if (typeof window === 'undefined') return;
    localStorage.setItem(STORAGE_KEY, m);
    setMarketState(m);
    window.dispatchEvent(new Event(EVENT_NAME));
  };

  return [market, setMarket];
}
