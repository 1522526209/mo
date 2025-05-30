import os

def replace_links_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    # 替换链接
    content = content.replace('https://ghfast.top/', '')
    content = content.replace('https://github.com/', 'https://ghfast.top/https://github.com/')
    content = content.replace('https://raw.githubusercontent.com/', 'https://ghfast.top/https://raw.githubusercontent.com/')
    content = content.replace('https://gist.github.com/', 'https://ghfast.top/https://gist.github.com/')
    content = content.replace('https://gist.githubusercontent.com/', 'https://ghfast.top/https://gist.githubusercontent.com/')
    content = content.replace('https://huggingface.co', 'https://hf-mirror.com')
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def find_and_replace_links(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                replace_links_in_file(file_path)
                print(f"Processed file: {file_path}")

# 指定要查找的目录路径
directory_path = './stable-diffusion-webui'
find_and_replace_links(directory_path)