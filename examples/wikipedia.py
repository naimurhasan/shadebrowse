from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path="./chrome",
                                headless=False,
                                args=["--shade-seed=42"])
    page = browser.new_page()

    page.goto("https://www.wikipedia.org")
    page.click("#searchInput")
    page.keyboard.type("Chromium web browser")
    page.keyboard.press("Enter")
    page.get_by_role("link", name="Blink").first.click()
    page.mouse.wheel(0, 500)

    browser.close()
