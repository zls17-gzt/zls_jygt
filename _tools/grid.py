# -*- coding: utf-8 -*-
import sys, xlrd, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

path = sys.argv[1]
book = xlrd.open_workbook(path, formatting_info=True)
for sh in book.sheets():
    print("SHEET: %r rows=%d cols=%d" % (sh.name, sh.nrows, sh.ncols))
    print("MERGED:", sh.merged_cells)
    print()
    # grid
    for r in range(sh.nrows):
        row = []
        for c in range(sh.ncols):
            v = sh.cell_value(r, c)
            if isinstance(v, float) and v == int(v):
                v = int(v)
            row.append(str(v).replace("\n", "\\n"))
        print("R%02d | %s" % (r, " | ".join(row)))
    print()
    print("### ROW STYLES (per row, sampled from first non-empty cell style signature)")
    for r in range(sh.nrows):
        h = sh.rowinfo_map[r].height/20.0 if r in sh.rowinfo_map else None
        print("R%02d h=%s" % (r, h))
    print()
    print("### COL WIDTH (px = raw/256*7+5)")
    for c in range(sh.ncols):
        w = sh.colinfo_map[c].width if c in sh.colinfo_map else None
        print("C%02d raw=%s px=%s" % (c, w, round(w/256.0*7+5) if w else None))
    print()
    print("### CELL STYLE DETAIL")
    seen = {}
    for r in range(sh.nrows):
        for c in range(sh.ncols):
            if sh.cell_type(r, c) == 0 and sh.cell_value(r, c) == '':
                continue
            xf = book.xf_list[sh.cell_xf_index(r, c)]
            fnt = book.font_list[xf.font_index]
            br = xf.border
            al = xf.alignment
            bg = xf.background
            fmt = book.format_map[xf.format_key]
            sig = (fnt.height/20.0, fnt.name, fnt.bold,
                   al.hor_align, al.vert_align, al.text_wrapped,
                   br.left_line_style, br.right_line_style, br.top_line_style, br.bottom_line_style,
                   bg.background_colour_index, bg.pattern_colour_index, fmt.format_str,
                   fnt.underline_type, fnt.italic, fnt.struck_out, al.rotation)
            key = sig
            if key not in seen:
                seen[key] = []
            seen[key].append("[%d,%d]%r" % (r, c, sh.cell_value(r, c))[:60])
    for sig, cells in seen.items():
        print("STYLE", sig)
        print("    cells(%d): %s" % (len(cells), "; ".join(cells[:14])))
        print()
