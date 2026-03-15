#!/usr/bin/env python3
"""
Generate matmul-how-it-works.png  —  "行ごとに掛けて足す" 説明図
Layout:
  Top half   : Matrix W^T (2×3) × vector x (3×1) = vector y (2×1), colored by row
  Bottom half: y1 and y2 arithmetic rows with colored mini-cells
"""
import cairo

W, H = 800, 410
out = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
ctx = cairo.Context(out)

# ── palette ─────────────────────────────────────────────────────────────────
BG        = (0.988, 0.988, 0.972)
INK       = (0.08,  0.08,  0.15)
MUTED     = (0.45,  0.45,  0.55)
BORDER    = (0.50,  0.50,  0.58, 1.0)
BRACKET   = (0.30,  0.30,  0.40)

C_R1      = (1.00, 0.63, 0.12, 0.78)   # orange  — matrix row 1 / y1
C_R1_B    = (0.82, 0.38, 0.0,  1.0)
C_R2      = (0.52, 0.18, 0.80, 0.68)   # purple  — matrix row 2 / y2
C_R2_B    = (0.42, 0.08, 0.68)
C_VEC     = (0.10, 0.52, 0.88, 0.62)   # blue    — input x
C_VEC_B   = (0.0,  0.30, 0.65)
C_RES1    = (1.00, 0.55, 0.10, 0.90)   # strong orange for y1 result
C_RES2    = (0.58, 0.22, 0.82, 0.88)   # strong purple for y2 result

# ── helpers ──────────────────────────────────────────────────────────────────
def bg():
    ctx.set_source_rgb(*BG)
    ctx.paint()

def cell(x, y, w, h, text, fill_rgba, fs=17):
    r, g, b, a = fill_rgba
    ctx.set_source_rgba(r, g, b, a)
    ctx.rectangle(x + 1, y + 1, w - 2, h - 2)
    ctx.fill()
    ctx.set_source_rgba(*BORDER)
    ctx.set_line_width(1.1)
    ctx.rectangle(x, y, w, h)
    ctx.stroke()
    ctx.set_source_rgb(*INK)
    ctx.select_font_face('sans-serif', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(fs)
    te = ctx.text_extents(text)
    ctx.move_to(x + (w - te.width) / 2 - te.x_bearing,
                y + (h + te.height) / 2)
    ctx.show_text(text)

def bracket(x0, x1, y_top, y_bot, lw=2.5):
    ctx.set_line_width(lw)
    ctx.set_source_rgb(*BRACKET)
    for bx, sign in [(x0, 1), (x1, -1)]:
        ctx.move_to(bx + sign * 5, y_top)
        ctx.line_to(bx, y_top)
        ctx.line_to(bx, y_bot)
        ctx.line_to(bx + sign * 5, y_bot)
        ctx.stroke()

def label(x, y, text, color=MUTED, fs=11.5, bold=False):
    ctx.select_font_face('sans-serif', cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(fs)
    ctx.set_source_rgb(*color)
    ctx.move_to(x, y)
    ctx.show_text(text)

def centered_text(x, y, text, color=MUTED, fs=11.5, bold=False):
    ctx.select_font_face('sans-serif', cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(fs)
    ctx.set_source_rgb(*color)
    te = ctx.text_extents(text)
    ctx.move_to(x - te.width / 2, y)
    ctx.show_text(text)

def operator(cx, cy, text, fs=24):
    ctx.select_font_face('sans-serif', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(fs)
    ctx.set_source_rgb(*MUTED)
    te = ctx.text_extents(text)
    ctx.move_to(cx - te.width / 2 - te.x_bearing, cy)
    ctx.show_text(text)

# ════════════════════════════════════════════════════════════════════════════════
# TOP SECTION — Matrix schematic
# ════════════════════════════════════════════════════════════════════════════════
bg()

MAT  = [[0.5, 0.2, 0.3], [0.1, 0.7, 0.2]]
XVEC = [80, 70, 90]
YVEC = [81, 75]

CW, CH = 66, 46  # matrix cell size
MX, MY = 36, 52  # matrix origin

# Title
ctx.select_font_face('sans-serif', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(13.5)
ctx.set_source_rgb(0.18, 0.18, 0.28)
t = '行ごとに「掛けて足す」— 行列積のしくみ'
te = ctx.text_extents(t)
ctx.move_to((W - te.width) / 2, 28)
ctx.show_text(t)

# Column labels
label(MX + CW // 2 - 8, MY - 8, '重みの行列  W', bold=True, fs=11, color=(0.22, 0.22, 0.32))

# Matrix cells
for r in range(2):
    c_fill = C_R1 if r == 0 else C_R2
    for c in range(3):
        cell(MX + c*CW, MY + r*CH, CW, CH, str(MAT[r][c]), c_fill)

# Row side labels
label(MX + 3*CW + 8, MY + CH//2 + 4,        '← 行 1', color=C_R1_B, fs=11, bold=True)
label(MX + 3*CW + 8, MY + CH + CH//2 + 4,   '← 行 2', color=C_R2_B, fs=11, bold=True)

# Matrix bracket
bracket(MX - 8, MX + 3*CW + 8, MY, MY + 2*CH)

# "×" operator
OP1X = MX + 3*CW + 66
operator(OP1X, MY + CH + 14, '×', 30)

# Vector x cells
VX = OP1X + 32
VY = MY
label(VX + 5, VY - 8, '入力ベクトル  x', bold=True, fs=11, color=C_VEC_B)
for i in range(3):
    cell(VX, VY + i*CH, CW - 6, CH, str(XVEC[i]), C_VEC)
bracket(VX - 8, VX + CW - 6 + 8, VY, VY + 3*CH)

# "=" operator
OP2X = VX + CW - 6 + 46
operator(OP2X, MY + CH + 14, '=', 30)

# Vector y cells  (offset vertically to center 2-row result vs 3-row input)
RX = OP2X + 30
RY = MY + CH // 2
label(RX + 4, RY - 8, '出力ベクトル  y', bold=True, fs=11, color=(0.40, 0.18, 0.0))
for i in range(2):
    cell(RX, RY + i*CH, CW - 6, CH, str(YVEC[i]), C_RES1 if i == 0 else C_RES2)
bracket(RX - 8, RX + CW - 6 + 8, RY, RY + 2*CH)

# ── divider ───────────────────────────────────────────────────────────────────
DIV_Y = MY + 3*CH + 22
ctx.set_source_rgba(0.68, 0.68, 0.74, 0.45)
ctx.set_line_width(1.0)
ctx.move_to(20, DIV_Y)
ctx.line_to(W - 20, DIV_Y)
ctx.stroke()

# ════════════════════════════════════════════════════════════════════════════════
# BOTTOM SECTION — Arithmetic walkthrough
# ════════════════════════════════════════════════════════════════════════════════
MW, MH, FS = 40, 28, 13   # mini-cell size, font size

def arith_row(start_x, base_y, pairs, row_color, res_val, res_color):
    """
    Draw one arithmetic row:
    [w0]×[x0] + [w1]×[x1] + [w2]×[x2]  =  [p0] + [p1] + [p2]  =  [result]
    """
    cx = start_x
    mid_y = base_y + MH // 2 + 4  # vertical center for operators

    for i, (w, x, p) in enumerate(pairs):
        if i > 0:
            ctx.select_font_face('sans-serif', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            ctx.set_font_size(15)
            ctx.set_source_rgb(*MUTED)
            ctx.move_to(cx + 3, mid_y)
            ctx.show_text('+')
            cx += 18
        # w cell
        cell(cx, base_y, MW, MH, str(w), row_color, FS)
        cx += MW
        # ×
        ctx.set_font_size(13)
        ctx.set_source_rgb(*MUTED)
        ctx.move_to(cx + 1, mid_y)
        ctx.show_text('×')
        cx += 13
        # x cell
        cell(cx, base_y, MW, MH, str(x), C_VEC, FS)
        cx += MW + 8

    # "=" separator
    ctx.set_font_size(18)
    ctx.set_source_rgb(*MUTED)
    ctx.move_to(cx + 4, mid_y + 1)
    ctx.show_text('=')
    cx += 28

    for i, (_, _, p) in enumerate(pairs):
        if i > 0:
            ctx.set_font_size(15)
            ctx.set_source_rgb(*MUTED)
            ctx.move_to(cx + 3, mid_y)
            ctx.show_text('+')
            cx += 18
        cell(cx, base_y, MW, MH, str(p), row_color, FS)
        cx += MW + 6

    # "=" and result
    ctx.set_font_size(18)
    ctx.set_source_rgb(*MUTED)
    ctx.move_to(cx + 4, mid_y + 1)
    ctx.show_text('=')
    cx += 28
    cell(cx, base_y, MW + 8, MH, str(res_val), res_color, FS + 1)

CALC_Y = DIV_Y + 16

# Row 1: y1
label(24, CALC_Y + MH - 2, 'y₁ の計算：', color=C_R1_B, fs=12, bold=True)
arith_row(130, CALC_Y,
          [(0.5, 80, 40), (0.2, 70, 14), (0.3, 90, 27)],
          C_R1, 81, C_RES1)

# Row 2: y2
CALC_Y2 = CALC_Y + MH + 18
label(24, CALC_Y2 + MH - 2, 'y₂ の計算：', color=C_R2_B, fs=12, bold=True)
arith_row(130, CALC_Y2,
          [(0.1, 80, 8), (0.7, 70, 49), (0.2, 90, 18)],
          C_R2, 75, C_RES2)

# Footer note
note_y = CALC_Y2 + MH + 22
ctx.select_font_face('sans-serif', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
ctx.set_font_size(11)
ctx.set_source_rgb(*MUTED)
note = '行ごとに：対応する重み × 入力 をすべて足すと、その行の出力値が得られる'
te = ctx.text_extents(note)
ctx.move_to((W - te.width) / 2, note_y)
ctx.show_text(note)

# ── save ────────────────────────────────────────────────────────────────────
OUT = '/home/limonene/ROCm-project/vega-hbmx-pages/media/img/matmul-how-it-works.png'
out.write_to_png(OUT)
print(f"Saved → {OUT}  ({W}×{H})")
