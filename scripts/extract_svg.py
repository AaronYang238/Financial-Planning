# 把章节 Markdown 里的内嵌 SVG 抽离成 assets/*.svg，并替换为图片引用
# 用法: python scripts/extract_svg.py
import re
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(ASSETS, exist_ok=True)

SVG_RE = re.compile(r"<svg.*?</svg>", re.DOTALL)
TEXT_RE = re.compile(r"<text[^>]*>([^<]+)</text>")

total = 0
for md_path in sorted(glob.glob(os.path.join(ROOT, "0*", "*.md"))):
    fname = os.path.basename(md_path)
    m = re.match(r"(\d+)-", fname)
    if not m:
        continue
    ch = m.group(1)
    with open(md_path, encoding="utf-8") as f:
        content = f.read()

    state = {"n": 0}

    def repl(match, ch=ch, state=state):
        global total
        state["n"] += 1
        total += 1
        svg = match.group(0)
        asset_name = f"ch{ch}-{state['n']}.svg"
        with open(os.path.join(ASSETS, asset_name), "w", encoding="utf-8") as out:
            out.write(svg + "\n")
        t = TEXT_RE.search(svg)
        alt = t.group(1).strip() if t else f"第{ch}章配图{state['n']}"
        return f"![{alt}](../assets/{asset_name})"

    new_content = SVG_RE.sub(repl, content)
    if state["n"]:
        with open(md_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_content)
        print(f"{fname}: {state['n']} svg -> assets/")

print(f"total: {total}")
