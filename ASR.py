import azure.cognitiveservices.speech as speechsdk
import time

# 语音转文本类
class STT:
    # 初始化语音转文本服务
    def __init__(self, SpeechKEY, # Azure API的密钥
                SpeechREGION, # Azure API的地区信息
                language # 指定语言
                ):
        self.SpeechKEY = SpeechKEY
        self.SpeechREGION = SpeechREGION
        self.speech_config = speechsdk.SpeechConfig(subscription=self.SpeechKEY, region=self.SpeechREGION)
        self.speech_config.speech_recognition_language=language

    # 使用Azure API获取语音转文本服务，从音频文件读入，返回识别的内容以及所在位置
    def Speech2Text(self, filename):
        # 配置语音识别器
        audio_config = speechsdk.AudioConfig(filename=filename)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)

        # 返回结果
        res = []
        
        # 终止标识符
        done = False

        # 定义终止函数
        def stop_cb(evt):
            print('CLOSING on {}'.format(evt))
            speech_recognizer.stop_continuous_recognition()
            nonlocal done
            done = True
        
        # 定义回调函数
        def recognized_handler(e : speechsdk.SpeechRecognitionEventArgs):
            if len(e.result.text) > 0 :
                return [e.result.text, e.result.offset, e.result.duration]

        # 建立语音识别流
        speech_recognizer.recognized.connect(lambda evt: (res.append(recognized_handler(evt))))
        speech_recognizer.session_started.connect(lambda evt: print('STT SESSION STARTED: {}'.format(evt)))
        speech_recognizer.session_stopped.connect(lambda evt: print('STT SESSION STOPPED {}'.format(evt)))
        speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)

        # 连续识别
        speech_recognizer.start_continuous_recognition()
        while not done:
            time.sleep(.5)

        # 识别内容格式为：[[识别文本, 识别内容偏移量, 识别内容持续时间], ...]
        return res
    