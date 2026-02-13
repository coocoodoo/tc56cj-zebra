#!/usr/bin/env bash
# Build Android APK. Run from project root inside WSL or Linux.
# Prereqs: buildozer, python-for-android deps (see buildozer docs).
# If building in WSL, ensure android.add_jars in buildozer.spec uses a path
# that exists in WSL (e.g. /mnt/c/Users/... for your Windows pywebview JAR).

set -e
cd "$(dirname "$0")"
buildozer android debug
echo "APK should be in bin/"
