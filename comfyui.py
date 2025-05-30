import subprocess
import threading
import time
import os

# 检查文件是否存在
def check_file_exists(file_path):
    while os.path.exists(file_path):
        print(f"等待文件 {file_path} 下载完成...")
        time.sleep(1)  # 等待 1 秒钟后再检查
    print(f"文件 {file_path} 已下载完成。")

# 下载并解压的函数
def download_file_A():
    download_cmd_A = "cd /root && aria2c -x 16 -s 16 -c -k 1M 'https://www.modelscope.cn/models/ACCC1380/Comfyui_buckup_20241201_1952/resolve/master/ComfyUI.tar.safetensors' -o ComfyUI-aki-v1.3.1.tar"
    subprocess.run(download_cmd_A, shell=True, check=True)  # 下载 A 文件并等待完成

    # 文件 A 下载完成后立即解压
    unzip_cmd = "cd /root && tar -xvf ComfyUI-aki-v1.3.1.tar"
    subprocess.run(unzip_cmd, shell=True, check=True)

def download_file_B():
    time.sleep(3)
    # 等待 A 文件下载完成
    check_file_exists('/root/ComfyUI-aki-v1.3.1.tar.aria2')
    # 下载 B 文件
    download_cmd_B = "cd /root && aria2c -x 16 -s 16 -c -k 1M 'https://www.modelscope.cn/models/ACCC1380/Comfyui_buckup_20241201_1952/resolve/master/cfvenv2.tar.safetensors' -o cfvenv.tar.safetensors -d /root"
    subprocess.run(download_cmd_B, shell=True, check=True)


    # 解压 B 文件
    tar_cmd = "cd /root && tar -xvf cfvenv.tar.safetensors"
    subprocess.run(tar_cmd, shell=True, check=True)


def extract_and_setup():
    


    # 删除原 Python 文件并创建虚拟环境
    #venv_cmd = "cd /root && rm /root/cfvenv/bin/python* && python -m venv cfvenv"
    #subprocess.run(venv_cmd, shell=True, check=True)

    # 运行 ComfyUI 的 Python 脚本
    run_comfyui_cmd = "cd /root/comfyui/ComfyUI-aki-v1.3.1 && /root/cfvenv/bin/python3 main.py"
    subprocess.Popen(run_comfyui_cmd, shell=True)

def cleanup():
    # 删除临时文件
    cleanup_cmd = "rm /root/ComfyUI-aki-v1.3.1.tar && rm /root/cfvenv.tar.safetensors"
    subprocess.run(cleanup_cmd, shell=True, check=True)

# 启动下载任务 A 和 B
thread_A = threading.Thread(target=download_file_A)
thread_B = threading.Thread(target=download_file_B)

thread_A.start()  # 开始下载 A 文件
thread_B.start()  # 开始下载 B 文件

# 等待 A 和 B 下载完成
thread_A.join()
thread_B.join()

# 解压并设置环境
extract_and_setup()

# 清理临时文件
cleanup()
while True:
    time.sleep(8888888)