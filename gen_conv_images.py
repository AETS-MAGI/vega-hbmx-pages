#!/usr/bin/env python3
"""
Generate convolution explanation images for deep-learning-for-rocm.html
Requires: pycairo  (python-cairo, available on this system)
"""
import cairo, math, sys

SRC = '/home/limonene/ROCm-project/vega-hbmx-pages/media/img/akatsuki-overview.png'
OUT = '/home/limonene/ROCm-project/vega-hbmx-pages/media/img/'

# ── Load source ──────────────────────────────────────────────────────────────
print("Loading source image...")
src = cairo.ImageSurface.create_from_png(SRC)
SW     = src.get_width()    # 1024
SH     = src.get_height()   # 1536
STRIDE = src.get_stride()   # bytes per row (= SW * 4 for ARGB32)
src_bytes = bytes(src.get_data())
print(f"  {SW}×{SH}  stride={STRIDE}")

# ── Crop region (face/hair upper-center of portrait) ─────────────────────────
CX0, CY0 = 250, 140
CW,  CH   = 300, 300

# ── Precompute grayscale for extended region (Sobel needs 1-px border) ───────
print("Precomputing grayscale…")
GX0 = CX0 - 1
GY0 = CY0 - 1
GW  = CW + 2
GH  = CH + 2

gray = [[0] * GW for _ in range(GH)]
for gy in range(GH):
    sy = max(0, min(SH - 1, GY0 + gy))
    roff = sy * STRIDE
    for gx in range(GW):
        sx = max(0, min(SW - 1, GX0 + gx))
        off = roff + sx * 4
        b = src_bytes[off];  g = src_bytes[off+1];  r = src_bytes[off+2]
        gray[gy][gx] = (r * 77 + g * 150 + b * 29) >> 8

# ── Sobel-x ──────────────────────────────────────────────────────────────────
print("Computing Sobel-x…")
edge = [[0] * CW for _ in range(CH)]
max_e = 1
for cy in range(CH):
    gy = cy + 1          # offset into gray[] (1-px border)
    for cx in range(CW):
        gx_i = cx + 1
        val = (  - gray[gy-1][gx_i-1] + gray[gy-1][gx_i+1]
               - 2*gray[gy  ][gx_i-1] + 2*gray[gy  ][gx_i+1]
               - gray[gy+1][gx_i-1] + gray[gy+1][gx_i+1] )
        v = abs(val)
        edge[cy][cx] = v
        if v > max_e:
            max_e = v
print(f"  max_e = {max_e}")

# ── Find the high-gradient position for the window overlay ───────────────────
best_x, best_y, best_v = CW//2, CH//4, 0
for cy in range(CH // 6, 5*CH // 6, 3):
    for cx in range(CW // 6, 5*CW // 6, 3):
        if edge[cy][cx] > best_v:
            best_v = edge[cy][cx]
            best_x, best_y = cx, cy
print(f"  Window placed at crop ({best_x}, {best_y})")


# ════════════════════════════════════════════════════════════════════════════════
# IMAGE 1 — akatsuki crop with 3×3 window overlay
# ════════════════════════════════════════════════════════════════════════════════
print("Image 1: window overlay…")
OUT1 = 480
out1 = cairo.ImageSurface(cairo.FORMAT_ARGB32, OUT1, OUT1)
ctx1 = cairo.Context(out1)

sc1 = OUT1 / CW
ctx1.save()
ctx1.scale(sc1, sc1)
ctx1.translate(-CX0, -CY0)
ctx1.set_source_surface(src, 0, 0)
pat = ctx1.get_source()
pat.set_filter(cairo.Filter.BILINEAR)
ctx1.paint()
ctx1.restore()

# 3×3 grid overlay
CELL1 = 26   # px per cell in the 480px output
gx0 = best_x * sc1 - CELL1 * 1.5
gy0 = best_y * sc1 - CELL1 * 1.5

for row in range(3):
    for col in range(3):
        rx = gx0 + col * CELL1
        ry = gy0 + row * CELL1
        ctx1.set_source_rgba(1.0, 0.50, 0.05, 0.20)
        ctx1.rectangle(rx, ry, CELL1, CELL1)
        ctx1.fill()
        ctx1.set_source_rgba(1.0, 0.28, 0.0, 0.90)
        ctx1.set_line_width(1.5)
        ctx1.rectangle(rx, ry, CELL1, CELL1)
        ctx1.stroke()

ctx1.set_source_rgba(1.0, 0.10, 0.0, 0.96)
ctx1.set_line_width(3.0)
ctx1.rectangle(gx0 - 1.5, gy0 - 1.5, 3*CELL1 + 3, 3*CELL1 + 3)
ctx1.stroke()

out1.write_to_png(OUT + 'convolution-akatsuki-window.png')
print("  → convolution-akatsuki-window.png")


# ════════════════════════════════════════════════════════════════════════════════
# IMAGE 2 — Sobel filter matrix drawing
# ════════════════════════════════════════════════════════════════════════════════
print("Image 2: Sobel matrix…")
W2, H2 = 320, 240
out2 = cairo.ImageSurface(cairo.FORMAT_ARGB32, W2, H2)
ctx2 = cairo.Context(out2)

# cream background
ctx2.set_source_rgb(0.992, 0.992, 0.975)
ctx2.paint()

MATRIX = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
CW2, CH2 = 64, 52          # cell width/height
MX2 = (W2 - 3 * CW2) // 2  # left margin for grid
MY2 = 36

def cell_rgba(v):
    if v < 0:   return (0.16, 0.44, 0.90, 0.72)   # blue
    elif v > 0: return (0.92, 0.32, 0.08, 0.72)   # orange
    else:       return (0.76, 0.76, 0.80, 0.52)   # neutral gray

# Title
ctx2.select_font_face('sans-serif', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx2.set_font_size(13)
ctx2.set_source_rgb(0.18, 0.18, 0.28)
title = 'Sobel フィルタ（x 方向）'
te = ctx2.text_extents(title)
ctx2.move_to((W2 - te.width) / 2, 24)
ctx2.show_text(title)

# Cells
ctx2.set_font_size(22)
for row in range(3):
    for col in range(3):
        v = MATRIX[row][col]
        rx = MX2 + col * CW2
        ry = MY2 + row * CH2

        r2, g2, b2, a2 = cell_rgba(v)
        ctx2.set_source_rgba(r2, g2, b2, a2)
        ctx2.rectangle(rx + 1, ry + 1, CW2 - 2, CH2 - 2)
        ctx2.fill()

        ctx2.set_source_rgba(0.55, 0.55, 0.62, 1.0)
        ctx2.set_line_width(1.0)
        ctx2.rectangle(rx, ry, CW2, CH2)
        ctx2.stroke()

        txt = str(v) if v != 0 else '0'
        ctx2.set_source_rgb(0.10, 0.10, 0.16)
        te = ctx2.text_extents(txt)
        ctx2.move_to(rx + (CW2 - te.width) / 2 - te.x_bearing,
                     ry + (CH2 + te.height) / 2)
        ctx2.show_text(txt)

# Matrix brackets
ctx2.set_line_width(2.5)
ctx2.set_source_rgb(0.28, 0.28, 0.38)
for bx, sign in [(MX2 - 10, 1), (MX2 + 3*CW2 + 10, -1)]:
    bt = MY2;  bb = MY2 + 3*CH2
    ctx2.move_to(bx + sign*6, bt)
    ctx2.line_to(bx, bt)
    ctx2.line_to(bx, bb)
    ctx2.line_to(bx + sign*6, bb)
    ctx2.stroke()

# Subtitle
ctx2.select_font_face('sans-serif', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
ctx2.set_font_size(12)
ctx2.set_source_rgb(0.42, 0.42, 0.52)
sub = '左右の明るさの差に反応'
te = ctx2.text_extents(sub)
ctx2.move_to((W2 - te.width) / 2, MY2 + 3*CH2 + 24)
ctx2.show_text(sub)

out2.write_to_png(OUT + 'sobel-filter-3x3.png')
print("  → sobel-filter-3x3.png")


# ════════════════════════════════════════════════════════════════════════════════
# IMAGE 3 — feature map (Sobel-x heatmap of same crop)
# ════════════════════════════════════════════════════════════════════════════════
print("Image 3: feature map…")

feat = bytearray(CW * CH * 4)
for cy in range(CH):
    for cx in range(CW):
        t = edge[cy][cx] / max_e    # 0.0 .. 1.0
        # Heatmap: dark navy (low) → blue → cyan-white (high)
        if t < 0.30:
            t2 = t / 0.30
            r3 = int(8   + t2 * 20)
            g3 = int(14  + t2 * 20)
            b3 = int(40  + t2 * 120)
        elif t < 0.65:
            t2 = (t - 0.30) / 0.35
            r3 = int(28  + t2 * 40)
            g3 = int(34  + t2 * 150)
            b3 = int(160 + t2 * 80)
        else:
            t2 = (t - 0.65) / 0.35
            r3 = int(68  + t2 * 187)
            g3 = int(184 + t2 * 56)
            b3 = int(240 + t2 * 15)
        r3 = max(0, min(255, r3))
        g3 = max(0, min(255, g3))
        b3 = max(0, min(255, b3))
        off = (cy * CW + cx) * 4
        feat[off]   = b3
        feat[off+1] = g3
        feat[off+2] = r3
        feat[off+3] = 255

feat_surf = cairo.ImageSurface.create_for_data(
    feat, cairo.FORMAT_ARGB32, CW, CH, CW * 4)

OUT3 = 480
out3 = cairo.ImageSurface(cairo.FORMAT_ARGB32, OUT3, OUT3)
ctx3 = cairo.Context(out3)
ctx3.scale(OUT3 / CW, OUT3 / CH)
ctx3.set_source_surface(feat_surf, 0, 0)
ctx3.get_source().set_filter(cairo.Filter.BILINEAR)
ctx3.paint()
out3.write_to_png(OUT + 'convolution-feature-map-example.png')
print("  → convolution-feature-map-example.png")

print("\nAll images generated.")
