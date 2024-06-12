import os, json
from openai import OpenAI
from dotenv import load_dotenv
import cv2
import base64
from functions import capture_image_from__camera, encode_image, chatgpt_stream, chatgpt_stream_with_image

load_dotenv()
openai_key = os.environ['OpenAI_API_KEY']
client = OpenAI(api_key=openai_key)


def identify_plant(user_input):
    _, image_path = capture_image_from__camera()
    base64_image = encode_image(image_path)

    system_prompt = """あなたは野草ハンターで，道草のプロです．画像に基づいて植物を同定し，\
                    俗名，科と属，利用法や面白い豆知識など，要点を押さえて簡潔に教えます．\
                        似た植物がある場合，特に毒草の可能性がある場合，候補を複数提示して，見分け方も簡潔に教えてください．\
                        ただし，口調はギャルでお願いします．\
                        あなたの出力は全て音声化されるので，自然な口語を使ってください．"""
    response_stream = chatgpt_stream_with_image(user_input, system_prompt, base64_image)

    return response_stream



def explain_plant(user_input):

    system_prompt = """あなたは野草ハンターで，道草のプロです．ユーザと散歩中で，あなたに特定の植物のことを聞いてきます．\
                    俗名，科と属，利用法や面白い豆知識など，要点を押さえて簡潔に教えます．\
                        似た植物がある場合，特に毒草の可能性がある場合，候補を複数提示して，見分け方も簡潔に教えてください．\
                            ただし，口調はギャルでお願いします．\
                        あなたの出力は全て音声化されるので，自然な口語を使ってください．"""
    response_stream = chatgpt_stream(user_input, system_prompt)

    return response_stream