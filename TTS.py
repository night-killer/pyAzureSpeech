import azure.cognitiveservices.speech as speechsdk

# 文本转语音类
class TTS:
    # 初始化语音转文本服务
    def __init__(self, SpeechKEY, # Azure API的密钥
                SpeechREGION # Azure API的地区信息
                ):
        self.SpeechKEY = SpeechKEY
        self.SpeechREGION = SpeechREGION
        self.speech_config = speechsdk.SpeechConfig(subscription=self.SpeechKEY, region=self.SpeechREGION)

    # 使用Azure API获取文本转语音服务，并根据指定音色生成对应语音，并将对应语音流保存为wav文件
    def Text2Speech(self, input, outputFilename, voice):
        # 获取文本内容
        text = input

        # 配置音色
        self.speech_config.speech_synthesis_language = voice["lan"]
        self.speech_config.speech_synthesis_voice_name = voice["name"]

        # 创建语音合成器
        audio_config = speechsdk.audio.AudioOutputConfig(filename=outputFilename)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=audio_config)
        
        # 获取生成语音流
        result = synthesizer.speak_text_async(text).get()
        stream = speechsdk.AudioDataStream(result)
        
        stream.save_to_wav_file(outputFilename)
