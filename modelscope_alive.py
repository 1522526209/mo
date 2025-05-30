import time
from datetime import datetime
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os

# os.system("bash /root/reset.sh")
# time.sleep(200)

class ModelScopeStudio:
    def __init__(self):
        # 初始化浏览器选项
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')  # 无界面模式
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')

        # Token缓存
        self.token = None

        # Token获取相关配置
        self.token_url = 'https://www.modelscope.cn/api/v1/studios/token'
        self.token_headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0',
            'Referer': 'https://www.modelscope.cn/studios/Akizuki/Large_Language_model/summary?header=default&fullWidth=false',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'X-Modelscope-Trace-Id': 'b305342d-c843-4337-ad15-a87377ccf1ec',
            'bx-v': '2.5.22',
            'sec-ch-ua': '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'x-modelscope-accept-language': 'zh_CN',
            'Cookie': 'cna=lLuvH970/3ABASQJiVoJjoAN; _ga=GA1.1.2144303129.1730727320; _gcl_au=1.1.88747731.1730727320; csrf_session=MTczMDcyNzMxOHxEdi1CQkFFQ180SUFBUkFCRUFBQU12LUNBQUVHYzNSeWFXNW5EQW9BQ0dOemNtWlRZV3gwQm5OMGNtbHVad3dTQUJCRWRIbDFRMnRqUkZOTWIwUjVWR1U0fNEFocJaKa22p0ICU4jlRtas84afzBAwuCXDK2nIKOkC; csrf_token=Cbrrdkl_rJjW-Ud7w-tU8ZciTrw%3D; t=7d9a55d751fb387a1db710aae3c32bb6; m_session_id=10cdd62e-c7ae-4686-891b-063654e18ce9; h_uid=2218303227545; xlly_s=1; acw_tc=0b62602617311525333143391eea9411e053b2f43a113522d274cc2c36e04c; _ga_K9CSTSKFC5=GS1.1.1731150509.11.1.1731152557.0.0.0; tfstk=f0bZmdXHDPUNuV4jlC8q8Kkn-LY95F27nZ9XisfD1dvi5VMcY96dlG6XCKWVMT-c5sTMnIf5E196CFYL3O1sfFs6SWLVgTI_BtEO0x553Os_W162gT6HIV_VMqRcitF9h5EC61Lvo8wWuz1O62nMkzeBoSfnG9rbVza561c6s713PN6UvJvJnExMmpYHpQJDohYDxWRDGAmmStVFtpdqnf0DsBYHNIgDoEXctWRxTz9DF2Ryj7BgV_3oJItwE6r-oq7nPhJlspu0EwRaeLfMLq0DCnouO65_Q4CBWZXyNOan7T5cwixFuv2yHw5hSifKQWYPTMsWbMyiup_6g3YDYj0cTeJdUNLurvRdx1scWOlqoCQ1PnJJYS0vcebWqgXZM7CHSIXv2Zw-WdfcwaIWzPkJ_Mfy8g7KHBxGFZIZnm-M9BJ7TWSlgxBLYB5jZmnvXMdeF5FtDmKM9BJ7TWoxDhLpTLNT6; isg=BMDAthbis6y8sk-vJ9hVzZUHkU6SSaQTxbMDRzpRjVtutWDf4lrZo62DzR11BVzr'
        }

        # 操作计数器
        self.operation_count = 0  # 新增：用于跟踪执行的operation次数

    def get_token(self):
        """获取token，如果已存在则返回缓存的token"""
        if self.token:
            return self.token  # 如果token已经获取过，直接返回

        try:
            response = requests.get(self.token_url, headers=self.token_headers)
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('Data', {}).get('Token')
                print("获取到的Token:", self.token)
                return self.token
            else:
                print(f"请求失败，状态码: {response.status_code}")
        except Exception as e:
            print(f"获取Token失败: {e}")
        return None

    def take_screenshot(self, url, screenshot_prefix="gradio_screenshot"):
        """截图功能"""
        driver = webdriver.Chrome(options=self.chrome_options)
        try:
            #url = "https://www.modelscope.cn/studios/Akizuki/Large_Language_model/summary?header=default&fullWidth=false"
            print(f"正在打开网页: {url}")
            driver.get(url)

            # 等待页面加载
            print("等待页面加载...")
            # wait = WebDriverWait(driver, 30)
            # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gradio-container")))

            time.sleep(6)  # 等待页面完全渲染

            # 生成带时间戳的文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"./shot/{screenshot_prefix}_{timestamp}.png"

            # 截图
            print("正在截图...")
            driver.save_screenshot(screenshot_path)
            print(f"截图已保存: {screenshot_path}")
        except Exception as e:
            print(f"发生错误: {e}")
            screenshot_path = f"./shot/error.png"
            print("正在截图...")
            driver.save_screenshot(screenshot_path)
            print(f"截图已保存: {screenshot_path}")
        finally:
            try:
                # 清除所有 Cookie
                driver.delete_all_cookies()
                # 清除浏览器缓存
                driver.execute_cdp_cmd('Network.clearBrowserCache', {})
                driver.execute_cdp_cmd('Network.clearBrowserCookies', {})
                print("已清除所有Cookie和浏览器缓存。")
            except Exception as e:
                print(f"清除Cookie和缓存时发生错误: {e}")
            driver.quit()

    def operation(self):
        """操作网页并点击按钮"""
        if not self.token:
            print("未获取Token，正在尝试获取...")
            self.get_token()
            if not self.token:
                print("未能获取到Token，退出操作。")
                return

        driver = webdriver.Chrome(options=self.chrome_options)

        # 确保 ./html 目录存在
        if not os.path.exists('./html'):
            os.makedirs('./html')

        try:
            # 构造包含token的url
            url = (
                f'https://s5k.cn/inner/studio/gradio?backend_url=/api/v1/studio/Akizuki/Large_Language_model/gradio/'
                f'&sdk_version=5.4.0&t=1730984958922&__theme=light&studio_token={self.token}'
            )

            # 打开url并进行操作
            print(f"正在打开带token的网页...:{url}")
            driver.get(url)

            # 等待按钮加载
            print("等待按钮加载...")
            wait = WebDriverWait(driver, 30)
            wait.until(EC.presence_of_element_located((By.ID, "component-12")))

            time.sleep(2)  # 确保元素可交互

            # 点击按钮
            print("正在点击按钮...")
            driver.execute_script("document.getElementById('component-12').click();")
            print("已点击")

            time.sleep(5)

            # 截图
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"./click/click_screenshot_{timestamp}.png"
            print("正在截图...")
            driver.save_screenshot(screenshot_path)
            print(f"截图已保存: {screenshot_path}")

            # 获取网页HTML
            html_content = driver.page_source

            # 检查是否有“Connection errored out.”字串
            if "Connection errored out." in html_content:
                print("连接错误：网页内容中发现 'Connection errored out.'，正在重启操作...")
                # 截图
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = f"./Failed_{timestamp}.png"
                print("正在截图...")
                driver.save_screenshot(screenshot_path)
                print(f"截图已保存: {screenshot_path}")
                os.system("echo 执行重启reset.sh && bash /root/reset.sh")

                # 等待150秒后重新执行操作
                time.sleep(150)
                self.operation()  # 重新调用operation函数

            # 保存网页HTML到文件
            html_filename = f"./html/page_source_{timestamp}.html"
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"网页HTML已保存: {html_filename}")

        except Exception as e:
            print(f"发生错误: {e}")
            os.system("echo 执行重启reset.sh && bash /root/reset.sh")
            driver.get("https://www.modelscope.cn/studios/Akizuki/Large_Language_model")
            time.sleep(30)

        finally:
            try:
                # 清除所有 Cookie
                driver.delete_all_cookies()
                # 清除浏览器缓存
                driver.execute_cdp_cmd('Network.clearBrowserCache', {})
                driver.execute_cdp_cmd('Network.clearBrowserCookies', {})
                print("已清除所有Cookie和浏览器缓存。")
            except Exception as e:
                print(f"清除Cookie和缓存时发生错误: {e}")
            driver.quit()

        # 更新操作计数器
        self.operation_count += 1
        print(f"当前已执行operation次数: {self.operation_count}")

    def run(self, screenshot_interval=30, operation_interval=30):
        """主运行方法"""
        # 首先获取Token
        print("正在获取Token...")
        if not self.get_token():
            print("未能获取到Token，程序将退出。")
            return
        else:
            print(f"成功获取Token: {self.token}")

        screenshot_count = 0
        gradio_url = "https://s5k.cn/inner/studio/gradio?backend_url=/api/v1/studio/Akizuki/Large_Language_model/gradio/"

        # 初始执行一次operation
        self.operation()

        while True:
            self.take_screenshot(url=gradio_url)
            screenshot_count += 1

            # 每执行operation_interval次take_screenshot后执行一次operation
            if screenshot_count >= operation_interval:
                self.operation()
                screenshot_count = 0  # 重置计数器

                # 检查是否需要重新获取Token
                if self.operation_count >= 100:
                    print("已执行100次operation，正在重新获取Token...")
                    self.token = None  # 清除现有Token
                    if self.get_token():
                        print("Token重新获取成功。")
                        self.operation_count = 0  # 重置操作计数器
                    else:
                        print("重新获取Token失败，程序将退出。")
                        break  # 退出循环或根据需要采取其他措施

            time.sleep(screenshot_interval)  # 等待指定秒数

if __name__ == "__main__":
    studio = ModelScopeStudio()
    studio.run()
