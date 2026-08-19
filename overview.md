# 家园沟通站 · 项目概览

## 当前状态

方式B 纯静态 PWA，Service Worker 缓存版本 **jiayuan-v10**。

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
- **后续更新**：修改代码后，把 `sw.js` 的 `CACHE_NAME` 升一版（如 v11），再 `git push` 即可；手机端关掉重开生效。

## 本次改动（v10）

- 回退 v9 的全屏海报 + 背景图更换方案：用户反馈不好看，已恢复为 v8 的日历卡片网格样式。
- 节假日倒计时现在只以卡片网格展示，每张卡片显示「几月 / 几日 / 星期几 / 名称 / 倒计时」，已过的节日名称加下划线、卡片变浅灰，今天高亮金色。
- 删除 `holiday-bg.jpg` 与背景图相关代码（更换/恢复默认按钮、canvas 压缩、localStorage 字段），`sw.js` 升级到 v10 并从缓存列表移除背景图。
- 同步更新 `preview.html`、`搭建与测试说明.md`。

## 主要文件

| 文件 | 说明 |
|---|---|
| `index.html` | 主应用（记录 / 周报 / 孩子 / 设置） |
| `sw.js` | 离线缓存（CACHE_NAME = jiayuan-v10） |
| `manifest.json` | PWA 安装名片 |
| `icon-192.png` / `icon-512.png` | 安装图标 |
| `start-server.bat` | 双击启动本地预览服务器 |
| `preview.html` | 离线预览入口，双击即可在浏览器查看（无需服务器/联网） |
| `搭建与测试说明.md` | 部署、测试、排错说明 |

## 下次注意

如果再次修改代码，请继续把 `sw.js` 里的 `CACHE_NAME` 升级到 v11、v12…，否则已安装的 PWA 会缓存旧版页面。
