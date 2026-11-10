"""Rebuild every SVG in ../assets from live GitHub data.   python scripts/build.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D
from parts_a import hero, ticker, header
from parts_b import card_agentx, card_aptino, card_twin, card_bike, card_nova, card_blood
from parts_c import craft, receipts, signal, heatmap, footer, pill

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)


def put(name, content):
    if content is None:
        return
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"{name:24s}{len(content) / 1024:7.1f} KB")


def main():
    data = D.load(refresh="--offline" not in sys.argv)
    put("hero.svg", hero(data))
    put("ticker.svg", ticker())
    put("h-work.svg", header("01", "Selected", "work", "6 OF 43 REPOSITORIES  ·  CLICK A CARD"))
    put("h-craft.svg", header("02", "The", "craft", "TOOLS I REACH FOR"))
    put("h-proof.svg", header("03", "Proof,", "not claims", "AWARDS  ·  IP  ·  PRODUCTION NUMBERS"))
    put("h-signal.svg", header("04", "Live", "signal", "REGENERATED DAILY FROM THE GITHUB API"))
    for n, fn in [("agentx", card_agentx), ("aptino", card_aptino), ("twin", card_twin),
                  ("bike", card_bike), ("nova", card_nova), ("blood", card_blood)]:
        put(f"card-{n}.svg", fn())
    put("craft.svg", craft())
    put("receipts.svg", receipts())
    put("signal.svg", signal(data))
    put("heatmap.svg", heatmap(data))
    put("footer.svg", footer())
    for name, label, acc in [("portfolio", "PORTFOLIO", True), ("linkedin", "LINKEDIN", False), ("leetcode", "LEETCODE", False)]:
        s, _ = pill(label, acc)
        put(f"pill-{name}.svg", s)


if __name__ == "__main__":
    main()
