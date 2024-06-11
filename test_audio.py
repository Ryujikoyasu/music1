from pathlib import Path
import pygame
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai_key = os.environ['OpenAI_API_KEY']
client = OpenAI(api_key=openai_key)
# ファイルパスを設定
speech_file_path = Path(__file__).parent / "speech.mp3"

# 音声ファイルを生成してストリーミング保存
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input="""Today is a wonderful day to build something people love! Let's get started!""",
)

response.stream_to_file(speech_file_path)

# Pygameを使って音声ファイルを再生
def play_audio(file_path):
    # Pygameの初期化
    pygame.mixer.init()
    
    # 音声ファイルのロード
    pygame.mixer.music.load(file_path)
    
    # 音声ファイルの再生
    pygame.mixer.music.play()
    
    # 再生が終了するまで待機
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# 音声ファイルを再生
play_audio(speech_file_path)
