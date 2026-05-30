# KI-008 — Resource Bundles Not Copied from xcframeworks

## Symptom
```
error: The file "AmericanUserMessaging.bundle" couldn't be opened because there is no such file.
error: The file "AmericanUpgrades.bundle" couldn't be opened because there is no such file.
(in target 'AmericanAirlines' from project 'AmericanAirlines')
```

## Root Cause
Each AA xcframework embeds a `.bundle` resource directory inside its simulator slice:
```
Carthage/Build/AmericanUpgrades.xcframework/
  ios-arm64_x86_64-simulator/AmericanUpgrades.framework/AmericanUpgrades.bundle
```
The `AmericanAirlines` project references these bundles flat at:
```
Carthage/Build/Resources/iOS/<FrameworkName>.bundle
```
`carthage bootstrap` does not create the `Resources/iOS/` directory or copy the bundles.

## Fix
After `carthage bootstrap`, copy all bundles from the simulator slice:
```bash
RESOURCES="Carthage/Build/Resources/iOS"
mkdir -p "$RESOURCES"
find Carthage/Build -path "*/ios-arm64_x86_64-simulator/*.framework/*.bundle" \
  -not -path "*/Resources/*" | while read b; do
  cp -r "$b" "$RESOURCES/$(basename $b)"
done
```
~49 bundles total. Add this to your bootstrap script alongside the vendored SDK copy step (KI-007).
