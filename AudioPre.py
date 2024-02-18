# 音视频处理代码库，使用ffmpeg，moviepy和pydub实现
# 为实现音频变速不变调，使用audiotsm库，使用WSOLA算法
# 中间结果均使用numpy读取
import ffmpeg
from moviepy.editor import AudioFileClip, VideoFileClip
from pydub import AudioSegment
import numpy as np
import os
from subprocess import run
import audiotsm
import audiotsm.io.wav
import audiotsm.io.array

# 定义抽取音频函数
def AudioExtraction(inputFilename, outputFilename):
    stream = ffmpeg.input(inputFilename)
    audio = stream.audio
    ffmpeg.output(audio, outputFilename).run()

# 定义获取音频长度函数
def GetAudioLen(inputFilename):
    return len(AudioSegment.from_file(inputFilename))

# 定义音频变速函数，speed = 源音频长度 / 翻译后的音频长度
def ChangeAudioSpeed(inputFilename, outputFilename, speed):
    reader = audiotsm.io.wav.WavReader(inputFilename)
    writer =  audiotsm.io.wav.WavWriter(outputFilename, 1, 16000)
    wsola = audiotsm.wsola(1, speed=speed)
    wsola.run(reader, writer)

# 定义音频拼接以及加入静音音轨的函数，音频文件名需按自然数顺序命名
def AudioConcat(inputFolder, configFile, outputAudio):
    conf = np.load(configFile)
    audio = AudioSegment.empty() # 定义空音频流
    for i in range(len(os.listdir(inputFolder))):
        filename = str(i) + ".wav"
        timeSilence = int(conf[i][1][:-4]) - len(audio) # 得到静音时长
        audioSilence = AudioSegment.silent(duration=timeSilence) # 创建静音音频
        audio = audio.append(audioSilence, crossfade=0)

        # 加入翻译后的音频
        audioAppend = AudioSegment.from_file(inputFolder + filename)
        audio = audio.append(audioAppend, crossfade=0)
    
    audio.export(outputAudio, format="wav")

# 定义音频格式转换函数
def AudioFormatConvert(inputAudio, outputAudio, format):
    cmd_str = f"ffmpeg -i {inputAudio} -acodec {format} -strict experimental -ab 128k -ar 16k -ac 2 -y {outputAudio}"
    run(cmd_str, shell=True)

# 定义音视频合并函数
def UnionAV(inputAudio, inputVideo, outputVideo):
    cmd_str = f"ffmpeg -i {inputVideo} -i {inputAudio} -c copy -map 0:v:0 -map 1:a:0 {outputVideo}"
    run(cmd_str, shell=True)