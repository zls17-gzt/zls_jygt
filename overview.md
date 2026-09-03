# 家园沟通站 · 项目概览

## 当前状态

方式B 纯静态 PWA，Service Worker 缓存版本 **jiayuan-v47**。

**永久网址（GitHub Pages，自主可控）：**
https://zls17-gzt.github.io/zls_jygt/

**备用网址（WorkBuddy 云托管，长期可用）：**
https://fe490d420d5d48e198d4e774eb14927b.app.workbuddy.link

两个网址都能用，手机/电脑浏览器打开即可，可「添加到主屏幕」当作 App；离线也能打开（Service Worker 在 https 下生效）。**建议以 GitHub Pages 网址为主**，它不依赖任何第三方、只要仓库在就一直有效。

## 部署到 GitHub Pages（已完成 ✅）

- **仓库**：https://github.com/zls17-gzt/zls_jygt （Public，空仓库初始化）
- **推送方式**：用户提供 Classic PAT，已 `git push` 到 `main` 分支（含 `.nojekyll`）。
- **Pages**：已通过 GitHub API 开启，`source = main / (root)`，构建完成返回 200。
- **永久网址**：https://zls17-gzt.github.io/zls_jygt/ （实测可访问，title=家园沟通站）
- **后续更新**：修改代码后，把 `sw.js` 的 `CACHE_NAME` 升一版（如 v13），再 `git push` 即可；手机端关掉重开生效。

## 本次改动（v44 · 表格弹窗底部留白，避免被浏览器导航栏遮挡）

- 三张园所表格弹窗（观察表 / 通风消毒记录表 / 交接班表）底部增加 `80px + env(safe-area-inset-bottom)` 留白。
- 弹窗内容区改为顶部对齐（`align-items:flex-start`），长表格可从顶部自然向下滚动。
- 解决华为浏览器等机型中，弹窗最下方的「说明」文字被底部浏览器导航栏盖住的问题。
- `sw.js` 升级到 v44。

## 本次改动（v45 · 点名册弹窗补上同样的底部留白）

- 点名册弹窗（`attendance-modal`）此前未应用 v44 的修复，在华为浏览器底部同样被导航栏遮挡。
- 统一补上：外层 `align-items:flex-start` + `padding-bottom: calc(12px + env(safe-area-inset-bottom, 0px) + 80px)`；内层卡片底部留白 `calc(16px + env(safe-area-inset-bottom, 0px) + 80px)`。
- 至此四类园所弹窗（点名册 / 观察表 / 通风消毒记录表 / 交接班表）底部留白一致。
- `sw.js` 升级到 v45。

## 本次改动（v47 · 体温选项收窄为 36.0~38.0）

- 体温下拉档位由 `35.5~39.9`（45 档）收窄为 `36.0~38.0`（每 0.1 度，共 21 档），减少滚动长度；`△（没来）` 与空值 `℃` 占位保留。
- 导出 Excel 版式不变，仍 1:1 还原原 xls。
- `sw.js` 升级到 v47。

## 本次改动（v46 · 点名册体温改为下拉选择）

- 点名册每个体温单元格由「自由输入」改为「下拉选择」：`35.5~39.9`（每 0.1 度一档）共 45 个可选项 + `△（没来）`。
- 没来的孩子可直接选 `△`；已存数据会在下拉中自动回显选中项。
- **导出 Excel 完全不变**：仍按原 xls 版式（标题/班级行/日期行/姓名+上午下午/体温逐格），单元格只填入所选数值或 `△`，样式 1:1 还原。
- `sw.js` 升级到 v46。

## 本次改动（v20 · 左侧边栏改回底部 Tab 栏）

- 导航从**左侧固定边栏**改回**底部 Tab 栏**，更适合手机单手操作。
- 底部栏图标在上、文字在下，5 个入口均分宽度；当前项文字加粗、图标高亮。
- 页面布局同步调整：顶栏恢复全宽，内容区底部留出 90px 避免被 Tab 栏遮挡。
- `sw.js` 升级到 v20。

> 之前 v19 的改动：修复手机端 CSV 模板下载无反应；添加孩子仅姓名必填。

> 之前 v18 的改动：新增「发现新版本」刷新提示条，SW 改为等待用户点击后才激活。

> 之前 v17 的改动：顶栏标题改为「遇见」。

> 之前 v16 的改动：设置页移除「节假日倒计时」，保留自定义节假日管理。

> 之前 v15 的改动：月历已写笔记的日期格半透明并直接显示编辑文字。

> 之前 v14 的改动：月历每个日期格支持双击编辑、填写「今天的待办 / 做了什么」，数据存 localStorage `jiayuan-daynotes`，全站共享。

> 之前 v11/v12/v13 的改动：奶油黄可爱风格首页、吉祥物大卡片、统计概览、卡通图标、左侧边栏导航、月历组件等已全部保留。

## 主要文件

| 文件 | 说明 |
|---|---|
| `index.html` | 主应用（底部 Tab 栏 + 奶油黄可爱风格） |
| `sw.js` | 离线缓存（CACHE_NAME = jiayuan-v45） |
| `manifest.json` | PWA 安装名片 |
| `icon-192.png` / `icon-512.png` | 安装图标 |
| `icons/` | 从素材图裁出的 9 张卡通图标 |
| `start-server.bat` | 双击启动本地预览服务器 |
| `preview.html` | 离线预览入口，双击即可在浏览器查看（由 `_tools/gen_preview.py` 从 index.html 生成） |
| `index.html.bak` | 改版前备份 |
| `_tools/` | xls 格式解析与导出验证脚本 |
| `_samples/` | 三张园所表格的导出样例，用于和原始 xls 对照 |
| `搭建与测试说明.md` | 部署、测试、排错说明 |

## 班级管理 · 四类园所表格

| 表格 | 入口 | 存储 key | 结构 |
|---|---|---|---|
| 点名册 | 班级管理 → 打开点名册 | `jiayuan-attendance` | 每孩上下午两行 × 工作日体温 |
| 全日制观察记录表 | 班级管理 → 打开观察表 | `jiayuan-obsform` | 19 列：日期 / 幼儿情况（B~R 合并）/ 记录教师，表尾 92pt 备注 |
| 通风消毒记录表 | 班级管理 → 打开消毒记录表 | `jiayuan-disinfect` | 19 列 × 两个半页块，单元格点一下打「√」 |
| 交接班记录表 | 班级管理 → 打开交接班表 | `jiayuan-handover` | 8 列 × 两个半页块，应到/实到/缺勤/在园情况 + 三位教师签字 |

**共用园历**：`jiayuan-table-dates`，按「班级 + 月份」存自定义日期数组；未设置时默认周一至周五。三张表共用，可在任一弹窗顶部用「＋加这天 / ×删除 / ↺恢复周一至周五」调整（原始模板含调休周日、排除中秋等法定假日，不能纯靠周一至周五推导）。

**导出规格**（与原 xls 逐项比对，见 `_tools/dump_xls.py` / `grid.py`）：

| 表格 | 行高(pt) | 字号/字体 | 列宽(px) | 合并 |
|---|---|---|---|---|
| 观察表 | 37 / 26 / 37 / 44 / 92 | 20pt 宋体标题，其余 12pt 宋体 | A 列 64(默认)，B~R 45~70，S 78 | B~R 合并 17 列；表尾合并 19 列 |
| 消毒表 | 39 / 26 / 42 / 35 / 92 | 20pt 宋体标题，其余 12pt 宋体 | 同观察表 | 通风 4 列、消毒 14 列；说明行合并 19 列 |
| 交接班表 | 42 / 42 / 39 / 35 | 12pt 方正小标宋简体标题，14pt 仿宋_GB2312 表头，12pt 宋体数据 | 42 / 58 / 61 / 56 / 331 / 114 ×3 | 前 5 列表头 rowspan=2；「交接班时间下午14:30」colspan=3 |

导出产物是 HTML 伪装的 `.xls`（`application/vnd.ms-excel`），Excel / WPS 打开即为带样式的表格。

## 下次注意

1. 如果再次修改代码，请继续把 `sw.js` 里的 `CACHE_NAME` 升级到 v42、v43…，否则已安装的 PWA 会缓存旧版页面。
2. **推送失败的解决办法**：本机环境变量里有代理 `http://127.0.0.1:61803`，它经常对 `github.com` 返回 `502 CONNECT tunnel failed`，导致 `git push` 反复失败。绕过它即可成功：

   ```bash
   env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY \
     git -c http.proxy= -c https.proxy= -c credential.helper= \
     push "https://zls17-gzt:<PAT>@github.com/zls17-gzt/zls_jygt.git" main
   ```

   （`credential.helper` 默认是 GitHub Desktop 的 `helper-selector`，直连时会取不到凭据，所以要显式带上 PAT。）
