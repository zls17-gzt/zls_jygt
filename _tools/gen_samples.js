// 生成三份带示例数据的导出样本，用于和原始 xls 对照
const fs = require('fs')
const code = fs.readFileSync('_tools/_s0.js', 'utf8')

const DAYS = [1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24, 28, 29, 30]
const store = {}
const ls = { getItem: k => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = String(v) }, removeItem: k => { delete store[k] } }

const NOTES = {
  1: '开学第一天，整体适应良好；王梓涵情绪稍紧张', 2: '李思远请假（感冒）；其余幼儿状态良好',
  3: '赵一诺早上用药，已登记；大便正常', 4: '全班户外活动，孙浩然轻微擦伤已处理',
  7: '周一如常；两名幼儿迟到', 8: '陈雨萱早接（9:30家长接走看牙医）',
  9: '午睡情况好；王梓涵大便一次', 10: '张子轩发烧37.8℃，已通知家长接回',
  11: '张子轩请假；其余正常', 14: '新生刘沐宸入园第二天，情绪稳定',
  15: '区域活动秩序良好', 16: '李思远返园，痊愈', 17: '周三维稳；个别幼儿挑食',
  18: '户外活动后大量饮水', 20: '周日补课，到园21人', 21: '孙浩然请假一天',
  22: '秋季运动会彩排', 23: '王梓涵大便两次，略有稀便已关注',
  24: '手工课，整体参与度高', 28: '李思远早接；其余正常',
  29: '月末整理，幼儿情绪平稳', 30: '全月无安全事故'
}
const TEACHERS = ['赵老师', '钱老师', '孙老师']
const obsData = {}
const disData = {}
const hanData = {}
DAYS.forEach((d, i) => {
  obsData[d] = { note: NOTES[d] || '', teacher: TEACHERS[i % 3] }
  const r = {}
  // 通风每天全做
  ;[1, 2, 3, 4].forEach(c => { r[c] = '√' })
  // 消毒项目轮换
  ;[5, 6, 7, 8, 9, 10, 11, 12, 13].forEach(c => { r[c] = '√' })
  // 被褥每周一、水杯毛巾每天、塑料玩具每周五
  r[14] = (d % 7 === 1 || d === 1) ? '√' : ''
  r[15] = '√'; r[16] = '√'
  r[17] = [4, 11, 18, 25].includes(d) ? '√' : ''
  r.sign = TEACHERS[i % 3]
  disData[d] = r
  const absent = (d === 2 || d === 11 || d === 21) ? 2 : (d === 10 ? 1 : 0)
  const should = 32
  hanData[d] = {
    should: String(should),
    actual: String(should - absent),
    absent: String(absent),
    situation: absent ? NOTES[d] + '；缺勤' + absent + '人已电话确认' : (NOTES[d] || ''),
    t1: TEACHERS[i % 3],
    t2: TEACHERS[(i + 1) % 3],
    t3: TEACHERS[(i + 2) % 3]
  }
})
obsData.__foot = '本月无重大安全事件，2 名幼儿因感冒请假，均已痊愈返园。'
store['jiayuan-obsform'] = JSON.stringify({ c1: { '2026-09': obsData } })
store['jiayuan-disinfect'] = JSON.stringify({ c1: { '2026-09': disData } })
store['jiayuan-handover'] = JSON.stringify({ c1: { '2026-09': hanData } })
store['jiayuan-table-dates'] = JSON.stringify({ c1: { '2026-09': DAYS } })

const els = {}
function el(id) {
  if (!els[id]) els[id] = { id, value: '', innerHTML: '', textContent: '', style: {}, dataset: {}, classList: { toggle() {}, add() {}, remove() {} } }
  return els[id]
}
const CLS = { id: 'c1', name: '大一', children: [], records: [] }
const captured = []

global.window = { addEventListener() {}, scrollTo() {}, scrollY: 0 }
global.navigator = { userAgent: 'node' }
global.location = { protocol: 'http:' }
global.alert = () => {}
global.confirm = () => true
global.Blob = class { constructor(p) { this._t = p.join('') } }
global.URL = { createObjectURL: () => 'blob:x', revokeObjectURL() {} }
global.FileReader = class {}
global.File = class {}
global.localStorage = ls
global.document = {
  documentElement: { scrollTop: 0 },
  body: { style: {}, appendChild() {}, removeChild() {} },
  getElementById: el,
  querySelector: () => null,
  querySelectorAll: () => [],   // 不覆盖已存数据
  createElement: () => ({ style: {}, click() {}, setAttribute() {} }),
  execCommand() {}, addEventListener() {}
}

const tail = '\n;return {exportObsFormExcel,exportDisExcel,exportHanExcel};'
const patched = code
  .replace('function getCurrentClass() {', 'function getCurrentClass() { if (__CLS__) return __CLS__;')
  .replace('function saveObsForm(silent) {', 'function saveObsForm(silent) { if (1) return;')
  .replace('function saveDis(silent) {', 'function saveDis(silent) { if (1) return;')
  .replace('function saveHan(silent) {', 'function saveHan(silent) { if (1) return;')
  .replace('async function downloadBlob(blob, filename) {', 'async function downloadBlob(blob, filename) { __dl(blob, filename); return;')
const api = new Function('__dl', '__CLS__', patched + tail)((b, f) => captured.push({ filename: f, html: b._t }), CLS)

el('obs-form-month').value = '2026-09'
el('dis-month').value = '2026-09'
el('han-month').value = '2026-09'
api.exportObsFormExcel(); api.exportDisExcel(); api.exportHanExcel()

captured.forEach(c => {
  fs.writeFileSync('_samples/' + c.filename, c.html, 'utf8')
  console.log('已生成 _samples/' + c.filename, c.html.length)
})
