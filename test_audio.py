from openai import OpenAI
import os
from dotenv import load_dotenv
import io
from pydub import AudioSegment
from pydub.playback import play


load_dotenv()
openai_key = os.environ['OpenAI_API_KEY']
client = OpenAI(api_key=openai_key)


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
                            "text": f"user_input:{user_input}"
                            }
                        ]
                    }
                ],
                stream=True
            )

    return response_stream


def stream_sound(response_stream):  
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

def main():
    user_input = "こんにちは"
    system_prompt = "あなたは里山で動く対話型のロボットです，ユーザからのにゅうりょくに対して、返答してください．ただし，user_inputとしてユーザの入力文を与えます．フレンドリーかつ簡潔に返答してください．"
    response_stream = chatgpt_stream(user_input, system_prompt)
    stream_sound(response_stream)
    
if __name__ == "__main__":
    main()