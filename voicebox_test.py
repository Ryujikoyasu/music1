import requests
import json
import pyaudio
import wave
from datetime import datetime

def vvox_test(text, filename="voice.wav", save_file=True):
    # エンジン起動時に表示されているIP、portを指定
    host = "127.0.0.1"
    port = 50021
    
    # 音声化する文言と話者を指定(3で標準ずんだもんになる) 42はちび式じい　52は麒ヶ島宗麟
    params = (
        ('text', text),
        ('speaker', 42),
    )
    
    # 音声合成用のクエリ作成
    query = requests.post(
        f'http://{host}:{port}/audio_query',
        params=params,
    )
    
    # クエリパラメータの調整
    query_data = query.json()
    # ピッチを少し下げる
    query_data['pitch_scale'] = 0.95
    # 話速を少し遅くして明瞭にする
    query_data['speed_scale'] = 0.95
    # 音質を改善
    query_data['volumeScale'] = 1.2
    query_data['prePhonemeLength'] = 0.1
    query_data['postPhonemeLength'] = 0.1
    
    # 音声合成を実施
    synthesis = requests.post(
        f'http://{host}:{port}/synthesis',
        headers = {"Content-Type": "application/json"},
        params = params,
        data = json.dumps(query_data)
    )
    
    # 再生処理
    voice = synthesis.content

    # サンプリングレート (Vvoxは24000Hz)
    sample_rate = 24000
    # 前後50msをカット　ノイズ対策
    trim_bytes = int(sample_rate * 0.05 * 2)  # 50ms分のバイト数 (16bit=2byte)
    trimmed_voice = voice[trim_bytes : len(voice) - trim_bytes]

    # ファイルとして保存
    if save_file:
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)  # モノラル
            wf.setsampwidth(2)  # 16bit
            wf.setframerate(sample_rate)
            wf.writeframes(trimmed_voice)
    
    if not save_file:
        pya = pyaudio.PyAudio()
        
        # サンプリングレートが24000以外だと高音になったり低音になったりする
        stream = pya.open(format=pyaudio.paInt16,
                          channels=1,
                          rate=24000,
                          output=True)
        
        stream.write(trimmed_voice)
        stream.stop_stream()
        stream.close()
        pya.terminate()

def process_text_file(filepath):
    # テキストファイルを読み込む
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 空行を除去
    texts = [line.strip() for line in lines if line.strip()]
    
    # 一文ずつ処理
    for i, text in enumerate(texts, 1):
        filename = f"voice_{i:03d}.wav"
        print(f"Generating {filename}...")
        print(f"Text: {text}")
        vvox_test(text, filename=filename, save_file=True)
        
if __name__ == "__main__":
    process_text_file("nyou.txt")
