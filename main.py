# THE WORLD TODAY -- broadsheet front page for 22 November 2026.
# Drawn entirely by this program: self-defined 5x7 bitmap font,
# hand-rolled PNG encoder (zlib + struct, stdlib only), no network,
# deterministic output (two runs are byte-identical).
import os
import struct
import zlib

W, H = 1024, 1024

PAPER = (253, 246, 227)
INK = (22, 22, 22)
RED = (178, 34, 34)
BLUE = (28, 78, 138)
SEA = (120, 165, 205)
LAND = (233, 221, 192)
LAND_LINE = (90, 80, 60)
GREY = (120, 115, 105)
LIGHT = (240, 234, 214)
ORANGE = (230, 120, 30)
GOLD = (245, 190, 60)
DARKBLUE = (18, 48, 88)

# ---------------------------------------------------------------- font: 5x7
FONT = {
    'A': [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    'B': ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    'C': [".####", "#....", "#....", "#....", "#....", "#....", ".####"],
    'D': ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    'E': ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    'F': ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    'G': [".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."],
    'H': ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    'I': [".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."],
    'J': ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    'K': ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    'L': ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    'M': ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    'N': ["#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"],
    'O': [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    'P': ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    'Q': [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    'R': ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    'S': [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    'T': ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    'U': ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    'V': ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    'W': ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    'X': ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    'Y': ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    'Z': ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    '0': [".###.", "#..##", "#.#.#", "#.#.#", "##..#", "#...#", ".###."],
    '1': ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    '2': [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
    '3': ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
    '4': ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    '5': ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    '6': [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    '7': ["#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."],
    '8': [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    '9': [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    '.': [".....", ".....", ".....", ".....", ".....", ".##..", ".##.."],
    ',': [".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."],
    ':': [".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."],
    ';': [".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."],
    '!': ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."],
    '?': [".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."],
    '-': [".....", ".....", ".....", ".###.", ".....", ".....", "....."],
    "'": ["..#..", "..#..", ".....", ".....", ".....", ".....", "....."],
    '(': ["...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."],
    ')': [".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."],
    '/': ["....#", "...#.", "...#.", "..#..", ".#...", ".#...", "#...."],
    '%': ["#...#", "#..#.", "...#.", "..#..", ".#...", ".#..#", "#...#"],
    '&': [".##..", "#..#.", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"],
    '+': [".....", "..#..", "..#..", ".###.", "..#..", "..#..", "....."],
    '=': [".....", ".....", ".###.", ".....", ".###.", ".....", "....."],
    '"': [".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."],
    '*': [".....", ".#.#.", "..#..", "#####", "..#..", ".#.#.", "....."],
    '$': ["..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."],
    ' ': [".....", ".....", ".....", ".....", ".....", ".....", "....."],
}


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg[0] for _ in range(w * h * 3))
        # fill properly (bytearray trick above only sets R channel pattern)
        for i in range(w * h):
            self.px[i * 3] = bg[0]
            self.px[i * 3 + 1] = bg[1]
            self.px[i * 3 + 2] = bg[2]

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = c

    def fill_rect(self, x, y, w, h, c):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = c

    def rect(self, x, y, w, h, c, t=1):
        self.fill_rect(x, y, w, t, c)
        self.fill_rect(x, y + h - t, w, t, c)
        self.fill_rect(x, y, t, h, c)
        self.fill_rect(x + w - t, y, t, h, c)

    def hline(self, x, y, w, c, t=1):
        self.fill_rect(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.fill_rect(x, y, t, h, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            for a in range(t):
                for b in range(t):
                    self.set(x0 + a, y0 + b, c)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c, fill=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) ** 2 + (yy - cy) ** 2
                if fill and d <= r * r:
                    self.set(xx, yy, c)
                elif not fill and r * r - 2 * r <= d <= r * r:
                    self.set(xx, yy, c)

    def poly(self, pts, c):
        # scanline fill
        ys = [p[1] for p in pts]
        for y in range(min(ys), max(ys) + 1):
            nodes = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    nodes.append(int(x0 + (y - y0) * (x1 - x0) / (y1 - y0)))
            nodes.sort()
            for i in range(0, len(nodes) - 1, 2):
                for x in range(nodes[i], nodes[i + 1] + 1):
                    self.set(x, y, c)
        # outline
        for i in range(len(pts)):
            x0, y0 = pts[i]
            x1, y1 = pts[(i + 1) % len(pts)]
            self.line(x0, y0, x1, y1, LAND_LINE)

    def text(self, x, y, s, scale=1, c=INK):
        s = s.upper()
        cx = x
        for ch in s:
            g = FONT.get(ch, FONT[' '])
            for r in range(7):
                row = g[r]
                for col in range(5):
                    if row[col] == '#':
                        self.fill_rect(cx + col * scale, y + r * scale,
                                       scale, scale, c)
            cx += 6 * scale
        return cx

    def text_w(self, s, scale=1):
        return len(s) * 6 * scale - scale

    def text_center(self, y, s, scale=1, c=INK):
        self.text((W - self.text_w(s, scale)) // 2, y, s, scale, c)


def wrap(s, max_chars):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if len(t) <= max_chars:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_para(cv, x, y, s, max_chars, scale=1, c=INK, lh=None):
    lh = lh or (7 * scale + 3)
    for ln in wrap(s, max_chars):
        cv.text(x, y, ln, scale, c)
        y += lh
    return y


# ---------------------------------------------------------------- PNG encoder
def png_bytes(cv):
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)  # filter: none
        raw += cv.px[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 6)

    def chunk(typ, data):
        out = struct.pack(">I", len(data)) + typ + data
        return out + struct.pack(">I", zlib.crc32(typ + data) & 0xffffffff)

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", comp) + chunk(b"IEND", b""))


# ---------------------------------------------------------------- world map
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 25), (-90, 20), (-97, 16),
     (-105, 20), (-117, 32), (-125, 40), (-125, 49), (-145, 60), (-165, 60)],
    # South America
    [(-80, 10), (-60, 5), (-50, 0), (-40, -5), (-35, -10), (-40, -20),
     (-50, -30), (-60, -38), (-70, -50), (-75, -40), (-70, -20), (-80, -5)],
    # Europe
    [(-10, 36), (-9, 43), (0, 46), (-2, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (30, 60), (30, 70), (20, 70), (12, 66),
     (5, 60), (-5, 58), (-10, 52), (-10, 43)],
    # Africa
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (32, -28),
     (20, -35), (12, -18), (9, 4), (-8, 4), (-15, 11)],
    # Asia
    [(30, 36), (36, 36), (43, 40), (50, 40), (55, 25), (58, 25), (60, 25),
     (66, 25), (70, 20), (77, 8), (80, 13), (88, 22), (92, 21), (97, 16),
     (100, 8), (104, 2), (108, 10), (110, 20), (120, 25), (122, 32),
     (127, 40), (130, 42), (135, 44), (140, 45), (142, 50), (142, 60),
     (158, 60), (170, 66), (178, 68), (170, 60), (162, 56), (158, 52),
     (150, 60), (140, 72), (130, 72), (120, 73), (110, 74), (100, 76),
     (90, 75), (80, 73), (70, 72), (60, 69), (50, 69), (40, 68), (35, 66),
     (30, 70), (30, 66)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (124, -33), (132, -32), (137, -35),
     (140, -38), (147, -39), (150, -37), (153, -27), (146, -19), (142, -11),
     (136, -12), (132, -12), (126, -14), (122, -17), (118, -20)],
]

# (number, lon, lat, label) -- stories keyed to the map
MAP_POINTS = [
    (1, 50.5, 26.2, "BAHRAIN - GULF STRIKES"),
    (2, -77.0, -10.0, "PERU - QUAKE 6.9"),
    (3, 25.0, 59.0, "ESTONIA - BORDER SHUT"),
    (4, 20.0, 57.0, "BALTIC SEA - SHIP HIT"),
    (5, 19.0, 52.0, "POLAND - GRIPEN MISS"),
    (6, 32.0, 49.0, "UKRAINE - G20 TALKS"),
    (7, -102.0, 23.0, "MEXICO - CARTEL BOSS HELD"),
    (8, -52.0, -10.0, "BRAZIL - BOLSONARO IN ICU"),
]


def draw_map(cv, x0, y0, w, h):
    cv.fill_rect(x0, y0, w, h, (214, 231, 240))  # ocean

    def proj(lon, lat):
        x = x0 + (lon + 180) / 360.0 * w
        y = y0 + (85 - lat) / 145.0 * h
        return int(x), int(y)

    # graticule
    for lon in range(-150, 181, 30):
        x, _ = proj(lon, 0)
        cv.vline(x, y0, h, (190, 205, 218))
    for lat in range(-60, 86, 30):
        _, y = proj(0, lat)
        cv.hline(x0, y, w, (190, 205, 218))
    for cont in CONTINENTS:
        cv.poly([proj(lon, lat) for lon, lat in cont], LAND)
    for num, lon, lat, _ in MAP_POINTS:
        x, y = proj(lon, lat)
        cv.circle(x, y, 7, RED, fill=True)
        cv.circle(x, y, 7, INK, fill=False)
        cv.text(x + 9, y - 4, str(num), 1, RED)


# ---------------------------------------------------------------- pictograms
def pic_quake(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, LIGHT)
    cv.poly([(x + 8, y + h - 6), (x + w // 3, y + 8),
             (x + w // 2, y + h - 14), (x + 2 * w // 3, y + 12),
             (x + w - 8, y + h - 6)], (150, 110, 70))
    cv.line(x + 10, y + 6, x + 22, y + 16, RED, 2)
    cv.line(x + 22, y + 16, x + 16, y + 26, RED, 2)
    cv.line(x + 16, y + 26, x + 28, y + 34, RED, 2)
    cv.text(x + w - 52, y + 6, "M6.9", 1, RED)


def pic_fence(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, LIGHT)
    for i in range(9):
        bx = x + 10 + i * (w - 20) // 8
        cv.vline(bx, y + 6, h - 12, INK, 2)
    cv.hline(x + 6, y + 10, w - 12, INK, 2)
    cv.hline(x + 6, y + h - 12, w - 12, INK, 2)
    cv.fill_rect(x + w // 2 - 34, y + h // 2 - 9, 68, 18, RED)
    cv.text(x + w // 2 - 28, y + h // 2 - 5, "CLOSED", 1, (255, 255, 255))


def pic_ship(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, SEA)
    cv.fill_rect(x, y + h - 16, w, 16, BLUE)
    # cargo ship
    cv.poly([(x + 20, y + h - 22), (x + w - 30, y + h - 22),
             (x + w - 44, y + h - 8), (x + 34, y + h - 8)], INK)
    cv.fill_rect(x + 44, y + h - 40, 26, 18, RED)
    cv.fill_rect(x + 74, y + h - 40, 26, 18, GOLD)
    cv.fill_rect(x + 104, y + h - 40, 26, 18, (255, 255, 255))
    # drone above with dashed trail
    dx, dy = x + w - 60, y + 8
    cv.fill_rect(dx - 8, dy - 2, 16, 4, INK)
    cv.fill_rect(dx - 2, dy - 8, 4, 16, INK)
    for i in range(6):
        cv.fill_rect(dx - 14 - i * 8, dy + 12 + i * 3, 4, 2, RED)


def pic_jet(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, LIGHT)
    # jet silhouette
    cv.poly([(x + 12, y + h // 2), (x + w - 60, y + h // 2 - 8),
             (x + w - 30, y + h // 2), (x + w - 60, y + h // 2 + 8)],
            (90, 95, 105))
    cv.poly([(x + w // 2 - 6, y + h // 2 - 4), (x + w // 2 + 14, y + h // 2 - 20),
             (x + w // 2 + 22, y + h // 2 - 4)], (90, 95, 105))
    cv.poly([(x + w // 2 - 6, y + h // 2 + 4), (x + w // 2 + 14, y + h // 2 + 20),
             (x + w // 2 + 22, y + h // 2 + 4)], (90, 95, 105))
    # missile streak the jet missed
    cv.line(x + w - 40, y + 6, x + w - 8, y + h - 8, RED, 2)
    cv.circle(x + w - 8, y + h - 8, 4, ORANGE, fill=True)
    cv.text(x + 10, y + 6, "NOT SEEN", 1, RED)


def pic_cuffs(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, LIGHT)
    cx1, cx2 = x + w // 3, x + 2 * w // 3
    cy = y + h // 2
    cv.circle(cx1, cy, 17, (255, 255, 255), fill=True)
    cv.circle(cx2, cy, 17, (255, 255, 255), fill=True)
    cv.circle(cx1, cy, 17, INK, fill=False)
    cv.circle(cx2, cy, 17, INK, fill=False)
    cv.circle(cx1, cy, 10, INK, fill=False)
    cv.circle(cx2, cy, 10, INK, fill=False)
    cv.line(cx1 + 13, cy - 6, cx2 - 13, cy - 6, INK, 3)
    cv.line(cx1 + 13, cy + 6, cx2 - 13, cy + 6, INK, 3)
    cv.text(x + w - 46, y + 6, "HELD", 1, RED)


def pic_hospital(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, LIGHT)
    bx, by = x + w // 2 - 26, y + 8
    cv.fill_rect(bx, by, 52, h - 16, (255, 255, 255))
    cv.rect(bx, by, 52, h - 16, INK)
    cv.fill_rect(bx + 22, by + 6, 8, 22, RED)
    cv.fill_rect(bx + 15, by + 13, 22, 8, RED)
    cv.fill_rect(bx + 6, by + 34, 12, 6, BLUE)
    cv.fill_rect(bx + 20, by + 34, 12, 6, BLUE)
    cv.fill_rect(bx + 34, by + 34, 12, 6, BLUE)


# ---------------------------------------------------------------- lead art
def draw_gulf(cv, x, y, w, h):
    cv.fill_rect(x, y, w, h, (250, 222, 160))          # dusk sky
    cv.fill_rect(x, y + h - 62, w, 62, SEA)            # gulf water
    cv.fill_rect(x, y + h - 62, w, 2, BLUE)
    # sun low on the horizon, left of the missile arcs
    cv.circle(x + 210, y + 30, 18, GOLD, fill=True)
    # tanker on the water
    tx, ty = x + 18, y + h - 52
    cv.poly([(tx, ty), (tx + 150, ty), (tx + 136, ty + 22), (tx + 14, ty + 22)],
            INK)
    cv.fill_rect(tx + 96, ty - 18, 26, 18, INK)
    cv.fill_rect(tx + 20, ty - 14, 18, 14, RED)
    cv.fill_rect(tx + 42, ty - 14, 18, 14, GOLD)
    cv.fill_rect(tx + 64, ty - 14, 18, 14, (255, 255, 255))
    # missile arcs from the top right
    for k, (sx, sy) in enumerate([(x + w - 30, y + 8), (x + w - 80, y + 4),
                                  (x + w - 130, y + 12)]):
        ex, ey = x + w - 46 - k * 40, y + 62
        cv.line(sx, sy, ex, ey, RED, 2)
        cv.circle(sx, sy, 3, ORANGE, fill=True)
    # explosion over the base on the right
    ex, ey = x + w - 66, y + 62
    for ang in range(0, 360, 30):
        import math
        r = 26
        x2 = ex + int(r * math.cos(math.radians(ang)))
        y2 = ey + int(r * math.sin(math.radians(ang)))
        cv.line(ex, ey, x2, y2, ORANGE, 2)
    cv.circle(ex, ey, 14, GOLD, fill=True)
    cv.circle(ex, ey, 7, ORANGE, fill=True)
    # labels
    cv.text(x + 10, y + 8, "STRAIT OF HORMUZ", 1, DARKBLUE)
    cv.text(x + w - 118, y + 96, "BAHRAIN", 1, RED)
    cv.text(x + 12, y + h - 26, "THE GULF", 1, (255, 255, 255))


# ---------------------------------------------------------------- build page
def build():
    cv = Canvas(W, H, PAPER)
    cv.rect(8, 8, W - 16, H - 16, INK, 2)
    cv.rect(13, 13, W - 26, H - 26, INK, 1)

    # ---- masthead
    cv.text_center(26, "THE WORLD TODAY", 8, INK)
    cv.text(28, 92, "EST. 2026", 1, GREY)
    cv.text(W - 28 - cv.text_w("WORLD EDITION", 1), 92, "WORLD EDITION", 1, GREY)
    cv.text_center(90, "SUNDAY 22 NOVEMBER 2026", 2, RED)
    cv.hline(24, 112, W - 48, INK, 2)
    cv.hline(24, 116, W - 48, INK, 1)

    # ---- lead story (left) + gulf art (right)
    lx, ly = 24, 128
    lw = 584
    cv.text(lx, ly, "GULF IN FLAMES - LEAD STORY", 1, RED)
    y = ly + 18
    y = draw_para(cv, lx, y, "IRAN STRIKES US BASES IN BAHRAIN AS GULF BURNS",
                  30, 3, INK, 27)
    y += 6
    lead_body = (
        "IRAN LAUNCHED DRONE AND MISSILE STRIKES ON UNITED STATES BASES IN "
        "BAHRAIN ON SATURDAY NIGHT, THE IRANIAN REVOLUTIONARY GUARD SAID, "
        "CLAIMING HITS ON THE AL-RIFFA AND AWALI BASES AND THE DESTRUCTION "
        "OF TWO AMERICAN PATRIOT RADARS. BAHRAIN SAID ITS AIR DEFENCES "
        "INTERCEPTED THE ATTACK, WITH A FIRE AT A CIVILIAN INDUSTRIAL "
        "COMPLEX AND NO INJURIES REPORTED. AT THE SAME TIME AT LEAST THREE "
        "TANKERS WERE ATTACKED IN OR NEAR THE STRAIT OF HORMUZ, AND THE "
        "GUARD RELEASED VIDEO IT SAID SHOWED DOWNED AMERICAN MQ-9 AND "
        "MQ-1 DRONES."
    )
    y = draw_para(cv, lx, y, lead_body, 94, 1, INK, 10)
    y += 6
    cv.hline(lx, y, lw, INK, 1)
    y += 8
    cv.text(lx, y, "OIL SLIDES, TANKER CREW MISSING - SEE MARKETS, PAGE 1",
            1, RED)

    ax, ay, aw, ah = 624, 128, 376, 172
    cv.rect(ax, ay, aw, ah, INK, 2)
    draw_gulf(cv, ax + 2, ay + 2, aw - 4, ah - 4)
    cv.fill_rect(ax, ay + ah, aw, 26, INK)
    cv.text(ax + 8, ay + ah + 9,
            "DRONES AND MISSILES OVER THE GULF, SATURDAY NIGHT", 1,
            (255, 255, 255))

    # ---- world map
    mx, my, mw, mh = 24, 344, 976, 212
    cv.rect(mx, my, mw, mh, INK, 1)
    cv.text(mx + 10, my + 8, "WHERE THE NEWS HAPPENED - 22 NOVEMBER 2026", 1, RED)
    draw_map(cv, mx + 10, my + 28, 726, mh - 38)
    lx0 = mx + 752
    cv.vline(lx0 - 8, my + 28, mh - 38, GREY, 1)
    yy = my + 30
    for num, _lon, _lat, label in MAP_POINTS:
        cv.text(lx0, yy, str(num), 1, RED)
        cv.text(lx0 + 14, yy, label, 1, INK)
        yy += 18

    # ---- six picture panels
    panels = [
        ("2  PERU SHAKEN BY 6.9 QUAKE",
         "A MAGNITUDE 6.9 EARTHQUAKE SHOOK THE ANDES OF PERU. NO DAMAGE OR "
         "CASUALTIES WERE REPORTED.", pic_quake),
        ("3  ESTONIA TO SHUT RUSSIAN BORDER",
         "ESTONIA WILL CLOSE ITS BORDER WITH RUSSIA. MOSCOW CONDEMNED THE "
         "MOVE AS A NEW IRON CURTAIN.", pic_fence),
        ("4  DRONE HITS RUSSIAN SHIP",
         "A DRONE STRUCK A RUSSIAN CARGO SHIP IN THE BALTIC AS FINLAND "
         "TIGHTENED SECURITY. FINNISH FORCES SAY UKRAINE MAY BE BEHIND IT.",
         pic_ship),
        ("5  GRIPEN JET MISSES MISSILE",
         "A GRIPEN JET FAILED TO INTERCEPT A RUSSIAN MISSILE OVER POLAND - "
         "ITS PILOT COULD NOT DETECT IT. NATO JETS WERE SCRAMBLED.",
         pic_jet),
        ("7  CARTEL BOSS EL CHAPO ISIDRO HELD",
         "MEXICO ARRESTED CARTEL LEADER EL CHAPO ISIDRO AS VIOLENCE IN "
         "SINALOA LEFT 11 DEAD.", pic_cuffs),
        ("8  BOLSONARO TAKEN TO ICU",
         "JAILED FORMER BRAZIL PRESIDENT JAIR BOLSONARO WAS MOVED TO "
         "INTENSIVE CARE WITH ACUTE INTESTINAL OBSTRUCTION.", pic_hospital),
    ]
    pw, ph = 317, 130
    gap = 10
    for i, (head, body, pic) in enumerate(panels):
        px = 24 + (i % 3) * (pw + gap)
        py = 568 + (i // 3) * (ph + gap)
        cv.rect(px, py, pw, ph, INK, 1)
        pic(cv, px + 6, py + 6, pw - 12, 46)
        draw_para(cv, px + 8, py + 58, head, 48, 1, INK, 10)
        draw_para(cv, px + 8, py + 80, body, 50, 1, GREY, 10)

    # ---- world in brief
    bx, by = 24, 842
    cv.hline(bx, by, 976, INK, 2)
    cv.text(bx, by + 8, "WORLD IN BRIEF", 2, RED)
    cv.hline(bx, by + 30, 976, INK, 1)
    briefs_left = [
        "UKRAINE: ZELENSKY PROPOSES NEW PEACE TALKS AT THE G20 SUMMIT.",
        "FRANCE ASKS UN SECURITY COUNCIL TO ACT AFTER MYANMAR REJECTS ICJ RULING.",
        "DENMARK: RUSSIA BEHIND PLOT TO KILL A US-UKRAINIAN CITIZEN.",
        "SAUDI COALITION SHOOTS DOWN 3 HOUTHI MISSILES HEADING FOR RIYADH.",
        "IRAQ: FIRE AT BASRA POWER PLANT KILLS 4, INJURES 35.",
        "INDIA: MODI OPENS NITISH SETU BRIDGE; CYCLONE AKVAN CANCELS 14 FLIGHTS.",
        "US AIRLINES WARNED OF POSSIBLE AL-QAEDA THREAT BEFORE THANKSGIVING.",
    ]
    briefs_right = [
        "TRUMP: IRAN DEAL COULD LAST 20 YEARS.",
        "CRICKET: INDIA LEAD NZ BY 118 AT STUMPS, DAY 3; ZVEREV BEATS MEDVEDEV.",
        "FOOTBALL: NEWCASTLE 2-2 ARSENAL; REAL MADRID 2-1 CELTA.",
        "OIL DOWN OVER 3% AS ADNOC TANKER IS HIT IN HORMUZ; 1 CREW MISSING.",
        "US: N. GUPTA JAILED 19 YEARS IN PANNUN MURDER-PLOT CASE.",
        "JAPAN TRAINS IN INDIA FOR THE FIRST TIME; THAI YOUTH MARCH; SPAIN PLANS BANK TAX; US-CANADA MILITARY LIMITS SET.",
    ]
    col_w = 480
    y = by + 40
    for b in briefs_left:
        y = draw_para(cv, bx, y, "* " + b, 78, 1, INK, 10)
        y += 3
    y = by + 40
    for b in briefs_right:
        y = draw_para(cv, bx + 496, y, "* " + b, 78, 1, INK, 10)
        y += 3

    # ---- footer
    cv.hline(24, 1000, 976, INK, 1)
    cv.text_center(1005,
                   "THE WORLD TODAY - SUNDAY 22 NOVEMBER 2026 - ALL STORIES "
                   "REPORTED 22 NOVEMBER 2026", 1, GREY)
    return cv


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    data = png_bytes(build())
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes)" % (path, len(data)))


if __name__ == "__main__":
    main()
