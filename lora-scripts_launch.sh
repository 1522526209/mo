#!/bin/bash

# 检查 /root/lora-scripts 目录是否存在
if [ -d "/root/xmz/lora-scripts" ]; then
    echo "/root/xmz/lora-scripts 目录已存在，跳过安装，直接启动..."
else
    # 目录不存在，开始下载和安装
    echo "开始下载和安装..."
    cd /root/xmz/ && aria2c -x 16 -s 16 -c -k 1M "https://www.modelscope.cn/models/ACCC1380/lora-scripts/resolve/master/lora-scritps.tar.safetensors"
    cd /root/xmz/ && tar -xvf lora-scritps.tar.safetensors
    /root/xmz/lora-scripts/loravenv/bin/python -m pip install onnxruntime-gpu --extra-index-url https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/onnxruntime-cuda-12/pypi/simple/
    aria2c "https://www.modelscope.cn/models/ACCC1380/Fulx_dev_Model/resolve/master/Flux/ul.py" -d /root/xmz/lora-scripts
    cd /root/xmz/ && aria2c -x 16 -s 16 -c -k 1M "https://www.modelscope.cn/models/ACCC1380/Fulx_dev_Model/resolve/master/ul.py" -d /root/xmz/lora-scripts/
    cd /root/xmz & aria2c -x 16 -s 16 "https://modelscope.cn/models/MusePublic/NoobAI-XL/resolve/1.0/noobaiXLNAIXL_epsilonPred10Version.safetensors" -o NoobAI-XL-epsilon1.0.safetensors -d /root/xmz/lora-scripts/sd-models
    
fi

# 启动程序
cd /root/xmz/lora-scripts && HF_ENDPOINT=https://hf-mirror.com /root/xmz/lora-scripts/loravenv/bin/python gui.py --skip-prepare-onnxruntime & python /root/ssh28000.py & python /root/xmz/lora-scripts/ul.py
