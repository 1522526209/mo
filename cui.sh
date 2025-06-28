#!/bin/bash

# 检查目录是否存在
if [ -d "/root/ComfyUI" ]; then
    echo "检测到文件存在，跳过安装直接启动"
    /root/ComfyUI/venv/bin/python main.py --disable-cuda-malloc & python bash /root/test.sh
else
    echo "开始安装 CUI"
    apt update && apt install -y aria2
    bash /root/test.sh

    # 下载必要文件
    modelscope download --model 'ACCC1380/Fulx_dev_Model' save_to_modelscope.py --local_dir '/root'
    modelscope download --model 'ACCC1380/Fulx_dev_Model' lora-scripts_launch.sh --local_dir '/root'
    aria2c -x 16 -s 16 -m 5 "https://gh-proxy.com/github.com/1522526209/mo/blob/main/Download.sh" -o Download.sh -d /root

    # 安装 venv 和模型
    echo "安装 venv 和模型"
    cd /root && \
    modelscope download --model 'ACCC1380/ComfyUI.safetensors_20250127_0035' ComfyUI.safetensors --local_dir '/root' && \
    mv ComfyUI.safetensors venv.tar && \
    tar -xvf venv.tar && \
    rm venv.tar

    # 创建模型目录
    echo "创建模型目录"
    mkdir -p /etc/sgpu/pmem/lora
    mkdir -p /etc/sgpu/pmem/vae
    mkdir -p /etc/sgpu/pmem/clip

    # 下载模型
    cd /root/ComfyUI/models/checkpoints && modelscope download --model 'menyudada/MiaoMiaoPixel' MiaoMiaoPixel_V1.0.safetensors --local_dir '/root/ComfyUI/models/checkpoints'
    cd /root/ComfyUI/models/checkpoints && modelscope download --model 'QWQ114514123/WAI-illustrious-SDXL' waiIllustrious_v130.safetensors --local_dir '/root/ComfyUI/models/checkpoints'
    cd /root/ComfyUI/models/checkpoints && modelscope download --model 'QWQ114514123/WAI-illustrious-SDXL-v14' waiNSFWIllustrious_v140.safetensors --local_dir '/root/ComfyUI/models/checkpoints'
    cd /root/ComfyUI/models/checkpoints && modelscope download --model 'QWQ114514123/WAI-SHUFFLE-NOOB' waiSHUFFLENOOB.safetensors --local_dir '/root/ComfyUI/models/checkpoints'
    # 下载 Lora 模型
    echo "下载 Lora 模型"
    cd /etc/sgpu/pmem/lora && modelscope download --model 'govm114/warma_wai' warma_wai.safetensors --local_dir '/etc/sgpu/pmem/lora'
    bash /root/Download.sh

    # 创建符号链接
    ln -s /etc/sgpu/pmem/lora/* /root/ComfyUI/models/loras
    ln -s /etc/sgpu/pmem/vae/* /root/ComfyUI/models/vae
    ln -s /etc/sgpu/pmem/clip/Flux/* /root/ComfyUI/models/clip

    # 下载 VAE-approx 文件
    echo "下载 VAE-approx 文件"
    cd /root/ComfyUI/models/vae_approx && modelscope download --model 'ACCC1380/Noobxl' vaeapprox-sdxl.pt --local_dir '/root/ComfyUI/models/VAE-approx/'

    # 启动 SD WebUI
    echo "启动 SD WebUI"
    /root/ComfyUI/venv/bin/python main.py --disable-cuda-malloc & python bash /root/test.sh
fi