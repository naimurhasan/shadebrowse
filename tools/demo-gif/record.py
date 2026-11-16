import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

from steps import STEPS

CHROME = str(Path.home() / "src/out/Release/chrome")
HIGHLIGHT = """(el) => {
  el.scrollIntoView({block: "center"});
  el.style.outline = "4px solid #2BB5A0";
  el.style.outlineOffset = "2px";
}"""
TARGETS = {
    1: lambda page: page.locator("#searchInput"),
    4: lambda page: page.get_by_role("link", name="Blink").first,
}
SLOW = {
    2: lambda page: page.keyboard.type("Chromium web browser", delay=90),
}


def run_step(page, index):
    if index in TARGETS:
        TARGETS[index](page).evaluate(HIGHLIGHT)
        page.wait_for_timeout(700)
    if index in SLOW:
        SLOW[index](page)
    else:
        eval(STEPS[index], {"page": page})
    page.wait_for_load_state("load")
    page.wait_for_timeout(1500)


def main():
    timeline = []
    start = time.monotonic()
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME,
            headless=False,
            args=["--shade-seed=42", "--window-position=0,0", "--window-size=900,700"],
        )
        page = browser.new_page(viewport={"width": 900, "height": 600})
        page.wait_for_timeout(800)
        for index in range(len(STEPS)):
            timeline.append({"step": index, "at": time.monotonic() - start})
            run_step(page, index)
        timeline.append({"step": None, "at": time.monotonic() - start})
        browser.close()
    Path("timeline.json").write_text(json.dumps(timeline))


if __name__ == "__main__":
    main()
