import pyaudio
import wave
import keyboard
import os
from dotenv import load_dotenv
from openai import OpenAI
import sounddevice as sd
from pydub import AudioSegment
import threading
import time

load_dotenv()
openai_key = os.environ['OpenAI_API_KEY']
client = OpenAI(api_key=openai_key)

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
WAVE_OUTPUT_FILENAME = "./media/output.wav"


def record_audio():
    """スペースキーが押されたときに呼び出される録音関数"""
    global recording

    if not recording:
        # 録音開始
        print("録音開始。もう一度スペースキーを押すと停止します。")
        # PyAudioインスタンスを関数内で作成
        audio = pyaudio.PyAudio()
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
        frames = []

        recording = True  # 録音開始状態を記録
        while recording:
            data = stream.read(CHUNK)
            frames.append(data)
            if keyboard.is_pressed('space'):  # スペースキーが押されたらループを抜ける
                recording = False

        # 録音停止
        stream.stop_stream()
        stream.close()

        # 音声データをファイルに保存
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        print(f"録音を停止しました。音声を {WAVE_OUTPUT_FILENAME} に保存しました。")
        audio.terminate()

# グローバル変数で録音状態を管理
recording = False

# スペースキーが押された時のイベントを設定
keyboard.add_hotkey('space', record_audio)


def transcribe_audio(audio_path):
    """音声ファイルを文字起こしする関数"""
    
    try:
        # pydubで使用するffmpegのパスを指定
        AudioSegment.converter = "/opt/homebrew/bin/ffmpeg"  # ここを実際のffmpegのパスに置き換える

        # WAVをMP3に変換
        print("WAVファイルをMP3に変換中...")
        sound = AudioSegment.from_wav(audio_path)
        sound.export("./media/output.mp3", format="mp3", bitrate="320k")
        print("MP3への変換完了")

        # Whisper APIを用いてテキスト化
        with open("./media/output.mp3", "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
        print("Transcription:", transcription)
        
        return transcription

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None


def main():
    """メイン関数"""
    global recording

    while True:

        print("スペースキーを押すと録音が開始します。")
        keyboard.wait('space')  # 最初のスペースキー押下を待機
        
        # 録音終了後、文字起こしを実行
        audio_path = "./media/output.wav"
        transcribe_audio(audio_path)
        user_input = transcribe_audio(audio_path)
        print("ユーザー：", user_input)
        response_stream = chatgpt_stream(user_input)
        print("ロボット：", response_stream)



if __name__ == "__main__":
    main()