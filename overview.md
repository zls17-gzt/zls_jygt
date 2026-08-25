# 家园沟通站 · 项目概览

## 当前状态

方式B 纯静态 PWA，Service Worker 缓存版本 **jiayuan-v11**。

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
- **后续更新**：修改代码后，把 `sw.js` 的 `CACHE_NAME` 升一版（如 v12），再 `git push` 即可；手机端关掉重开生效。

## 本次改动（v11 · 可爱风格改版）

- 按用户提供的「星星小屋」参考图，把整体 UI 改成奶油黄可爱风格：固定顶栏（标题 + 日期 + 本地存储状态）、首页大卡片（问候 + 实时时间 + 卡通吉祥物 + 4 个快捷入口）、统计概览（今日记录 / 孩子总数 / 最近节日）、今日小提示。
- 底部 Tab 改用卡通图标：首页 / 记录 / 周报 / 孩子 / 设置。
- 从用户素材图 `01.jpg`（3×3 网格）裁出 9 张图标（mascot / eat / work / sport / briefcase / flower / drink / rest / card），存入 `icons/` 目录并加入 sw.js 离线缓存。
- 记录 / 周报 / 孩子 / 设置四个页功能全部保留（多选幼儿、图片压缩、编辑删除、CSV 导入、班级切换、节假日日历卡片等），仅重排样式。
- `index.html` 已备份为 `index.html.bak`；`sw.js` 升级到 v11 并把 `icons/*` 全部加入缓存列表；同步更新 `preview.html`。

## 主要文件

| 文件 | 说明 |
|---|---|
| `index.html` | 主应用（首页 / 记录 / 周报 / 孩子 / 设置，奶油黄可爱风格） |
| `sw.js` | 离线缓存（CACHE_NAME = jiayuan-v11） |
| `manifest.json` | PWA 安装名片 |
| `icon-192.png` / `icon-512.png` | 安装图标 |
| `icons/` | 从素材图裁出的 9 张卡通图标（mascot/eat/work/sport/briefcase/flower/drink/rest/card） |
| `start-server.bat` | 双击启动本地预览服务器 |
| `preview.html` | 离线预览入口，双击即可在浏览器查看（无需服务器/联网） |
| `index.html.bak` | 改版前备份 |
| `搭建与测试说明.md` | 部署、测试、排错说明 |

## 下次注意

如果再次修改代码，请继续把 `sw.js` 里的 `CACHE_NAME` 升级到 v12、v13…，否则已安装的 PWA 会缓存旧版页面。
