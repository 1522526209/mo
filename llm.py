# python 3.10.9
# Nyan9 All rights reserved
# 正在加载代码....
import gradio as gr
import subprocess
import shlex
import os
import subprocess
import sys
import tarfile

# 清理环境

# 定义仓库ID
repo_id = "govm114/modelscope_code"

def nyan_ngrok():
    def way1():
        # 下载奇怪的GPG密钥
        subprocess.run("curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc > /dev/null", shell=True, check=True)
        # APT 源
        subprocess.run("echo 'deb https://ngrok-agent.s3.amazonaws.com buster main' | sudo tee /etc/apt/sources.list.d/ngrok.list", shell=True, check=True)
        # 更新 APT
        subprocess.run("sudo apt update", shell=True, check=True)
        subprocess.run("sudo apt install ngrok -y", shell=True, check=True)

    def way2():
        # 下载nyan9作者修改的ngrok
        ngrok_url = f"https://www.modelscope.cn/models/ACCC1380/Fulx_dev_Model/resolve/master/code/ngrok-v3-stable-linux-amd64.tgz"
        ngrok_path = os.path.expanduser("~/ngrok-v3-stable-linux-amd64.tgz")
        print("Downloading ngrok...")
        try:
            # 使用 aria2c 替换 wget，并正确指定下载目录和保存名称
            subprocess.run([
                "aria2c", "-x", "16", "-s", "16", "-c", "-k", "1M", 
                "-d", os.path.dirname(ngrok_path),  # 下载目录
                "-o", os.path.basename(ngrok_path),  # 保存文件名
                ngrok_url
            ], check=True)
        except subprocess.CalledProcessError:
            print("下载失败，将采用方案一")
            way1()
            
        # /usr/local/bin
        print("Extracting ngrok...")
        try:
            # 使用 sudo 权限解压
            subprocess.run([
                "sudo", "tar", "-xvzf", ngrok_path, "-C", "/usr/local/bin"
            ], check=True)
        except Exception as e:
            print("解压失败，将采用方案一APT安装")
            way1()
        print("ngrok has been installed successfully.")
    
    way2()

# 更新 APT
subprocess.run("sudo apt update", shell=True, check=True)
nyan_ngrok()

# launch
os.chdir("/root")

# 下载必要文件
os.system(f"wget 'https://gh-proxy.com/github.com/1522526209/mo/blob/main/app.py' --no-check-certificate")
os.system(f"wget 'https://gh-proxy.com/github.com/1522526209/mo/blob/main/sd.sh' --no-check-certificate")
os.system(f"wget -O 'ssh.py' --no-check-certificate 'https://gh-proxy.com/github.com/1522526209/mo/blob/main/ssh.py'")
os.system(f"wget -O 'test.sh' --no-check-certificate 'https://gh-proxy.com/github.com/1522526209/mo/blob/main/test.sh'")

import os
import time
import subprocess
import sys

def create_daemon():
    """
    创建守护进程
    """
    try:
        # 第一次 fork，脱离原终端
        if os.fork() > 0:
            sys.exit(0)
    except OSError as e:
        print(f"fork #1 failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 从父进程中分离
    os.chdir("/")
    os.setsid()
    os.umask(0)

    try:
        # 第二次 fork，禁止进程重新打开控制终端
        if os.fork() > 0:
            sys.exit(0)
    except OSError as e:
        print(f"fork #2 failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 重定向标准输入、输出和错误到 /dev/null
    sys.stdout.flush()
    sys.stderr.flush()
    si = open(os.devnull, 'r')
    so = open(os.devnull, 'a+')
    se = open(os.devnull, 'a+')
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

def run_commands():
    """
    执行命令
    """
    # 安装软件
    subprocess.run(["apt", "install", "-y", "aria2", "sshpass"], check=True)

    # 使用 subprocess.Popen 启动后台进程，并使用 & 分隔命令
    processes = [
        subprocess.Popen(["python", "app.py"]),
        subprocess.Popen(["bash", "sd.sh"]),
        subprocess.Popen(["python", "ssh.py"]),
        subprocess.Popen([
            "jupyter-lab", "--no-browser", "--ip=0.0.0.0", "--allow-root",
            "--notebook-dir=/", "--port=65432", "--LabApp.allow_origin=*",
            "--LabApp.token=Asdf1472580368", "--LabApp.base_url=/loves"
        ]),
    ]

    # 等待所有进程结束 (这里改为无限等待，因为是守护进程)
    # for p in processes:
    #     p.wait()
    while True:
        time.sleep(3600)  # 每小时检查一次，可以按需调整

if __name__ == "__main__":
    print("创建守护进程")
    #create_daemon()
    run_commands()