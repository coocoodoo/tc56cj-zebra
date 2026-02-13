"""
Python API exposed to the pywebview frontend.
Handles CSV path resolution, add_scan(), get_scans(), get_csv_path() with thread-safe writes.
"""
import csv
import os
import threading
from datetime import datetime
from pathlib import Path

CSV_FILENAME = "scans.csv"
CSV_HEADERS = ["timestamp", "barcode"]
DEFAULT_GET_SCANS_LIMIT = 100
_write_lock = threading.Lock()


def _csv_path() -> Path:
    """Resolve writable path for scans.csv (desktop vs Android)."""
    # Android: app storage is often cwd or ANDROID_APP_PATH / ANDROID_PRIVATE
    if os.environ.get("ANDROID_APP_PATH"):
        base = Path(os.environ["ANDROID_APP_PATH"])
    elif os.environ.get("ANDROID_PRIVATE"):
        base = Path(os.environ["ANDROID_PRIVATE"])
    else:
        base = Path.cwd()
    path = base / CSV_FILENAME
    # If cwd is not writable (e.g. install dir), fall back to user home
    if not base.exists() or not os.access(base, os.W_OK):
        base = Path.home()
        path = base / CSV_FILENAME
    return path


class ScanAPI:
    """API class for pywebview js_api. Method names must not start with underscore."""

    def add_scan(self, barcode: str) -> dict:
        """Append one scan (timestamp, barcode) to CSV. Returns {ok, message, total} or error."""
        barcode = (barcode or "").strip()
        if not barcode:
            return {"ok": False, "message": "Empty barcode", "total": 0}
        path = _csv_path()
        with _write_lock:
            try:
                file_exists = path.exists()
                with open(path, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    if not file_exists:
                        writer.writerow(CSV_HEADERS)
                    writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), barcode])
                total = self._count_rows(path)
                return {"ok": True, "message": "Logged", "total": total}
            except Exception as e:
                return {"ok": False, "message": str(e), "total": 0}

    def get_scans(self, limit: int = DEFAULT_GET_SCANS_LIMIT) -> list:
        """Read last N rows from CSV. Returns list of {timestamp, barcode}."""
        path = _csv_path()
        if not path.exists():
            return []
        with _write_lock:
            try:
                with open(path, "r", newline="", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    if reader.fieldnames != CSV_HEADERS:
                        return []
                    rows = list(reader)
                # Last N, most recent last
                rows = rows[-limit:] if limit else rows
                return [{"timestamp": r["timestamp"], "barcode": r["barcode"]} for r in rows]
            except Exception:
                return []

    def get_csv_path(self) -> str:
        """Return absolute path string for the CSV file (for UI display)."""
        return str(_csv_path().resolve())

    @staticmethod
    def _count_rows(path: Path) -> int:
        """Count data rows (excluding header) in CSV."""
        if not path.exists():
            return 0
        try:
            with open(path, "r", newline="", encoding="utf-8") as f:
                return max(0, sum(1 for _ in csv.DictReader(f)))
        except Exception:
            return 0
