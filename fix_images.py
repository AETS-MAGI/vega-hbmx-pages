#!/usr/bin/env python3
"""
Fix 1: matmul-how-it-works.png  — replace y₁/y₂ (Unicode sub) with y1/y2 (ASCII)
Fix 2: convolution-akatsuki-window.png — larger, clearer 3×3 observation window
Fix 3: convolution-feature-map-example.png — grayscale edge detection look
"""
import cairo

OUT = '/home/limonene/ROCm-project/vega-hbmx-pages/media/img/'

# ════════════════════════════════════════════════════════════════════════════════
# FIX 1 — Regenerate matmul-how-it-works.png (ASCII labels for y1/y2)
# ════════════════════════════════════════════════════════════════════════════════
W, H = 800, 410
out = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
ctx = cairo.Context(out)

BG     = (0.988, 0.988, 0.972)
INK    = (0.08,  0.08,  0.15)
MUTED  = (0.45,  0.45,  0.55)
BORDER = (0.50,  0.50,  0.58, 1.0)
C_R1   = (1.00, 0.63, 0.12, 0.78)
C_R1_B = (0.82, 0.38, 0.0)
C_R2   = (0.52, 0.18, 0.80, 0.68)
C_R2_B = (0.42, 0.08, 0.68)
C_VEC  = (0.10, 0.52, 0.88, 0.62)
C_VEC_B= (0.0,  0.30, 0.65)
C_RES1 = (1.00, 0.55, 0.10, 0.90)
C_RES2 = (0.58, 0.22, 0.82, 0.88)

ctx.set_source_rgb(*BG); ctx.paint()

def cell(x, y, w, h, text, fill_rgba, fs=17):
    r, g, b, a = fill_rgba
    ctx.set_source_rgba(r, g, b, a)
    ctx.rectangle(x+1, y+1, w-2, h-2); ctx.fill()
    ctx.set_source_rgba(*BORDER); ctx.set_line_width(1.1)
    ctx.rectangle(x, y, w, h); ctx.stroke()
    ctx.set_source_rgb(*INK)
    ctx.select_font_face('sans-serif', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(fs); te = ctx.text_extents(text)
    ctx.move_to(x+(w-te.width)/2-te.x_bearing, y+(h+te.height)/2)
    ctx.show_text(text)

def bracket(x0, x1, yt, yb, lw=2.5):
    ctx.set_line_width(lw); ctx.set_source_rgb(0.30, 0.30, 0.40)
    for bx, s in [(x0, 1), (x1, -1)]:
        ctx.move_to(bx+s*5, yt); ctx.line_to(bx, yt)
        ctx.line_to(bx, yb); ctx.line_to(bx+s*5, yb); ctx.stroke()

def label(x, y, text, color=MUTED, fs=11.5, bold=False):
    ctx.select_font_face('sans-serif', cairo.FONT_SLANT_NORMAL,
        cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(fs); ctx.set_source_rgb(*color)
    ctx.move_to(x, y); ctx.show_text(text)

def operator(cx, cy, text, fs=24):
    ctx.select_font_face('sans-serif', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(fs); ctx.set_source_rgb(*MUTED)
    te = ctx.text_extents(text)
    ctx.move_to(cx-te.width/2-te.x_bearing, cy); ctx.show_text(text)

MAT = [[0.5, 0.2, 0.3], [0.1, 0.7, 0.2]]
XVEC = [80, 70, 90]; YVEC = [81, 75]
CW, CH = 66, 46; MX, MY = 36, 52

# Title
ctx.select_font_face('sans-serif', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(13.5); ctx.set_source_rgb(0.18, 0.18, 0.28)
t = '行ごとに「掛けて足す」— 行列積のしくみ'
te = ctx.text_extents(t); ctx.move_to((W-te.width)/2, 28); ctx.show_text(t)

label(MX+CW//2-8, MY-8, '重みの行列  W', bold=True, fs=11, color=(0.22,0.22,0.32))
for r in range(2):
    c = C_R1 if r == 0 else C_R2
    for col in range(3):
        cell(MX+col*CW, MY+r*CH, CW, CH, str(MAT[r][col]), c)

label(MX+3*CW+8, MY+CH//2+4,       '← 行 1', color=C_R1_B, fs=11, bold=True)
label(MX+3*CW+8, MY+CH+CH//2+4,    '← 行 2', color=C_R2_B, fs=11, bold=True)
bracket(MX-8, MX+3*CW+8, MY, MY+2*CH)

OP1X = MX+3*CW+66; operator(OP1X, MY+CH+14, 'x', 30)
VX = OP1X+32; VY = MY
label(VX+5, VY-8, '入力ベクトル  x', bold=True, fs=11, color=C_VEC_B)
for i in range(3):
    cell(VX, VY+i*CH, CW-6, CH, str(XVEC[i]), C_VEC)
bracket(VX-8, VX+CW-6+8, VY, VY+3*CH)

OP2X = VX+CW-6+46; operator(OP2X, MY+CH+14, '=', 30)
RX = OP2X+30; RY = MY+CH//2
label(RX+4, RY-8, '出力ベクトル  y', bold=True, fs=11, color=(0.40,0.18,0.0))
for i in range(2):
    cell(RX, RY+i*CH, CW-6, CH, str(YVEC[i]), C_RES1 if i==0 else C_RES2)
bracket(RX-8, RX+CW-6+8, RY, RY+2*CH)

DIV_Y = MY+3*CH+22
ctx.set_source_rgba(0.68,0.68,0.74,0.45); ctx.set_line_width(1.0)
ctx.move_to(20, DIV_Y); ctx.line_to(W-20, DIV_Y); ctx.stroke()

MW, MH, FS = 40, 28, 13
CALC_Y = DIV_Y+16

def arith_row(start_x, base_y, pairs, row_color, res_val, res_color):
    cx = start_x; mid_y = base_y+MH//2+4
    for i, (w, x, p) in enumerate(pairs):
        if i > 0:
            ctx.select_font_face('sans-serif', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            ctx.set_font_size(15); ctx.set_source_rgb(*MUTED)
            ctx.move_to(cx+3, mid_y); ctx.show_text('+'); cx += 18
        cell(cx, base_y, MW, MH, str(w), row_color, FS); cx += MW
        ctx.set_font_size(13); ctx.set_source_rgb(*MUTED)
        ctx.move_to(cx+1, mid_y); ctx.show_text('x'); cx += 13
        cell(cx, base_y, MW, MH, str(x), C_VEC, FS); cx += MW+8
    ctx.set_font_size(18); ctx.set_source_rgb(*MUTED)
    ctx.move_to(cx+4, mid_y+1); ctx.show_text('='); cx += 28
    for i, (_, _, p) in enumerate(pairs):
        if i > 0:
            ctx.set_font_size(15); ctx.set_source_rgb(*MUTED)
            ctx.move_to(cx+3, mid_y); ctx.show_text('+'); cx += 18
        cell(cx, base_y, MW, MH, str(p), row_color, FS); cx += MW+6
    ctx.set_font_size(18); ctx.set_source_rgb(*MUTED)
    ctx.move_to(cx+4, mid_y+1); ctx.show_text('='); cx += 28
    cell(cx, base_y, MW+8, MH, str(res_val), res_color, FS+1)

# ← ASCII labels: "y1" and "y2" (no Unicode subscripts)
label(24, CALC_Y+MH-2, 'y1 の計算：', color=C_R1_B, fs=12, bold=True)
arith_row(130, CALC_Y, [(0.5,80,40),(0.2,70,14),(0.3,90,27)], C_R1, 81, C_RES1)

CALC_Y2 = CALC_Y+MH+18
label(24, CALC_Y2+MH-2, 'y2 の計算：', color=C_R2_B, fs=12, bold=True)
arith_row(130, CALC_Y2, [(0.1,80,8),(0.7,70,49),(0.2,90,18)], C_R2, 75, C_RES2)

ctx.select_font_face('sans-serif', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
ctx.set_font_size(11); ctx.set_source_rgb(*MUTED)
note = '行ごとに：対応する重み × 入力 をすべて足すと、その行の出力値が得られる'
te = ctx.text_extents(note); ctx.move_to((W-te.width)/2, CALC_Y2+MH+22); ctx.show_text(note)

out.write_to_png(OUT+'matmul-how-it-works.png')
print('Fix 1 done: matmul-how-it-works.png')


# ════════════════════════════════════════════════════════════════════════════════
# FIX 2 + 3 — Regenerate convolution images
# ════════════════════════════════════════════════════════════════════════════════
SRC = '/home/limonene/ROCm-project/vega-hbmx-pages/media/img/akatsuki-overview.png'
src = cairo.ImageSurface.create_from_png(SRC)
SW = src.get_width(); SH = src.get_height(); STRIDE = src.get_stride()
src_bytes = bytes(src.get_data())
CX0, CY0, CW2, CH2 = 250, 140, 300, 300

# Precompute grayscale
GX0 = CX0-1; GY0 = CY0-1; GW = CW2+2; GH = CH2+2
gray = [[0]*GW for _ in range(GH)]
for gy in range(GH):
    sy = max(0, min(SH-1, GY0+gy)); roff = sy*STRIDE
    for gx in range(GW):
        sx = max(0, min(SW-1, GX0+gx)); off = roff+sx*4
        b=src_bytes[off]; g=src_bytes[off+1]; r=src_bytes[off+2]
        gray[gy][gx] = (r*77+g*150+b*29)>>8

# Sobel-x
edge = [[0]*CW2 for _ in range(CH2)]; max_e = 1
for cy in range(CH2):
    gy = cy+1
    for cx in range(CW2):
        gxi = cx+1
        val = (-gray[gy-1][gxi-1]+gray[gy-1][gxi+1]
               -2*gray[gy][gxi-1]+2*gray[gy][gxi+1]
               -gray[gy+1][gxi-1]+gray[gy+1][gxi+1])
        v = abs(val); edge[cy][cx] = v
        if v > max_e: max_e = v

# Best window position
best_x, best_y, best_v = CW2//2, CH2//4, 0
for cy in range(CH2//6, 5*CH2//6, 3):
    for cx2 in range(CW2//6, 5*CW2//6, 3):
        if edge[cy][cx2] > best_v:
            best_v = edge[cy][cx2]; best_x, best_y = cx2, cy
print(f'  window at ({best_x},{best_y}), edge={best_v}')

# ── Fix 2: window image — larger, clearer 3×3 grid ──────────────────────────
OUT1 = 480; sc1 = OUT1/CW2
out1 = cairo.ImageSurface(cairo.FORMAT_ARGB32, OUT1, OUT1)
ctx1 = cairo.Context(out1)

ctx1.save()
ctx1.scale(sc1, sc1); ctx1.translate(-CX0, -CY0)
ctx1.set_source_surface(src, 0, 0)
ctx1.get_source().set_filter(cairo.Filter.BILINEAR)
ctx1.paint(); ctx1.restore()

# 3x3 grid: CELL1=44px → grid = 132×132px in 480px image (clearly visible)
CELL1 = 44
gx0 = best_x * sc1 - CELL1 * 1.5
gy0 = best_y * sc1 - CELL1 * 1.5

# Semi-transparent fill per cell
for row in range(3):
    for col in range(3):
        rx = gx0 + col*CELL1; ry = gy0 + row*CELL1
        ctx1.set_source_rgba(1.0, 0.50, 0.05, 0.15)
        ctx1.rectangle(rx, ry, CELL1, CELL1); ctx1.fill()
        ctx1.set_source_rgba(1.0, 0.22, 0.0, 0.92)
        ctx1.set_line_width(2.0)
        ctx1.rectangle(rx, ry, CELL1, CELL1); ctx1.stroke()

# Outer border (thicker)
ctx1.set_source_rgba(1.0, 0.08, 0.0, 0.97)
ctx1.set_line_width(4.0)
ctx1.rectangle(gx0-2, gy0-2, 3*CELL1+4, 3*CELL1+4); ctx1.stroke()

# Small label "3×3 の窓" below the box
ctx1.select_font_face('sans-serif', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx1.set_font_size(13)
ctx1.set_source_rgba(1.0, 0.9, 0.8, 0.96)
lbl = '3x3 の窓'
te = ctx1.text_extents(lbl)
lx = gx0 + (3*CELL1 - te.width) / 2
ly = gy0 + 3*CELL1 + 18
# Shadow
ctx1.set_source_rgba(0, 0, 0, 0.55)
ctx1.move_to(lx+1, ly+1); ctx1.show_text(lbl)
# Text
ctx1.set_source_rgba(1.0, 0.92, 0.82, 1.0)
ctx1.move_to(lx, ly); ctx1.show_text(lbl)

out1.write_to_png(OUT+'convolution-akatsuki-window.png')
print('Fix 2 done: convolution-akatsuki-window.png')

# ── Fix 3: feature map — clean grayscale ────────────────────────────────────
feat = bytearray(CW2 * CH2 * 4)
for cy in range(CH2):
    for cx2 in range(CW2):
        v = int(edge[cy][cx2] / max_e * 255)
        off = (cy*CW2+cx2)*4
        feat[off] = v; feat[off+1] = v; feat[off+2] = v; feat[off+3] = 255

feat_surf = cairo.ImageSurface.create_for_data(
    feat, cairo.FORMAT_ARGB32, CW2, CH2, CW2*4)

OUT3 = 480
out3 = cairo.ImageSurface(cairo.FORMAT_ARGB32, OUT3, OUT3)
ctx3 = cairo.Context(out3)
ctx3.scale(OUT3/CW2, OUT3/CH2)
ctx3.set_source_surface(feat_surf, 0, 0)
ctx3.get_source().set_filter(cairo.Filter.BILINEAR)
ctx3.paint()
out3.write_to_png(OUT+'convolution-feature-map-example.png')
print('Fix 3 done: convolution-feature-map-example.png')

print('\nAll fixes applied.')
