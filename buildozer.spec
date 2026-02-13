# Buildozer spec for Barcode Scanner to CSV (Zebra TC56cj).
# Before building: get pywebview JAR path and set android.add_jars below:
#   python -c "from webview import util; print(util.android_jar_path())"

[app]
title = Barcode Scanner to CSV
package.name = scan2csv
package.domain = org.tc56cj

source.dir = .
source.include_exts = py,html,css,js
source.include_patterns = assets/*,lib/*
source.exclude_exts = spec

version = 0.1

requirements = python3,kivy,pywebview

orientation = portrait,landscape
fullscreen = 0

# Android
android.presplash_color = #FFFFFF
android.permissions = android.permission.INTERNET,android.permission.WRITE_EXTERNAL_STORAGE
android.apptheme = @android:style/Theme.Material.NoActionBar
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# JAR bundled in repo so GitHub Actions / any build can find it
android.add_jars = lib/pywebview-android.jar
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
