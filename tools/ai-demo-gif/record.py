import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

from shadebrowse import Shade
from steps import STEPS, URL

CHROME = str(Path.home() / "src/out/Release/chrome")
HIGHLIGHT = """(el) => {
  el.style.outline = "4px solid #2BB5A0";
  el.style.outlineOffset = "2px";
}"""


def main():
    Path("shade-steps.json").unlink(missing_ok=True)
    timeline = []
    start = time.monotonic()
    mark = lambda **entry: timeline.append({**entry, "at": time.monotonic() - start})
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME,
            headless=False,
            args=["--shade-seed=42", "--window-position=0,0", "--window-size=900,700"],
        )
        page = browser.new_page(viewport={"width": 900, "height": 600})
        page.goto(URL)
        page.wait_for_timeout(1200)
        shade = Shade(page)
        for index, instruction in enumerate(STEPS):
            mark(step=index, code=None)
            step = shade.plan(instruction)
            mark(step=index, code=step.code)
            page.locator(step.selector).first.evaluate(HIGHLIGHT)
            page.wait_for_timeout(900)
            shade.run(step)
            page.wait_for_load_state("load")
            page.wait_for_timeout(1300)
        mark(step=None, code=None)
        browser.close()
    Path("timeline.json").write_text(json.dumps(timeline))


if __name__ == "__main__":
    main()
