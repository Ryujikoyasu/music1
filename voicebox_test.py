import requests
import json
import pyaudio
import wave
from datetime import datetime

def vvox_test(text, save_file=True):
    # エンジン起動時に表示されているIP、portを指定
    host = "127.0.0.1"
    port = 50021
    
    # 音声化する文言と話者を指定(3で標準ずんだもんになる) 42はちび式じい
    params = (
        ('text', text),
        ('speaker', 2),
    )
    
    # 音声合成用のクエリ作成
    query = requests.post(
        f'http://{host}:{port}/audio_query',
        params=params,
    )
    
    # 音声合成を実施
    synthesis = requests.post(
        f'http://{host}:{port}/synthesis',
        headers = {"Content-Type": "application/json"},
        params = params,
        data = json.dumps(query.json())
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
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"voice_{timestamp}.wav"
        
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)  # モノラル
            wf.setsampwidth(2)  # 16bit
            wf.setframerate(sample_rate)
            wf.writeframes(trimmed_voice)
    
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
    
if __name__ == "__main__":
    text = "こんにちは，しゅうちゃん．良い天気なので今日も畑仕事頑張ろう．"
    vvox_test(text)
