import json
import requests
def load_config():
    # 从 JSON 文件加载配置
    with open('hco.json', 'r') as json_file:
        hco = json.load(json_file)
    return hco 

print(load_config())

response = requests.get("http://127.0.0.1:8082/MyWcfService/getstring?duankou=0&hco=1996&daima=X-10Y10Z0")