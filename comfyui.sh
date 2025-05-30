cd /root && aria2c -x 16 -s 16 "https://www.modelscope.cn/models/ACCC1380/ComfyUI.safetensors_20250127_0035/resolve/master/ComfyUI.safetensors" -o cf.safetensors
cd /root && tar -xvf cf.safetensors
cd /root/ComfyUI/models/loras & aria2c -x 16 -s 16 "https://www.modelscope.cn/models/govm114/diao/resolve/ckpt-20/20.safetensors" -o diao-flux.safetensors -d /root/ComfyUI/models/loras
cd /root/ComfyUI/models/unet & aria2c -x 16 -s 16 "https://www.modelscope.cn/models/MusePublic/489_ckpt_FLUX_1/resolve/2172/2172.safetensors" -o flux.safetensors -d /root/ComfyUI/models/unet
cd /root/ComfyUI/models/unet & aria2c -x 16 -s 16 "https://www.modelscope.cn/models/AI-ModelScope/FLUX.1-dev/resolve/master/ae.safetensors" -o ae.safetensors -d /root/ComfyUI/models/vae
cd /root/ComfyUI/models/unet & aria2c -x 16 -s 16 "https://www.modelscope.cn/models/ACCC1380/Fulx_dev_Model/resolve/master/Flux/t5xxl_fp16.safetensors" -o t5xxl_fp16.safetensors -d /root/ComfyUI/models/clip
cd /root/ComfyUI/models/unet & aria2c -x 16 -s 16 "https://www.modelscope.cn/models/ACCC1380/Fulx_dev_Model/resolve/master/Flux/clip_l.safetensors" -o clip_l.safetensors -d /root/ComfyUI/models/clip
cd /root/ComfyUI
/root/ComfyUI/venv/bin/python main.py --disable-cuda-malloc & python /root/ComfyUI/ssh8188.py