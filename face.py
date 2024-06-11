import cv2
import face_recognition
import os


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
                face_encoding = face_recognition.face_encodings(image)[0]
                
                # 人物名とエンコーディングを追加
                known_face_encodings.append(face_encoding)
                known_face_names.append(person_name)

    return known_face_encodings, known_face_names
                
def greeting_with_name():
    # 顔画像と名前の対応を取得
    known_face_encodings, known_face_names = face_registration()

    # カメラから1フレームだけキャプチャ
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    video_capture.release()  # カメラを解放


    # 顔認識処理
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # 登録された顔画像と照合し、認識結果を取得
    for face_encoding, face_location in zip(face_encodings, face_locations):
        match_results = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distance = face_recognition.face_distance(known_face_encodings, face_encoding)
        
        # 最も近い顔画像のインデックスを取得
        best_match_index = face_distance.argmin()
        
        if match_results[best_match_index]:
            # 知っている人の場合
            name = known_face_names[best_match_index]
            print(f"{name} さん、こんにちは！")
        else:
            # 知らない人の場合
            print("はじめまして！")

        # 顔の周りに枠を描画 (オプション)
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    # キャプチャした画像を表示 (オプション)
    cv2.imshow('Captured Image', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    greeting_with_name()