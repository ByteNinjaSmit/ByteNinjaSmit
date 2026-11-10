import math, random, datetime, re
from lib import *

W = 1000
RISE = ("@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}"
        ".rise{animation:rise .9s cubic-bezier(.2,.7,.2,1) both}"
        "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}.pulse{animation:pulse 1.8s ease-in-out infinite}"
        "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}")


def dotgrid(id_="g", size=24):
    return f'<pattern id="{id_}" width="{size}" height="{size}" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#24211D"/></pattern>'


# ═════════════════════════ CONSTELLATION ════════════════════════════════════
CLUSTERS = [
    ("Agents & ", "GenAI", (230, 228), [
        ("AgentX", 0, -6, 1.0), ("Claim Engine", 82, 36, .8), ("NovaGhost", -78, 30, .7),
        ("KaamSathi", -34, -76, .5), ("KrishiMitra", 48, -74, .5), ("Mental-health AI", 6, 72, .4)]),
    ("Embedded & ", "IIoT", (770, 228), [
        ("Digital Twin", 0, -4, 1.0), ("Balancing bike", 76, 40, .8), ("PathHole", -72, 36, .7),
        ("USV", 40, -76, .5), ("Smart irrigation", -62, -58, .55)]),
    ("Real-world ", "platforms", (230, 520), [
        ("Blood Bank", 0, 0, 1.0), ("Student Sahayyak", 78, 38, .5), ("Hostellers Sahayyak", -76, 34, .5),
        ("Voting system", -52, -66, .4), ("Freelance market", 56, -66, .4)]),
    ("Vision & ", "ML", (770, 520), [
        ("LipNet", -4, -6, 1.0), ("Fake-job detector", 78, 34, .75), ("Used-car pricing", -74, 38, .5),
        ("Health monitor", -38, -72, .4), ("Attendance AIML", 52, -64, .4)]),
]


def constellation():
    H = 730
    random.seed(11)
    core = (500, 385)
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/><rect width="{W}" height="{H}" fill="url(#g)"/>']
    css = RISE + "@keyframes tw{0%,100%{opacity:.35}50%{opacity:1}}@keyframes spin{to{transform:rotate(360deg)}}@keyframes flow{to{stroke-dashoffset:-40}}"
    # spokes from core
    for ci, (_, _, (cx, cy), nodes) in enumerate(CLUSTERS):
        mx, my = (core[0] + cx) / 2, (core[1] + cy) / 2
        bend = 36 if ci % 2 == 0 else -36
        d = f"M{core[0]},{core[1]} Q{mx + bend},{my - bend} {cx},{cy}"
        b.append(f'<path d="{d}" fill="none" stroke="{LINE2}" stroke-width="1" stroke-dasharray="2 6"/>')
        b.append(f'<circle r="3" fill="{ACC}"><animateMotion dur="{3.2 + ci * .5:.1f}s" begin="{ci * .7:.1f}s" repeatCount="indefinite" path="{d}"/>'
                 f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.15;.8;1" dur="{3.2 + ci * .5:.1f}s" begin="{ci * .7:.1f}s" repeatCount="indefinite"/></circle>')
    # clusters
    for ci, (a, bi, (cx, cy), nodes) in enumerate(CLUSTERS):
        R = 112
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{LINE2}" stroke-dasharray="1 9" stroke-linecap="round" stroke-width="2" '
                 f'style="transform-origin:{cx}px {cy}px;animation:spin {90 + ci * 25}s linear infinite{";animation-direction:reverse" if ci % 2 else ""}"/>')
        b.append(f'<circle cx="{cx}" cy="{cy}" r="{R + 14}" fill="none" stroke="{LINE}"/>')
        hub = nodes[0]
        hx, hy = cx + hub[1], cy + hub[2]
        pos = [(cx + dx, cy + dy) for _, dx, dy, _ in nodes]
        # edges: hub to all, plus ring neighbours
        for i in range(1, len(nodes)):
            b.append(f'<line x1="{hx}" y1="{hy}" x2="{pos[i][0]}" y2="{pos[i][1]}" stroke="{LINE2}" stroke-width="1"/>')
            nxt = pos[i % (len(nodes) - 1) + 1]
            b.append(f'<line x1="{pos[i][0]}" y1="{pos[i][1]}" x2="{nxt[0]}" y2="{nxt[1]}" stroke="{LINE}" stroke-width="1"/>')
            b.append(f'<line x1="{hx}" y1="{hy}" x2="{pos[i][0]}" y2="{pos[i][1]}" stroke="{ACC}" stroke-opacity=".55" stroke-width="1" stroke-dasharray="3 37" '
                     f'style="animation:flow {2.4 + i * .3:.1f}s linear infinite"/>')
        for i, ((name, dx, dy, wt), (x, y)) in enumerate(zip(nodes, pos)):
            r = 4 + wt * 6
            dl = random.uniform(0, 3)
            col = ACC if i == 0 else PAPER
            b.append(f'<circle cx="{x}" cy="{y}" r="{r + 7:.1f}" fill="{col}" opacity=".08" style="animation:tw {2.4 + random.random() * 2:.1f}s ease-in-out {dl:.1f}s infinite"/>')
            b.append(f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="{INK}" stroke="{col}" stroke-width="{1.8 if i == 0 else 1.2}"/>')
            b.append(f'<circle cx="{x}" cy="{y}" r="{max(1.6, r / 2.6):.1f}" fill="{col}"/>')
            left = dx < -20 or (dx < 10 and i == 0 and False)
            sz = 10.5 if i == 0 else 9.5
            if i == 0:
                b.append(T(name.upper(), MONOB, sz, x, y + r + 16, ACC, "middle", 1.3))
            elif dy < -60:
                b.append(T(name, MONO, sz, x, y - r - 9, DIM, "middle", .4))
            elif dy > 70:
                b.append(T(name, MONO, sz, x, y + r + 16, DIM, "middle", .4))
            elif dx < 0:
                b.append(T(name, MONO, sz, x - r - 9, y + 3.5, DIM, "end", .4))
            else:
                b.append(T(name, MONO, sz, x + r + 9, y + 3.5, DIM, "start", .4))
        # label
        la = T(a, SANS, 30, 0, 0, PAPER, track=-.8)
        wa = width(a, SANS, 30, -.8)
        wb = width(bi, SERIFI, 38, -.3)
        x0 = cx - (wa + wb) / 2
        ly = cy - R - 30
        b.append(f'<g class="rise" style="animation-delay:{.2 + ci * .15:.2f}s">' + T(a, SANS, 30, x0, ly, PAPER, track=-.8) +
                 T(bi, SERIFI, 38, x0 + wa, ly, ACC, track=-.3) +
                 T(f"{len(nodes):02d} REPOS", MONO, 9.5, cx, ly + 18, DIM, "middle", 2) + "</g>")
    # core
    cx, cy = core
    b.append(f'<circle cx="{cx}" cy="{cy}" r="30" fill="none" stroke="{ACC}" stroke-opacity=".5"><animate attributeName="r" values="28;54;28" dur="3.6s" repeatCount="indefinite"/>'
             f'<animate attributeName="stroke-opacity" values=".6;0;.6" dur="3.6s" repeatCount="indefinite"/></circle>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="28" fill="{INK}" stroke="{ACC}" stroke-width="1.6"/>')
    b.append(T("SB", SERIFI, 30, cx, cy + 10, ACC, "middle", -.5))
    b.append(T("ONE ENGINEER, FOUR DOMAINS", MONO, 9, cx, cy + 50, DIM, "middle", 1.6))
    # stars
    for _ in range(46):
        x, y = random.uniform(10, W - 10), random.uniform(10, H - 10)
        b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.choice([.6, .8, 1.1])}" fill="{PAPER}" opacity=".5" style="animation:tw {2 + random.random() * 4:.1f}s ease-in-out {random.random() * 3:.1f}s infinite"/>')
    return svg(W, H, "".join(b), css, dotgrid(), "Map of the work: four domains — GenAI agents, embedded and IIoT, real-world platforms, vision and ML")


# ═════════════════════════ TIMELINE ═════════════════════════════════════════
MILES = [
    ("DEC 2019", "Joined GitHub", "Day one of seven years", ""),
    ("2023", "B.Tech, Comp. Engg.", "Sanjivani College of Engg.", ""),
    ("MAR 2025", "10-hour build", "Solo ticketing for a 3,000+ concert", ""),
    ("AUG 2025", "Karmacts Systems", "NestJS · Next.js · 5 ERP modules", ""),
    ("DEC 2025", "Events platform lead", "Digital ordering + vendors", ""),
    ("MAR 2026", "Twistark Technologies", "3+ client platforms, end to end", ""),
    ("JUL 2026", "2 design patents", "Saffron robot · SmartMediTrack", ""),
    ("AUG 2026", "AgentX takes 1st", "24-hour AI hackathon", ""),
    ("OCT 2026", "CTF champions", "Cyber Quest · team Bugsploit", ""),
    ("NOW", "NextGen Rakshak", "Edge-AI lost-child recovery", "TEAM LEAD"),
]


def timeline():
    H = 440
    ly = 220
    x0, x1 = 84, 916
    n = len(MILES)
    xs = [x0 + i * (x1 - x0) / (n - 1) for i in range(n)]
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    css = RISE + ("@keyframes draw{from{stroke-dashoffset:900}to{stroke-dashoffset:0}}"
                  "@keyframes pop{from{opacity:0;transform:scale(.1)}to{opacity:1;transform:none}}"
                  ".pop{transform-box:fill-box;transform-origin:center;animation:pop .6s cubic-bezier(.2,.9,.3,1.4) both}")
    b.append(f'<line x1="{x0}" y1="{ly}" x2="{x1}" y2="{ly}" stroke="{LINE2}" stroke-width="2"/>')
    b.append(f'<line x1="{x0}" y1="{ly}" x2="{x1}" y2="{ly}" stroke="{ACC}" stroke-width="2" stroke-dasharray="900" style="animation:draw 3.2s cubic-bezier(.5,0,.2,1) .2s both"/>')
    b.append(f'<circle r="4" fill="{PAPER}"><animateMotion dur="7s" begin="3.4s" repeatCount="indefinite" path="M{x0},{ly} L{x1},{ly}"/>'
             f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.9;1" dur="7s" begin="3.4s" repeatCount="indefinite"/></circle>')
    for i, ((date, title, sub, tag), x) in enumerate(zip(MILES, xs)):
        up = i % 2 == 0
        delay = .2 + i / (n - 1) * 3.2
        now = i == n - 1
        stem = 56
        ey = ly - stem if up else ly + stem
        b.append(f'<line x1="{x:.1f}" y1="{ly}" x2="{x:.1f}" y2="{ey}" stroke="{ACC if now else LINE2}" stroke-width="1" style="animation:rise .6s ease {delay:.2f}s both"/>')
        if now:
            b.append(f'<circle cx="{x:.1f}" cy="{ly}" r="10" fill="none" stroke="{ACC}"><animate attributeName="r" values="8;22;8" dur="2.4s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values=".9;0;.9" dur="2.4s" repeatCount="indefinite"/></circle>')
        b.append(f'<g class="pop" style="animation-delay:{delay:.2f}s"><circle cx="{x:.1f}" cy="{ly}" r="{8 if now else 6}" fill="{ACC if now else INK}" stroke="{ACC}" stroke-width="2"/></g>')
        # label block
        al = "middle"
        ty = 0
        g = [T(date, MONOB, 10.5, x, ty + 12, ACC, al, 1.6)]
        tl = title.split(" ")
        # wrap title to <=16 chars/line
        lines, cur = [], ""
        for w_ in tl:
            if len(cur) + len(w_) + 1 > 17 and cur:
                lines.append(cur)
                cur = w_
            else:
                cur = (cur + " " + w_).strip()
        lines.append(cur)
        for li, ln in enumerate(lines):
            g.append(T(ln, SANSM, 16, x, ty + 34 + li * 18, PAPER, al, -.2))
        by = ty + 34 + len(lines) * 18 + 4
        sl, cur = [], ""
        for w_ in sub.split(" "):
            if len(cur) + len(w_) + 1 > 21 and cur:
                sl.append(cur)
                cur = w_
            else:
                cur = (cur + " " + w_).strip()
        sl.append(cur)
        for li, ln in enumerate(sl):
            g.append(T(ln, MONO, 9, x, by + 8 + li * 13, DIM, al, .1))
        if tag:
            tw = width(tag, MONOB, 8.5, 1.4) + 16
            py = by + 8 + len(sl) * 13 + 2
            g.append(f'<rect x="{x - tw / 2:.1f}" y="{py:.1f}" width="{tw:.1f}" height="17" rx="8.5" fill="{ACC}"/>')
            g.append(T(tag, MONOB, 8.5, x, py + 11.8, INK, al, 1.4))
        bh = (by - ty) + 8 + len(sl) * 13 + (26 if tag else 0)
        Y = (ey - 10 - bh) if up else (ey + 14)
        b.append(f'<g class="rise" style="animation-delay:{delay + .25:.2f}s"><g transform="translate(0,{Y:.1f})">{"".join(g)}</g></g>')
    b.append(T("CHRONOLOGICAL — NOT TO SCALE", MONO, 9.5, 60, H - 14, DIM, track=1.8))
    return svg(W, H, "".join(b), css, "", "Career timeline from joining GitHub in 2019 to NextGen Rakshak today")


# ═════════════════════════ LIVE TERMINAL ════════════════════════════════════
def _clean(s):
    return re.sub(r"[^\x20-\x7e·→—]", "?", s)


def _ago(iso):
    t = datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    s = (datetime.datetime.now(datetime.timezone.utc) - t).total_seconds()
    if s < 3600:
        return f"{max(1, int(s // 60))}m ago"
    if s < 86400:
        return f"{int(s // 3600)}h ago"
    return f"{int(s // 86400)}d ago"


def terminal(data):
    fs, adv, lh = 13.5, 13.5 * 0.6, 24
    x0, y0 = 40, 104
    cal = data.get("calendar") or {}
    lines = []  # list of (segments[(text,fill)], speed)
    lines.append(([("$ ", ACC), ("whoami", PAPER)], .06))
    lines.append(([("smitraj bankar · software engineer · b.tech ce '27 @ scoe", DIM)], .016))
    lines.append(([("$ ", ACC), ("cat now.txt", PAPER)], .06))
    lines.append(([("→ ", ACC), ("leading NextGen Rakshak: edge-ai lost-child recovery", DIM)], .016))
    lines.append(([("→ ", ACC), ("shipping client platforms @ twistark technologies", DIM)], .016))
    lines.append(([("$ ", ACC), ("git log --oneline -5", PAPER), ("   # live from the api", "#6B655A")], .05))
    for r in (data.get("recent") or [])[:5]:
        msg = _clean(r["msg"])
        msg = msg if len(msg) <= 50 else msg[:49] + "…"
        msg = msg.replace("…", "...")
        lines.append(([(r["sha"] + "  ", ACC), (f"{msg:<53}", PAPER), (f"{_clean(r['repo'])[:24]:<24} {_ago(r['at'])}", DIM)], .012))
    lines.append(([("$ ", ACC), ("uptime", PAPER)], .06))
    tot = cal.get("totalContributions", 0)
    lines.append(([(f"{datetime.date.today().year - data['since']}y on github · {data['repos']} public repos · {tot:,} contributions / 12 months", DIM)], .016))
    lines.append(([("$ ", ACC)], .06))

    H = y0 + len(lines) * lh + 34
    # timing
    t = 0.7
    sched = []
    for segs, sp in lines:
        n = sum(len(s) for s, _ in segs)
        sched.append((t, sp, n))
        t += n * sp + 0.38
    HOLD = 7.0
    TOT = round(t + HOLD, 2)
    reset = TOT - 0.9
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/><rect width="{W}" height="{H}" fill="url(#g)"/>']
    # window
    b.append(f'<rect x="8" y="8" width="{W - 16}" height="{H - 16}" rx="14" fill="{SURF}" stroke="{LINE2}"/>')
    b.append(f'<path d="M8,52 H{W - 8}" stroke="{LINE2}"/>')
    for i, c in enumerate(["#3A352E", "#3A352E", "#3A352E"]):
        b.append(f'<circle cx="{34 + i * 20}" cy="30" r="5.5" fill="{c}"/>')
    b.append(f'<circle cx="34" cy="30" r="5.5" fill="{ACC}"/>')
    b.append(T("smitraj@twistark: ~/profile — zsh", MONO, 11, W / 2, 34, DIM, "middle", .8))
    b.append(f'<circle class="pulse" cx="{W - 96}" cy="30" r="3.5" fill="{OK}"/>')
    b.append(T("LIVE", MONOB, 9.5, W - 86, 33.5, OK, track=1.6))
    # lines
    cur_k, cur_v = [0.0], [f"{x0},{y0 - fs}"]
    defs = [dotgrid()]
    for li, ((segs, sp), (ts, _, n)) in enumerate(zip(lines, sched)):
        y = y0 + li * lh
        cx = x0
        g = []
        for text, fill in segs:
            g.append(T(text, MONO, fs, cx, y, fill))
            cx += len(text) * adv
        # clip width steps
        kt, vals = [0.0], [0.0]
        for k in range(1, n + 1):
            kt.append((ts + k * sp) / TOT)
            vals.append(round(k * adv + 0.5, 1))
            cur_k.append((ts + k * sp) / TOT)
            cur_v.append(f"{x0 + k * adv:.1f},{y - fs}")
        kt.append(reset / TOT)
        vals.append(0.0)
        cur_k.append(reset / TOT)
        cur_v.append(f"{x0},{y0 - fs}")
        defs.append(f'<clipPath id="c{li}"><rect x="{x0 - 2}" y="{y - fs - 3}" width="0" height="{lh}">'
                    f'<animate attributeName="width" dur="{TOT}s" repeatCount="indefinite" calcMode="discrete" '
                    f'keyTimes="{";".join(f"{k:.5f}" for k in kt)}" values="{";".join(str(v) for v in vals)}"/></rect></clipPath>')
        b.append(f'<g clip-path="url(#c{li})">{"".join(g)}</g>')
    # cursor (xy discrete)
    # ensure strictly increasing keyTimes
    pk, pv = [], []
    last = -1
    for k, v in sorted(zip(cur_k, cur_v), key=lambda z: z[0]):
        k = max(k, last + 1e-6)
        pk.append(k)
        pv.append(v)
        last = k
    pk[0] = 0.0
    xs_ = [v.split(",")[0] for v in pv]
    ys_ = [v.split(",")[1] for v in pv]
    kts = ";".join(f"{k:.6f}" for k in pk)
    b.append(f'<g style="animation:blink 1.05s steps(1) infinite"><rect width="{adv * .9:.1f}" height="{fs + 3}" fill="{ACC}">'
             f'<animate attributeName="x" dur="{TOT}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kts}" values="{";".join(xs_)}"/>'
             f'<animate attributeName="y" dur="{TOT}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kts}" values="{";".join(ys_)}"/></rect></g>')
    return svg(W, H, "".join(b), RISE, "".join(defs), "Live terminal: whoami, now, latest git commits, uptime")


# ═════════════════════════ HALFTONE PORTRAIT + FOOTER ═══════════════════════
def halftone(x0, y0, h, pitch=6):
    """Photo -> vector dots. Returns (svg_group, n_dots, width)."""
    from PIL import Image
    import os
    im = Image.open(os.path.join(HERE, "src", "photo2.jpg")).convert("RGB")
    crop = im.crop((120, 110, 780, 900))
    cols, rows = crop.width // pitch, crop.height // pitch
    small = crop.resize((cols, rows), Image.BOX)
    sc = h / (rows * pitch)
    w = cols * pitch * sc
    rmax = pitch * sc * 0.54
    NB = 12
    bands = {}
    n = 0
    for r in range(rows):
        for c in range(cols):
            R, G, B = small.getpixel((c, r))
            lum = .299 * R + .587 * G + .114 * B
            warm = R - B
            if lum < 95:
                tone, rad = "hair", rmax * (.20 + .32 * lum / 95)
            elif warm > 30:
                tone, rad = "skin", rmax * min(.98, max(.30, (lum / 190) ** 1.1 * .95))
            elif r > rows * .66 and lum > 215:
                tone, rad = "shirt", rmax * min(.95, (lum - 150) / 105)
            else:
                continue
            x = x0 + (c + .5) * pitch * sc
            y = y0 + (r + .5) * pitch * sc
            band = min(NB - 1, int(c / cols * NB))
            bands.setdefault((band, tone), []).append(
                f"M{x - rad:.1f} {y:.1f}a{rad:.1f} {rad:.1f} 0 1 0 {2 * rad:.1f} 0a{rad:.1f} {rad:.1f} 0 1 0 -{2 * rad:.1f} 0")
            n += 1
    fills = {"hair": "#8F897D", "skin": ACC, "shirt": PAPER}
    parts = []
    for (band, tone), segs in sorted(bands.items()):
        parts.append(f'<path class="dots" style="animation-delay:{.3 + band * .11:.2f}s" fill="{fills[tone]}" d="{"".join(segs)}"/>')
    return "".join(parts), n, w


def footer2():
    H = 460
    css = RISE + ("@keyframes dot{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}"
                  ".dots{animation:dot .9s cubic-bezier(.2,.7,.2,1) both}"
                  "@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}"
                  "@keyframes breathe{0%,100%{opacity:.55;transform:scale(1)}50%{opacity:1;transform:scale(1.08)}}")
    ph = 372
    grp, n, pw = halftone(0, 0, ph)
    px, py = 640, 36
    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>']
    b.append(f'<circle cx="{px + pw / 2:.0f}" cy="{py + 160}" r="190" fill="url(#gl)" style="transform-origin:{px + pw / 2:.0f}px {py + 160}px;animation:breathe 5s ease-in-out infinite"/>')
    b.append(f'<g transform="translate({px},{py})"><g style="animation:float 7s ease-in-out infinite">{grp}</g></g>')
    # waves over the shoulders
    layers = [("#171512", 336, 18, 500, 0, 26), ("#1E1B17", 362, 16, 500, 1.7, 20), ("#26221D", 388, 14, 500, 3.1, 15)]
    from parts_c import wave_path
    for i, (col, base, amp, wl, ph_, dur) in enumerate(layers):
        d = wave_path(W, base, amp, wl, ph_) + f"L{W + wl * 2:.0f},{H} L{-wl},{H} Z"
        b.append(f'<g style="animation:wv{i} {dur}s linear infinite"><path d="{d}" fill="{col}"/></g>')
        css += f"@keyframes wv{i}{{from{{transform:translateX(0)}}to{{transform:translateX({-wl}px)}}}}"
    b.append(f'<g style="animation:wv0 26s linear infinite"><path d="{wave_path(W, 336, 18, 500, 0)}" fill="none" stroke="{ACC}" stroke-width="1.6"/></g>')
    # copy
    b.append(f'<g class="rise">{T("Let’s build".replace("’", chr(39)), SANS, 66, 8, 108, PAPER, track=-2)}</g>')
    b.append(f'<g class="rise" style="animation-delay:.2s">{T("something real.", SERIFI, 92, 6, 200, ACC, track=-1)}</g>')
    b.append(f'<g class="rise" style="animation-delay:.4s">{T("OPEN TO COLLABORATIONS  ·  HARD PROBLEMS  ·  GOOD TEAMS", MONOB, 11.5, 10, 246, DIM, track=2)}</g>')
    b.append(f'<g class="rise" style="animation-delay:.6s">{T(f"FIG. 01  —  THIS PORTRAIT IS {n:,} VECTOR DOTS. NO IMAGE FILE.", MONO, 9.5, 10, 276, LINE2, track=1.6)}</g>')
    gdef = f'<radialGradient id="gl"><stop offset="0" stop-color="{ACC}" stop-opacity=".38"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/></radialGradient>'
    return svg(W, H, "".join(b), css, gdef, "Let's build something real. Halftone dot portrait of Smitraj Bankar rising from animated waves.")
