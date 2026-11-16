from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    for seed in [42, 42, 7]:
        browser = p.chromium.launch(
            executable_path="./chrome",
            headless=False,
            args=[f"--shade-seed={seed}"],
        )
        page = browser.new_page()
        page.goto("https://browserleaks.com/canvas")
        page.wait_for_timeout(4000)
        browser.close()
