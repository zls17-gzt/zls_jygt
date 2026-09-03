# -*- coding: utf-8 -*-
"""由 index.html 生成 preview.html：把 localStorage 安全包装层替换为直接透传。
（preview 用于本地 file:// 双击打开，不需要 iOS 无痕模式的降级逻辑）"""
import io, re, sys

src = io.open('index.html', encoding='utf-8').read()

START = '    const ls = {'
END_MARK = '    /* ============ B0-2'

i = src.index(START)
j = src.index(END_MARK)
assert i < j, '标记顺序异常'

REPL = '''    const ls = (function () {
      try {
        const t = '_t_' + Date.now()
        window.localStorage.setItem(t, '1')
        window.localStorage.removeItem(t)
        return window.localStorage
      } catch (e) {
        const mem = {}
        return {
          getItem: function (k) { return (k in mem) ? mem[k] : null },
          setItem: function (k, v) { mem[k] = String(v) },
          removeItem: function (k) { delete mem[k] }
        }
      }
    })()

'''

out = src[:i] + REPL + src[j:]
io.open('preview.html', 'w', encoding='utf-8', newline='\n').write(out)
print('preview.html 已生成，长度', len(out))
print('剩余 localStorage. 引用数：', len(re.findall(r'localStorage\.', out)))
