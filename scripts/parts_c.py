import math, datetime
from lib import *

W = 1000
RISE = ("@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}"
        ".rise{animation:rise .9s cubic-bezier(.2,.7,.2,1) both}"
        "@keyframes lineDraw{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
        ".ld{transform-origin:0 0;transform-box:fill-box;animation:lineDraw 1.2s cubic-bezier(.6,0,.2,1) both}"
        "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}.pulse{animation:pulse 1.8s ease-in-out infinite}")


# ───────────────────────────── CRAFT ────────────────────────────────────────
def craft():
    cols = [
        ("LANGUAGES", ["Python", "TypeScript", "JavaScript", "C / C++", "SQL", "Java"]),
        ("BACKEND + DATA", ["Node · NestJS · Express", "FastAPI · Django", "PostgreSQL · pgvector", "MongoDB · Redis", "WebSockets · JWT · RBAC", "TimescaleDB"]),
        ("CLOUD + DEVOPS", ["AWS · GCP · Firebase", "Docker · Compose", "CI/CD pipelines", "Linux VPS deploys", "Nginx · cron automation", "pytest · code review"]),
        ("GENAI + EDGE", ["LLM agents · multi-agent", "RAG · hybrid retrieval", "Gemini · OpenAI · Ollama", "scikit-learn · TFLite", "ESP32 · MQTT · Modbus", "Flutter · Kotlin"]),
    ]
    H = 330
    colw = (W - 16) / 4
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    css = RISE + "@keyframes hl{0%{opacity:0}6%,24%{opacity:1}30%,100%{opacity:0}}"
    for ci, (head, items) in enumerate(cols):
        x = 8 + ci * colw
        if ci:
            b.append(f'<rect x="{x - 14}" y="12" width="1" height="{H - 36}" fill="{LINE}"/>')
        b.append(f'<g class="rise" style="animation-delay:{ci * .12:.2f}s">{T(head, MONOB, 11.5, x, 34, ACC, track=2)}</g>')
        for ri, it in enumerate(items):
            y = 82 + ri * 38
            dl = .25 + ci * .1 + ri * .07
            b.append(f'<g class="rise" style="animation-delay:{dl:.2f}s">'
                     f'<rect x="{x}" y="{y + 11}" width="{colw - 36}" height="1" fill="{LINE}"/>'
                     + T(it, SANSM, 17.5, x, y + 3, PAPER, track=-.1) + "</g>")
        # cycling highlight sweep, staggered per row
    for ci in range(4):
        x = 8 + ci * colw
        for ri in range(6):
            y = 82 + ri * 38
            idx = ri * 4 + ci
            b.append(f'<rect x="{x - 8}" y="{y - 17}" width="3" height="28" fill="{ACC}" opacity="0" style="animation:hl 12s linear {idx * .5:.2f}s infinite"/>')
    return svg(W, H, "".join(b), css, "", "Craft: languages, backend and data, cloud and devops, GenAI and edge")


# ───────────────────────────── RECEIPTS ─────────────────────────────────────
def receipts():
    H = 470
    cells = [
        ("1st", "CTF — Sanjivani Cyber Quest 2026", "Team Bugsploit · 100+ teams · 8,843 pts · 26 solves"),
        ("1st", "24-hour AI hackathon", "AgentX — autonomous competitive-intelligence agent"),
        ("3", "registered software copyrights", "Fake-job detection AI · pothole navigation · PDA evaluator"),
        ("2", "design patents filed", "Saffron-harvesting robot · SmartMediTrack IoT reminder"),
        ("10h", "to ship concert ticketing, solo", "3,000+ capacity — the institute's first concert in 41 years"),
        ("850K", "rupees processed via Razorpay", "Event ticketing · 11,600+ users · 30+ vendors · 11,450+ bookings"),
    ]
    cw, ch = (W - 16) / 3, 200
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    css = RISE
    for i, (big, lab, sub) in enumerate(cells):
        r, c = divmod(i, 3)
        x, y = 8 + c * cw, 6 + r * ch
        fnt = SERIF
        size = 104 if len(big) <= 3 else 84
        dl = .1 + i * .13
        g = [T(big, fnt, size, x, y + 108, ACC if i < 2 else PAPER, track=-2)]
        g.append(T(lab.upper(), MONOB, 10.5, x + 2, y + 142, PAPER, track=1.3))
        # wrap sub at ~ 44 chars
        words, lines, cur = sub.split(" "), [], ""
        for w_ in words:
            if len(cur) + len(w_) + 1 > 44:
                lines.append(cur)
                cur = w_
            else:
                cur = (cur + " " + w_).strip()
        lines.append(cur)
        for li, ln in enumerate(lines):
            g.append(T(ln, MONO, 10.5, x + 2, y + 162 + li * 16, DIM))
        b.append(f'<g class="rise" style="animation-delay:{dl:.2f}s">{"".join(g)}</g>')
        # separators
        b.append(f'<rect class="ld" x="{x}" y="{y}" width="{cw - 24}" height="1" fill="{LINE2}" style="animation-delay:{dl:.2f}s"/>')
    b.append(f'<g class="rise" style="animation-delay:1.1s"><circle class="pulse" cx="14" cy="{H - 26}" r="4" fill="{OK}"/>' +
             T("ALSO  ·  FINALIST, MeitY AGRI EXCELLENCE HACKATHON 2025–26  ·  PRESENTED TO THE JURY AT SKUAST-KASHMIR, SRINAGAR", MONO, 10.5, 28, H - 22, DIM, track=1) + "</g>")
    return svg(W, H, "".join(b), css, "", "Receipts: awards, patents, copyrights and production numbers")


# ───────────────────────────── SIGNAL (stats + languages) ───────────────────
def signal(data):
    H = 300
    skip = {"Jupyter Notebook", "HTML", "CSS", "Makefile", "Dockerfile", "Shell", "SCSS", "TeX", "Batchfile"}
    langs = [(k, v) for k, v in sorted(data["langs"].items(), key=lambda x: -x[1]) if k not in skip][:6]
    tot = sum(v for _, v in langs)
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    css = RISE + "@keyframes bar{from{transform:scaleX(0)}to{transform:scaleX(1)}}.bar{transform-origin:0 0;transform-box:fill-box;animation:bar 1.4s cubic-bezier(.5,0,.2,1) both}"
    # left stats
    stats = [(str(data["repos"]), "PUBLIC REPOS"), (str(data["followers"]), "FOLLOWERS"), (f'{datetime.date.today().year - data["since"]}y', f'ON GITHUB · SINCE {data["since"]}')]
    for i, (n, l) in enumerate(stats):
        y = 56 + i * 80
        b.append(f'<g class="rise" style="animation-delay:{i * .15:.2f}s">{T(n, SERIF, 66, 8, y + 38, PAPER, track=-1.5)}'
                 f'{T(l, MONOB, 10.5, 8 + width(n, SERIF, 66, -1.5) + 16, y + 36, DIM, track=1.4)}</g>')
        b.append(f'<rect x="8" y="{y + 54}" width="300" height="1" fill="{LINE}"/>')
    # right bars
    bx, bw = 400, 520
    b.append(T("MOST-USED LANGUAGES  /  BY BYTES, OWN REPOS", MONOB, 10.5, bx, 30, ACC, track=1.8))
    tones = [ACC, "#E8C14A", "#C7A743", "#9C8A58", "#766C57", "#54503F"]
    for i, (name, v) in enumerate(langs):
        y = 62 + i * 38
        pct = v / tot * 100
        b.append(f'<g class="rise" style="animation-delay:{.2 + i * .1:.2f}s">{T(name, SANSM, 16, bx, y + 4, PAPER)}'
                 f'{T(f"{pct:.1f}%", MONO, 12, bx + bw + 40, y + 4, DIM, "end")}</g>')
        b.append(f'<rect x="{bx + 130}" y="{y - 6}" width="{bw - 130}" height="8" rx="4" fill="{LINE}"/>')
        b.append(f'<rect class="bar" x="{bx + 130}" y="{y - 6}" width="{(bw - 130) * v / langs[0][1]:.1f}" height="8" rx="4" fill="{tones[i]}" style="animation-delay:{.3 + i * .12:.2f}s"/>')
    b.append(T(f'LAST PUSH  {data["last_push"]}', MONO, 10, 8, H - 10, DIM, track=1.4))
    return svg(W, H, "".join(b), css, "", "GitHub stats and most-used languages")


# ───────────────────────────── HEATMAP ──────────────────────────────────────
def heatmap(data):
    cal = data.get("calendar")
    if not cal:
        return None
    H = 232
    weeks = cal["weeks"]
    counts = [d["contributionCount"] for w in weeks for d in w["contributionDays"]]
    nz = sorted(c for c in counts if c > 0)
    q = [nz[int(len(nz) * p)] for p in (.25, .5, .75)] if nz else [1, 2, 3]
    ramp = ["#1C1A17", "#4A3F14", "#8A7119", "#D1AB26", ACC]

    def lvl(c):
        if c == 0: return 0
        return 1 + sum(c > t for t in q)

    total = cal["totalContributions"]
    cs, gap = 13, 3.4
    x0, y0 = 60, 78
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    css = RISE + "@keyframes pop{from{opacity:0;transform:scale(.2)}to{opacity:1;transform:none}}.p{animation:pop .5s cubic-bezier(.2,.7,.3,1) both;transform-box:fill-box;transform-origin:center}"
    b.append(f'<g class="rise">{T(f"{total:,}", SERIF, 64, 8, 62, PAPER, track=-1.5)}'
             f'{T("CONTRIBUTIONS  /  LAST 12 MONTHS", MONOB, 10.5, 8 + width(f"{total:,}", SERIF, 64, -1.5) + 16, 56, DIM, track=1.6)}</g>')
    last_m = None
    for wi, w in enumerate(weeks):
        for d in w["contributionDays"]:
            dt = datetime.date.fromisoformat(d["date"])
            x = x0 + wi * (cs + gap)
            y = y0 + 30 + d["weekday"] * (cs + gap)
            L = lvl(d["contributionCount"])
            b.append(f'<rect class="p" x="{x:.1f}" y="{y:.1f}" width="{cs}" height="{cs}" rx="3" fill="{ramp[L]}" style="animation-delay:{wi * .035 + d["weekday"] * .02:.2f}s"/>')
            if d["weekday"] == 0 and dt.month != last_m and dt.day <= 7:
                last_m = dt.month
                b.append(T(dt.strftime("%b").upper(), MONO, 9, x, y0 + 22, DIM, track=1))
    for lab, wd in (("MON", 1), ("WED", 3), ("FRI", 5)):
        b.append(T(lab, MONO, 8.5, 8, y0 + 30 + wd * (cs + gap) + 10, DIM, track=1))
    gw = len(weeks) * (cs + gap)
    b.append(f'<g style="animation:shine 9s cubic-bezier(.5,0,.5,1) 2s infinite"><rect x="{x0 - 80}" y="{y0 + 24}" width="80" height="{7 * (cs + gap) + 8}" fill="url(#sh)"/></g>')
    css += f"@keyframes shine{{0%{{transform:translateX(0);opacity:0}}6%{{opacity:1}}55%{{opacity:1}}62%,100%{{transform:translateX({gw + 100:.0f}px);opacity:0}}}}"
    # legend
    lx = W - 8 - 5 * 18 - 44
    ly = 40
    b.append(T("LESS", MONO, 8.5, lx - 8, ly + 10, DIM, "end", 1))
    for i, c in enumerate(ramp):
        b.append(f'<rect x="{lx + i * 18}" y="{ly}" width="13" height="13" rx="3" fill="{c}"/>')
    b.append(T("MORE", MONO, 8.5, lx + 5 * 18 + 6, ly + 10, DIM, track=1))
    sh = f'<linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="{PAPER}" stop-opacity="0"/><stop offset=".6" stop-color="{PAPER}" stop-opacity=".22"/><stop offset="1" stop-color="{PAPER}" stop-opacity="0"/></linearGradient>'
    return svg(W, H, "".join(b), css, sh, f"Contribution heatmap — {cal['totalContributions']} contributions in the last year")


# ───────────────────────────── FOOTER (waves) ───────────────────────────────
def wave_path(w, base, amp, wl, phase=0, step=8):
    pts = []
    x = -wl
    d = ""
    first = True
    while x <= w + wl * 2:
        y = base + amp * math.sin((x / wl) * 2 * math.pi + phase)
        d += ("M" if first else "L") + f"{x:.1f},{y:.1f} "
        first = False
        x += step
    return d


def footer():
    H = 360
    wl = 500
    layers = [("#171512", 250, 18, 500, 0, 26), ("#1E1B17", 276, 16, 500, 1.7, 20), ("#26221D", 302, 14, 500, 3.1, 15)]
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    css = RISE
    for i, (col, base, amp, wl_, ph, dur) in enumerate(layers):
        d = wave_path(W, base, amp, wl_, ph) + f"L{W + wl_ * 2:.0f},{H} L{-wl_},{H} Z"
        d = d.replace("M", "M", 1)
        b.append(f'<g style="animation:wv{i} {dur}s linear infinite"><path d="{d}" fill="{col}"/></g>')
        css += f"@keyframes wv{i}{{from{{transform:translateX(0)}}to{{transform:translateX({-wl_}px)}}}}"
    # accent crest line
    d = wave_path(W, 250, 18, 500, 0)
    b.append(f'<g style="animation:wv0 26s linear infinite"><path d="{d}" fill="none" stroke="{ACC}" stroke-width="1.6" stroke-opacity=".9"/></g>')
    a = T("Let's build", SANS, 70, 8, 128, PAPER, track=-2)
    wa = width("Let's build ", SANS, 70, -2)
    c = T("something real.", SERIFI, 88, 8 + wa - 2, 128, ACC, track=-1)
    b.append(f'<g class="rise">{a}{c}</g>')
    b.append(f'<g class="rise" style="animation-delay:.3s">{T("OPEN TO COLLABORATIONS  ·  HARD PROBLEMS  ·  GOOD TEAMS", MONOB, 11.5, 10, 182, DIM, track=2)}</g>')
    return svg(W, H, "".join(b), css, "", "Let's build something real")


def pill(label, accent=False):
    w = width(label, MONOB, 12, 2) + 84
    h = 44
    fill = ACC if accent else "none"
    col = INK if accent else PAPER
    body = (f'<rect width="{w}" height="{h}" rx="22" fill="{INK}"/><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="22" fill="{fill}" stroke="{ACC if accent else LINE2}" stroke-width="1.2"/>'
            + T(label, MONOB, 12, 26, 27, col, track=2) + T("↗", MONOB, 13, w - 26, 27, col, "middle"))
    return svg(int(w), h, body, "", "", label), int(w)
