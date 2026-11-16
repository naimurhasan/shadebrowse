import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from steps import SETUP, STEPS

WIDTH, HEIGHT = 700, 700
OFFSET = -0.1
BACKGROUND = (13, 17, 23)
ACTIVE = (35, 70, 64)
DONE = (110, 118, 129)
COLORS = {"string": (165, 214, 255), "number": (121, 192, 255), "plain": (230, 237, 243), "muted": (139, 148, 158)}
LABELS = ["open the page", "click the search box", "type a query", "press Enter", "click a link", "scroll"]
MONO = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 15)
BOLD = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)


def draw_code(draw, x, y, text, dim):
    for token in re.findall(r"\s+|\"[^\"]*\"|\w+|.", text):
        if dim:
            color = DONE
        elif token.startswith("\""):
            color = COLORS["string"]
        elif token.isdigit():
            color = COLORS["number"]
        else:
            color = COLORS["plain"]
        draw.text((x, y), token, font=MONO, fill=color)
        x += draw.textlength(token, font=MONO)


def render(active):
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw.text((24, 22), "ShadeBrowse + Playwright", font=BOLD, fill=COLORS["plain"])
    y = 70
    for line in SETUP:
        draw_code(draw, 24, y, line, False)
        y += 24
    for index, line in enumerate(STEPS):
        if index == active:
            draw.rectangle([12, y - 4, WIDTH - 12, y + 40], fill=ACTIVE)
        draw.text((24, y), f"# {index + 1}. {LABELS[index]}", font=MONO, fill=COLORS["muted"])
        draw_code(draw, 24, y + 18, line, active is not None and index < active)
        y += 54
    return image


timeline = json.loads(Path("timeline.json").read_text())
entries = [(None, 0.0)] + [(t["step"], t["at"] + OFFSET) for t in timeline]
lines = []
for (step, start), (_, end) in zip(entries, entries[1:]):
    name = "panel-idle.png" if step is None else f"panel-{step}.png"
    render(step).save(name)
    lines += [f"file {name}", f"duration {end - start:.2f}"]
lines.append(f"file {name}")
Path("panels.txt").write_text("\n".join(lines) + "\n")
