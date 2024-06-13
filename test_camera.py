import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Failed to open camera")

ret, frame = cap.read()
if not ret:
    print("Failed to capture image")

image_path = "./media/temp.jpg"
cv2.imwrite(image_path, frame)

# 画像を表示
cv2.imshow("Captured Image", frame)
cv2.waitKey(0)  # キーが押されるまで待機
cv2.destroyAllWindows()

cap.release()

