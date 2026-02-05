---
name: build-pipeline
description: Quest build/deploy. ADB sideload. App Lab submission.
---

# Quest Build Pipeline

## Unity Build Settings
```
Platform: Android
Texture Compression: ASTC
Min API Level: 29 (Quest 2), 32 (Quest 3)
Scripting Backend: IL2CPP
Target Architecture: ARM64
```

## Build Command
```bash
# Unity CLI build
Unity -quit -batchmode -projectPath . \
  -executeMethod BuildScript.BuildQuest \
  -logFile build.log
```

## ADB Sideload
```bash
# Connect Quest (USB or wireless)
adb devices
adb connect 192.168.1.x:5555

# Install
adb install -r app.apk

# Launch
adb shell am start -n com.company.app/.MainActivity
```

## Wireless ADB Setup
```bash
adb tcpip 5555
adb connect <quest-ip>:5555
# Unplug USB
```

## App Lab Submission
1. Create app: developer.oculus.com
2. Upload APK via CLI or dashboard
3. Set release channel: ALPHA → PRODUCTION
4. Submit for review

## Meta Quest Developer Hub (MQDH)
- Real-time perf monitoring
- Log viewer
- APK management
- Cast to PC

## Gotchas
- Sign APK with upload keystore
- Quest 3 needs separate APK (different features)
- App Lab review: 3-5 business days
