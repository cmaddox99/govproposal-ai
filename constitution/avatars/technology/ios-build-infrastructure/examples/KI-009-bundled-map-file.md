# KI-009 — Bundled LocusLabs Map Archive Not Copied

## Symptom
```
error: The file "ios-A1B4XSN6HDHIR2-2024-04-14T21-48-28.tar.gz" couldn't be opened
because there is no such file. (in target 'AmericanAirlines' from project 'AmericanAirlines')
```

## Root Cause
The maps feature (LocusLabs) ships a bundled offline map archive inside the `maps-ios` Carthage checkout. The project references it at:
```
Carthage/Build/Resources/iOS/ios-A1B4XSN6HDHIR2-2024-04-14T21-48-28.tar.gz
```
Source location (after `carthage bootstrap`):
```
Carthage/Checkouts/maps-ios/ios/AmericanMaps/ThirdParty/LocusLabs/BundledMapFiles/
  ios-A1B4XSN6HDHIR2-2024-04-14T21-48-28.tar.gz
```

## Fix
```bash
RESOURCES="Carthage/Build/Resources/iOS"
mkdir -p "$RESOURCES"
cp Carthage/Checkouts/maps-ios/ios/AmericanMaps/ThirdParty/LocusLabs/BundledMapFiles/*.tar.gz \
   "$RESOURCES/"
```
Note: filename encodes device model + timestamp — do not hardcode. Use glob `*.tar.gz`.
