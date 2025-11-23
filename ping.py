import shlex
import tkinter as tk
import tkinter.messagebox as messagebox
import time
import os
import json
import requests
import sys
import subprocess
import ctypes
import win32com.client
import threading
import logging
import random
import urllib.parse

# def check_server_connectivity(server_url):
#     try:
#         response = requests.get(server_url, timeout=5)  # 设置超时为5秒
#         if response.status_code == 200:
#             print(f"{server_url}连通性正常。")
#             return True
#         else:
#             print(f"{server_url}返回错误，状态码: {response.status_code}")
#     except requests.ConnectionError:
#         print(f"无法连接到{server_url}，网络可能出现问题。")
#         return False
#     except requests.Timeout:
#         print("请求超时，请检查服务器状态。")
#         return False
#     except Exception as e:
#         print(f"发生未知错误: {e}")
#         return False

# def get_url(username, password):
#     if check_server_connectivity("http://172.17.100.200:801"):
#         print("走旧流程。")
#         timestamp = int(time.time() * 1000)
#         base_url = "http://172.17.100.200:801/eportal/"
#         params = {
#             "c": "GetMsg",
#             "a": "loadToken",
#             "callback": f"jQuery_{timestamp}",
#             "account": username,
#             "password": password,
#             "mac": "000000000000",
#             "_": timestamp
#         }
#         url = f"{base_url}?{'&'.join(f'{key}={value}' for key, value in params.items())}"
#         return url
#     elif check_server_connectivity("http://10.255.200.254:803"):
#         print("走新流程。")
        
#         return url
    
    
class JsonpClient:
    def __init__(self, enable_alias=0, page_data_encrypt=1, encryption_type=1, secret_key='drcom'):
        self.enable_alias = enable_alias
        self.page_data_encrypt = page_data_encrypt
        self.encryption_type = encryption_type
        self.secret_key = secret_key
        self.lang = 'zh'  # 默认语言设置为中文

    def get_random(self):
        return random.randint(500, 10500)

    def encrypt_data(self, data):
        # 模拟数据加密
        if self.encryption_type == 1:
            keys = self.get_key(self.secret_key)
        else:
            keys = self.get_key('终端实际IP')  # 可根据实际IP来获取密钥

        encrypted_data = {}
        for key, value in data.items():
            if key == "error_code":
                encrypted_data[key] = value
            else:
                encrypted_data[key] = self.enc_pwd(value, keys)
        return encrypted_data

    def get_key(self, key):
        # 这里应该用实际的加密逻辑
        return key  # 简化处理

    def enc_pwd(self, value, keys):
        # 这里应该用实际的加密逻辑，这里仅仅是返回原值
        return value  # 简化处理

    def format_params(self, data):
        arr = []
        for name, value in data.items():
            if name == 'callback':
                arr.insert(0, f"{urllib.parse.quote(name)}={urllib.parse.quote(value)}")
            else:
                # 中文别名认证的处理
                if self.enable_alias == 1 and (name == 'DDDDD' or name == 'user_account') and any(u'\u4e00' <= char <= u'\u9fa5' for char in value):
                    arr.append(f"{name}={value}")
                else:
                    arr.append(f"{urllib.parse.quote(name)}={urllib.parse.quote(value)}")
        
        arr.append(f'v={self.get_random()}')  # 添加随机数防止缓存
        arr.append(f'lang={self.lang}')  # 添加语言标识
        return '&'.join(arr)

    def jsonp_request(self, url, params):
        params['callback'] = 'dr' + str(int(time.time() * 1000))  # 使用时间戳作为callback
        params['jsVersion'] = '4.X'  # 默认JS版本
        
        if self.page_data_encrypt == 1 and 'drcom/chkstatus' not in url and 'drcom/login' not in url:
            encrypted_data = self.encrypt_data(params)
            data = self.format_params(encrypted_data)
        else:
            data = self.format_params(params)

        # 这里模拟发送请求
        print(f"Sending JSONP request to: {url}?{data}")
        
        # 此处实现真正的网络请求时，需考虑超时与错误处理等

# 示例使用
client = JsonpClient()
params = {
    'DDDDD': '202303',
    'user_account': 'user123',
    'error_code': '0'
}
print(client.jsonp_request('http://example.com/api', params))






