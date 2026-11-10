"""Rebuild every SVG in ../assets from live GitHub data.   python scripts/build.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D
from parts_a import hero, ticker, header
from parts_b import card_agentx, card_aptino, card_twin, card_bike, card_nova, card_blood
from parts_c import craft, receipts, signal, heatmap, pill
from parts_d import constellation, timeline, terminal, footer2

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)


def put(name, content):
    if content is None:
        return
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{name:24s}{len(content) / 1024:7.1f} KB")


def slim(c):
    return {"total": c["totalContributions"],
            "days": [[d["date"], d["contributionCount"]] for w in c["weeks"] for d in w["contributionDays"]]}


def publish_page(data):
    import json, shutil, datetime
    docs = os.path.join(os.path.dirname(OUT), "docs")
    os.makedirs(docs, exist_ok=True)
    shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), "page.html"), os.path.join(docs, "index.html"))
    payload = {"updated": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"), "repos": data["repos"],
               "langs": data["langs"], "calendar": slim(data["calendar"]),
               "calendars": {y: slim(c) for y, c in (data.get("calendars") or {}).items()}}
    with open(os.path.join(docs, "data.json"), "w") as f:
        json.dump(payload, f, separators=(",", ":"))
    open(os.path.join(docs, ".nojekyll"), "w").close()


def readme(data):
    here = os.path.dirname(os.path.abspath(__file__))
    tpl = open(os.path.join(here, "README.tpl.md"), encoding="utf-8").read()
    blocks = []
    for y, c in sorted((data.get("calendars") or {}).items(), reverse=True):
        if c["totalContributions"] < 1 or int(y) < 2023:
            continue
        put(f"heatmap-{y}.svg", heatmap(data, c, f"IN {y}"))
        blocks.append(f'<details name="year"><summary><b>{y}</b> &nbsp;·&nbsp; {c["totalContributions"]:,} contributions</summary>'
                      f'<img src="assets/heatmap-{y}.svg" alt="Contribution heatmap for {y}" width="100%"/></details>')
    html = ("<sub>pick a year ↓</sub>\n\n" + "\n".join(blocks)) if blocks else ""
    with open(os.path.join(here, "..", "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(tpl.replace("<!--YEARS-->", html))


def main():
    data = D.load(refresh="--offline" not in sys.argv)
    put("hero.svg", hero(data))
    put("ticker.svg", ticker())
    put("h-work.svg", header("01", "Selected", "work", "6 OF 43 REPOSITORIES  ·  CLICK A CARD"))
    put("h-map.svg", header("02", "The", "map", "FOUR DOMAINS  ·  ONE ENGINEER"))
    put("h-craft.svg", header("03", "The", "craft", "TOOLS I REACH FOR"))
    put("h-journey.svg", header("04", "The", "journey", "CHRONOLOGICAL  ·  NOT TO SCALE"))
    put("h-proof.svg", header("05", "Proof,", "not claims", "AWARDS  ·  IP  ·  PRODUCTION NUMBERS"))
    put("h-signal.svg", header("06", "Live", "signal", "REGENERATED EVERY 6 HOURS FROM THE GITHUB API"))
    for n, fn in [("agentx", card_agentx), ("aptino", card_aptino), ("twin", card_twin),
                  ("bike", card_bike), ("nova", card_nova), ("blood", card_blood)]:
        put(f"card-{n}.svg", fn())
    put("constellation.svg", constellation())
    put("timeline.svg", timeline())
    put("terminal.svg", terminal(data))
    put("craft.svg", craft())
    put("receipts.svg", receipts())
    put("signal.svg", signal(data))
    put("heatmap.svg", heatmap(data))
    put("footer.svg", footer2())
    readme(data)
    publish_page(data)
    for name, label, acc in [("interactive", "INTERACTIVE EXPLORER", True), ("portfolio", "PORTFOLIO", False), ("linkedin", "LINKEDIN", False), ("leetcode", "LEETCODE", False)]:
        s, _ = pill(label, acc)
        put(f"pill-{name}.svg", s)


if __name__ == "__main__":
    main()
