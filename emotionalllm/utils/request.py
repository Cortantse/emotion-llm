import sys
import time
import os
import requests
import json
from typing import List, Tuple, Dict
from emotionalllm.modules import exception
from emotionalllm.modules import config

class Request:
    def __init__(self, url, model, api_key, temperature=config.temperature, top_p=config.top_p):
        self.url = url
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.top_p = top_p
        
    def to_str(self):
        return f"Request(url={self.url}, model={self.model}, temperature={self.temperature}, top_p={self.top_p})"
    
    


def send_message(messages: List, request: Request, timeout=config.timeout, need_retry=True) -> Tuple[str, int, int]:
    """
    发送消息给模型
    
    Args:
        messages: 消息列表
        request: 请求对象和配置
        timeout: 超时时间
        need_retry: 是否需要重试，一般需要，防止断网
    """
    # 发送请求
    if need_retry:
        response, total_token, generation_token = _send_request_with_retry(messages, request, timeout)
    else:
        response, total_token, generation_token = _send_request(messages, request, timeout)
        
    return response, total_token, generation_token



def _send_request(messages: List, request: Request, timeout=config.timeout) -> Tuple[str, int, int]:
    # 默认值
    model, api_key, url = request.model, request.api_key, request.url

    '''
    发送messages给model
    :param messages: 消息队列
    :param model: 选择的模型，有默认值
    :param api_key，有默认值
    :param url:，有默认值
    :return: 模型的输出，总体token，生成token
    模型输出格式
    {"id":"aea940d6-6a02-4b8b-b2f2-16b362651f8c","object":"chat.completion","created":1733216568,"model":"deepseek-chat",
    "choices":[{"index":0,"message":{"role":"assistant",
    "content":"你好！"},"logprobs":null,"finish_reason":"stop"}],
    "usage":{"prompt_tokens":18,"completion_tokens":67,"total_tokens":85,"prompt_cache_hit_tokens":0,"prompt_cache_miss_tokens":18},
    "system_fingerprint":"fp_1c141eb703"}
    '''

    if config.debug_request:
        print(f"发送请求: {messages}")
        # 断点
        breakpoint()  

    payload = json.dumps({
        "messages": messages,
        "model": model,
        "frequency_penalty": 0,
        "presence_penalty": 0,
        "response_format": {
            "type": "text"
        },
        "stop": None,
        "stream": False,
        "stream_options": None,
        "temperature": request.temperature,
        "top_p": request.top_p,
        "tools": None,
        "tool_choice": "none",
        "logprobs": False,
        "top_logprobs": None
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    try:
        # 发送请求并设置超时时间
        response = requests.post(url, headers=headers, data=payload, timeout=timeout)
        response.raise_for_status()  # 检查 HTTP 错误

        # 解析 JSON 响应
        response_json = json.loads(response.text)

        # 获取令牌使用量
        total_token = response_json['usage']['total_tokens']
        generation_token = response_json['usage']['completion_tokens']

        if config.debug_request:
            print(f"响应: {response_json['choices'][0]['message']['content']}")
            # 断点
            breakpoint()  

        return response_json['choices'][0]['message']['content'], total_token, generation_token
    except requests.exceptions.Timeout:
        raise requests.exceptions.Timeout("请求超时，请检查网络连接或增加超时时间。")
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError("网络连接错误，请检查网络状态。")
    except requests.exceptions.RequestException as e:
        raise Exception(f"请求失败: {e}")


def _send_request_with_retry(messages, request: Request, max_retries=config.max_retries,
                             base_delay=config.base_delay, timeout=config.timeout):
    """
    使用指数级延迟重试发送请求。
    :param messages: 要发送的消息
    :param max_retries: 最大重试次数
    :param base_delay: 基础延迟（秒）
    :param timeout: 每次请求的超时时间（秒）
    :return: 模型的响应内容，总体 token，生成 token
    """
    retries = 0  # 当前实际执行的次数
    attempt = 1  # 当前重试次数，按指数增长
    delay = base_delay  # 初始延迟时间

    while attempt <= max_retries:
        try:
            # 调用 _send_request
            response, total_token, generation_token = _send_request(messages, request, timeout=timeout)
            return response, total_token, generation_token  # 请求成功返回结果
        except requests.exceptions.ConnectionError as e:
            retries += 1
            exception.print_warning(
                _send_request_with_retry,
                f"网络连接错误: {e}. 正在重试 {attempt}/{max_retries}，延迟 {delay} 秒后重试。",
                "中风险"
            )

            if attempt >= max_retries:
                exception.print_error(_send_request_with_retry, "重试次数过多，网络请求失败！")

            time.sleep(delay)
            delay = min(delay * 2, timeout * 16)  # 限制最大延迟时间
            attempt *= 2  # 重试次数按指数增长
        except Exception as e:
            retries += 1
            exception.print_warning(
                _send_request_with_retry,
                f"未知错误: {e}. 正在重试 {attempt}/{max_retries}，延迟 {delay} 秒后重试。",
                "高风险"
            )

            if attempt >= max_retries:
                exception.print_error(_send_request_with_retry, "重试次数过多，网络请求失败！")

            time.sleep(delay)
            delay = min(delay * 2, timeout * 16)  # 限制最大延迟时间
            attempt *= 2  # 重试次数按指数增长

    exception.print_error(_send_request_with_retry, "重试次数过多，网络请求失败！")
