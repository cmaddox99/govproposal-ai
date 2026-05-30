---
laws: [ENG-6.1, ENG-6.4, ENG-6.7]
avatar: [mobile-react-native]
title: Security Laws — Mobile React Native
---

# Security Laws: ENG-6.1, ENG-6.4, ENG-6.7 — Mobile React Native

## ENG-6.1: Security by Design

Use `react-native-keychain` for any credential storage. Disable cleartext traffic. Block screenshots on payment screens.

```typescript
import * as Keychain from 'react-native-keychain';

// ✅ Store auth token in secure Keychain / Keystore
export async function saveAuthToken(token: string): Promise<void> {
  await Keychain.setGenericPassword('aa_session', token, {
    accessible: Keychain.ACCESSIBLE.WHEN_UNLOCKED_THIS_DEVICE_ONLY,
    securityLevel: Keychain.SECURITY_LEVEL.SECURE_HARDWARE,
  });
}

export async function getAuthToken(): Promise<string | null> {
  const creds = await Keychain.getGenericPassword();
  return creds ? creds.password : null;
}

// ❌ NEVER: AsyncStorage.setItem('token', jwt)
```

Android network security config (certificate pinning):

```xml
<!-- android/app/src/main/res/xml/network_security_config.xml -->
<network-security-config>
  <domain-config cleartextTrafficPermitted="false">
    <domain includeSubdomains="true">api.aa.com</domain>
    <pin-set>
      <pin digest="SHA-256">AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=</pin>
    </pin-set>
  </domain-config>
</network-security-config>
```

Disable screenshots on payment screen (Android):

```typescript
import { NativeModules, Platform } from 'react-native';

// PaymentScreen.tsx
useEffect(() => {
  if (Platform.OS === 'android') {
    NativeModules.ScreenCapturePreventer?.enable();
  }
  return () => NativeModules.ScreenCapturePreventer?.disable();
}, []);
```

Validate all form inputs client-side before API call:

```typescript
function validateBookingInput(pnr: string, seatCode: string): void {
  if (!/^[A-Z]{6}$/.test(pnr)) throw new Error('Invalid PNR format');
  if (!/^[0-9]{1,3}[A-F]$/.test(seatCode)) throw new Error('Invalid seat code');
}
```

## ENG-6.4: Data Protection

Never persist PII or tokens via `AsyncStorage`. Encrypt any offline data. Strip sensitive values from error logs.

```typescript
// redux/bookingSlice.ts
interface BookingState {
  flightId: string;
  seatCode: string;
  correlationId: string;
  // ✅ No passenger name, email, card number in Redux state
  // ❌ passengerName: string  — would be persisted by redux-persist
}

// Error boundary — strip PII before sending to Sentry
import * as Sentry from '@sentry/react-native';

Sentry.init({
  beforeSend(event) {
    // Remove any breadcrumbs or extras containing card/PII data
    event.breadcrumbs?.values?.forEach(b => {
      if (b.data?.cardNumber) delete b.data.cardNumber;
      if (b.data?.email)      delete b.data.email;
    });
    return event;
  },
});
```

Encrypted persistence for offline itinerary data:

```typescript
import EncryptedStorage from 'react-native-encrypted-storage';

// ✅ Use encrypted storage for any sensitive persisted data
await EncryptedStorage.setItem('offline_itinerary', JSON.stringify(safeItinerary));

// ❌ NEVER persist payment data, even encrypted
// await EncryptedStorage.setItem('card_details', JSON.stringify(card))
```

## ENG-6.7: Audit Trail

Attach correlation ID (from `X-Correlation-ID` response header) to every audit event. Send booking/payment events to backend.

```typescript
// useCorrelationId.ts
import { useRef } from 'react';

export function useApiClient() {
  const correlationIdRef = useRef<string>('');

  const post = async (url: string, body: unknown) => {
    const res = await fetch(`https://api.aa.com${url}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    correlationIdRef.current = res.headers.get('X-Correlation-ID') ?? '';
    return res.json();
  };
  return { post, getCorrelationId: () => correlationIdRef.current };
}

// auditLogger.ts
interface AuditEvent {
  event: string;
  correlationId: string;
  timestamp: string;
  screenName: string;
  // ❌ No pnr, passengerName, cardNumber, email
}

export async function logAuditEvent(event: string, screenName: string,
                                    correlationId: string): Promise<void> {
  const entry: AuditEvent = {
    event, correlationId, screenName,
    timestamp: new Date().toISOString(),
  };
  await fetch('https://api.aa.com/audit/mobile-events', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(entry),
  });
  // ❌ NEVER: console.log(JSON.stringify(apiResponse))
}
```

## Anti-Patterns

1. **`AsyncStorage` for JWT tokens** — AsyncStorage is unencrypted plaintext on the device filesystem; use `react-native-keychain` instead.
2. **`console.log(apiResponse)` including PII** — booking and loyalty API responses contain passenger names, PNR, and itinerary details; logs are readable via Metro and device logs.
3. **No certificate pinning in production** — React Native apps running over airport or hotel Wi-Fi are vulnerable to MITM without pinning; configure `network_security_config.xml` and iOS `Info.plist` pinning.
4. **PII in Sentry/Crashlytics events** — a crash in the payment flow may capture Redux state containing card data; always configure `beforeSend` to strip sensitive fields.
5. **Persisting Redux state with payment card data** — `redux-persist` writes the entire store to AsyncStorage; never include card numbers, CVV, or raw PNR in persisted slices.
