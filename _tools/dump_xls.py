# -*- coding: utf-8 -*-
import sys, xlrd, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

FILES = [
    r"C:\Users\15770\Desktop\新建文件夹\新建文件夹\2026年 秋季全日制观察电子版.xls",
    r"C:\Users\15770\Desktop\新建文件夹\新建文件夹\2026夏季消毒记录表电子班.xls",
    r"C:\Users\15770\Desktop\新建文件夹\新建文件夹\交接班记录 - 新版2026电子版.xls",
]

def fmt_cell(sheet, r, c, book):
    xf = book.xf_list[sheet.cell_xf_index(r, c)]
    fnt = book.font_list[xf.font_index]
    br = xf.border
    parts = []
    parts.append("F:sz=%s name=%s bold=%s color=%s" % (
        fnt.height/20.0, fnt.name, fnt.bold,
        book.colour_map.get(fnt.colour_index) if fnt.colour_index not in (0x7FFF, 32767) else 'auto'))
    al = xf.alignment
    parts.append("AL:h=%s v=%s wrap=%s rot=%s" % (al.hor_align, al.vert_align, al.text_wrapped, al.rotation))
    parts.append("B:l=%s r=%s t=%s b=%s(lc=%s rc=%s tc=%s bc=%s)" % (
        br.left_line_style, br.right_line_style, br.top_line_style, br.bottom_line_style,
        br.left_colour_index, br.right_colour_index, br.top_colour_index, br.bottom_colour_index))
    parts.append("BG:%s pat=%s" % (xf.background.background_colour_index, xf.background.pattern_colour_index))
    fmt = book.format_map[xf.format_key]
    parts.append("NUM:%s" % fmt.format_str)
    return " | ".join(parts)

for path in FILES:
    print("="*100)
    print("FILE:", path)
    book = xlrd.open_workbook(path, formatting_info=True)
    for sh in book.sheets():
        print("-"*100)
        print("SHEET: %r  dims rows=%d cols=%d" % (sh.name, sh.nrows, sh.ncols))
        print("MERGED:", sh.merged_cells)
        print("COLWIDTH(raw):", [ (i, sh.colinfo_map[i].width if i in sh.colinfo_map else None) for i in range(sh.ncols)])
        print("COLWIDTH(px):", [ (i, round(sh.colinfo_map[i].width/256.0*7+5) if i in sh.colinfo_map else None) for i in range(sh.ncols)])
        print("COL hidden:", [ (i, sh.colinfo_map[i].hidden if i in sh.colinfo_map else 0) for i in range(sh.ncols)])
        print("ROWHEIGHT(pt):", [ (i, sh.rowinfo_map[i].height/20.0 if i in sh.rowinfo_map else None) for i in range(sh.nrows)])
        print("-"*40, "CELLS", "-"*40)
        for r in range(sh.nrows):
            for c in range(sh.ncols):
                v = sh.cell_value(r, c)
                t = sh.cell_type(r, c)
                if v == '' and t == 0:
                    continue
                print("[%d,%d] type=%s val=%r" % (r, c, t, v))
                print("       %s" % fmt_cell(sh, r, c, book))
