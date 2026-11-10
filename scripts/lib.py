"""Tiny SVG toolkit: text is shaped with HarfBuzz and emitted as outlined paths,
so the artwork renders identically on GitHub (no font loading, no fallbacks)."""
import os
import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, "fonts")

# ── palette ────────────────────────────────────────────────────────────────
INK = "#0D0C0B"
SURF = "#151311"
SURF2 = "#1B1815"
LINE = "#2B2723"
LINE2 = "#3A352E"
PAPER = "#EFEAE0"
DIM = "#8F897D"
ACC = "#FFD23F"
OK = "#7DE3A3"


class Font:
    def __init__(self, file, variations=None):
        blob = hb.Blob.from_file_path(os.path.join(FD, file))
        self.face = hb.Face(blob)
        self.font = hb.Font(self.face)
        if variations:
            self.font.set_variations(variations)
        self.upem = self.face.upem

    def shape(self, s):
        buf = hb.Buffer()
        buf.add_str(s)
        buf.guess_segment_properties()
        hb.shape(self.font, buf, {"kern": True, "liga": False})
        return list(zip(buf.glyph_infos, buf.glyph_positions))

    def glyph_d(self, gid, size, x, y):
        k = size / self.upem
        pen = SVGPathPen(None, ntos=lambda v: ("%.1f" % v).rstrip("0").rstrip("."))
        tp = TransformPen(pen, (k, 0, 0, -k, x, y))
        self.font.draw_glyph_with_pen(gid, tp)
        return pen.getCommands()


SANS = Font("Bricolage.ttf", {"wght": 800, "wdth": 100, "opsz": 96})
SANSM = Font("Bricolage.ttf", {"wght": 600, "wdth": 100, "opsz": 24})
SERIF = Font("InstrumentSerif-Regular.ttf")
SERIFI = Font("InstrumentSerif-Italic.ttf")
MONO = Font("JetBrainsMono.ttf", {"wght": 500})
MONOB = Font("JetBrainsMono.ttf", {"wght": 700})


def width(s, font, size, track=0.0):
    k = size / font.upem
    return sum(p.x_advance * k + track for _, p in font.shape(s)) - (track if s else 0)


def glyphs(s, font, size, x=0.0, y=0.0, track=0.0, anchor="start"):
    """-> list of (char_index, x_start, advance, d)"""
    w = width(s, font, size, track)
    if anchor == "middle":
        x -= w / 2
    elif anchor == "end":
        x -= w
    k = size / font.upem
    out, cx = [], x
    for info, pos in font.shape(s):
        d = font.glyph_d(info.codepoint, size, cx + pos.x_offset * k, y - pos.y_offset * k)
        adv = pos.x_advance * k + track
        out.append((info.cluster, cx, adv, d))
        cx += adv
    return out


def T(s, font, size, x, y, fill=PAPER, anchor="start", track=0.0, extra=""):
    d = "".join(g[3] for g in glyphs(s, font, size, x, y, track, anchor))
    return f'<path d="{d}" fill="{fill}" {extra}/>' if d else ""


def svg(w, h, body, css="", defs="", title=""):
    t = f"<title>{title}</title>" if title else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">{t}'
        f"<defs>{defs}</defs>"
        f"<style>{css}\n@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}</style>"
        f"{body}</svg>"
    )


def mix(*parts):
    return "".join(parts)


def ease(t):
    return t * t * (3 - 2 * t)
