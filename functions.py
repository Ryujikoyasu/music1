import json
from openai import OpenAI
import google.generativeai as genai
import os
from dotenv import load_dotenv
import pyaudio
import wave

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

  return f"歌います！「{target}」の歌ですね！\n{response.text}"

# --- サービスレベルの関数 ---
def serve_drink():
  return "冷たいお飲み物はいかがですか〜"


### 他の便利な関数

# OpenAI APIを使ってテキストを音声に変換し、ストリーミング再生する
def stream_speech(text):
  """OpenAI APIを使ってテキストを音声に変換し、ストリーミング再生する。"""
  client = OpenAI(api_key=openai_key)
  try:
    with open("output.mp3", "wb") as f:
      response = client.audio.speech.create(
          model="tts-1",
          voice="alloy",  # 適切な音声を選択
          input=text,
      )
      response.stream_to_file("output.mp3")

  except Exception as e:
    print(f"音声生成中にエラーが発生しました: {e}")

def main():

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input="この修正により、エラーを回避し、OpenAI APIから取得した音声データをファイルに保存できるようになります。",
        response_format="mp3",
    )

    with open("output.mp3", "wb") as audio_file:
        audio_file.write(response.content)

    # PyAudioを初期化
    p = pyaudio.PyAudio()

    # 音声ファイルを開く
    wf = wave.open("output.mp3", 'rb')

    # ストリームを開く
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # チャンクごとにデータを読み込み、再生
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)

    # 再生終了処理
    stream.stop_stream()
    stream.close()
    p.terminate()
  
if __name__ == "__main__":
    main()