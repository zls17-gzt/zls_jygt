@echo off
chcp 65001 >nul
echo 正在启动家园沟通站本地预览...
echo 启动后请用浏览器访问：http://localhost:8081/
echo 按 Ctrl+C 可关闭服务器
echo.
python -m http.server 8081
pause
