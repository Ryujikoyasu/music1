# functions.py

import json
from openai import OpenAI

client = OpenAI()

# --- 基本動作レベルの関数 ---
def GO_TO(target):
  return f"GO_TO(\"{target}\")"

def GO_ALONG(target):
  return f"GO_ALONG(\"{target}\")"

# --- タスクレベルの関数 ---
def identify_plant():
  
  return "これはお花です"

def sing_folk_song(target):
  # 歌詞生成部分はOpenAI APIに任せる
  response = client.openai.ChatCompletion.create(
    model="gpt-4o",  # 適切なモデルを選択
    messages=[
      {"role": "user", "content": f"「{target}」についての歌詞を作ってください。"}
    ]
  )
  lyrics = response.choices[0].message.content
  return f"歌います！「{target}」の歌ですね！\n{lyrics}"

# --- サービスレベルの関数 ---
def serve_drink():
  return "冷たいお飲み物はいかがですか〜"