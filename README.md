# Barcode Scanner to CSV (Zebra TC56cj)

Python app with a pywebview GUI: scan barcodes on a Zebra TC56cj (or type them on desktop), see them in a list, and save every scan to a CSV file.

## Run on Windows (development)

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   python app.py
   ```
3. Type a barcode in the input and press Enter to simulate a scan. Scans are appended to `scans.csv` in the current directory (or your user home if the current dir is not writable).

## Run on Zebra TC56cj (Android)

### 1. Build the APK

**Option A: GitHub Actions (recommended)**  
Push to `main` or `master` (or run the workflow manually from the Actions tab). The workflow at `.github/workflows/build_apk.yml` builds the APK; download it from the run’s **Artifacts** (android-apk).

**Working CI configuration (for future builds):**
- **Runner:** `ubuntu-latest` (Ubuntu 24).
- **System packages:** `autoconf`, `automake`, `libtool`, `libltdl-dev` (for libtool m4 macros used by libffi), `libtinfo6` (not `libtinfo5` — not available on Ubuntu 24), plus `pkg-config`, `zlib1g-dev`, `libncurses*`, `cmake`, `libffi-dev`, `libssl-dev`, `openjdk-17-jdk`.
- **Build env:** `ACLOCAL_PATH=/usr/share/aclocal` so `aclocal`/`autoreconf` find libtool macros (e.g. `LT_SYS_SYMBOL_USCORE`) when python-for-android builds libffi.
- **buildozer.spec:** `android.accept_sdk_license = True` for non-interactive CI; `android.add_jars = lib/pywebview-android.jar` (JAR is in repo under `lib/`).

**Option B: Local build (WSL or Linux only)**

Buildozer does not run on Windows natively; use **WSL** (Ubuntu, etc.) or a Linux machine.

1. **Install buildozer and dependencies** (see [buildozer installation](https://buildozer.readthedocs.io/en/latest/installation.html)). On Ubuntu WSL:
   ```bash
   sudo apt update
   sudo apt install -y buildozer python3-pip
   pip install pywebview
   ```
2. **Set the JAR path in `buildozer.spec`.**  
   The spec may already have `android.add_jars` set to a path on this PC. If you build in **WSL**, that path must be valid inside WSL: use the same file as a Linux path, e.g.  
   ` /mnt/c/Users/<You>/AppData/Local/Packages/PythonSoftwareFoundation.Python.3.11_.../LocalCache/local-packages/Python311/site-packages/webview/lib/pywebview-android.jar`  
   Or from WSL run:  
   `python3 -c "from webview import util; print(util.android_jar_path())"`  
   (with pywebview installed in WSL) and put that path in `android.add_jars`.
3. **Build the APK** (from the project directory in WSL/Linux):
   ```bash
   chmod +x build_apk.sh
   ./build_apk.sh
   ```
   Or run: `buildozer android debug`
4. **Install the APK** from `bin/` onto the TC56cj (e.g. copy the `.apk` to the device and open it, or use `adb install bin/*.apk`).

### 2. DataWedge setup on the TC56cj

So that the built-in scanner sends data to this app:

1. Open **DataWedge** (in the device app drawer or Settings).
2. Create a new profile (e.g. **Barcode Scanner App**) or duplicate an existing one.
3. **Associated apps**: Add this app by package name: `org.tc56cj.scan2csv` (or the `package.domain.package.name` from `buildozer.spec`).
4. **Input**: Enable **Barcode** (or leave default).
5. **Keystroke output**: Enable it. Set **Action key** to **Carriage return** (so each scan ends with Enter).
6. Save and make sure this profile is active when you open the app.

After that, open the app, focus the text field (it’s focused by default), and scan. Each scan is logged to the list and appended to the CSV. The CSV path is shown at the top of the screen (on Android it will be in the app’s storage).

## CSV format

- File name: `scans.csv`
- Columns: `timestamp`, `barcode`
- One row per scan; new scans are appended.

## Project layout

- `app.py` – Entry point (desktop): creates window, loads UI, exposes API.
- `main.py` – Entry point for Android/buildozer (calls `app.main()`).
- `api.py` – Python API exposed to the frontend: `add_scan`, `get_scans`, `get_csv_path`.
- `assets/index.html` – Web UI: scanner input, scan list, CSV path.
- `requirements.txt` – `pywebview`
- `buildozer.spec` – Android APK build; JAR in `lib/`, see spec for CI-friendly options.
- `.github/workflows/build_apk.yml` – GitHub Actions workflow for building the APK (see README “Working CI configuration”).
