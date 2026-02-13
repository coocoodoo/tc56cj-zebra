# CI build configuration (Android APK)

This file records the working configuration for building the APK in CI (GitHub Actions). Keep these settings when updating the workflow or building elsewhere.

## Runner

- **OS:** `ubuntu-latest` (Ubuntu 24)
- **Python:** 3.11
- **Java:** 17 (Temurin)

## System packages (apt)

Install these before running buildozer:

```
git zip unzip openjdk-17-jdk \
autoconf automake libtool libltdl-dev pkg-config zlib1g-dev \
libncurses5-dev libncursesw5-dev libtinfo6 \
cmake libffi-dev libssl-dev
```

Notes:

- **libtinfo6** (not libtinfo5): `libtinfo5` is not available on Ubuntu 24; use `libtinfo6`.
- **libltdl-dev**: Provides libtool m4 macros (e.g. `LT_SYS_SYMBOL_USCORE`) required when python-for-android builds libffi; without it, `configure.ac` fails with "possibly undefined macro".

## Build environment

Set when running `buildozer android debug`:

| Variable       | Value                | Reason |
|----------------|----------------------|--------|
| `ACLOCAL_PATH` | `/usr/share/aclocal` | So `aclocal`/`autoreconf` find libtool macros when p4a builds libffi (e.g. `LT_SYS_SYMBOL_USCORE`). |

## buildozer.spec

- **android.accept_sdk_license** = `True` — Required for non-interactive CI (no license prompt).
- **android.add_jars** = `lib/pywebview-android.jar` — JAR is committed under `lib/` so CI does not need a machine-specific path.
- **source.include_patterns** — Include `assets/*` and `lib/*`.

## Workflow file

- **Path:** `.github/workflows/build_apk.yml`
- Steps: checkout → Set up Python 3.11 → Set up Java 17 → Install system dependencies (above) → Install Buildozer + app deps → Build APK (with `ACLOCAL_PATH`) → Upload artifact `bin/*.apk`.

## Local / WSL build

For building on WSL or Linux, install the same apt packages, set `ACLOCAL_PATH` when running buildozer, and ensure `android.add_jars` in `buildozer.spec` points to a valid path (e.g. `lib/pywebview-android.jar` if the JAR is in the repo).
