"""Regenerate the hover thumbnails in ./previews (run after changing page content).

Usage:  streamlit run app.py        # in one terminal
        python tools/make_previews.py [http://localhost:8501]
Requires: pip install playwright pillow && playwright install chromium
"""
import io
import sys
from pathlib import Path

from PIL import Image
from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8501"
OUT = Path(__file__).resolve().parent.parent / "previews"
OUT.mkdir(exist_ok=True)
PAGES = ["01", "02", "03", "04", "05", "06", "07", "08"]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    page.goto(URL)
    page.wait_for_selector('[data-testid="stSidebar"]')
    page.wait_for_timeout(2500)
    for num in PAGES:
        page.locator('[data-testid="stSidebar"] label', has_text=f"{num} ·").first.click()
        page.wait_for_timeout(3500)
        png = page.screenshot(clip={"x": 300, "y": 40, "width": 1140, "height": 720})
        img = Image.open(io.BytesIO(png)).convert("RGB")
        img = img.resize((680, round(680 * img.height / img.width)), Image.LANCZOS)
        img.save(OUT / f"{num}.jpg", quality=80, optimize=True)
        print("saved", num)
    browser.close()
