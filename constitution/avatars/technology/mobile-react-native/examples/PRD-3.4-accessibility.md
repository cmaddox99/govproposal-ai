---
law_id: PRD-3.4
avatar: mobile-react-native
---

# PRD-3.4: Accessibility Examples for React Native

## COMPLIANT: Properly Labeled Form with Error Handling

```typescript
// LoginForm.tsx
import React, { useState, useRef } from 'react';
import {
  View,
  Text,
  TextInput,
  Pressable,
  StyleSheet,
  AccessibilityInfo
} from 'react-native';

interface FormData {
  email: string;
  password: string;
}

interface FormErrors {
  email?: string;
  password?: string;
}

export function LoginForm({ onSubmit }: { onSubmit: (data: FormData) => void }) {
  const [formData, setFormData] = useState<FormData>({ email: '', password: '' });
  const [errors, setErrors] = useState<FormErrors>({});
  const [submitted, setSubmitted] = useState(false);

  const passwordRef = useRef<TextInput>(null);

  const validate = (): boolean => {
    const newErrors: FormErrors = {};

    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Invalid email format';
    }

    if (!formData.password.trim()) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    }

    setErrors(newErrors);

    // Announce errors to screen readers
    const errorMessages = Object.values(newErrors).join('. ');
    if (errorMessages) {
      AccessibilityInfo.announceForAccessibility(`Form has errors: ${errorMessages}`);
    }

    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = () => {
    if (validate()) {
      onSubmit(formData);
      setSubmitted(true);
      AccessibilityInfo.announceForAccessibility('Login successful');
    }
  };

  if (submitted) {
    return (
      <View
        style={styles.container}
        accessibilityRole="alert"
        accessibilityLiveRegion="polite"
      >
        <Text style={styles.success}>Login successful!</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.inputGroup}>
        <Text
          nativeID="email-label"
          style={styles.label}
        >
          Email <Text style={styles.required}>*</Text>
        </Text>
        <TextInput
          style={[styles.input, errors.email && styles.inputError]}
          value={formData.email}
          onChangeText={(text) => setFormData({ ...formData, email: text })}
          accessibilityLabel="Email"
          accessibilityLabelledBy="email-label"
          accessibilityHint="Enter your email address"
          accessibilityState={{ error: !!errors.email }}
          keyboardType="email-address"
          autoCapitalize="none"
          autoComplete="email"
          textContentType="emailAddress"
          returnKeyType="next"
          onSubmitEditing={() => passwordRef.current?.focus()}
          blurOnSubmit={false}
        />
        {errors.email && (
          <Text
            style={styles.error}
            accessibilityRole="alert"
            accessibilityLiveRegion="assertive"
          >
            {errors.email}
          </Text>
        )}
      </View>

      <View style={styles.inputGroup}>
        <Text
          nativeID="password-label"
          style={styles.label}
        >
          Password <Text style={styles.required}>*</Text>
        </Text>
        <TextInput
          ref={passwordRef}
          style={[styles.input, errors.password && styles.inputError]}
          value={formData.password}
          onChangeText={(text) => setFormData({ ...formData, password: text })}
          accessibilityLabel="Password"
          accessibilityLabelledBy="password-label"
          accessibilityHint="Enter your password, minimum 8 characters"
          accessibilityState={{ error: !!errors.password }}
          secureTextEntry
          autoComplete="password"
          textContentType="password"
          returnKeyType="done"
          onSubmitEditing={handleSubmit}
        />
        {errors.password && (
          <Text
            style={styles.error}
            accessibilityRole="alert"
            accessibilityLiveRegion="assertive"
          >
            {errors.password}
          </Text>
        )}
      </View>

      <Pressable
        style={styles.button}
        onPress={handleSubmit}
        accessibilityRole="button"
        accessibilityLabel="Sign in"
        accessibilityHint="Double tap to submit the login form"
      >
        <Text style={styles.buttonText}>Sign In</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 16 },
  inputGroup: { marginBottom: 16 },
  label: { fontSize: 16, fontWeight: '600', marginBottom: 4 },
  required: { color: '#d32f2f' },
  input: { borderWidth: 1, borderColor: '#ccc', borderRadius: 8, padding: 12, fontSize: 16 },
  inputError: { borderColor: '#d32f2f' },
  error: { color: '#d32f2f', fontSize: 14, marginTop: 4 },
  button: { backgroundColor: '#1976d2', padding: 16, borderRadius: 8, alignItems: 'center' },
  buttonText: { color: '#fff', fontSize: 18, fontWeight: '600' },
  success: { fontSize: 18, color: '#2e7d32', textAlign: 'center' }
});
```

**Why compliant:** Uses accessibilityLabel and accessibilityLabelledBy for proper labeling. Includes accessibilityHint for additional context. Uses accessibilityState to communicate error state. Announces errors using AccessibilityInfo.announceForAccessibility(). Includes autoComplete and textContentType for autofill. Manages keyboard flow with returnKeyType and focus handling.

---

## COMPLIANT: Accessible Touchable with Proper Roles

```typescript
// ActionButton.tsx
import React from 'react';
import { Pressable, Text, StyleSheet, ActivityIndicator } from 'react-native';

interface ActionButtonProps {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary' | 'danger';
  loading?: boolean;
  disabled?: boolean;
  icon?: React.ReactNode;
}

export function ActionButton({
  title,
  onPress,
  variant = 'primary',
  loading = false,
  disabled = false,
  icon
}: ActionButtonProps) {
  const isDisabled = disabled || loading;

  return (
    <Pressable
      style={({ pressed }) => [
        styles.button,
        styles[variant],
        pressed && styles.pressed,
        isDisabled && styles.disabled
      ]}
      onPress={onPress}
      disabled={isDisabled}
      accessibilityRole="button"
      accessibilityLabel={title}
      accessibilityState={{
        disabled: isDisabled,
        busy: loading
      }}
      accessibilityHint={
        loading
          ? 'Action in progress, please wait'
          : disabled
            ? 'Button is currently disabled'
            : `Double tap to ${title.toLowerCase()}`
      }
    >
      {loading ? (
        <ActivityIndicator
          color="#fff"
          accessibilityLabel="Loading"
        />
      ) : (
        <>
          {icon}
          <Text style={[styles.text, icon && styles.textWithIcon]}>
            {title}
          </Text>
        </>
      )}
    </Pressable>
  );
}

const styles = StyleSheet.create({
  button: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
    borderRadius: 8,
    minHeight: 48, // Minimum touch target size
    minWidth: 48
  },
  primary: { backgroundColor: '#1976d2' },
  secondary: { backgroundColor: '#757575' },
  danger: { backgroundColor: '#d32f2f' },
  pressed: { opacity: 0.8 },
  disabled: { opacity: 0.5 },
  text: { color: '#fff', fontSize: 16, fontWeight: '600' },
  textWithIcon: { marginLeft: 8 }
});
```

**Why compliant:** Uses accessibilityRole="button" for proper semantics. Includes accessibilityState for disabled and busy states. Provides contextual accessibilityHint. Minimum touch target size of 48x48 points. Loading state is communicated via both visual indicator and accessibility properties.

---

## COMPLIANT: Accessible List with Screen Reader Support

```typescript
// ProductList.tsx
import React from 'react';
import {
  FlatList,
  View,
  Text,
  Image,
  Pressable,
  StyleSheet,
  AccessibilityInfo
} from 'react-native';

interface Product {
  id: string;
  name: string;
  price: number;
  imageUrl: string;
  inStock: boolean;
}

interface ProductListProps {
  products: Product[];
  onProductSelect: (product: Product) => void;
}

export function ProductList({ products, onProductSelect }: ProductListProps) {
  const renderItem = ({ item, index }: { item: Product; index: number }) => (
    <Pressable
      style={styles.productCard}
      onPress={() => onProductSelect(item)}
      accessibilityRole="button"
      accessibilityLabel={`${item.name}, ${formatPrice(item.price)}${
        item.inStock ? '' : ', out of stock'
      }`}
      accessibilityHint="Double tap to view product details"
      accessibilityActions={[
        { name: 'activate', label: 'View details' },
        { name: 'magicTap', label: 'Add to cart' }
      ]}
      onAccessibilityAction={(event) => {
        switch (event.nativeEvent.actionName) {
          case 'activate':
            onProductSelect(item);
            break;
          case 'magicTap':
            // Add to cart action
            AccessibilityInfo.announceForAccessibility(
              `${item.name} added to cart`
            );
            break;
        }
      }}
    >
      <Image
        source={{ uri: item.imageUrl }}
        style={styles.productImage}
        accessibilityIgnoresInvertColors
        accessible={false} // Image is decorative, info is in parent label
      />
      <View style={styles.productInfo}>
        <Text
          style={styles.productName}
          numberOfLines={2}
          accessible={false} // Part of parent's label
        >
          {item.name}
        </Text>
        <Text
          style={styles.productPrice}
          accessible={false}
        >
          {formatPrice(item.price)}
        </Text>
        {!item.inStock && (
          <Text
            style={styles.outOfStock}
            accessible={false}
          >
            Out of Stock
          </Text>
        )}
      </View>
    </Pressable>
  );

  return (
    <FlatList
      data={products}
      renderItem={renderItem}
      keyExtractor={(item) => item.id}
      accessibilityRole="list"
      accessibilityLabel={`Product list with ${products.length} items`}
      ListEmptyComponent={
        <View
          style={styles.empty}
          accessibilityRole="alert"
          accessibilityLiveRegion="polite"
        >
          <Text style={styles.emptyText}>No products found</Text>
        </View>
      }
    />
  );
}

function formatPrice(price: number): string {
  return `$${price.toFixed(2)}`;
}

const styles = StyleSheet.create({
  productCard: {
    flexDirection: 'row',
    padding: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
    minHeight: 88 // Adequate touch target
  },
  productImage: { width: 64, height: 64, borderRadius: 8 },
  productInfo: { flex: 1, marginLeft: 12, justifyContent: 'center' },
  productName: { fontSize: 16, fontWeight: '600' },
  productPrice: { fontSize: 14, color: '#1976d2', marginTop: 4 },
  outOfStock: { fontSize: 12, color: '#d32f2f', marginTop: 2 },
  empty: { padding: 32, alignItems: 'center' },
  emptyText: { fontSize: 16, color: '#666' }
});
```

**Why compliant:** List has accessibilityRole="list" with item count. Each item has comprehensive accessibilityLabel including price and availability. Uses accessibilityActions for custom gestures. Child elements marked as non-accessible to prevent redundant announcements. Empty state uses accessibilityLiveRegion for announcements.

---

## COMPLIANT: Accessible Modal with Focus Management

```typescript
// Modal.tsx
import React, { useEffect, useRef } from 'react';
import {
  Modal as RNModal,
  View,
  Text,
  Pressable,
  StyleSheet,
  AccessibilityInfo,
  findNodeHandle
} from 'react-native';

interface ModalProps {
  visible: boolean;
  title: string;
  onClose: () => void;
  children: React.ReactNode;
}

export function Modal({ visible, title, onClose, children }: ModalProps) {
  const closeButtonRef = useRef<View>(null);

  useEffect(() => {
    if (visible && closeButtonRef.current) {
      // Set accessibility focus to the close button when modal opens
      const reactTag = findNodeHandle(closeButtonRef.current);
      if (reactTag) {
        AccessibilityInfo.setAccessibilityFocus(reactTag);
      }

      // Announce modal opened
      AccessibilityInfo.announceForAccessibility(`${title} dialog opened`);
    }
  }, [visible, title]);

  const handleClose = () => {
    AccessibilityInfo.announceForAccessibility('Dialog closed');
    onClose();
  };

  return (
    <RNModal
      visible={visible}
      transparent
      animationType="fade"
      onRequestClose={handleClose}
      accessibilityViewIsModal={true}
    >
      <View
        style={styles.overlay}
        accessibilityRole="none"
        importantForAccessibility="no"
      >
        <View
          style={styles.content}
          accessibilityRole="alert"
          accessibilityLabel={`${title} dialog`}
          accessibilityViewIsModal={true}
        >
          <View style={styles.header}>
            <Text
              style={styles.title}
              accessibilityRole="header"
            >
              {title}
            </Text>
            <Pressable
              ref={closeButtonRef}
              onPress={handleClose}
              style={styles.closeButton}
              accessibilityRole="button"
              accessibilityLabel="Close dialog"
              accessibilityHint="Double tap to close this dialog"
              hitSlop={{ top: 12, bottom: 12, left: 12, right: 12 }}
            >
              <Text style={styles.closeIcon} accessibilityElementsHidden>
                ✕
              </Text>
            </Pressable>
          </View>

          <View style={styles.body}>
            {children}
          </View>
        </View>
      </View>
    </RNModal>
  );
}

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center'
  },
  content: {
    backgroundColor: '#fff',
    borderRadius: 12,
    width: '90%',
    maxWidth: 400,
    maxHeight: '80%'
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#eee'
  },
  title: { fontSize: 20, fontWeight: '600' },
  closeButton: {
    width: 44,
    height: 44,
    alignItems: 'center',
    justifyContent: 'center'
  },
  closeIcon: { fontSize: 24, color: '#666' },
  body: { padding: 16 }
});
```

**Why compliant:** Uses accessibilityViewIsModal to trap focus within modal. Sets accessibility focus to close button when opened. Announces modal open and close to screen readers. Close button has minimum 44x44 touch target with hitSlop. Title has accessibilityRole="header" for proper navigation.

---

## VIOLATION: Missing Accessibility Labels

```typescript
// BAD: IconButton.tsx - No accessibility information
import React from 'react';
import { TouchableOpacity, Image, StyleSheet } from 'react-native';

export function IconButton({ iconSource, onPress }) {
  return (
    // No accessibilityLabel or accessibilityRole
    <TouchableOpacity
      onPress={onPress}
      style={styles.button}
    >
      {/* Image without accessible description */}
      <Image source={iconSource} style={styles.icon} />
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  button: { padding: 8 },
  icon: { width: 24, height: 24 }
});
```

**Why violates PRD-3.4:** TouchableOpacity has no accessibilityLabel or accessibilityRole. Screen readers will announce nothing meaningful. Image has no accessible description. Users cannot understand what the button does.

---

## VIOLATION: Inaccessible Custom Toggle

```typescript
// BAD: Toggle.tsx - Poor accessibility implementation
import React, { useState } from 'react';
import { View, Text, TouchableOpacity, Animated, StyleSheet } from 'react-native';

export function Toggle({ label, onChange }) {
  const [isOn, setIsOn] = useState(false);
  const animation = useState(new Animated.Value(0))[0];

  const toggle = () => {
    const newValue = !isOn;
    setIsOn(newValue);
    onChange?.(newValue);
  };

  return (
    <View style={styles.container}>
      <Text>{label}</Text>
      {/* Missing accessibility role and state */}
      <TouchableOpacity onPress={toggle} style={styles.track}>
        {/* Visual-only state indication */}
        <Animated.View
          style={[
            styles.thumb,
            { transform: [{ translateX: animation }] }
          ]}
        />
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flexDirection: 'row', alignItems: 'center' },
  track: {
    width: 50,
    height: 30,
    backgroundColor: '#ccc',
    borderRadius: 15
  },
  thumb: {
    width: 26,
    height: 26,
    backgroundColor: '#fff',
    borderRadius: 13
  }
});
```

**Why violates PRD-3.4:** No accessibilityRole="switch" to identify the control type. No accessibilityState to communicate on/off state. Label is not associated with the toggle. Screen readers cannot understand or operate this control properly.

---

## VIOLATION: Missing State Announcements

```typescript
// BAD: SearchResults.tsx - No accessibility announcements
import React from 'react';
import { View, Text, FlatList, ActivityIndicator, StyleSheet } from 'react-native';

export function SearchResults({ query, results, loading }) {
  if (loading) {
    // Loading state not announced
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  if (results.length === 0) {
    // Empty state not announced
    return (
      <View style={styles.center}>
        <Text>No results for "{query}"</Text>
      </View>
    );
  }

  // Results change not announced
  return (
    <FlatList
      data={results}
      renderItem={({ item }) => (
        <View style={styles.item}>
          <Text>{item.title}</Text>
        </View>
      )}
      keyExtractor={(item) => item.id}
    />
  );
}

const styles = StyleSheet.create({
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  item: { padding: 16, borderBottomWidth: 1, borderBottomColor: '#eee' }
});
```

**Why violates PRD-3.4:** Loading state shows only a visual spinner with no accessible label. Empty state is not announced to screen readers. When results change, users are not informed. Should use accessibilityLiveRegion and AccessibilityInfo.announceForAccessibility().

---

## VIOLATION: Inadequate Touch Targets

```typescript
// BAD: SmallButtons.tsx - Touch targets too small
import React from 'react';
import { View, TouchableOpacity, Text, StyleSheet } from 'react-native';

export function SmallButtons({ onEdit, onDelete, onShare }) {
  return (
    <View style={styles.container}>
      {/* Touch targets are only 24x24, below minimum */}
      <TouchableOpacity onPress={onEdit} style={styles.smallButton}>
        <Text style={styles.icon}>✏️</Text>
      </TouchableOpacity>

      <TouchableOpacity onPress={onDelete} style={styles.smallButton}>
        <Text style={styles.icon}>🗑️</Text>
      </TouchableOpacity>

      <TouchableOpacity onPress={onShare} style={styles.smallButton}>
        <Text style={styles.icon}>📤</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flexDirection: 'row', gap: 4 },
  smallButton: {
    width: 24,  // Too small! Minimum should be 44
    height: 24, // Too small!
    alignItems: 'center',
    justifyContent: 'center'
  },
  icon: { fontSize: 14 }
});
```

**Why violates PRD-3.4:** Touch targets are 24x24 points, well below the minimum 44x44 required for accessibility. Buttons are too close together without adequate spacing. Users with motor impairments will have difficulty tapping the correct button. Should use hitSlop or increase button sizes.
