import google.generativeai as genai
import io
import cv2
import tempfile
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

system_instruction = """私は中学生の自然科学部です．自然観察をしていて，色々な生き物や植物があり，とっても楽しいです！あなたは私たちの先生で，動植物のことを楽しく教えてくれるので，みんなから好かれています．
あなたの出力は，全て音声化されるため，簡潔な出力が好ましいです．"""
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", system_instruction=system_instruction)

cap = cv2.VideoCapture(0)  # 0はデフォルトカメラ。必要に応じて変更
if not cap.isOpened():
    print("カメラを開けません")
    exit()

ret, frame = cap.read()
if not ret:
    print("画像をキャプチャできません")
    exit()

cap.release()



# 画像を一時ファイルとして保存
with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
    cv2.imwrite(temp_file.name, frame)
    temp_file_path = temp_file.name

    sample_file = genai.upload_file(path=temp_file_path,
                                    display_name="Sample drawing")


response = model.generate_content(["先生，これは何？", sample_file])
print(response.text)

