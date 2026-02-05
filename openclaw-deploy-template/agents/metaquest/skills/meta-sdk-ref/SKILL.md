---
name: meta-sdk-ref
description: Meta XR SDK APIs. Hand tracking. Passthrough. Interaction.
---

# Meta XR SDK Reference

## Setup (Unity)
```
Package Manager → Add by name:
com.meta.xr.sdk.core
com.meta.xr.sdk.interaction
com.meta.xr.sdk.platform
```

## Core Components
```csharp
// Camera Rig
OVRCameraRig rig;
Transform leftHand = rig.leftHandAnchor;
Transform rightHand = rig.rightHandAnchor;

// Input
OVRInput.Get(OVRInput.Button.One);  // A button
OVRInput.Get(OVRInput.Axis1D.PrimaryIndexTrigger);
```

## Hand Tracking
```csharp
OVRHand hand = GetComponent<OVRHand>();
bool pinching = hand.GetFingerIsPinching(OVRHand.HandFinger.Index);
float pinchStrength = hand.GetFingerPinchStrength(OVRHand.HandFinger.Index);
```

## Passthrough
```csharp
// Enable in OVRManager
OVRManager.instance.isInsightPassthroughEnabled = true;

// Layer setup
OVRPassthroughLayer layer;
layer.textureOpacity = 1.0f;
```

## Interaction SDK
```csharp
// Grab interactable
[RequireComponent(typeof(Grabbable))]
public class MyObject : MonoBehaviour { }

// Poke interaction
PokeInteractable poke;
poke.WhenPokeStarted += OnPoke;
```

## Platform (Entitlements)
```csharp
Entitlements.IsUserEntitledToApplication().OnComplete(msg => {
    if (msg.IsError) Application.Quit();
});
```

## Gotchas
- Test entitlements FIRST (blocks non-owners)
- Passthrough requires manifest permission
- Hand tracking + controllers = fallback needed
