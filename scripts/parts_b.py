import math, random
from lib import *

CW, CH = 480, 340

BASE_CSS = (
    "@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}"
    ".rise{animation:rise .8s cubic-bezier(.2,.7,.2,1) both}"
    "@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}.pulse{animation:pulse 1.8s ease-in-out infinite}"
    "@keyframes spin{to{transform:rotate(360deg)}}"
    "@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}"
)


def frame(idx, tag, status, bold, ital, desc, stack, viz, css="", defs="", title=""):
    b = [f'<rect x="0.5" y="0.5" width="{CW - 1}" height="{CH - 1}" rx="16" fill="{SURF}" stroke="{LINE2}"/>',
         # faint grid
         f'<rect x="1" y="1" width="{CW - 2}" height="{CH - 2}" rx="16" fill="url(#cg)" opacity=".7"/>']
    b.append(T(f"{idx:02d}", MONOB, 11, 28, 40, ACC, track=1.5))
    b.append(T("—  " + tag, MONO, 11, 28 + 24, 40, DIM, track=1.6))
    # status pill
    sw = width(status, MONOB, 9.5, 1.4) + 30
    b.append(f'<rect x="{CW - 28 - sw}" y="26" width="{sw}" height="20" rx="10" fill="none" stroke="{LINE2}"/>')
    b.append(f'<circle class="pulse" cx="{CW - 28 - sw + 12}" cy="36" r="3" fill="{OK if status in ("LIVE", "IN PRODUCTION") else ACC}"/>')
    b.append(T(status, MONOB, 9.5, CW - 28 - sw + 22, 39.5, PAPER, track=1.4))
    # title
    t1 = T(bold + " ", SANS, 34, 26, 90, PAPER, track=-1)
    x2 = 26 + width(bold + " ", SANS, 34, -1)
    t2 = T(ital, SERIFI, 42, x2, 90, ACC, track=-0.5)
    b.append(f'<g class="rise">{t1}{t2}</g>')
    for i, line in enumerate(desc):
        b.append(T(line, MONO, 11.5, 28, 118 + i * 17, DIM))
    b.append(viz)
    b.append(f'<rect x="28" y="{CH - 44}" width="{CW - 56}" height="1" fill="{LINE}"/>')
    b.append(T(stack, MONO, 10.5, 28, CH - 21, PAPER, track=0.4))
    b.append(T("OPEN ↗", MONOB, 10.5, CW - 28, CH - 21, ACC, anchor="end", track=1.4))
    d = defs + f'<pattern id="cg" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".8" fill="#24211D"/></pattern>'
    return svg(CW, CH, "".join(b), BASE_CSS + css, d, title)


# ── 01 AgentX ────────────────────────────────────────────────────────────────
def card_agentx():
    ox, oy = 92, 224
    lanes = [("PAPERS", 176), ("PATENTS", 203), ("NEWS", 230), ("SOCIAL", 257)]
    v = [f'<circle cx="{ox}" cy="{oy}" r="21" fill="{INK}" stroke="{ACC}" stroke-width="1.5"/>',
         f'<circle cx="{ox}" cy="{oy}" r="31" fill="none" stroke="{LINE2}" stroke-dasharray="3 6" style="transform-origin:{ox}px {oy}px;animation:spin 14s linear infinite"/>',
         f'<circle cx="{ox}" cy="{oy}" r="6" fill="{ACC}"><animate attributeName="r" values="5;8;5" dur="2s" repeatCount="indefinite"/></circle>',
         T("ORCHESTRATOR", MONO, 8.5, ox, 276, DIM, "middle", 1.2)]
    css = ""
    for i, (lab, y) in enumerate(lanes):
        path = f"M{ox + 22},{oy} C{ox + 110},{oy} {ox + 120},{y} 278,{y}"
        v.append(f'<path d="{path}" fill="none" stroke="{LINE2}" stroke-width="1.2"/>')
        v.append(f'<circle r="3.2" fill="{ACC}"><animateMotion dur="2.6s" begin="{i * .55:.2f}s" repeatCount="indefinite" path="{path}" keyPoints="0;1" keyTimes="0;1" calcMode="linear"/>'
                 f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.85;1" dur="2.6s" begin="{i * .55:.2f}s" repeatCount="indefinite"/></circle>')
        v.append(f'<circle cx="278" cy="{y}" r="2.5" fill="{PAPER}"/>')
        v.append(T(lab, MONOB, 10.5, 290, y + 3.5, PAPER, track=1.2))
        fill = [.92, .64, .78, .46][i]
        v.append(f'<rect x="372" y="{y - 2}" width="80" height="4" rx="2" fill="{LINE}"/>')
        v.append(f'<rect x="372" y="{y - 2}" width="{80 * fill:.1f}" height="4" rx="2" fill="{ACC}" style="transform-origin:372px {y}px;animation:grow{i} 5.2s cubic-bezier(.5,0,.2,1) {i * .25}s infinite"/>')
        css += f"@keyframes grow{i}{{0%{{transform:scaleX(0)}}30%,85%{{transform:scaleX(1)}}100%{{transform:scaleX(0)}}}}"
    v.append(T("SCORE", MONO, 8.5, 412, 158, DIM, "middle", 1.2))
    return frame(1, "MULTI-AGENT / LLM", "LIVE", "AgentX", "intelligence",
                 ["Researches papers, patents, news & social for a goal,", "scores every finding, alerts only on new high-impact signal."],
                 "Python · LLM agents · TypeScript · Docker", "".join(v), css, title="AgentX — autonomous competitive-intelligence agent")


# ── 02 Aptino claim engine ───────────────────────────────────────────────────
def card_aptino():
    v = []
    dx, dy, dw, dh = 40, 152, 112, 124
    v.append(f'<rect x="{dx}" y="{dy}" width="{dw}" height="{dh}" rx="6" fill="{INK}" stroke="{LINE2}"/>')
    v.append(T("POLICY.PDF", MONO, 8.5, dx + 10, dy + 16, DIM, track=1.2))
    ws = [78, 90, 66, 84, 72, 88, 58, 80]
    css = ""
    for i, w_ in enumerate(ws):
        y = dy + 28 + i * 11.5
        v.append(f'<rect x="{dx + 10}" y="{y}" width="{w_}" height="4" rx="2" fill="{LINE2}"/>')
    hits = [(1, 0.0), (4, 1.0), (6, 2.0)]
    for k, (li, dl) in enumerate(hits):
        y = dy + 28 + li * 11.5
        v.append(f'<rect x="{dx + 8}" y="{y - 3}" width="{ws[li] + 4}" height="10" rx="3" fill="{ACC}" opacity="0" style="animation:hit{k} 9s linear infinite"/>')
        a = (dl) / 9 * 100
        css += f"@keyframes hit{k}{{0%,{a:.1f}%{{opacity:0}}{a + 3:.1f}%,38%{{opacity:.5}}46%,100%{{opacity:0}}}}"
    # link arrow
    v.append(f'<path d="M158,214 C190,214 196,214 244,214" stroke="{LINE2}" stroke-width="1.2" fill="none" stroke-dasharray="3 4"/>')
    v.append(f'<path d="M240,209 l7,5 -7,5" stroke="{ACC}" stroke-width="1.4" fill="none"/>')
    v.append(f'<circle r="3" fill="{ACC}"><animateMotion dur="1.8s" repeatCount="indefinite" path="M158,214 L244,214"/></circle>')
    v.append(T("HYBRID", MONO, 8.5, 201, 202, DIM, "middle", 1.2))
    v.append(T("RETRIEVAL", MONO, 8.5, 201, 238, DIM, "middle", 1.2))
    # verdict
    vx, vy, vw, vh = 254, 160, 198, 108
    v.append(f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="8" fill="{INK}" stroke="{LINE2}"/>')
    v.append(T("VERDICT", MONO, 8.5, vx + 14, vy + 20, DIM, track=1.4))
    states = [("ADMISSIBLE", ACC), ("NOT ADMISSIBLE", PAPER), ("ABSTAIN", DIM)]
    subs = ["evidence + citation found", "clause excludes this claim", "evidence insufficient — no guess"]
    for i, ((txt, col), sub) in enumerate(zip(states, subs)):
        v.append(f'<g style="animation:st{i} 9s linear infinite;opacity:0">' +
                 T(txt, SANS, 21 if len(txt) < 12 else 18, vx + vw / 2, vy + 63, col, "middle", -.4) +
                 T(sub, MONO, 9, vx + vw / 2, vy + 88, DIM, "middle", .2) + "</g>")
        a, b = i * 33.33, (i + 1) * 33.33
        css += f"@keyframes st{i}{{0%,{a:.2f}%{{opacity:0}}{a + 2.5:.2f}%,{b - 3:.2f}%{{opacity:1}}{b - .5:.2f}%,100%{{opacity:0}}}}"
        if i == 0:
            css = css.replace(f"@keyframes st0{{0%,0.00%{{opacity:0}}", "@keyframes st0{0%{opacity:0}")
    return frame(2, "RAG / MULTI-AGENT", "LIVE", "Claim", "engine",
                 ["Health-insurance claim admissibility against a policy PDF —", "inspectable citations, and it abstains when evidence is thin."],
                 "Python · hybrid retrieval · multi-agent · Docker", "".join(v), css, title="Aptino claim engine")


# ── 03 Digital twin ──────────────────────────────────────────────────────────
def card_twin():
    x0, x1 = 30, 450
    cy = 214
    random.seed(7)
    pred, meas = [], []
    for i in range(0, 85):
        x = x0 + i * (x1 - x0) / 84
        p = cy + 17 * math.sin(i / 5.5) + 5 * math.sin(i / 2.1)
        m = p + random.uniform(-1.6, 1.6)
        if 50 <= i <= 66:
            k = ease(min(1, (i - 50) / 4)) * ease(min(1, (66 - i) / 4 + .0))
            m += k * (-30 + 6 * math.sin(i))
        pred.append((x, p))
        meas.append((x, m))
    f = lambda pts: " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    ax0, ax1 = x0 + 50 * (x1 - x0) / 84, x0 + 66 * (x1 - x0) / 84
    v = [f'<rect x="{ax0:.1f}" y="156" width="{ax1 - ax0:.1f}" height="106" fill="{ACC}" opacity=".08"/>',
         f'<path d="M{ax0:.1f},156 V262 M{ax1:.1f},156 V262" stroke="{ACC}" stroke-opacity=".35" stroke-dasharray="2 4"/>',
         T("ATTACK WINDOW", MONO, 8.5, (ax0 + ax1) / 2, 169, ACC, "middle", 1.2),
         f'<polyline points="{f(pred)}" fill="none" stroke="{DIM}" stroke-width="1.4" stroke-dasharray="4 4"/>',
         f'<polyline points="{f(meas)}" fill="none" stroke="{PAPER}" stroke-width="1.8" stroke-linejoin="round"/>',
         f'<g style="animation:sweep 6s linear infinite"><rect x="{x0}" y="152" width="1.5" height="114" fill="{ACC}"/><rect x="{x0 - 26}" y="152" width="26" height="114" fill="url(#sg)"/></g>',
         f'<g style="animation:flag 6s linear infinite;opacity:0"><rect x="{ax1 + 6:.1f}" y="196" width="104" height="22" rx="5" fill="{ACC}"/>' +
         T("DETECTED", MONOB, 10.5, ax1 + 6 + 52, 211, INK, "middle", 1.6) + "</g>",
         T("— PHYSICS (predicted)", MONO, 8.5, 30, 281, DIM, track=.8),
         T("— MEASURED", MONO, 8.5, 175, 281, PAPER, track=.8),
         T("9/9 attacks  ·  F1 0.897  ·  0% FP", MONOB, 8.5, 450, 281, ACC, "end", .8)]
    ts = (ax0 - x0 + 8) / (x1 - x0)
    css = (f"@keyframes sweep{{from{{transform:translateX(0)}}to{{transform:translateX({x1 - x0}px)}}}}"
           f"@keyframes flag{{0%,{ts * 100 + 3:.1f}%{{opacity:0}}{ts * 100 + 6:.1f}%,{ts * 100 + 24:.1f}%{{opacity:1}}{ts * 100 + 27:.1f}%,100%{{opacity:0}}}}")
    defs = f'<linearGradient id="sg" x1="0" x2="1"><stop offset="0" stop-color="{ACC}" stop-opacity="0"/><stop offset="1" stop-color="{ACC}" stop-opacity=".22"/></linearGradient>'
    return frame(3, "IIOT / SECURITY", "OPEN SOURCE", "Digital", "twin",
                 ["Real-time twin of a 4-stage production line. Detects attacks", "by comparing what the PLC is told with what physics predicts."],
                 "Python · FastAPI · MQTT · Modbus · TimescaleDB", "".join(v), css, defs, title="Digital twin for cyber-attack detection in IIoT")


# ── 04 Self-balancing bicycle ────────────────────────────────────────────────
def card_bike():
    px, py = 190, 262
    ang = [-13, 9, -5.5, 3, -1.5, 0, 0, -13]
    kt = "0;.1;.2;.3;.4;.5;.92;1"
    rot = ";".join(f"{a} {px} {py}" for a in ang)
    sp = ";".join(["0.42 0 0.58 1"] * 7)
    wheel = lambda cx: (f'<circle cx="{cx}" cy="{py - 32}" r="32" fill="none" stroke="{PAPER}" stroke-width="2"/>'
                        f'<circle cx="{cx}" cy="{py - 32}" r="2.5" fill="{PAPER}"/>'
                        + "".join(f'<line x1="{cx}" y1="{py - 32}" x2="{cx + 32 * math.cos(a):.1f}" y2="{py - 32 + 32 * math.sin(a):.1f}" stroke="{LINE2}"/>' for a in [i * math.pi / 4 for i in range(8)]))
    A, B = (px - 40, py - 32), (px + 40, py - 32)
    bb, seat, head = (px - 4, py - 32), (px - 22, py - 78), (px + 24, py - 78)
    frame_ = (f'<path d="M{A[0]},{A[1]} L{bb[0]},{bb[1]} L{seat[0]},{seat[1]} L{head[0]},{head[1]} L{B[0]},{B[1]} M{bb[0]},{bb[1]} L{head[0]},{head[1]}" '
              f'fill="none" stroke="{ACC}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"/>'
              f'<path d="M{head[0] - 4},{head[1] - 8} h10 M{seat[0] - 8},{seat[1] - 3} h14" stroke="{PAPER}" stroke-width="2.4" stroke-linecap="round"/>')
    rw = (f'<g transform="translate({px - 2},{py - 98})"><circle r="12" fill="{INK}" stroke="{ACC}" stroke-width="1.5"/>'
          f'<g><line x1="-12" x2="12" stroke="{ACC}"/><line y1="-12" y2="12" stroke="{ACC}"/>'
          f'<animateTransform attributeName="transform" type="rotate" values="0;360" dur="1.1s" repeatCount="indefinite"/></g></g>')
    v = [f'<path d="M30,{py} H450" stroke="{LINE2}"/>',
         f'<g><animateTransform attributeName="transform" type="rotate" values="{rot}" keyTimes="{kt}" calcMode="spline" keySplines="{sp}" dur="6s" repeatCount="indefinite"/>'
         f'{wheel(A[0])}{wheel(B[0])}{frame_}{rw}</g>']
    # tilt gauge
    gx, gy = 340, 216
    v.append(T("TILT", MONOB, 9, gx + 55, gy - 22, DIM, "middle", 1.6))
    v.append(f'<line x1="{gx}" y1="{gy}" x2="{gx + 110}" y2="{gy}" stroke="{LINE2}" stroke-width="1.5"/>'
             f'<path d="M{gx + 55},{gy - 7} v14" stroke="{DIM}"/>')
    cxs = ";".join(f"{gx + 55 + a * 3.8:.1f}" for a in ang)
    v.append(f'<circle cy="{gy}" r="5" fill="{ACC}"><animate attributeName="cx" values="{cxs}" keyTimes="{kt}" calcMode="spline" keySplines="{sp}" dur="6s" repeatCount="indefinite"/></circle>')
    v.append(T("PID RECOVERY", MONO, 8.5, gx + 55, gy + 28, DIM, "middle", 1.2))
    return frame(4, "EMBEDDED / CONTROL", "OPEN SOURCE", "Balancing", "bicycle",
                 ["Steers into the fall, reaction wheel for momentum,", "FreeRTOS + independent safety supervisor on ESP32."],
                 "C++ · ESP32 · MPU6050 · FreeRTOS · WebSocket", "".join(v), title="Self-balancing bicycle")


# ── 05 NovaGhost ─────────────────────────────────────────────────────────────
def card_nova():
    wx, wy, ww, wh = 34, 152, 270, 120
    v = [f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="8" fill="{INK}" stroke="{LINE2}"/>',
         f'<circle cx="{wx + 14}" cy="{wy + 12}" r="3" fill="{LINE2}"/><circle cx="{wx + 26}" cy="{wy + 12}" r="3" fill="{LINE2}"/><circle cx="{wx + 38}" cy="{wy + 12}" r="3" fill="{LINE2}"/>']
    ws = [190, 150, 220, 120, 200, 170, 140]
    for i, w_ in enumerate(ws):
        v.append(f'<rect x="{wx + 16}" y="{wy + 30 + i * 12.5}" width="{w_}" height="4" rx="2" fill="{LINE2}"/>')
    sx, sy, sw, sh = wx + 50, wy + 42, 140, 42
    v.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="{ACC}" fill-opacity=".1" stroke="{ACC}" stroke-dasharray="5 4" style="animation:sel 8s linear infinite;opacity:0"/>')
    tx, ty = sx + sw / 2, sy + sh / 2
    for i in range(3):
        v.append(f'<circle cx="{tx}" cy="{ty}" r="4" fill="none" stroke="{ACC}" stroke-width="1.6" style="transform-origin:{tx}px {ty}px;animation:rip 8s linear {i * .32:.2f}s infinite;opacity:0"/>')
    # bubble
    bx, by, bw, bh = 252, 168, 204, 92
    bub = [f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="{SURF2}" stroke="{ACC}"/>',
           f'<circle cx="{bx + 16}" cy="{by + 16}" r="4" fill="{ACC}"/>' + T("AI OVERLAY", MONOB, 8.5, bx + 26, by + 19.5, ACC, track=1.4)]
    for i, w_ in enumerate([164, 150, 172, 96]):
        bub.append(f'<rect x="{bx + 16}" y="{by + 34 + i * 13}" width="{w_}" height="5" rx="2.5" fill="{PAPER}" opacity=".85" style="transform-origin:{bx + 16}px 0;animation:ty 8s linear {i * .45:.2f}s infinite"/>')
    v.append(f'<g style="animation:bub 8s linear infinite;opacity:0">{"".join(bub)}</g>')
    v.append(T("triple-tap  →  region  →  answer", MONO, 9, 30, 289, DIM, track=.8))
    css = ("@keyframes rip{0%,4%{opacity:0;transform:scale(.6)}6%{opacity:1}18%{opacity:0;transform:scale(5)}100%{opacity:0}}"
           "@keyframes sel{0%,17%{opacity:0}20%,86%{opacity:1}90%,100%{opacity:0}}"
           "@keyframes bub{0%,30%{opacity:0;transform:translateY(8px)}35%,86%{opacity:1;transform:none}90%,100%{opacity:0}}"
           "@keyframes ty{0%,36%{transform:scaleX(0)}48%,100%{transform:scaleX(1)}}")
    return frame(5, "DESKTOP / AI", "OPEN SOURCE", "Nova", "Ghost",
                 ["Triple-tap any screen region, get an AI answer as an overlay.", "Gemini / OpenAI / Ollama, JWT auth, HWID device binding."],
                 "Python · CustomTkinter · Node.js · SQLite", "".join(v), css, title="NovaGhost — AI screen assistant")


# ── 06 Blood bank ────────────────────────────────────────────────────────────
def card_blood():
    rows = [("100,000+", "BLOOD DONATIONS RECORDED"), ("160,000+", "COMPONENT ISSUES TRACKED"), ("3,000+", "DONATION CAMPS MANAGED")]
    v, css = [], ""
    for i, (num, lab) in enumerate(rows):
        y = 190 + i * 40
        v.append(T(num, SANS, 30, 28, y + 8, PAPER, track=-.8))
        v.append(T(lab, MONO, 9.5, 196, y - 6, DIM, track=1.2))
        v.append(f'<rect x="196" y="{y + 2}" width="256" height="5" rx="2.5" fill="{LINE}"/>')
        v.append(f'<rect x="196" y="{y + 2}" width="256" height="5" rx="2.5" fill="{ACC}" style="transform-origin:196px {y}px;animation:g{i} 7s cubic-bezier(.5,0,.2,1) {i * .35}s infinite"/>')
        css += f"@keyframes g{i}{{0%{{transform:scaleX(0)}}35%,88%{{transform:scaleX(1)}}100%{{transform:scaleX(0)}}}}"
    return frame(6, "CLIENT / FULL-STACK", "IN PRODUCTION", "Sanjivani", "Blood Bank",
                 ["MERN platform with role-based access and cron workflows,", "running real operations across multiple talukas."],
                 "MongoDB · Express · React · Node · Cloud", "".join(v), css, title="Sanjivani blood bank platform")
