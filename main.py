import os
from AudioPre import *
from ASR import STT
from TRANS import Translator
from TTS import TTS
import json
import numpy as np


if __name__=="__main__":
    with open("config.json") as f:
        conf = json.load(f) # 加载配置

    AudioExtraction("video/sample1.mp4", "audio/sample1.wav") # 音频抽取

    # 语音转文字
    speech2Text = STT(conf["SpeechKEY"], conf["SpeechREGION"], "en-US")
    res = speech2Text.Speech2Text("audio/sample1.wav")
    res = np.array(res)
    np.save("text/sample1.npy", res)

    # 翻译
    language = {"from": "en-US",
                "to": ["es", "ru", "ja", "de"]
    } # 语言选项

    # 初始化存储翻译结果的字典
    res_trans = {}
    for lan in language["to"]:
        res_trans[lan] = []

    # 初始化翻译器
    translator = Translator(conf["TranslatorKEY"], conf["TranslatorENDPOINT"], conf["TranslatorREGION"], language)
    
    print(f"TRANS SESSION STARTED")
    # 执行翻译
    for word in res:
        translations = translator.translate(word[0])
        for translation in translations:
            res_trans[translation["to"]].append([translation["text"], word[1], word[2]])
    print(f"TRANS SESSION STOPED")

    for (key, value) in res_trans.items():
        value = np.array(value)
        np.save(f"text/sample1_{key}.npy", value)

    # 文字转语音
    # 初始化文字转语音服务
    text2Speech = TTS(conf["SpeechKEY"], conf["SpeechREGION"])

    voices = [
        {"lan": "es", "name": "es-ES-DarioNeural"},
        {"lan": "ru", "name": "ru-RU-DmitryNeural"},
        {"lan": "ja", "name": "ja-JP-KeitaNeural"},
        {"lan": "de", "name": "de-DE-BerndNeural"}
    ] # 音色选项

    print(f"TTS SESSION STARTED")
    # 执行文字转语音
    for voice in voices:
        if not os.path.exists(f"audio/{voice['lan']}"):
            os.mkdir(f"audio/{voice['lan']}")
        for i in range(len(res_trans[voice["lan"]])):
            text = res_trans[voice["lan"]][i][0]
            text2Speech.Text2Speech(text, f"audio/{voice['lan']}/{i}.wav", voice)
    print(f"TTS SESSION STOPED")

    # 执行音频变速
    root = "./audio/"
    preRoot = "./audio_pre/"
    lanFolders = ["es/", "ru/", "ja/", "de/"]
    config = np.load("text/sample1.npy")
    for lan in lanFolders:
        folder = root + lan
        preFolder = preRoot + lan
        if not os.path.exists(preFolder):
            os.mkdir(preFolder)
        for i in range(len(os.listdir(folder))):
            audio = str(i) + ".wav"
            input = folder + audio
            output = preFolder + audio
            speed = GetAudioLen(input) / int(config[i][2][:-4])
            print(f"{lan}{i}: {speed}")
            ChangeAudioSpeed(input, output, speed)
    
    # 执行音频拼接
    for lan in lanFolders:
        inputFolder = preRoot + lan
        configFile = "text/sample1.npy"
        outputAudio = preRoot + f"final_{lan[:2]}.wav"
        AudioConcat(inputFolder, configFile, outputAudio)

    # 执行音频格式转换
    AudioFormatConvert("audio_pre/final_de.wav", "audio_pre/final_de.aac", "aac")
    AudioFormatConvert("audio_pre/final_es.wav", "audio_pre/final_es.aac", "aac")
    AudioFormatConvert("audio_pre/final_ja.wav", "audio_pre/final_ja.aac", "aac")
    AudioFormatConvert("audio_pre/final_ru.wav", "audio_pre/final_ru.aac", "aac")

    # 执行音视频合并
    UnionAV("audio_pre/final_de.aac", "video/sample1.mp4", "video_pre/final_de.mp4")
    UnionAV("audio_pre/final_es.aac", "video/sample1.mp4", "video_pre/final_es.mp4")
    UnionAV("audio_pre/final_ja.aac", "video/sample1.mp4", "video_pre/final_ja.mp4")
    UnionAV("audio_pre/final_ru.aac", "video/sample1.mp4", "video_pre/final_ru.mp4")
