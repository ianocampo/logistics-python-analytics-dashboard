#!/usr/bin/env python3
"""Capture six clean 1920x1080 Streamlit screenshots, without Chrome browser UI.

Runs against YOUR local dashboard. Set DASHBOARD_PORT=8502 if needed.
Only writes images to Assets/. It does not alter analysis code or push to GitHub.
"""
from pathlib import Path
import os
import struct
import sys

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "Assets"
APP_URL = f"http://127.0.0.1:{os.environ.get('DASHBOARD_PORT', '8501')}"

# Exact tab names, verified against logistics_delivery_dashboard.py.
PAGES = (
    ("01 · Overview", "Operational Snapshot", "dashboard_01_overview_1920x1080.png"),
    ("02 · Courier Performance", "Courier Delivery Times", "dashboard_02_courier_performance_1920x1080.png"),
    ("03 · Returns Intelligence", "Return Requests & Category Associations", "dashboard_03_returns_intelligence_1920x1080.png"),
    ("04 · Data Quality", "Source Data Quality Exception Register", "dashboard_04_data_quality_1920x1080.png"),
    ("05 · Executive Brief", "Business Priorities & Evidence", "dashboard_05_executive_brief_1920x1080.png"),
    ("06 · Data & Methodology", "Explore the Data & Methodology", "dashboard_06_data_methodology_1920x1080.png"),
)

def check_png(path: Path) -> None:
    # The PNG header stores its pixel width and height at bytes 16-23.
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise RuntimeError(f"Invalid PNG image: {path}")
    width, height = struct.unpack(">II", header[16:24])
    if (width, height) != (1920, 1080):
        raise RuntimeError(f"Unexpected image size: {path}: {width}x{height}")

def capture() -> None:
    # Headless Chrome produces webpage-only images, excluding browser tabs,
    # bookmarks, address bar and personal browser side panels.
    ASSETS.mkdir(exist_ok=True)
    with sync_playwright() as playwright:
        try:
            browser = playwright.chromium.launch(channel="chrome", headless=True)
        except Exception as error:
            raise RuntimeError(
                "Google Chrome was not found. Install Chrome or ask for help."
            ) from error

        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=1,
            reduced_motion="reduce",
            color_scheme="dark",
        )
        page = context.new_page()
        try:
            page.goto(APP_URL, wait_until="domcontentloaded", timeout=90000)
            page.get_by_role("tab", name=PAGES[0][0], exact=True).wait_for(timeout=90000)
            page.wait_for_timeout(2500)

            # Screenshot-only CSS: hide development toolbar, not dashboard content.
            page.add_style_tag(content="""
                [data-testid="stToolbar"],
                [data-testid="stDecoration"],
                [data-testid="stStatusWidget"],
                #MainMenu { visibility: hidden !important; }
            """)

            for number, (label, page_title, filename) in enumerate(PAGES, 1):
                # Click the ACTUAL Streamlit tab, not a fabricated dashboard image.
                tab = page.get_by_role("tab", name=label, exact=True)
                tab.click(timeout=30000)

                # Verify the selected tab and its real content before capture.
                page.wait_for_function(
                    "(target) => { const e = [...document.querySelectorAll('[role=tab]')].find(x => x.textContent.trim() === target); return !!e && e.getAttribute('aria-selected') === 'true'; }",
                    arg=label,
                    timeout=30000,
                )
                page.get_by_text(page_title, exact=False).first.wait_for(
                    state="visible", timeout=30000
                )
                page.wait_for_timeout(1600)

                # Reset Streamlit's internal main panel to its top position.
                page.evaluate("""
                    () => {
                        window.scrollTo(0, 0);
                        for (const element of document.querySelectorAll('[data-testid="stMain"], [data-testid="stAppViewContainer"]')) {
                            element.scrollTop = 0;
                        }
                    }
                """)
                page.wait_for_timeout(500)

                body = page.locator("body").inner_text().lower()
                if "file bundle not present in this local installation" in body:
                    raise RuntimeError(
                        f"Page {number} reports missing data files. Screenshot not saved."
                    )

                destination = ASSETS / filename
                page.screenshot(
                    path=str(destination), full_page=False, animations="disabled"
                )
                check_png(destination)
                print(f"PASS {number}/6 | {filename} | 1920x1080")

            print("\nSUCCESS — all six dashboard previews captured.")
            print(f"Saved to: {ASSETS}")
            print("No Git commit or push has been performed.")
        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    try:
        capture()
    except Exception as error:
        print(f"\nCAPTURE STOPPED: {error}", file=sys.stderr)
        sys.exit(1)
