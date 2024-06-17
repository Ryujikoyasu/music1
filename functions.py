import json
from openai import OpenAI
import google.generativeai as genai
import os
from dotenv import load_dotenv
import io
from pydub import AudioSegment
from pydub.playback import play
import cv2
import base64
import sounddevice as sd
import numpy as np
from io import BytesIO
from voicebox_test import vvox_test

load_dotenv()
openai_key = os.environ['OpenAI_API_KEY']
client = OpenAI(api_key=openai_key)

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
genai.configure(api_key=GOOGLE_API_KEY)

# --- 基本動作レベルの関数 ---
def GO_TO(target):
  return f"GO_TO(\"{target}\")"

def GO_ALONG(target):
  return f"GO_ALONG(\"{target}\")"

def GO_TO_PERSON(target):
  return f"GO_TO(\"{target}\")"

# --- タスクレベルの関数 ---

def sing_folk_song(target):
  # Geminiが作詞して，Sunoが音楽生成
  model = genai.GenerativeModel(model_name="gemini-1.5-pro")
  prompt = f"""{target}についての歌詞を書いてください．ただし，子供から大人まで「へぇー」って思えるような\
    生態や特徴，利用の仕方などを積極的に盛り込んでください．歌は２番構成で，なるべく短く，児童曲スタイルで書いて．\
    漢字は使わずに平仮名と片仮名のみで書いてください．
      短い歌詞なので，余計なワードや繰り返しはなるべく含めないことで情報量を多くしてください．\
        あなたの出力は全て歌詞になるので，「（イントロ）」などの余計な文字を含めてはいけません．"""
  response = model.generate_content(prompt)
  
  # この歌詞から音楽を生成する
  ### api 

  return f"{target} {response.text}"

# --- サービスレベルの関数 ---
def take_break(user_input):
  system_prompt = """あなたは里山の対話型ロボットです．\
          農作業を終えたユーザの言葉を聞いて，疲れを労ったり冷たい飲み物を勧めたりします．"""
  response_stream = chatgpt_stream(user_input, system_prompt)
  return response_stream

### 他の便利な関数
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
      return base64.b64encode(image_file.read()).decode('utf-8')

def capture_image_from__camera(device_id=0):
    cap = cv2.VideoCapture(device_id)
    ret, frame = cap.read()
    if not ret:
        print("failed to capture image")
        return
    image_path = "temp.jpg"
    cv2.imwrite(image_path, frame)

    # # 画像を表示
    # cv2.imshow("Captured Image", frame)
    # cv2.waitKey(0)  # キーが押されるまで待機
    # cv2.destroyAllWindows()
    
    cap.release()
    # cv2.destroyAllWindows()
    return frame, image_path

# OpenAI APIを使ってストリーミングチャットを行う
def chatgpt_stream(user_input, system_prompt):
    response_stream = client.chat.completions.create(
                model='gpt-4o',
                messages=[
                    {
                        'role': 'system',
                        'content': system_prompt
                    },
                    {
                        'role': 'user',
                        'content': [
                            {"type":"text",
                            "text": user_input
                            }
                        ]
                    }
                ],
                stream=True
            )

    return response_stream

def chatgpt_stream_with_image(user_input, system_prompt, base64_image):
    response_stream = client.chat.completions.create(
        model='gpt-4o',
        messages=[
            {
                'role': 'system',
                'content': system_prompt
            },
            {
                'role': 'user',
                'content': [
                    {"type":"text",
                    "text": user_input
                    },
                    {"type":"image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        stream=True
    )

    return response_stream

# OpenAI APIを使ってストリーミングテキストを一文一文音声に変換し再生する
def stream_sound_openai(response_stream):  
    assistant_text = ""
    for chunk in response_stream:
        bot_response = chunk.choices[0].delta.content
        if bot_response:
            # 一文ずつTTSに入力するため、文末を検出するまでテキストを溜め込む
            assistant_text += bot_response
            if any(char in assistant_text for char in ".．。!！?？"):
                # 文末が検出された場合、TTSに入力
                print("Assistant:", assistant_text)
                # TTSを使用して音声に変換
                tts_response = client.audio.speech.create(
                    model="tts-1",
                    voice="nova",
                    input=assistant_text,
                )
                # 音声データを取得して再生
                audio_stream = io.BytesIO(tts_response.content)
                sound = AudioSegment.from_file(audio_stream, format="mp3")
                play(sound)
                assistant_text = ""

def stream_sound_vvox(response_stream):
    assistant_text = ""
    for chunk in response_stream:
        bot_response = chunk.choices[0].delta.content
        if bot_response:
            assistant_text += bot_response
            if any(char in assistant_text for char in ".．。!！?？"):
                print("Assistant:", assistant_text)
                vvox_test(assistant_text)
                assistant_text = ""


def main():
    user_input = "こんにちは"
    system_prompt = "あなたは里山で動く対話型のロボットです，ユーザからの入力に対して、返答してください．ただし，user_inputとしてユーザの入力文を与えます．フレンドリーかつ簡潔に返答してください．"
    response_stream = chatgpt_stream(user_input, system_prompt)
    stream_sound_openai(response_stream)
  

if __name__ == "__main__":
    main()