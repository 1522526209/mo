#!/bin/bash

# 定义模型映射表
declare -A model_mapping=(
    ["govm114/diao:20.safetensors"]="diao.safetensors:/etc/sgpu/pmem/lora"
    ["QWQ114514123/diao_r34:20.safetensors"]="diao_flux.safetensors:/etc/sgpu/pmem/lora"
    ["QWQ114514123/shenchaoweiba:20.safetensors"]="shenchaoweiba.safetensors:/etc/sgpu/pmem/lora"
    ["govm114/warma:30.safetensors"]="warma.safetensors:/etc/sgpu/pmem/lora"
    ["QWQ114514123/abmayo_flux:50.safetensors"]="abmayo_flux.safetensors:/etc/sgpu/pmem/lora"
    ["QWQ114514123/diao-wai:diao-wai.safetensors"]="diao-wai.safetensors:/etc/sgpu/pmem/lora"
    ["QWQ114514123/shenchaoweiba-w:shenchaoweiba-w.safetensors"]="shenchaoweiba-w.safetensors:/etc/sgpu/pmem/lora"
    ["QWQ114514123/shenchaoweiba-w2:shenchaoweiba-w2.safetensors"]="shenchaoweiba-w2.safetensors:/etc/sgpu/pmem/lora"
    ["QWQ114514123/cookie-wa:cookie-wa.safetensors"]="cookie-wa.safetensors:/etc/sgpu/pmem/lora"
    ["QWQ114514123/beni-wai:beni-wai.safetensors"]="beni-wai.safetensors:/etc/sgpu/pmem/lora"
)

# 日志文件路径
log_file="download_and_rename.log"

# 清空日志文件
> "$log_file"

# 遍历模型映射表
for key in "${!model_mapping[@]}"; do
    # 分离用户仓库和原始文件名
    user_repo="${key%:*}"       # 用户仓库（如 govm114/diao）
    original_file="${key#*:}"  # 原始文件名（如 30.safetensors）
    
    # 分离目标文件名和保存路径
    target_info="${model_mapping[$key]}"
    target_file="${target_info%:*}"  # 目标文件名（如 diao.safetensors）
    save_path="${target_info#*:}"   # 保存路径（如 /etc/sgpu/pmem/lora）
    
    # 创建保存路径（如果不存在）
    mkdir -p "$save_path"
    
    # 检查目标文件是否已存在
    if [ -f "$save_path/$target_file" ]; then
        echo "文件已存在，跳过下载: $save_path/$target_file"
        echo "$(date): 文件已存在，跳过下载: $save_path/$target_file" >> "$log_file"
        continue
    fi
    
    # 下载模型
    echo "正在下载模型: $user_repo ($original_file)"
    modelscope download --model "$user_repo" "$original_file" --local_dir "$save_path"
    
    # 检查下载是否成功
    if [ $? -eq 0 ]; then
        # 获取下载的文件路径
        downloaded_path="$save_path/$original_file"
        
        # 检查文件是否存在
        if [ -f "$downloaded_path" ]; then
            # 检查目标文件是否冲突
            if [ -f "$save_path/$target_file" ]; then
                echo "目标文件已存在，跳过重命名: $save_path/$target_file"
                echo "$(date): 目标文件已存在，跳过重命名: $save_path/$target_file" >> "$log_file"
            else
                # 重命名文件
                mv "$downloaded_path" "$save_path/$target_file"
                echo "重命名成功: $original_file -> $target_file"
                echo "$(date): 重命名成功: $original_file -> $target_file" >> "$log_file"
            fi
        else
            echo "文件未找到: $downloaded_path"
            echo "$(date): 文件未找到: $downloaded_path" >> "$log_file"
        fi
    else
        echo "下载失败: $user_repo ($original_file)"
        echo "$(date): 下载失败: $user_repo ($original_file)" >> "$log_file"
    fi
done