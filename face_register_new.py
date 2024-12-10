import face_recognition
import cv2
import os

def register_new_person(name, num_pictures=5):
    """
    新しい人物を登録する関数

    Args:
        name (str): 登録する人物の名前
        num_pictures (int, optional): 撮影する顔写真の枚数. Defaults to 5.
    """

    # フォルダを作成
    folder_path = os.path.join("faces", name)
    os.makedirs(folder_path, exist_ok=True)

    # カメラを初期化
    video_capture = cv2.VideoCapture(0)

    print(f"{name} さんの顔写真を撮影します。")
    print("スペースキーを押して撮影、'q'キーを押して終了")

    count = 0
    while count < num_pictures:
        # カメラからフレームを取得
        ret, frame = video_capture.read()

        # カメラの映像を表示
        cv2.imshow('Registering Face', frame)

        # キー入力待ち
        key = cv2.waitKey(1) & 0xFF

        # スペースキーで撮影
        if key == ord(' '):
            image_path = os.path.join(folder_path, f"{name}_{count}.jpg")
            cv2.imwrite(image_path, frame)
            count += 1
            print(f"{count}/{num_pictures} 枚撮影しました。")

        # 'q' キーで終了
        if key == ord('q'):
            break

    # カメラを解放
    video_capture.release()
    cv2.destroyAllWindows()

    print(f"{name} の顔写真を {count} 枚保存しました。")

# --- 使用例 ---
register_new_person("まろんちゃん")