import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from functions import GO_TO, GO_ALONG, GO_TO_PERSON, sing_song, take_break, stream_sound_openai, stream_sound_vvox,  chatgpt_stream, chatgpt_stream_with_image
from face import greeting_with_name, face_registration
import google.generativeai as genai
from identify_plant import identify_plant, explain_plant
import keyboard
from whispertest import transcribe_audio, record_audio


### GPT-4oは会話やfunction calling担当．Geminiは作詞担当． ###
load_dotenv()
openai_key = os.environ['OpenAI_API_KEY']
client = OpenAI(api_key=openai_key)

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
genai.configure(api_key=GOOGLE_API_KEY)

### 初期化の処理
# 顔を覚えるやつ
known_face_encodings, known_face_names = face_registration()

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
      "properties": {},
      },
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
      "name": "sing_song",
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
      "name": "take_break",
      "description": "ユーザーが休憩を示唆したとき・飲み物をほしがっているときに呼び出します。",
      "parameters": {
        "type": "object",
        "properties": {},
      },
    }
  },
  {
    "type": "function",
    "function": {
      "name": "greeting_with_name",
      "description": "ユーザーが「こんにちは」のように挨拶してきたときに呼び出します。",
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

  # コンテキストのサイズを制限
  if len(context) > 20:
      context = context[-20:]

  # 関数呼び出しがある場合
  if response_message.tool_calls:
    tool_call = response_message.tool_calls[0]
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)

    # 関数を実行
    if function_name == "identify_plant":
        result_type, result = "text", identify_plant(user_input)
    elif function_name == "explain_plant":
        result_type, result = "text", explain_plant(user_input)
    elif function_name == "GO_TO":
        result_type, result = "text", GO_TO(function_args.get("target"))
    elif function_name == "GO_ALONG":
        result_type, result = "text", GO_ALONG(function_args.get("target"))
    elif function_name == "GO_TO_PERSON":
        result_type, result = "text", GO_TO_PERSON(function_args.get("target"))

    elif function_name == "take_break":
        result_type, result = "text", take_break(user_input)
    elif function_name == "greeting_with_name":
        result_type, result = "text", greeting_with_name(user_input, known_face_encodings, known_face_names)
    elif function_name == "sing_song":
        result_type, result = "audio", sing_song(function_args.get("target"))
    else:
        result_type, result = "text", f"エラー：関数 '{function_name}' は定義されていません。"

    # コンテキストを更新
    context.append({"role": "user", "content": user_input})
    # print(type(result))
    context.append({"role": "assistant", "content": result})

    return function_name, result_type, result, context

  # 関数呼び出しがない場合は，ユーザと通常の会話をする
  else:
    system_prompt = """あなたは里山の対話型ロボットです．\
        ユーザの入力に対して，適当な返答を行います．\
          ただし，あなたが行動に移せなさそうな場合は，ギャルっぽく断るようにしてください．"""
    response_stream = chatgpt_stream(user_input, system_prompt)
    print(response_stream)
      # コンテキストを更新
    context.append({"role": "user", "content": user_input})
    context.append({"role": "assistant", "content": response_stream})
    
    return "no_function", "text", response_stream, context  # ダミーの値を追加


# --- 対話例 ---

# スペースキーが押された時のイベントを設定
# keyboard.add_hotkey('space', record_audio)

context = []
while True:
    
    print("スペースキーを押すと録音が開始します。")
    keyboard.wait('space')  # 最初のスペースキー押下を待機
    # 録音終了後、文字起こしを実行
    audio_path = "./media/output.wav"
    user_input = transcribe_audio(audio_path)
    print("ユーザー：", user_input)
    
    if user_input is None:
        continue
    
    function_name, result_type, result, context = process_user_input(user_input, context)
    if function_name == "identify_plant" or function_name == "explain_plant":
        stream_sound_vvox(result)
    elif function_name == "greeting_with_name":
        stream_sound_vvox(result)
    elif function_name == "take_break":
        stream_sound_vvox(result)
    elif function_name == "sing_song":
        stream_sound_vvox(result)
    elif function_name == "no_function":
        stream_sound_vvox(result)
    else:
        print("ロボット：", result)

    print("コンテキスト：", context)
  
    
