---
law_id: ENG-3.2
avatar: mobile-react-native
---

# ENG-3.2: Immutability Law Examples for Mobile React Native

## COMPLIANT: Redux Reducer with Immutable State Updates

### Readonly State Types

```typescript
type Passenger = {
  readonly id: string;
  readonly firstName: string;
  readonly lastName: string;
  readonly seatAssignment: string | null;
};

type BoardingPassState = {
  readonly passengers: readonly Passenger[];
  readonly flightNumber: string;
  readonly gate: string | null;
  readonly status: "loading" | "ready" | "boarding" | "departed";
  readonly error: string | null;
};

const initialState: BoardingPassState = {
  passengers: [],
  flightNumber: "",
  gate: null,
  status: "loading",
  error: null,
};
```

### Redux Reducer with Spread Operator

```typescript
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

const boardingPassSlice = createSlice({
  name: "boardingPass",
  initialState,
  reducers: {
    // Immutable update: spread existing state, replace passengers array
    setPassengers(state, action: PayloadAction<readonly Passenger[]>) {
      // Redux Toolkit uses Immer internally -- writes look mutable but produce
      // immutable updates under the hood
      state.passengers = action.payload as Passenger[];
      state.status = "ready";
      state.error = null;
    },

    // Immutable update: map array to produce new array with one item changed
    assignSeat(
      state,
      action: PayloadAction<{ passengerId: string; seatId: string }>
    ) {
      const passenger = state.passengers.find(
        (p) => p.id === action.payload.passengerId
      );
      if (passenger) {
        passenger.seatAssignment = action.payload.seatId;
      }
    },

    updateGate(state, action: PayloadAction<string>) {
      state.gate = action.payload;
    },

    setError(state, action: PayloadAction<string>) {
      state.error = action.payload;
      state.status = "loading";
    },
  },
});

export const { setPassengers, assignSeat, updateGate, setError } =
  boardingPassSlice.actions;
export default boardingPassSlice.reducer;
```

### Immutable State in React Native Components

```tsx
import React from "react";
import { View, Text, FlatList, TouchableOpacity } from "react-native";
import { useSelector, useDispatch } from "react-redux";

type RootState = {
  readonly boardingPass: BoardingPassState;
};

function BoardingPassScreen() {
  // useSelector returns immutable state slices
  const passengers = useSelector(
    (state: RootState) => state.boardingPass.passengers
  );
  const status = useSelector(
    (state: RootState) => state.boardingPass.status
  );
  const dispatch = useDispatch();

  // Immutable update through dispatch -- never mutate state directly
  const handleSeatSelect = (passengerId: string, seatId: string) => {
    dispatch(assignSeat({ passengerId, seatId }));
  };

  return (
    <View>
      <Text>Status: {status}</Text>
      <FlatList
        data={passengers}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <PassengerRow
            passenger={item}
            onSeatSelect={(seatId) => handleSeatSelect(item.id, seatId)}
          />
        )}
      />
    </View>
  );
}

type PassengerRowProps = {
  readonly passenger: Passenger;
  readonly onSeatSelect: (seatId: string) => void;
};

function PassengerRow({ passenger, onSeatSelect }: PassengerRowProps) {
  return (
    <View>
      <Text>{passenger.firstName} {passenger.lastName}</Text>
      <Text>Seat: {passenger.seatAssignment ?? "Not assigned"}</Text>
      <TouchableOpacity onPress={() => onSeatSelect("12A")}>
        <Text>Assign Seat</Text>
      </TouchableOpacity>
    </View>
  );
}
```

**Why compliant:** All state types use `readonly` to prevent compile-time mutations. Redux Toolkit with Immer ensures state updates are always immutable, even though the reducer syntax looks mutable. Components receive immutable state via `useSelector` and dispatch actions to request changes rather than mutating state directly. Props are marked `readonly` to prevent accidental mutation.

---

## VIOLATION: Direct State Mutation

```tsx
import React, { useState } from "react";
import { View, Text, TouchableOpacity } from "react-native";

// BAD: Mutable state types
type AppState = {
  passengers: Passenger[];  // VIOLATION: No readonly
  gate: string | null;
};

// BAD: Global mutable state
let globalState: AppState = {
  passengers: [],
  gate: null,
};

function BoardingPassScreen() {
  const [passengers, setPassengers] = useState<Passenger[]>([]);

  const addPassenger = (passenger: Passenger) => {
    // VIOLATION: Mutating existing state array
    passengers.push(passenger);
    setPassengers(passengers); // Same reference -- React may not re-render!
  };

  const assignSeat = (passengerId: string, seatId: string) => {
    // VIOLATION: Mutating object inside state array
    const passenger = passengers.find((p) => p.id === passengerId);
    if (passenger) {
      passenger.seatAssignment = seatId; // Direct mutation of state object
      setPassengers([...passengers]); // Spread does not fix deep mutation
    }
  };

  const updateGate = (gate: string) => {
    // VIOLATION: Mutating global state directly
    globalState.gate = gate;
  };

  // VIOLATION: Sorting mutates the array in place
  const sortPassengers = () => {
    passengers.sort((a, b) => a.lastName.localeCompare(b.lastName));
    setPassengers(passengers); // Same reference!
  };

  return (
    <View>
      {passengers.map((p) => (
        <View key={p.id}>
          <Text>{p.firstName} {p.lastName}</Text>
          {/* VIOLATION: Mutating prop directly */}
          <TouchableOpacity onPress={() => { p.seatAssignment = "1A"; }}>
            <Text>Quick Assign</Text>
          </TouchableOpacity>
        </View>
      ))}
    </View>
  );
}
```

**Why violates ENG-3.2:** `passengers.push()` and `passengers.sort()` mutate the array in place. Since React compares references to detect changes, setting the same reference via `setPassengers(passengers)` may not trigger a re-render. Direct mutation of objects inside state (`passenger.seatAssignment = seatId`) causes stale UI and breaks memoized selectors. Global mutable state (`globalState.gate = gate`) is shared across the app without any change tracking, making bugs nearly impossible to trace.

---

## Quick Reference

| Pattern | Mutable (Avoid) | Immutable (Prefer) |
|---------|-----------------|---------------------|
| State types | `{ passengers: Passenger[] }` | `{ readonly passengers: readonly Passenger[] }` |
| Add to array | `arr.push(item)` | `[...arr, item]` |
| Update in array | `arr[i].prop = val` | `arr.map(x => x.id === id ? { ...x, prop: val } : x)` |
| Sort array | `arr.sort()` | `[...arr].sort()` |
| Redux state | hand-written spread reducers | Redux Toolkit `createSlice` (Immer) |
| Global state | mutable module-level variable | Redux store or React Context with `useReducer` |
