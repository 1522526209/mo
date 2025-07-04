#!/bin/bash

# 检测是否安装了cloudflared
if ! command -v cloudflared &> /dev/null; then
    echo "检测到未安装cloudflared，开始安装..."
    wget -O cloudflared.deb "https://gh-proxy.com/https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb" --no-check-certificate && 
    sudo dpkg -i cloudflared.deb && 
    rm cloudflared.deb
else
    echo "检测到已安装cloudflared。"
fi

# 检测是否已登录
if  cloudflared status | grep -q "Connected to Cloudflare"; then
    echo "检测到已登录cloudflared。"
else
    echo "检测到未登录cloudflared，开始登录..."
    cloudflared service install eyJhIjoiNTMyMjBjYzE2ZjFlMzgwZDg3OTRjMzI3MjEyNmM2OTEiLCJ0IjoiZDg3NWMxM2ItOTdlZi00MzU4LTgzYTItOTMxZTY1NWE5ZWI1IiwicyI6Ik1XUXlPVGd6TldVdFpUYzNNeTAwWlRBM0xXSTBaVGN0TWpRd09XSTNOemd3TXpFMCJ9    
    if [ $? -eq 0 ]; then
        echo "登录成功！"
    else
        echo "登录失败，请检查配置和网络连接！"
    fi
fi
sleep 5
echo "检查服务状态：$(date)"
echo "操作完成！"