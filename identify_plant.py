import os, json
from openai import OpenAI
from dotenv import load_dotenv
import cv2

load_dotenv()
openai_key = os.environ['OpenAI_API_KEY']
client = OpenAI(api_key=openai_key)

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


def identify_plant(user_input):
    image_path = capture_image_from__camera()

    response = client.chat.completion.create(
        model='gpt-4o',
        messages=[
            {
                'role': 'system',
                'content': """あなたは野草ハンターで，道草のプロです．画像に基づいて植物を同定し，\
                    俗名，科と属，利用法や面白い豆知識など，要点を押さえて簡潔に教えます．\
                        似た植物がある場合，特に毒草の可能性がある場合，候補を複数提示して，見分け方も簡潔に教えてください．\
                            ただし，口調はギャルでお願いします．"""
            },
            {
                'role': 'user',
                'content': [
                    {"type":"text",
                     "text": user_input},
                    {"type":"image",
                        "url": image_path}
                ]
            }
        ],
    )