import xlrd, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
D = r'C:\Users\15770\Desktop\新建文件夹\新建文件夹\\'
HA = {0: 'gen', 1: 'left', 2: 'ctr', 3: 'right', 4: 'fill', 5: 'just', 6: 'ctrsel'}

def expand_merged(b, s):
    mg = {}
    for (r1, r2, c1, c2) in s.merged_cells:
        for r in range(r1, r2):
            for c in range(c1, c2):
                mg[(r, c)] = (r1, c1)
    return mg

def cell_style(b, s, r, c, mg):
    # resolve to top-left of merged region
    rr, cc = mg.get((r, c), (r, c))
    xf = b.xf_list[s.cell_xf_index(rr, cc)]
    f = b.font_list[xf.font_index]
    return (f.name, f.height/20.0, f.weight >= 700, HA.get(xf.alignment.hor_align, '?'))

p = '交接班记录 - 新版2026电子版.xls'
b = xlrd.open_workbook(D+p, formatting_info=True)
s = b.sheet_by_index(0)
mg = expand_merged(b, s)
print('交接班 逐格字体字号(展开合并后):')
for r in range(s.nrows):
    line = []
    for c in range(s.ncols):
        name, sz, bold, ha = cell_style(b, s, r, c, mg)
        line.append('%d:%s/%.0f/%s' % (c, name[:6], sz, ha))
    print('r%-2d %s' % (r, ' | '.join(line)))
