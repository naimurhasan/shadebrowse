import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path.home() / "compare" / "shots"
SHADE = str(Path.home() / "src/out/Release/chrome")
SITES = {
    "sannysoft": "https://bot.sannysoft.com/",
    "areyouabot": "https://deviceandbrowserinfo.com/are_you_a_bot",
    "creepjs": "https://abrahamjuliot.github.io/creepjs/",
    "canvas": "https://browserleaks.com/canvas",
}
PROBE = """() => ({
  webdriver: navigator.webdriver,
  userAgent: navigator.userAgent,
  cores: navigator.hardwareConcurrency,
  failed: document.querySelectorAll("td.failed, .failed").length,
  text: document.body.innerText.slice(0, 4000),
})"""


def launch(p, name):
    if name == "chromium":
        return p.chromium.launch(headless=False)
    if name == "shadebrowse":
        return p.chromium.launch(executable_path=SHADE, headless=False, args=["--shade-seed=42"])
    if name == "cloakbrowser":
        import cloakbrowser
        return cloakbrowser.launch(headless=False)
    raise ValueError(name)


def visit(browser, name):
    results = {}
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    for site, url in SITES.items():
        try:
            page.goto(url, wait_until="load", timeout=60000)
            page.wait_for_timeout(8000)
            page.screenshot(path=str(OUT / f"{name}-{site}.png"))
            results[site] = page.evaluate(PROBE)
        except Exception as error:
            results[site] = {"error": str(error)[:200]}
    return results


def main(name):
    OUT.mkdir(parents=True, exist_ok=True)
    if name == "camoufox":
        from camoufox.sync_api import Camoufox
        with Camoufox(headless=False) as browser:
            results = visit(browser, name)
    else:
        with sync_playwright() as p:
            browser = launch(p, name)
            results = visit(browser, name)
            browser.close()
    (OUT / f"{name}.json").write_text(json.dumps(results, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
