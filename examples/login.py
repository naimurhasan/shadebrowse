from playwright.sync_api import sync_playwright

from shadebrowse import Shade

STEPS = [
    "type tomsmith into the username field",
    "type SuperSecretPassword! into the password field",
    "click login",
    "click logout",
]

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="./chrome", headless=False, args=["--shade-seed=42"])
    page = browser.new_page()
    shade = Shade(page)

    page.goto("https://the-internet.herokuapp.com/login")
    for instruction in STEPS:
        step = shade.do(instruction)
        print(f"{instruction:52} -> {step.code}{'  (cached)' if step.cached else ''}")
        page.wait_for_load_state("load")

    browser.close()
