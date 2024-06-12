import cv2
import face_recognition
import os
from dotenv import load_dotenv
from openai import OpenAI
from functions import capture_image_from__camera, encode_image, chatgpt_stream_with_image

load_dotenv()
openai_key = os.environ['OpenAI_API_KEY']
client = OpenAI(api_key=openai_key)

def face_registration():

    # --- 顔画像と名前のデータ ---
    known_face_encodings = []
    known_face_names = []

    faces_dir = "./faces"
    for person_name in os.listdir(faces_dir):
        person_dir = os.path.join(faces_dir, person_name)

        # ディレクトリ内の画像ファイルを処理
        for filename in os.listdir(person_dir):
            if filename.endswith((".jpg", ".jpeg", ".png")):
                image_path = os.path.join(person_dir, filename)
                image = face_recognition.load_image_file(image_path)
                
                # 顔認識処理前に顔の検出を行う
                face_locations = face_recognition.face_locations(image)

                if len(face_locations)  == 1:
                    face_encoding = face_recognition.face_encodings(image)[0]
                    
                    # 人物名とエンコーディングを追加
                    known_face_encodings.append(face_encoding)
                    known_face_names.append(person_name)

    return known_face_encodings, known_face_names
                
def greeting_with_name(user_input):
    # 顔画像と名前の対応を取得
    known_face_encodings, known_face_names = face_registration()

    print("顔画像と名前の対応を取得しました")
    # カメラから1フレームだけキャプチャ
    frame, image_path = capture_image_from__camera()
    base64_image = encode_image(image_path)

    # 顔認識処理
    face_locations = face_recognition.face_locations(frame)

    # 認識された名前を格納するリスト
    recognized_names = []

    if len(face_locations) > 0:
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # 登録された顔画像と照合し、認識結果を取得
        for face_encoding, face_location in zip(face_encodings, face_locations):
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = face_distances.argmin()
            
            if face_distances[best_match_index] < 0.6:
                name = known_face_names[best_match_index]
                recognized_names.append(name)  # リストに名前を追加

            else:
                # 知らない人の場合
                recognized_names.append("初めましてさん")

            # 顔の周りに枠を描画 (オプション)
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    
        # カンマ区切りで名前を表示. 「初めましてさん」と呼ぶことで、名前が登録されていない場合に対応
        # 顔を認識できなかった場合は，適当に誤魔化す
        print(",".join(recognized_names))

        system_prompt =  """あなたは里山で動く対話型のロボットです，\
                                地域の人が挨拶をしてきたので，挨拶をし返してください．\
                                ただし，user_inputとしてユーザの挨拶文を,\
                                    user_nameとして画像に写っている人の名前をリストで与えます．\
                                ただし，名前がわからない場合は「初めましてさん」としています．\
                                    また，名前が複数ある場合は，カンマ区切りで名前を教えます．\
                                        フレンドリーかつ簡潔に挨拶をしてください．\
                                        画像を見て，状況を把握しても良いですね．"""
        text = f"user_input:{user_input},user_name:{recognized_names}"

        response_stream = chatgpt_stream_with_image(text, system_prompt, base64_image)

    else:
        system_prompt =  """あなたは里山で動く対話型のロボットです，\
                    地域の人が挨拶をしてきたのですが，あなたはその人の顔が見えませんでした．\
                            そこで，挨拶をするとともに，「どこにいるのよ」など，顔が見えなかったことを伝えてください．"""
        
        response_stream = chatgpt_stream_with_image(user_input, system_prompt, base64_image)


    # # キャプチャした画像を表示 (オプション)
    # cv2.imshow('Captured Image', frame)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return response_stream


if __name__ == "__main__":
    greeting_with_name("こんにちは")