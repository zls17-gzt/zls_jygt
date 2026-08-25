# 家园沟通站 · 项目概览

## 当前状态

方式B 纯静态 PWA，Service Worker 缓存版本 **jiayuan-v16**。

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

## 本次改动（v16 · 设置页移除节假日倒计时）

- 设置页里的**「节假日倒计时」卡片已删除**，不再展示内置节假日的倒计时网格。
- **自定义节假日管理保留**：仍可添加、删除自己的节假日；自定义节假日继续用于月历粉点标记和首页「最近节日」统计。
- 同步清理了仅用于倒计时的 `.holiday-grid` / `.holiday-card` 等 CSS。
- `sw.js` 升级到 v16。

> 之前 v15 的改动：月历已写笔记的日期格半透明并直接显示编辑文字。

> 之前 v14 的改动：月历每个日期格支持双击编辑、填写「今天的待办 / 做了什么」，数据存 localStorage `jiayuan-daynotes`，全站共享。

> 之前 v11/v12/v13 的改动：奶油黄可爱风格首页、吉祥物大卡片、统计概览、卡通图标、左侧边栏导航、月历组件等已全部保留。

## 主要文件

| 文件 | 说明 |
|---|---|
| `index.html` | 主应用（左侧边栏 + 奶油黄可爱风格） |
| `sw.js` | 离线缓存（CACHE_NAME = jiayuan-v16） |
| `manifest.json` | PWA 安装名片 |
| `icon-192.png` / `icon-512.png` | 安装图标 |
| `icons/` | 从素材图裁出的 9 张卡通图标 |
| `start-server.bat` | 双击启动本地预览服务器 |
| `preview.html` | 离线预览入口，双击即可在浏览器查看 |
| `index.html.bak` | 改版前备份 |
| `搭建与测试说明.md` | 部署、测试、排错说明 |

## 下次注意

如果再次修改代码，请继续把 `sw.js` 里的 `CACHE_NAME` 升级到 v14、v15…，否则已安装的 PWA 会缓存旧版页面。
