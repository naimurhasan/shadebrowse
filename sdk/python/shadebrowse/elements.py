SNAPSHOT = """() => {
  const seen = new Set();
  const visible = (el) => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== "hidden" && s.display !== "none";
  };
  const label = (el) => {
    const byFor = el.id && document.querySelector(`label[for="${el.id}"]`);
    return [el.getAttribute("aria-label"), byFor && byFor.innerText, el.placeholder, el.innerText, el.value, el.title]
      .find((v) => v && v.trim())?.trim().slice(0, 60) || "";
  };
  const unique = (selector) => document.querySelectorAll(selector).length === 1;
  const selectorOf = (el) => {
    const tag = el.tagName.toLowerCase();
    if (el.id && unique(`#${CSS.escape(el.id)}`)) return `#${CSS.escape(el.id)}`;
    const name = el.getAttribute("name");
    if (name && unique(`${tag}[name="${name}"]`)) return `${tag}[name="${name}"]`;
    const text = el.innerText && el.innerText.trim();
    if (text) return `${tag}:has-text('${text.slice(0, 40).replace(/'/g, "\\'")}')`;
    return `${tag} >> nth=${[...document.querySelectorAll(tag)].indexOf(el)}`;
  };
  return [...document.querySelectorAll("a, button, input, select, textarea, [role=button], [onclick]")]
    .filter((el) => visible(el) && !seen.has(el) && seen.add(el))
    .slice(0, 150)
    .map((el, index) => ({
      index,
      tag: el.tagName.toLowerCase(),
      type: el.getAttribute("type") || "",
      label: label(el),
      selector: selectorOf(el),
    }));
}"""


def collect(page):
    return page.evaluate(SNAPSHOT)
