# 家园沟通站 · 项目概览

## 当前状态

方式B 纯静态 PWA，Service Worker 缓存版本 **jiayuan-v10**。

**已部署公网网址（HTTPS，长期可用）：**
https://fe490d420d5d48e198d4e774eb14927b.app.workbuddy.link

手机/电脑浏览器打开即可使用，可「添加到主屏幕」当作 App；离线也能打开（Service Worker 在 https 下生效）。

> 该链接依托 WorkBuddy 云托管，长期有效；可作为临时/备用网址。

## 部署到 GitHub Pages（用户已选，永久自主）

用户已明确要求走 GitHub Pages 永久托管（见 `搭建与测试说明.md` B4 章节）。

- **代码已就绪**：本机 `jiayuan-workbench/` 已 `git init` 并提交初始版本（含 `.nojekyll`）。
- **两种方式**：① 网页拖拽上传 6 个文件（推荐，零安装）；② 装 `gh` 并 `gh auth login` 后由我一键发布。
- **必须用户本人做的步骤**：注册 GitHub 账号、创建 `jiayuan-workbench` 公开仓库、开启 Pages（`Settings → Pages → main / (root)`）。
- **最终网址**：`https://你的用户名.github.io/jiayuan-workbench/`（永久有效，不依赖第三方）。

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
