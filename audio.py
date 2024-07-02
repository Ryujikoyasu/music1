from pydub import AudioSegment

# 入力ファイルのパス
input_file = "../../../Downloads/落合バー未踏修了式.wav"

# オーディオファイルの読み込み
audio = AudioSegment.from_wav(input_file)

# オーディオファイルの長さ（ミリ秒単位）
duration_ms = len(audio)

# 分割する部分の数
num_parts = 5

# 1つの部分の長さ
part_length = duration_ms // num_parts

# 分割して保存
for i in range(num_parts):
    start_time = i * part_length
    end_time = (i + 1) * part_length if i < num_parts - 1 else duration_ms
    part_audio = audio[start_time:end_time]
    
    # 出力ファイル名の生成
    output_file = f"../../../Downloads/落合バー未踏修了式_{i+1}.wav"
    
    # 分割されたオーディオファイルの保存
    part_audio.export(output_file, format="wav")

print("ファイルの分割が完了しました。")
