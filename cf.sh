#!/bin/bash
set -e  # 遇到错误立即终止脚本

# 检测是否安装了cloudflared
if ! command -v cloudflared &> /dev/null; then
    echo "检测到未安装cloudflared，开始安装..."
    
    # 使用官方GitHub直接下载链接（修复了原代理链接的404问题）
    wget -O cloudflared.deb "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb " || {
        echo "下载失败，请检查网络连接！"
        exit 1
    }
    
    sudo dpkg -i cloudflared.deb && rm cloudflared.deb
    echo "cloudflared安装完成。"
else
    echo "检测到已安装cloudflared。"
fi

# 检测是否已登录
if sudo cloudflared status | grep -q "Connected to Cloudflare"; then
    echo "检测到已登录cloudflared。"
else
    echo "检测到未登录cloudflared，开始登录..."
    
    # 安装服务并验证结果（修复了语法错误，拆分为两行）
    sudo cloudflared service install eyJhIjoiNTMyMjBjYzE2ZjFlMzgwZDg3OTRjMzI3MjEyNmM2OTEiLCJ0IjoiZDg3NWMxM2ItOTdlZi00MzU4LTgzYTItOTMxZTY1NWE5ZWI1IiwicyI6Ik1XUXlPVGd6TldVdFpUYzNNeTAwWlRBM0xXSTBaVGN0TWpRd09XSTNOemd3TXpFMCJ9
    if [ $? -eq 0 ]; then
        echo "登录成功！"
        # 启动并启用开机自启（参考[[3]]和[[10]]）
        sudo systemctl enable --now cloudflared
    else
        echo "登录失败，请检查配置和网络连接！"
        exit 1
    fi
fi

# 检查服务状态（参考[[10]]）
sleep 5
echo "检查服务状态：$(date)"
sudo systemctl status cloudflared --no-pager
echo "操作完成！"