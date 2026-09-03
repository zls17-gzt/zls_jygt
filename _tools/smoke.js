// 冒烟测试：在 Node 中用最小 DOM 桩执行三个导出函数，输出生成的 HTML
const fs = require('fs')
const code = fs.readFileSync('_tools/_s0.js', 'utf8')

const store = {}
const ls = {
  getItem: k => (k in store ? store[k] : null),
  setItem: (k, v) => { store[k] = String(v) },
  removeItem: k => { delete store[k] }
}
const els = {}
function el(id) {
  if (!els[id]) els[id] = { id, value: '', innerHTML: '', textContent: '', style: {}, dataset: {}, classList: { toggle() {}, add() {}, remove() {} } }
  return els[id]
}
const CLS = { id: 'c1', name: '大一', children: [], records: [] }
let captured = []

global.window = { addEventListener() {}, scrollTo() {}, scrollY: 0 }
global.navigator = { userAgent: 'node', serviceWorker: undefined }
global.location = { protocol: 'http:' }
global.alert = m => console.log('[alert]', m)
global.confirm = () => true
global.console = console
global.Blob = class { constructor(parts) { this._t = parts.join('') } }
global.URL = { createObjectURL: () => 'blob:x', revokeObjectURL() {} }
global.FileReader = class {}
global.File = class {}
// 模拟页面上已填写的输入项
const qsaMap = {
  '[data-obs-note]': [
    { dataset: { obsNote: '1' }, value: '张三请假一天；王五早接' },
    { dataset: { obsNote: '2' }, value: '李四大便两次，状态良好' }
  ],
  '[data-obs-teacher]': [
    { dataset: { obsTeacher: '1' }, value: '赵老师' },
    { dataset: { obsTeacher: '2' }, value: '钱老师' }
  ],
  '[data-dis-day]': [
    { dataset: { disDay: '1', disCol: '1' }, textContent: '√' },
    { dataset: { disDay: '1', disCol: '3' }, textContent: '√' },
    { dataset: { disDay: '1', disCol: '5' }, textContent: '√' },
    { dataset: { disDay: '2', disCol: '2' }, textContent: '√' }
  ],
  '[data-dis-sign]': [
    { dataset: { disSign: '1' }, value: '赵老师' },
    { dataset: { disSign: '2' }, value: '' }
  ],
  '[data-han-day]': [
    { dataset: { hanDay: '1', hanF: 'should' }, value: '32' },
    { dataset: { hanDay: '1', hanF: 'actual' }, value: '30' },
    { dataset: { hanDay: '1', hanF: 'absent' }, value: '2' },
    { dataset: { hanDay: '1', hanF: 'situation' }, value: '整体平稳，两名幼儿感冒请假' },
    { dataset: { hanDay: '1', hanF: 't1' }, value: '赵老师' },
    { dataset: { hanDay: '1', hanF: 't2' }, value: '钱老师' },
    { dataset: { hanDay: '1', hanF: 't3' }, value: '孙老师' }
  ]
}
global.document = {
  documentElement: { scrollTop: 0 },
  body: { style: {}, appendChild() {}, removeChild() {} },
  getElementById: id => el(id),
  querySelector: sel => (sel === '[data-obs-foot]' ? { value: '本月无特殊事项' } : null),
  querySelectorAll: sel => qsaMap[sel] || [],
  createElement: () => ({ style: {}, click() {}, setAttribute() {} }),
  execCommand() {},
  addEventListener() {}
}
global.localStorage = ls

const fnNames = ['exportObsFormExcel', 'exportDisExcel', 'exportHanExcel',
  'getCurrentClass', 'escapeHtml', 'getWorkdays', 'resolveDates', 'localMonthStr',
  'splitBlocks', 'xTd', 'xlsColGroup', 'xlsDoc', 'saveObsForm', 'saveDis', 'saveHan',
  'renderObsForm', 'renderDis', 'renderHan', 'getObsFormData', 'getDisData', 'getHanData',
  'renderDateBar', 'openObsFormModal', 'openDisModal', 'openHanModal']

// 在代码末尾追加导出绑定
const tail = '\n;return {' + fnNames.map(n => n + ':' + n).join(',') + '};'
function downloadBlob(blob, filename) {
  captured.push({ filename, html: blob._t })
}

// 预置数据
const OBS = { c1: { '2026-09': { 1: { note: '张三请假一天', teacher: '赵老师' }, 2: { note: '李四大便两次', teacher: '钱老师' }, __foot: '本月无特殊事项' } } }
const DIS = { c1: { '2026-09': { 1: { 1: '√', 3: '√', 5: '√', 18: undefined, sign: '赵老师' }, 2: { 2: '√', 6: '√', sign: '' } } } }
const HAN = { c1: { '2026-09': { 1: { should: '32', actual: '30', absent: '2', situation: '整体平稳，两名幼儿感冒请假', t1: '赵老师', t2: '钱老师', t3: '孙老师' } } } }
store['jiayuan-obsform'] = JSON.stringify(OBS)
store['jiayuan-disinfect'] = JSON.stringify(DIS)
store['jiayuan-handover'] = JSON.stringify(HAN)
// 自定义园历：2026-09 使用与原始表格一致的 22 天
store['jiayuan-table-dates'] = JSON.stringify({ c1: { '2026-09': [1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24, 28, 29, 30] } })

console.log('== 代码加载检查 ==')
function run() {
  const patched = code
    .replace('function getCurrentClass() {', 'function getCurrentClass() { if (__CLS__) return __CLS__;')
    .replace('async function downloadBlob(blob, filename) {', 'async function downloadBlob(blob, filename) { __dl(blob, filename); return;')
  const w2 = new Function('__dl', '__CLS__', patched + tail)
  const a = w2((b, f) => { captured.push({ filename: f, html: b._t }) }, CLS)
  console.log('函数加载成功:', Object.keys(a).length)
  el('obs-form-month').value = '2026-09'
  el('dis-month').value = '2026-09'
  el('han-month').value = '2026-09'

  a.exportObsFormExcel()
  a.exportDisExcel()
  a.exportHanExcel()

  // 渲染测试
  a.renderObsForm(); a.renderDis(); a.renderHan()
  console.log('\n[render] obs-form 长度', el('obs-form-table-container').innerHTML.length)
  console.log('[render] dis 长度', el('dis-table-container').innerHTML.length)
  console.log('[render] han 长度', el('han-table-container').innerHTML.length)
  console.log('[render] dateBar:', el('obs-form-dates').innerHTML.slice(0, 200))
  // 保存落盘检查
  a.saveObsForm(true); a.saveDis(true); a.saveHan(true)
  console.log('\n[save] obsform:', store['jiayuan-obsform'].slice(0, 220))
  console.log('[save] dis:', store['jiayuan-disinfect'].slice(0, 160))
  console.log('[save] han:', store['jiayuan-handover'].slice(0, 200))
  // 渲染结果落盘
  fs.writeFileSync('_tools/render_obs.html', el('obs-form-table-container').innerHTML)
  fs.writeFileSync('_tools/render_dis.html', el('dis-table-container').innerHTML)
  fs.writeFileSync('_tools/render_han.html', el('han-table-container').innerHTML)
  fs.writeFileSync('_tools/render_datebar.html', el('obs-form-dates').innerHTML)
}
run()

captured.forEach(c => {
  fs.writeFileSync('_tools/out_' + c.filename.replace(/[^\w\u4e00-\u9fa5.-]/g, '_'), c.html)
  console.log('\n=== ' + c.filename + ' (' + c.html.length + ' 字符) ===')
})
console.log('\n文件已写入 _tools/')
