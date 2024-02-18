import requests, uuid

# 文本翻译类
class Translator:
    # 初始化文本翻译服务
    def __init__(self, TranslatorKEY, # Azure API的密钥
                TranslatorENDPOINT, # Azure API的终结点
                TranslatorREGION, # Azure API的地区信息
                language # 指定语言
                ):
        # 定义发送request报文所需的各种字段
        self.constructed_url = TranslatorENDPOINT + "/translate"
        self.headers = {
            "Ocp-Apim-Subscription-Key": TranslatorKEY,
            "Ocp-Apim-Subscription-Region": TranslatorREGION,
            "Content-type": "application/json",
            "X-ClientTraceId": str(uuid.uuid4())
        }
        self.params = {
            "api-version": "3.0",
            "from": language["from"],
            "to": language["to"]
        }

    # 使用Azure API获取文本翻译，输入为源语言字符串
    def translate(self, ori):
        # 从文件读入文本并放入报文的body中
        body = [{
            "text": ori
        }]
        
        # 以post方式发送request报文并返回响应即翻译文本
        request = requests.post(self.constructed_url, params=self.params, headers=self.headers, json=body)
        response = request.json()
        return response[0]["translations"]
