from playwright.sync_api import sync_playwright

from shadebrowse import Shade

STEPS = [
    "type Chromium web browser into the search box",
    "press Enter in the search box",
    "click the Blink link",
]

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="./chrome", headless=False, args=["--shade-seed=42"])
    page = browser.new_page()
    shade = Shade(page)

    page.goto("https://www.wikipedia.org")
    for instruction in STEPS:
        step = shade.do(instruction)
        print(f"{instruction:48} -> {step.code}{'  (cached)' if step.cached else ''}")
        page.wait_for_load_state("load")

    browser.close()
