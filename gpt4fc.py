import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from functions import GO_TO, GO_ALONG, GO_TO_PERSON, sing_folk_song, serve_drink, stream_speech
import google.generativeai as genai
from identify_plant import identify_plant, explain_plant

### GPT-4oは会話やfunction calling担当．Geminiは作詞担当． ###

load_dotenv()
openai_key = os.environ['OpenAI_API_KEY']
client = OpenAI(api_key=openai_key)

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
genai.configure(api_key=GOOGLE_API_KEY)

# --- Function Calling の設定 ---
tools = [
  ### 植物に関するもの ###
  {
    "type": "function",
    "function": {
      "name": "identify_plant",
      "description": "ユーザーが植物の同定を尋ねたときに呼び出します。",
      "parameters": {
        "type": "object",
        "properties": {},
      },
    }
  },
    {
    "type": "function",
    "function": {
      "name": "explain_plant",
      "description": "ユーザーが植物の名前を指定して説明を尋ねたときに呼び出します。",
      "parameters": {
        "type": "object",
        "properties": {
          "target": {
            "type": "string",
            "description": "植物名"
          }
        },
        "required": ["target"]
      }
    }
  },

    ### ロボットの行動に関するもの ###
  {
    "type": "function",
    "function": {
      "name": "GO_TO",
      "description": "ユーザーがロボットに対象物への移動を指示したときに呼び出します。",
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
      "name": "GO_TO_PERSON",
      "description": "ユーザーがロボットに人を追従するよう指示したときに呼び出します。",
      "parameters": {
        "type": "object",
        "properties": {
          "target": {
            "type": "string",
            "description": "（指定があれば）追従する人の服の色などの特徴.指定が無ければ単に「person」"
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
      "description": "ユーザーが休憩を示唆したとき・飲み物をほしがっているときに呼び出します。",
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
        result_type, result = "text", identify_plant(user_input)
    elif function_name == "explain_plant":
        result_type, result = "text", explain_plant(function_args.get("target"))
    elif function_name == "GO_TO":
        result_type, result = "text", GO_TO(function_args.get("target"))
    elif function_name == "GO_ALONG":
        result_type, result = "text", GO_ALONG(function_args.get("target"))
    elif function_name == "GO_TO_PERSON":
        result_type, result = "text", GO_TO_PERSON(function_args.get("target"))
    elif function_name == "sing_folk_song":
        result_type, result = "audio", sing_folk_song(function_args.get("target"))
    elif function_name == "serve_drink":
        result_type, result = "text", serve_drink()
    else:
        result_type, result = "text", f"エラー：関数 '{function_name}' は定義されていません。"

    # コンテキストを更新
    context.append({"role": "user", "content": user_input})
    context.append({"role": "assistant", "content": result})
    return function_name, result_type, result, context

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
    function_name, result_type, result, context = process_user_input(user_input, context)
    if function_name == "identify_plant" or function_name == "explain_plant":
        stream_speech(result)
    else:
        print("ロボット：", result)