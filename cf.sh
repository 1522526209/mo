wget -O cloudflared.deb "https://gh-proxy.com/https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb" --no-check-certificate && 
sudo dpkg -i cloudflared.deb && 
rm cloudflared.deb
cloudflared service install eyJhIjoiNTMyMjBjYzE2ZjFlMzgwZDg3OTRjMzI3MjEyNmM2OTEiLCJ0IjoiZDg3NWMxM2ItOTdlZi00MzU4LTgzYTItOTMxZTY1NWE5ZWI1IiwicyI6Ik1XUXlPVGd6TldVdFpUYzNNeTAwWlRBM0xXSTBaVGN0TWpRd09XSTNOemd3TXpFMCJ9    
