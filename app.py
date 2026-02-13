"""
Entry point: create pywebview window, load UI, expose API, start webview.
Zebra TC56cj: use DataWedge keystroke output (Action key = Carriage return) into this app.
"""
import sys
from pathlib import Path

import webview

from api import ScanAPI

# Resolve path to assets so it works when run from project root or from another cwd
_SCRIPT_DIR = Path(__file__).resolve().parent
_ASSETS_DIR = _SCRIPT_DIR / "assets"
_INDEX_HTML = _ASSETS_DIR / "index.html"


def main() -> None:
    if not _INDEX_HTML.exists():
        print("Error: assets/index.html not found at", _INDEX_HTML, file=sys.stderr)
        sys.exit(1)
    # file:// URL so the webview loads the local HTML
    url = _INDEX_HTML.as_uri()
    api = ScanAPI()
    window = webview.create_window(
        "Barcode Scanner to CSV",
        url=url,
        js_api=api,
    )
    webview.start()


if __name__ == "__main__":
    main()
