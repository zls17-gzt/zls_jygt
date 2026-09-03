# -*- coding: utf-8 -*-
"""逐格比对：原始 xls  vs  导出的 HTML(.xls)
比对维度：网格尺寸、合并跨度(colspan/rowspan)、字号、字体、粗体、水平/垂直对齐、
          边框、行高、列宽。内容差异单列出来（模板里由用户填写的格子本就该不同）。
"""
import io, os, re, sys, html
import xlrd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESK = r'C:\Users\15770\Desktop\新建文件夹\新建文件夹'

# 字体名归一化（导出里用的是通用族名）
FF_MAP = {
    '宋体': '宋体', 'SimSun': '宋体', '仿宋_GB2312': '仿宋', '仿宋': '仿宋',
    '方正小标宋简体': '方正小标宋', '黑体': '黑体', '楷体': '楷体',
}
def norm_ff(name):
    n = (name or '').strip()
    return FF_MAP.get(n, n)

# ---------- 读原始 xls ----------
def read_xls(path):
    book = xlrd.open_workbook(path, formatting_info=True)
    sh = book.sheet_by_index(0)
    nrows, ncols = sh.nrows, sh.ncols

    merges = {}            # (r,c) -> (rs, cs)  仅在原点记录
    merge_origin = {}      # (r,c) -> (r0,c0)
    for (rlo, rhi, clo, chi) in sh.merged_cells:
        merges[(rlo, clo)] = (rhi - rlo, chi - clo)
        for r in range(rlo, rhi):
            for c in range(clo, chi):
                merge_origin[(r, c)] = (rlo, clo)

    grid = []
    for r in range(nrows):
        row = []
        for c in range(ncols):
            xf = book.xf_list[sh.cell_xf_index(r, c)]
            f = book.font_list[xf.font_index]
            al = xf.alignment
            bd = xf.border
            # 边框：只要有任一边有线就认为有框
            has_border = any(getattr(bd, k, 0) not in (0, None)
                             for k in ('left_line_style', 'right_line_style',
                                       'top_line_style', 'bottom_line_style'))
            row.append({
                'v': sh.cell_value(r, c),
                'fs': round(f.height / 20.0, 1),
                'ff': norm_ff(f.name),
                'b': 1 if f.weight >= 700 else 0,
                'ha': al.hor_align, 'va': al.vert_align,
                'bd': 1 if has_border else 0,
                'rs': 1, 'cs': 1,
                'merge': (r, c) in merge_origin,
            })
        grid.append(row)

    # 合并跨度写回原点格
    for (r0, c0), (rs, cs) in merges.items():
        grid[r0][c0]['rs'] = rs
        grid[r0][c0]['cs'] = cs

    heights = []
    for r in range(nrows):
        ri = sh.rowinfo_map.get(r)
        heights.append(round(ri.height / 20.0, 1) if ri and ri.height else None)

    widths = []
    for c in range(ncols):
        ci = sh.colinfo_map.get(c)
        w = ci.width if ci else None
        # xlrd 的 width 单位是 1/256 字符宽 → px：字符宽≈7px，再 +5 补内边距
        widths.append(int(round(w * 7.0 / 256.0)) + 5 if w else None)

    return {'grid': grid, 'nrows': nrows, 'ncols': ncols,
            'heights': heights, 'widths': widths, 'merges': merges}

# ---------- 读导出 HTML ----------
def parse_style(s):
    d = {}
    for part in s.split(';'):
        if ':' not in part:
            continue
        k, v = part.split(':', 1)
        d[k.strip()] = v.strip()
    return d

TD_RE = re.compile(r'<(td|th)([^>]*)>(.*?)</\1>', re.S)

def read_html(path):
    s = io.open(path, encoding='utf-8').read()
    s = s[s.find('<body'):] if '<body' in s else s

    # 列宽
    widths = [int(x) for x in re.findall(r'<col style="width:(\d+)px"', s)]

    rows_raw = re.findall(r'<tr>(.*?)</tr>', s, re.S)
    # 先解析每行的原始 td
    raw = []
    for r in rows_raw:
        cells = []
        for m in re.finditer(r'<(td|th)([^>]*)>(.*?)</\1>', r, re.S):
            attr = m.group(2)
            inner = re.sub(r'<[^>]+>', '', m.group(3))
            rs = int(re.search(r'rowspan="(\d+)"', attr).group(1)) if 'rowspan=' in attr else 1
            cs = int(re.search(r'colspan="(\d+)"', attr).group(1)) if 'colspan=' in attr else 1
            st = parse_style(re.search(r'style="([^"]*)"', attr).group(1)) if 'style="' in attr else {}
            cells.append({'v': html.unescape(inner).strip(), 'rs': rs, 'cs': cs, 'st': st})
        raw.append(cells)

    ncols = max((sum(c['cs'] for c in cells) for cells in raw), default=0)
    # 考虑 rowspan 占位后真实列数
    nrows = len(raw)
    grid = [[None] * ncols for _ in range(nrows)]

    for r, cells in enumerate(raw):
        c = 0
        for cell in cells:
            while c < ncols and grid[r][c] is not None:
                c += 1
            st = cell['st']
            fs = st.get('font-size', '')
            fs = float(re.match(r'([\d.]+)', fs).group(1)) if fs else None
            ff = st.get('font-family', '').split(',')[0].strip()
            bd = st.get('border', '')
            if bd == 'none':
                has_bd = 0
            elif bd:
                has_bd = 1
            else:
                # 逐边写法
                has_bd = 1 if any(k in st for k in
                                  ('border-top', 'border-left', 'border-right', 'border-bottom')) else 0
            hgt = st.get('height', '')
            hgt = float(re.match(r'([\d.]+)', hgt).group(1)) if hgt else None
            rec = {
                'v': cell['v'], 'fs': fs, 'ff': norm_ff(ff),
                'b': 1 if 'bold' in st.get('font-weight', '') else 0,
                'ha': st.get('text-align', ''), 'va': st.get('vertical-align', ''),
                'bd': has_bd, 'rs': cell['rs'], 'cs': cell['cs'],
                'h': hgt, 'merge': (cell['rs'] > 1 or cell['cs'] > 1),
            }
            for dr in range(cell['rs']):
                for dc in range(cell['cs']):
                    if r + dr < nrows and c + dc < ncols:
                        grid[r + dr][c + dc] = 'span'
            grid[r][c] = rec
            c += cell['cs']

    heights = []
    for r, cells in enumerate(raw):
        h = None
        for cell in cells:
            hh = cell['st'].get('height', '')
            if hh:
                h = float(re.match(r'([\d.]+)', hh).group(1))
                break
        heights.append(h)

    return {'grid': grid, 'nrows': nrows, 'ncols': ncols,
            'heights': heights, 'widths': widths}

# ---------- 比对 ----------
HA_MAP = {0: 'general', 1: 'left', 2: 'center', 3: 'right'}
VA_MAP = {0: 'top', 1: 'middle', 2: 'bottom'}

def compare(label, xls_path, html_path, skip_value_rows=()):
    A = read_xls(xls_path)
    B = read_html(html_path)
    print('=' * 74)
    print('【%s】' % label)
    print('  原始 %d行×%d列   导出 %d行×%d列   %s'
          % (A['nrows'], A['ncols'], B['nrows'], B['ncols'],
             'OK' if (A['nrows'] == B['nrows'] and A['ncols'] == B['ncols']) else '❌不一致'))

    diffs = {'fs': [], 'ff': [], 'b': [], 'ha': [], 'va': [], 'bd': [], 'span': [], 'val': []}
    R = min(A['nrows'], B['nrows'])
    C = min(A['ncols'], B['ncols'])
    for r in range(R):
        for c in range(C):
            a = A['grid'][r][c]
            b = B['grid'][r][c]
            if b is None or b == 'span':
                continue
            if a['fs'] and b['fs'] and abs(a['fs'] - b['fs']) > 0.05:
                diffs['fs'].append((r, c, a['fs'], b['fs']))
            if a['ff'] and b['ff'] and a['ff'] not in b['ff'] and b['ff'] not in a['ff']:
                diffs['ff'].append((r, c, a['ff'], b['ff']))
            if a['b'] != b['b']:
                diffs['b'].append((r, c, a['b'], b['b']))
            if a['ha'] is not None and b['ha']:
                exp = HA_MAP.get(a['ha'], '')
                if exp and exp != b['ha'] and not (exp == 'general' and b['ha'] == 'left'):
                    diffs['ha'].append((r, c, exp, b['ha']))
            if a['va'] is not None and b['va']:
                exp = VA_MAP.get(a['va'], '')
                if exp and exp != b['va']:
                    diffs['va'].append((r, c, exp, b['va']))
            if a['bd'] != b['bd']:
                diffs['bd'].append((r, c, a['bd'], b['bd']))
            if (a['rs'], a['cs']) != (b['rs'], b['cs']):
                diffs['span'].append((r, c, (a['rs'], a['cs']), (b['rs'], b['cs'])))
            av = str(a['v']).strip()
            if r not in skip_value_rows and av and av.replace('\n', '') != b['v'].replace('\n', ''):
                diffs['val'].append((r, c, av[:26], b['v'][:26]))

    for k, name in [('span', '合并跨度'), ('fs', '字号'), ('ff', '字体'), ('b', '粗体'),
                    ('ha', '水平对齐'), ('va', '垂直对齐'), ('bd', '边框'), ('val', '内容')]:
        lst = diffs[k]
        if lst:
            print('  ❌ %s：%d 处不同' % (name, len(lst)))
            for it in lst[:8]:
                print('       %s' % (it,))
            if len(lst) > 8:
                print('       ... 另 %d 处' % (len(lst) - 8))
        else:
            print('  ✅ %s 全部一致' % name)

    # 行高 / 列宽
    hd = [(r, a, b) for r, (a, b) in enumerate(zip(A['heights'], B['heights']))
          if a and b and abs(a - b) > 1.5]
    print('  %s 行高：%s' % ('❌' if hd else '✅',
                            '原始 %s / 导出 %s' % (A['heights'][:6], B['heights'][:6]) if not hd
                            else '%d 处不同 ' % len(hd) + str(hd[:5])))
    wd = [(c, a, b) for c, (a, b) in enumerate(zip(A['widths'], B['widths']))
          if a and b and abs(a - b) > 3]
    print('  %s 列宽：%s' % ('❌' if wd else '✅',
                            '原始 %s' % (A['widths'][:8]) + ' / 导出 %s' % (B['widths'][:8]) if not wd
                            else '%d 处不同 ' % len(wd) + str(wd[:6])))
    return diffs

CASES = [
    ('全日制观察记录表',
     os.path.join(DESK, '2026年 秋季全日制观察电子版.xls'),
     os.path.join(BASE_DIR, '_samples', '全日制观察记录表-大一-2026年9月.xls'),
     set()),
    ('通风消毒记录表',
     os.path.join(DESK, '2026夏季消毒记录表电子班.xls'),
     os.path.join(BASE_DIR, '_samples', '通风消毒记录表-大一-2026年9月.xls'),
     set(range(3, 26))),          # 日期与打勾区由用户填写，跳过内容比对
    ('交接班记录表',
     os.path.join(DESK, '交接班记录 - 新版2026电子版.xls'),
     os.path.join(BASE_DIR, '_samples', '交接班记录-大一-2026年9月.xls'),
     set()),
]

if __name__ == '__main__':
    for label, xp, hp, skip in CASES:
        if not os.path.exists(xp):
            print('!! 缺少原始文件', xp); continue
        if not os.path.exists(hp):
            print('!! 缺少导出文件', hp); continue
        compare(label, xp, hp, skip)
        print()
