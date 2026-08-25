import zlib, struct, os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

def write_png(path, size, rows):
    raw = b''
    for row in rows:
        raw += b'\x00' + row
    compressed = zlib.compress(raw, 9)
    def chunk(typ, data):
        return (struct.pack('>I', len(data)) + typ + data +
                struct.pack('>I', zlib.crc32(typ + data) & 0xffffffff))
    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0)
    png = sig + chunk(b'IHDR', ihdr) + chunk(b'IDAT', compressed) + chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)

def make_icon(size):
    bg = (255, 215, 0, 255)       # 金 #FFD700
    brown = (93, 64, 55, 255)     # 棕 #5D4037
    white = (255, 255, 255, 255)
    cx = size / 2
    apex_y = size * 0.27
    base_y = size * 0.58
    body_top = base_y
    body_bottom = size * 0.80
    body_left = size * 0.32
    body_right = size * 0.68
    door_w = size * 0.10
    door_h = size * 0.18
    rows = []
    for y in range(size):
        row = bytearray()
        for x in range(size):
            color = bg
            # 屋顶（三角形）
            if apex_y <= y <= base_y:
                t = (y - apex_y) / (base_y - apex_y)
                half = t * (size * 0.23)
                if abs(x - cx) <= half:
                    color = brown
            # 房身（白色方块）
            if body_top <= y <= body_bottom and body_left <= x <= body_right:
                color = white
                # 门（棕色）
                if (cx - door_w / 2 <= x <= cx + door_w / 2) and (body_bottom - door_h <= y <= body_bottom):
                    color = brown
            row += bytes(color)
        rows.append(bytes(row))
    return rows

for size in (192, 512):
    rows = make_icon(size)
    write_png(os.path.join(OUT_DIR, f'icon-{size}.png'), size, rows)
    print('wrote icon-%d.png' % size)
