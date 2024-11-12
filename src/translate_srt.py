import os
import shutil
import datetime
import deepl
import torch
from moviepy.editor import VideoFileClip
import whisper
import deeplx_api

#api key方式
auth_key = "b34f9b65-8824-4730-85e7-d176d3f8f58e:fx"  # Replace with your key
translator = deepl.Translator(auth_key)

def extract_audio(mp4_file_path, output_audio_file_path):
    """从MP4文件中提取音频。"""
    try:
        video = VideoFileClip(mp4_file_path)
        audio = video.audio
        audio.write_audiofile(output_audio_file_path)
        video.close()
        return True
    except Exception as e:
        print(f"提取音频时出错：{e}")
        return False
#使用apikey方式
def translate_to_chinese(text):
    try:
        result = translator.translate_text(text, target_lang="ZH")
        return result
    except Exception as e:
        print(f"翻译过程中出错：{e}")
        return ""

def transcribe_audio(audio_file, model_name='base', time_offset=0, use_gpu=True):
    """使用Whisper模型将音频转录为文本。"""
    try:
        device = "cuda" if use_gpu and torch.cuda.is_available() else "cpu"
        model = whisper.load_model(model_name, device=device)
        result = model.transcribe(audio_file, verbose=False)
        return result
    except Exception as e:
        print(f"音频转录时出错：{e}")
        return None

def generate_srt(result, output_file, time_offset=0):
    """根据转录结果生成SRT文件。"""
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            for i, segment in enumerate(result["segments"], start=1):
                start_time = format_srt_time(segment["start"] + time_offset)
                end_time = format_srt_time(segment["end"] + time_offset)
                """使用deeplx 作为翻译源 """
                #deepl pro 方式
                translation = deeplx_api.invoke_deeplx_api(segment['text'])
                #api key方式
                #translation = translate_to_chinese(segment['text'])

                f.write(f"{i}\n{start_time} --> {end_time}\n{segment['text']}\n{translation}\n")

        print(f"SRT文件已生成：{output_file}")
    except Exception as e:
        print(f"生成SRT文件时出错：{e}")

def format_srt_time(seconds):
    """Converts seconds to SRT time format."""
    milliseconds = int((seconds - int(seconds)) * 1000)
    hours = int(seconds / 3600)
    seconds = seconds % 3600
    minutes = int(seconds / 60)
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"

if __name__ == "__main__":
    input_folder = r"../static_movie/"
    output_folder = r"../output/"
    srt_folder=r"../SRT/"

    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取输入文件夹下所有的视频文件路径
    video_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.mkv')]

    for video_file in video_files:
        # 生成相应的音频文件路径和SRT文件路径
        audio_file_path = os.path.join(output_folder, os.path.splitext(os.path.basename(video_file))[0] + '.mp3')
        srt_file_path = os.path.join(output_folder, os.path.splitext(os.path.basename(video_file))[0] + '.srt')

        # 提取音频
        if extract_audio(video_file, audio_file_path):
            # 转录音频并生成SRT
            result = transcribe_audio(audio_file_path)
            if result:
                generate_srt(result, srt_file_path)
                # 将SRT文件移动到输出文件夹
                if os.path.exists(srt_file_path):  # 检查SRT文件是否存在
                    try:
                        shutil.move(srt_file_path, output_folder)
                    except Exception as e:

                        continue
                else:
                    print(f"SRT文件不存在：{srt_file_path}")

                # 删除提取的音频文件
                os.remove(audio_file_path)
    # 完成转录任务后，移动 SRT 文件到 static_movie 文件夹
    srt_files = [os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.endswith('.srt')]
    for srt_file in srt_files:
        try:
            shutil.move(srt_file, srt_folder)
        except Exception as e:
            print(f"移动 SRT 文件时出错：{e}")
            continue
    try:
        shutil.rmtree(output_folder)
        print(f"文件夹 {output_folder} 及其内容已成功删除。")
    except Exception as e:
        print(f"删除文件夹 {output_folder} 及其内容时出错：{e}")
