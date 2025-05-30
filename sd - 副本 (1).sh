#!/bin/bash

# 检查目录是否存在
if [ -d "/home/epors/stable-diffusion-webui-forge" ]; then
    echo "检测到文件存在，跳过安装直接启动"
    bash /root/test.sh
    (
        su - epors -c "cd /home/epors/stable-diffusion-webui-forge && HF_ENDPOINT=https://hf-mirror.com /home/epors/stable-diffusion-webui-forge/venv/bin/python launch.py --api --port=7865 --xformers --lora-dir=/etc/sgpu/pmem/lora --vae-dir=/etc/sgpu/pmem/vae --clip-models-path=/etc/sgpu/pmem/clip/Flux/"
    ) &
    python /root/ssh7865.py &
    bash /root/test.sh
else
    echo "开始安装 SD WebUI"
    apt update && apt install -y aria2
    bash /root/test.sh
    sudo groupadd sdgroup
    sudo useradd -m -G sdgroup epors
    sudo usermod -aG sudo epors

    # 下载必要文件
    aria2c -x 16 -s 16 -m 5 "https://gh-proxy.com/github.com/1522526209/mo/blob/main/ssh7865.py" -o ssh7865.py -d /root
    modelscope download --model 'ACCC1380/Fulx_dev_Model' save_to_modelscope.py --local_dir '/root'
    modelscope download --model 'ACCC1380/Fulx_dev_Model' lora-scripts_launch.sh --local_dir '/root'
    aria2c -x 16 -s 16 -m 5 "https://gh-proxy.com/github.com/1522526209/mo/blob/main/ssh28000.py" -o ssh28000.py -d /root
    aria2c -x 16 -s 16 -m 5 "https://gh-proxy.com/github.com/1522526209/mo/blob/main/Download.sh" -o Download.sh -d /root

    # 安装 venv 和模型
    echo "安装 venv 和模型"
    cd /home/epors && \
    modelscope download --model 'govm114/wowtest' sd-forge.tar.safetensors --local_dir '/home/epors/' && \
    mv sd-forge.tar.safetensors venv.tar && \
    tar -xvf venv.tar && \
    rm venv.tar

    # 创建模型目录
    echo "创建模型目录"
    mkdir -p /etc/sgpu/pmem/lora
    mkdir -p /etc/sgpu/pmem/vae
    mkdir -p /etc/sgpu/pmem/clip

    # 下载模型
    cd /home/epors/stable-diffusion-webui-forge/models/Stable-diffusion && modelscope download --model 'MusePublic/489_ckpt_FLUX_1' 2172.safetensors --local_dir '/home/epors/stable-diffusion-webui-forge/models/Stable-diffusion'
    cd /home/epors/stable-diffusion-webui-forge/models/Stable-diffusion && modelscope download --model 'menyudada/MiaoMiaoPixel' MiaoMiaoPixel_V1.0.safetensors --local_dir '/home/epors/stable-diffusion-webui-forge/models/Stable-diffusion'
    cd /home/epors/stable-diffusion-webui-forge/models/Stable-diffusion && modelscope download --model 'QWQ114514123/WAI-illustrious-SDXL' waiIllustrious_v130.safetensors --local_dir '/home/epors/stable-diffusion-webui-forge/models/Stable-diffusion'
    cd /home/epors/stable-diffusion-webui-forge/models/Stable-diffusion && modelscope download --model 'MusePublic/14_ckpt_SD_XL' 48.safetensors --local_dir '/home/epors/stable-diffusion-webui-forge/models/Stable-diffusion'
    cd /etc/sgpu/pmem/vae && modelscope download --model 'AI-ModelScope/FLUX.1-dev' ae.safetensors --local_dir '/etc/sgpu/pmem/vae'
    cd /etc/sgpu/pmem/clip && modelscope download --model 'ACCC1380/Fulx_dev_Model' Flux/t5xxl_fp16.safetensors --local_dir '/etc/sgpu/pmem/clip'
    cd /etc/sgpu/pmem/clip && modelscope download --model 'ACCC1380/Fulx_dev_Model' Flux/clip_l.safetensors --local_dir '/etc/sgpu/pmem/clip'

    # 下载 Lora 模型
    echo "下载 Lora 模型"
    cd /etc/sgpu/pmem/lora && modelscope download --model 'govm114/warma_wai' warma_wai.safetensors --local_dir '/etc/sgpu/pmem/lora'
    bash /root/Download.sh

    # 创建符号链接
    ln -s /etc/sgpu/pmem/lora/* /home/epors/stable-diffusion-webui-forge/models/Lora
    ln -s /etc/sgpu/pmem/vae/* /home/epors/stable-diffusion-webui-forge/models/VAE
    ln -s /etc/sgpu/pmem/clip/Flux/* /home/epors/stable-diffusion-webui-forge/models/text_encoder

    # 下载 VAE-approx 文件
    echo "下载 VAE-approx 文件"
    cd /home/epors/stable-diffusion-webui-forge/models/VAE-approx/ && modelscope download --model 'ACCC1380/Noobxl' vaeapprox-sdxl.pt --local_dir '/home/epors/stable-diffusion-webui-forge/models/VAE-approx/'

    # 启动 SD WebUI
    echo "启动 SD WebUI"
    (
        su - epors -c "cd /home/epors/stable-diffusion-webui-forge && HF_ENDPOINT=https://hf-mirror.com /home/epors/stable-diffusion-webui-forge/venv/bin/python launch.py --api --port=7865 --xformers --lora-dir=/etc/sgpu/pmem/lora --vae-dir=/etc/sgpu/pmem/vae --clip-models-path=/etc/sgpu/pmem/clip/Flux/"
    ) &
    python /root/ssh7865.py &
    bash /root/test.sh
fi