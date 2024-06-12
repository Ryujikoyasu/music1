import os
from pathlib import Path
from openai import OpenAI
import io
from pydub import AudioSegment
from pydub.playback import play
import requests
import json
import cv2
import time
from dotenv import load_dotenv

#plantnet
plantnet_api_key = os.environ.get('PlantNet_API_KEY')
PROJECT = "japan"; # try specific floras: "weurope", "canada"…
api_endpoint = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={plantnet_api_key}"
# output_file_path = "/content/output.json"

#openai
openai_api_key = os.environ.get('OpenAI_API_KEY')
instructions = """あなたは家庭菜園ロボットの雑草同定・解説機能を担っています!植物同定用のJSONデータをみて，植物の同定をした後、
この植物や特徴や生態，利用法などの情報を面白おかしく解説してください。日本人が聞いて理解できるよう，わかりやすく楽しい説明を心がけてください。
聞き手にとっての楽しさが一番です！
あなたの出力は，「この植物は，おそらく」から始めてください．文は必ずビックリマーク[!]で終わるようにしてください．
"""
initial_reply = "わかりました！jsonデータを入力してください！"

def capture_image_from__camera(device_id=2):
    cap = cv2.VideoCapture(device_id)
    ret, frame = cap.read()
    if not ret:
        print("failed to capture image")
        return
    image_path = "temp.jpg"
    cv2.imwrite(image_path, frame)
    cap.release()
    # cv2.destroyAllWindows()
    return image_path

def get_result_from_api(image_path):
    image_data = open(image_path, 'rb')
    data = {
    # 'organs': ['flower', 'leaf'],
    'organs': ['leaf']
    }
    files = [
    ('images', (image_path, image_data)),
    # ('images', (image_path_2, image_data_2))
    ]
    req = requests.Request('POST', url=api_endpoint, files=files, data=data)
    prepared = req.prepare()
    s = requests.Session()
    response = s.send(prepared)
    json_result = json.loads(response.text)
    # print(json_result)

    if response.status_code != 200:
        return None, None
    if json_result['results'][0]['score'] > 0.25:
        top_candidates = [json_result['results'][0]]
    else:
        top_candidates = json_result['results'][:4]
    simplified_json = {
        "top_candidates": [
            {
                "scientific_name": candidate['species']['scientificNameWithoutAuthor'],
                "common_names": candidate['species']['commonNames'],
                "score": candidate['score'],
                "genus": candidate['species']['genus']['scientificNameWithoutAuthor'],
                "family": candidate['species']['family']['scientificNameWithoutAuthor'],
            } for candidate in top_candidates
        ]
    }

    # with open(output_file_path, 'w') as file:
    #     json.dump(simplified_json, file, indent=4)
    
    return response, simplified_json


def main():
    client = OpenAI(
        api_key=openai_api_key
    )
    messages = []
    messages.append({"role": "user", "content": instructions})
    messages.append({"role": "assistant", "content": initial_reply})

    while True:
        image_path = capture_image_from__camera()
        if image_path is None:
            break
        _, simplified_json = get_result_from_api(image_path)
        if simplified_json is None:
            print("no plant detected")
            time.sleep(5)
            continue
        messages.append({"role": "user", "content": json.dumps(simplified_json)})
        response_stream = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=messages,
            stream=True
        )

        assistant_text = ""
        # for chunk in response_stream:
        #     bot_response = chunk.choices[0].delta.content
        #     if bot_response:
        #         # 一文ずつTTSに入力するため、文末を検出するまでテキストを溜め込む
        #         assistant_text += bot_response
        #         if any(char in assistant_text for char in "!！"):
        #             # 文末が検出された場合、TTSに入力
        #             print("Assistant:", assistant_text)
        #             messages.append({"role": "assistant", "content": assistant_text})
        #             # TTSを使用して音声に変換
        #             tts_response = client.audio.speech.create(
        #                 model="tts-1",
        #                 voice="onyx",
        #                 input=assistant_text,
        #             )
        #             # 音声データを取得して再生
            #             audio_stream = io.BytesIO(tts_response.content)
            #             sound = AudioSegment.from_file(audio_stream, format="mp3")
            #             play(sound)

        #             assistant_text = ""  # テキストをリセット

        for chunk in response_stream:
            bot_response = chunk.choices[0].delta.content
            if bot_response:
                # 一文ずつTTSに入力するため、文末を検出するまでテキストを溜め込む
                assistant_text += bot_response
            
        print("Assistant:", assistant_text)
        messages.append({"role": "assistant", "content": assistant_text})
        # TTSを使用して音声に変換
        tts_response = client.audio.speech.create(
            model="tts-1",
            voice="onyx",
            input=assistant_text,
        )
        # 音声データを取得して再生
        audio_stream = io.BytesIO(tts_response.content)
        sound = AudioSegment.from_file(audio_stream, format="mp3")

        output_path = "output_audio.mp3"
        sound.export(output_path, format="mp3")
        play(sound)



        assistant_text = ""  # テキストをリセット



if __name__ == "__main__":
    main()