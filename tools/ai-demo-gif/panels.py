import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from urllib.parse import urlsplit

from steps import STEPS, URL

WIDTH, HEIGHT = 820, 700
OFFSET = -0.1
BACKGROUND = (13, 17, 23)
ACTIVE = (35, 70, 64)
TEXT = (230, 237, 243)
STRING = (165, 214, 255)
MUTED = (139, 148, 158)
TEAL = (43, 181, 160)
MONO = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 18)
SMALL = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 15)
BOLD = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 23)
HEADER = [
    "shade = Shade(page)",
    f"page.goto(\"{urlsplit(URL).netloc}{urlsplit(URL).path.rstrip('/')}\")",
    "",
]


def wrap(text, width=84):
    return [text[i:i + width] for i in range(0, len(text), width)] or [""]


def render(active, codes):
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw.text((24, 22), "Plain English -> Playwright, via Gemini Decision 1", font=BOLD, fill=TEXT)
    y = 70
    for line in HEADER:
        draw.text((24, y), line, font=MONO, fill=TEXT)
        y += 28
    for index, instruction in enumerate(STEPS):
        lines = wrap(codes[index]) if index in codes else ["Decision 1 is picking the element..."] if index == active else []
        height = 30 + 20 * len(lines)
        if index == active:
            draw.rectangle([12, y - 6, WIDTH - 12, y + height], fill=ACTIVE)
        draw.text((24, y), "shade.do(", font=MONO, fill=TEXT)
        draw.text((24 + draw.textlength("shade.do(", font=MONO), y), f"\"{instruction}\"", font=MONO, fill=STRING)
        draw.text((24 + draw.textlength(f"shade.do(\"{instruction}\"", font=MONO), y), ")", font=MONO, fill=TEXT)
        for offset, line in enumerate(lines):
            color = TEAL if index in codes else MUTED
            draw.text((40, y + 28 + 20 * offset), ("-> " if offset == 0 else "   ") + line, font=SMALL, fill=color)
        y += height + 26
    draw.text((24, HEIGHT - 64), "Answers are saved to shade-steps.json, so the next", font=SMALL, fill=MUTED)
    draw.text((24, HEIGHT - 40), "run replays the same selectors without calling the model.", font=SMALL, fill=MUTED)
    return image


timeline = json.loads(Path("timeline.json").read_text())
starts = [0.0] + [entry["at"] + OFFSET for entry in timeline]
states = [(None, {})]
codes = {}
for entry in timeline:
    if entry["code"]:
        codes[entry["step"]] = entry["code"]
    states.append((entry["step"], dict(codes)))
lines = []
for number, ((active, shown), start, end) in enumerate(zip(states, starts, starts[1:] + [starts[-1] + 2.0])):
    name = f"panel-{number}.png"
    render(active, shown).save(name)
    lines += [f"file {name}", f"duration {end - start:.2f}"]
lines.append(f"file {name}")
Path("panels.txt").write_text("\n".join(lines) + "\n")
