import json
from openai import OpenAI
import google.generativeai as genai
import os
from dotenv import load_dotenv

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