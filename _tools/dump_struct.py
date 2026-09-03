import xlrd, io, sys, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
D = r'C:\Users\15770\Desktop\新建文件夹\新建文件夹\\'

HA = {0: 'gen', 1: 'left', 2: 'ctr', 3: 'right', 4: 'fill', 5: 'just', 6: 'ctrsel'}
VA = {0: 'top', 1: 'mid', 2: 'bot'}

def rowheights(b, s):
    out = []
    for r in range(s.nrows):
        ri = s.rowinfo_map.get(r)
        out.append(round(ri.height/20.0, 1) if ri and ri.height else None)
    return out

def dump(name, p):
    b = xlrd.open_workbook(D+p, formatting_info=True)
    s = b.sheet_by_index(0)
    print('='*70)
    print(name, s.nrows, 'rows x', s.ncols, 'cols')
    print('merged:', sorted(s.merged_cells))
    hs = rowheights(b, s)
    print('row heights:', hs)
    for r in range(s.nrows):
        vals = []
        aligns = []
        fonts = []
        for c in range(s.ncols):
            xf = b.xf_list[s.cell_xf_index(r, c)]
            f = b.font_list[xf.font_index]
            v = str(s.cell_value(r, c)).replace('\n', '\\n').strip()
            vals.append(v[:16])
            aligns.append(HA.get(xf.alignment.hor_align, '?') + '/' + VA.get(xf.alignment.vert_align, '?'))
            fonts.append('%s/%.0f' % (f.name[:10], f.height/20.0))
        # compact: show row, height, and first non-empty columns with align/font
        nonempty = [(c, vals[c], aligns[c], fonts[c]) for c in range(s.ncols) if vals[c]]
        print('r%-2d h=%s %s' % (r, hs[r], nonempty))

dump('消毒表', '2026夏季消毒记录表电子班.xls')
dump('交接班', '交接班记录 - 新版2026电子版.xls')
dump('观察表', '2026年 秋季全日制观察电子版.xls')
