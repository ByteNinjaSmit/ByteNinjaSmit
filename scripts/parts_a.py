import base64, io, math
from PIL import Image
from lib import *

W = 1000


def dotgrid(id_="g", size=24, col="#27231F"):
    return (f'<pattern id="{id_}" width="{size}" height="{size}" patternUnits="userSpaceOnUse">'
            f'<circle cx="1" cy="1" r="1" fill="{col}"/></pattern>')


# ───────────────────────────── HERO ─────────────────────────────────────────
def hero(data):
    H = 560
    # photo → duotone, embedded
    im = Image.open(__import__("os").path.join(HERE, "src", "photo.jpg")).convert("RGB")
    im = im.resize((456, 608), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=84, optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode()

    roles = ["full-stack engineer", "cloud + devops", "multi-agent llm systems",
             "industrial iot security", "ctf winner / team bugsploit"]
    CYC = 3.7
    TOT = CYC * len(roles)
    tx, ty, fs = 76, 452, 17
    adv = fs * 0.6
    css = [
        f"@keyframes rise{{from{{opacity:0;transform:translateY(26px)}}to{{opacity:1;transform:none}}}}",
        ".rise{animation:rise 1.1s cubic-bezier(.2,.7,.2,1) both}",
        "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}.pulse{animation:pulse 1.8s ease-in-out infinite}",
        "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}.blink{animation:blink 1s steps(1) infinite}",
        "@keyframes scan{0%{transform:translateY(-6px);opacity:0}8%{opacity:1}70%{opacity:1}"
        "85%,100%{transform:translateY(310px);opacity:0}}.scan{animation:scan 4.8s cubic-bezier(.5,0,.3,1) infinite}",
        "@keyframes drift{from{transform:translateX(0)}to{transform:translateX(-24px)}}.drift{animation:drift 3s linear infinite}",
        ".ch{opacity:0}",
        "@keyframes lineDraw{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
        ".ld{transform-origin:0 0;transform-box:fill-box;animation:lineDraw 1.4s cubic-bezier(.6,0,.2,1) .2s both}",
    ]
    typed, cursor_vals, cursor_keys = [], [], []
    n = 0
    for ri, role in enumerate(roles):
        t0 = ri * CYC + 0.25
        cursor_keys.append(ri * CYC / TOT)
        cursor_vals.append(tx)
        for gi, (ci, gx, ga, gd) in enumerate(glyphs(role, MONO, fs, tx, ty)):
            ts = t0 + gi * 0.05
            te = (ri + 1) * CYC - 0.02
            a, b = ts / TOT * 100, te / TOT * 100
            css.append(f"@keyframes c{n}{{0%,{a:.3f}%{{opacity:0}}{a + .001:.3f}%,{b:.3f}%{{opacity:1}}{b + .001:.3f}%,100%{{opacity:0}}}}"
                       f".c{n}{{animation:c{n} {TOT}s linear infinite}}")
            if gd:
                typed.append(f'<path class="ch r{ri} c{n}" d="{gd}" fill="{PAPER}"/>')
            cursor_keys.append(ts / TOT)
            cursor_vals.append(gx + ga)
            n += 1
    css.append("@media (prefers-reduced-motion: reduce){.ch.r0{opacity:1!important}}")
    kt = ";".join(f"{k:.4f}" for k in cursor_keys)
    kv = ";".join(f"{v:.1f}" for v in cursor_vals)

    defs = dotgrid() + f"""
    <clipPath id="ph"><rect x="724" y="92" width="228" height="304" rx="6"/></clipPath>
    <filter id="duo" color-interpolation-filters="sRGB">
      <feColorMatrix type="matrix" values="0.33 0.5 0.17 0 0  0.33 0.5 0.17 0 0  0.33 0.5 0.17 0 0  0 0 0 1 0"/>
      <feComponentTransfer>
        <feFuncR type="table" tableValues="0.07 0.55 0.94"/>
        <feFuncG type="table" tableValues="0.06 0.50 0.92"/>
        <feFuncB type="table" tableValues="0.05 0.42 0.88"/>
      </feComponentTransfer>
    </filter>
    <linearGradient id="trail" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{ACC}" stop-opacity=".38"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/></linearGradient>
    <linearGradient id="fadeb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{INK}" stop-opacity="0"/><stop offset="1" stop-color="{INK}"/></linearGradient>
    """

    b = [f'<rect width="{W}" height="{H}" fill="{INK}"/>',
         f'<g class="drift"><rect x="0" y="0" width="{W + 24}" height="{H}" fill="url(#g)"/></g>']

    # top bar
    b.append(f'<circle class="pulse" cx="52" cy="34" r="4" fill="{OK}"/>')
    b.append(T("SMITRAJ BANKAR  /  PORTFOLIO 2026", MONO, 11.5, 68, 38, DIM, track=1.6))
    b.append(T("MAHARASHTRA, IN  ·  UTC+5:30", MONO, 11.5, 952, 38, DIM, anchor="end", track=1.6))
    b.append(f'<rect class="ld" x="48" y="58" width="904" height="1" fill="{LINE2}"/>')

    # label
    b.append('<g class="rise" style="animation-delay:.15s">' +
             T("SOFTWARE ENGINEER", MONOB, 12.5, 52, 120, ACC, track=2.4) +
             T("FULL-STACK  ·  CLOUD  ·  GENAI  ·  IIOT", MONO, 12.5, 52 + width("SOFTWARE ENGINEER", MONOB, 12.5, 2.4) + 22, 120, DIM, track=1.8) + "</g>")

    # headline
    h1 = T("I build software", SANS, 76, 48, 214, PAPER, track=-2.2)
    h2a = T("that ", SERIFI, 96, 46, 300, ACC, track=-1)
    w_that = width("that ", SERIFI, 96, -1)
    h2b = T("survives", SERIFI, 96, 46 + w_that, 300, ACC, track=-1)
    h3 = T("production.", SANS, 76, 48, 384, PAPER, track=-2.2)
    b.append(f'<g class="rise" style="animation-delay:.3s">{h1}</g>')
    b.append(f'<g class="rise" style="animation-delay:.5s">{h2a}{h2b}</g>')
    b.append(f'<g class="rise" style="animation-delay:.7s">{h3}</g>')
    # underline squiggle under "survives"
    sx = 46 + w_that
    sw = width("survives", SERIFI, 96, -1)
    seg = sw / 14
    x = sx
    d = f"M{x:.1f},310"
    for i in range(14):
        d += f" q{seg / 2:.1f},{-7 if i % 2 == 0 else 7} {seg:.1f},0"
    b.append(f'<path class="ld" d="{d}" fill="none" stroke="{ACC}" stroke-width="2" stroke-linecap="round" style="animation-delay:1.2s"/>')

    # typewriter row
    b.append(T(">", MONOB, fs, 52, ty, ACC))
    b.append("".join(typed))
    b.append(f'<g class="blink"><rect y="{ty - fs + 2}" width="{adv * 0.85:.1f}" height="{fs + 2}" fill="{ACC}" x="{tx}">'
             f'<animate attributeName="x" dur="{TOT}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}" values="{kv}"/></rect></g>')

    # photo card
    px, py, pw, ph = 724, 92, 228, 304
    b.append(f'<g class="rise" style="animation-delay:.45s">')
    b.append(f'<rect x="{px - 12}" y="{py - 12}" width="{pw + 24}" height="{ph + 24}" rx="10" fill="{SURF}" stroke="{LINE2}"/>')
    b.append(f'<image href="data:image/jpeg;base64,{b64}" x="{px}" y="{py}" width="{pw}" height="{ph}" preserveAspectRatio="xMidYMin slice" clip-path="url(#ph)" filter="url(#duo)"/>')
    b.append(f'<g clip-path="url(#ph)"><g class="scan"><rect x="{px}" y="{py - 40}" width="{pw}" height="40" fill="url(#trail)"/>'
             f'<rect x="{px}" y="{py}" width="{pw}" height="1.6" fill="{ACC}"/></g></g>')
    for cx_, cy_, sx_, sy_ in [(px - 12, py - 12, 1, 1), (px + pw + 12, py - 12, -1, 1), (px - 12, py + ph + 12, 1, -1), (px + pw + 12, py + ph + 12, -1, -1)]:
        b.append(f'<path d="M{cx_ + sx_ * 16},{cy_} H{cx_} V{cy_ + sy_ * 16}" fill="none" stroke="{ACC}" stroke-width="2"/>')
    b.append("</g>")
    b.append('<g class="rise" style="animation-delay:.9s">' +
             T("SMITRAJ D. BANKAR", MONOB, 11, px - 12, py + ph + 44, PAPER, track=1.2) +
             T("B.TECH CE  ·  SCOE  ·  2027", MONO, 10, px - 12, py + ph + 61, DIM, track=0.6) + "</g>")

    # metrics strip
    my = 494
    b.append(f'<rect class="ld" x="48" y="{my - 22}" width="904" height="1" fill="{LINE2}" style="animation-delay:.9s"/>')
    mets = [(str(data["repos"]), "PUBLIC REPOSITORIES"), ("8.58", "CGPA  /  B.TECH CE"),
            ("3 + 2", "COPYRIGHTS + DESIGN PATENTS"), ("1st × 2", "CTF + 24-HOUR HACKATHON")]
    xs = [52, 292, 532, 772]
    for i, ((num, lab), x) in enumerate(zip(mets, xs)):
        b.append(f'<g class="rise" style="animation-delay:{1.0 + i * .12:.2f}s">' +
                 T(num, SERIF, 42, x, my + 26, PAPER, track=-0.5) +
                 T(lab, MONO, 9.5, x + 2, my + 46, DIM, track=1.2) + "</g>")
    return svg(W, H, "".join(b), "\n".join(css), defs, "Smitraj Bankar — software engineer: I build software that survives production")


# ───────────────────────────── TICKER ───────────────────────────────────────
def ticker():
    H = 60
    items = ["Python", "TypeScript", "Node.js", "NestJS", "FastAPI", "React", "Next.js", "PostgreSQL", "pgvector",
             "Docker", "AWS", "Redis", "MQTT", "Modbus/TCP", "ESP32", "RAG", "LLM Agents", "Flutter", "Kotlin", "TimescaleDB", "Linux VPS"]
    seq, x = [], 0
    for i, it in enumerate(items):
        italic = i % 3 == 1
        f, sz = (SERIFI, 30) if italic else (SANSM, 21)
        col = ACC if italic else PAPER
        seq.append(T(it, f, sz, x, 38, col, track=0.2 if not italic else 0))
        x += width(it, f, sz) + 26
        seq.append(f'<circle cx="{x - 13:.1f}" cy="30" r="2.5" fill="{LINE2}"/>')
    tw = x
    dur = tw / 38
    group = "".join(seq)
    body = (f'<rect width="{W}" height="{H}" fill="{INK}"/>'
            f'<rect y="0" width="{W}" height="1" fill="{LINE}"/><rect y="{H - 1}" width="{W}" height="1" fill="{LINE}"/>'
            f'<g mask="url(#m)"><g class="t"><g>{group}</g><g transform="translate({tw:.1f},0)">{group}</g></g></g>')
    css = f"@keyframes tk{{to{{transform:translateX(-{tw:.1f}px)}}}}.t{{animation:tk {dur:.1f}s linear infinite}}"
    defs = (f'<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="#000"/><stop offset=".08" stop-color="#fff"/>'
            f'<stop offset=".92" stop-color="#fff"/><stop offset="1" stop-color="#000"/></linearGradient>'
            f'<mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>')
    return svg(W, H, body, css, defs, "Technology ticker")


# ───────────────────────────── SECTION HEADERS ──────────────────────────────
def header(num, a, b, right):
    H = 104
    css = ("@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}"
           ".rise{animation:rise .9s cubic-bezier(.2,.7,.2,1) both}"
           "@keyframes lineDraw{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
           ".ld{transform-origin:0 0;transform-box:fill-box;animation:lineDraw 1.2s cubic-bezier(.6,0,.2,1) .1s both}")
    wn = width(num, MONOB, 13, 2)
    xa = 8
    ta = T(a + " ", SANS, 52, xa, 76, PAPER, track=-1.4)
    xb = xa + width(a + " ", SANS, 52, -1.4)
    tb = T(b, SERIFI, 64, xb, 76, ACC, track=-0.6)
    body = (f'<rect width="{W}" height="{H}" fill="{INK}"/>'
            f'<g class="rise">{T(num, MONOB, 13, 8, 24, ACC, track=2)}{T("/", MONO, 13, 8 + wn + 8, 24, LINE2)}</g>'
            f'<g class="rise" style="animation-delay:.12s">{ta}{tb}</g>'
            f'<g class="rise" style="animation-delay:.3s">{T(right, MONO, 11, 992, 74, DIM, anchor="end", track=1.2)}</g>'
            f'<rect class="ld" x="8" y="94" width="984" height="1" fill="{LINE2}"/>')
    return svg(W, H, body, css, "", f"{num} {a} {b}")
