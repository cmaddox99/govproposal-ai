import { useEffect, useState } from 'react';

/**
 * Hook to reliably get the current organization ID from localStorage.
 * Polls briefly to handle the race condition where the dashboard layout
 * hasn't finished setting currentOrgId yet when child pages mount.
 */
export function useOrgId(): string | null {
  const [orgId, setOrgId] = useState<string | null>(() => {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem('currentOrgId');
  });

  useEffect(() => {
    if (orgId) return;

    // Poll a few times in case layout is still initializing
    let attempts = 0;
    const maxAttempts = 10;
    const interval = setInterval(() => {
      const id = localStorage.getItem('currentOrgId');
      if (id) {
        setOrgId(id);
        clearInterval(interval);
      } else if (++attempts >= maxAttempts) {
        clearInterval(interval);
      }
    }, 100);

    return () => clearInterval(interval);
  }, [orgId]);

  return orgId;
}
