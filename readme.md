# 多语种语音替换Pipeline

## 一、配置说明

配置文件为`config.json`，各项配置说明如下。

```json
{
    "TranslatorKEY": "翻译器密钥",
    "TranslatorENDPOINT": "翻译器终结点",
    "TranslatorREGION": "翻译器地区",
    "SpeechKEY": "语音服务密钥",
    "SpeechREGION": "语音服务地区"
}
```

*本项目的主要功能均依托于Azure服务，项目运行前要先在Azure上创建翻译服务和语音服务。*

## 二、依赖项

本项目利用`ffmpeg`包提取音频，并使用`moviepy`和`pydub`来处理音视频，使用`audiotsm`实现WSOLA算法，从而使得音频变速不变调，使用`azure-cognitiveservices-speech`包（Azure语音SDK）来获取语音服务，使用`requests`、 `uuid`包发送`request`来获取翻译服务（Azure翻译器）。

```shell
pip install ffmpeg-python moviepy pydub
pip install azure-cognitiveservices-speech
pip install requests uuid
pip isntall audiotsm
```

## 三、代码说明

- `ASR.py`包含语音转文本类`STT`。
- `TRANS.py`包含翻译器类`Translator`。
- `TTS.py`包含文本转语音类`TTS`。
- `AudioPre.py`包含各种音视频处理函数，部分函数采用命令行方式使用`ffmpeg`。
- `main.py`提供了简单的使用样例。