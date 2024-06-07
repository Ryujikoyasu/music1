import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from functions import GO_TO, GO_ALONG, identify_plant, sing_folk_song, serve_drink

load_dotenv()
openai_key = os.environ['OpenAI_API_KEY']
client = OpenAI(api_key=openai_key)

# --- Function Calling の設定 ---
tools = [
  {
    "type": "function",
    "function": {
      "name": "identify_plant",
      "description": "ユーザーが植物について尋ねたときに呼び出します。",
      "parameters": {
        "type": "object",
        "properties": {},
      },
    }
  },
  {
    "type": "function",
    "function": {
      "name": "GO_TO",
      "description": "ユーザーがロボットに人追跡や移動を指示したときに呼び出します。",
      "parameters": {
        "type": "object",
        "properties": {
          "target": {
            "type": "string",
            "description": "移動先の対象"
          }
        },
        "required": ["target"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "GO_ALONG",
      "description": "ユーザーがロボットに道の追従を指示したときに呼び出します。",
      "parameters": {
        "type": "object",
        "properties": {
          "target": {
            "type": "string",
            "description": "追従対象"
          }
        },
        "required": ["target"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "sing_folk_song",
      "description": "ユーザーが歌をリクエストしたときに呼び出します。",
      "parameters": {
        "type": "object",
        "properties": {
          "target": {
            "type": "string",
            "description": "歌の対象"
          }
        },
        "required": ["target"]
      }
    }
  },
  {
    "type": "function",
    "function": {
      "name": "serve_drink",
      "description": "ユーザーが飲み物をほしがっているときに呼び出します。",
      "parameters": {
        "type": "object",
        "properties": {},
      },
    }
  }
]


def process_user_input(user_input, context=[]):
  """
  ユーザー入力を処理し、適切なアクションを実行します。

  Args:
      user_input (str): ユーザー入力
      context (list): 対話コンテキスト

  Returns:
      str: ロボットの応答
  """

  response = client.chat.completions.create(
      model="gpt-4o",
      messages=[
          {"role": "system", "content": "あなたは対話型除草ロボットの頭脳です。ユーザーの指示を理解し、適切な行動を選択してください。"},
          *context,
          {"role": "user", "content": user_input}
      ],
      tools=tools,
      tool_choice="auto"  # モデルに判断を任せる
  )

  # モデルの応答を取得
  response_message = response.choices[0].message

  # 関数呼び出しがある場合
  if response_message.tool_calls:
      tool_call = response_message.tool_calls[0]
      function_name = tool_call.function.name
      function_args = json.loads(tool_call.function.arguments)

      # 関数を実行
      if function_name == "identify_plant":
          result = identify_plant()
      elif function_name == "GO_TO":
          result = GO_TO(function_args.get("target"))
      elif function_name == "GO_ALONG":
          result = GO_ALONG(function_args.get("target"))
      elif function_name == "sing_folk_song":
          result = sing_folk_song(function_args.get("target"))
      elif function_name == "serve_drink":
          result = serve_drink()
      else:
          result = f"エラー：関数 '{function_name}' は定義されていません。"

      # コンテキストを更新
      context.append({"role": "user", "content": user_input})
      context.append({"role": "assistant", "content": result})
      return result, context

  # 関数呼び出しがない場合
  else:
      # コンテキストを更新
      context.append({"role": "user", "content": user_input})
      context.append({"role": "assistant", "content": response_message.content})
      return response_message.content, context

# --- 対話例 ---
context = []
while True:
  user_input = input("あなた：")
  response, context = process_user_input(user_input, context)
  print(f"ロボット：{response}")