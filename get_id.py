import requests
import json

def save_config(hco):
    # 将配置写入 JSON 文件
    with open('hco.json', 'w') as json_file:
        json.dump(hco, json_file, indent=4)

def load_config():
    # 从 JSON 文件加载配置
    with open('hco.json', 'r') as json_file:
        hco = json.load(json_file)
    return hco 



url = "http://127.0.0.1:8082/MyWcfService/getstring"
params = {
    "duankou": "COM9",
    "hco": 0,
    "daima": 0
}

response = requests.get(url, params=params)
print(response.text)
save_config(response.text)
print(load_config())