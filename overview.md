# 家园沟通站 · 项目概览

## 当前状态

方式B 纯静态 PWA，Service Worker 缓存版本 **jiayuan-v13**。

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

## 本次改动（v13 · 首页月历）

- 在首页快捷入口大卡片下方、统计区域上方新增**月历组件**：显示当月日期网格，顶部有「上月 / 下月」切换。
- 月历标记：
  - **当天**高亮为奶油黄主色；
  - **有记录的日期**显示橘色小圆点；
  - **节假日**显示粉色小圆点（hover 显示节日名）。
- 点击日期：如果当天有记录，弹窗列出记录；如果无记录，询问是否跳转到「记录」页添加。
- 样式保持奶油黄可爱风，与现有卡片、侧边栏统一。
- `sw.js` 升级到 v13。

> 之前 v11/v12 的改动：奶油黄可爱风格首页、吉祥物大卡片、统计概览、卡通图标、左侧边栏导航等已全部保留。

## 主要文件

| 文件 | 说明 |
|---|---|
| `index.html` | 主应用（左侧边栏 + 奶油黄可爱风格） |
| `sw.js` | 离线缓存（CACHE_NAME = jiayuan-v13） |
| `manifest.json` | PWA 安装名片 |
| `icon-192.png` / `icon-512.png` | 安装图标 |
| `icons/` | 从素材图裁出的 9 张卡通图标 |
| `start-server.bat` | 双击启动本地预览服务器 |
| `preview.html` | 离线预览入口，双击即可在浏览器查看 |
| `index.html.bak` | 改版前备份 |
| `搭建与测试说明.md` | 部署、测试、排错说明 |

## 下次注意

如果再次修改代码，请继续把 `sw.js` 里的 `CACHE_NAME` 升级到 v14、v15…，否则已安装的 PWA 会缓存旧版页面。
