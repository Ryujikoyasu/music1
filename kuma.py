import numpy as np
import sounddevice as sd
import time
from scipy import signal

# 英数字のモールス信号辞書
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '0': '-----', ' ': ' '
}

# 日本語（カタカナ）のモールス信号辞書
JAPANESE_MORSE_DICT = {
    'ア': '--.--', 'イ': '.-', 'ウ': '..-', 'エ': '-.---', 'オ': '.-...',
    'カ': '.-.', 'キ': '-.-..', 'ク': '...-', 'ケ': '-.--', 'コ': '----',
    'サ': '-.-.-', 'シ': '--.-.', 'ス': '---.-', 'セ': '.---.', 'ソ': '---.',
    'タ': '-.', 'チ': '..-.', 'ツ': '.--.',  'テ': '.-.--', 'ト': '..-..', 
    'ナ': '.-.', 'ニ': '-.-.', 'ヌ': '....', 'ネ': '--.-', 'ノ': '..--',
    'ハ': '-...', 'ヒ': '--..-', 'フ': '--..', 'ヘ': '.', 'ホ': '-..',
    'マ': '-..-', 'ミ': '..-.-', 'ム': '-', 'メ': '-...-', 'モ': '-..-.',
    'ヤ': '.--', 'ユ': '-..--', 'ヨ': '--',
    'ラ': '...', 'リ': '--.', 'ル': '-.--.',  'レ': '---', 'ロ': '.-.-',
    'ワ': '-.-', 'ヲ': '.---', 'ン': '.-.-.',
    '゛': '.', '゜': '..-..', '、': '.-.-.-', '。': '.-.-.-'
}

# 音声パラメータ
SAMPLE_RATE = 44100  # サンプリングレート
DOT_DURATION = 0.2  # ドットの長さ (秒)
DASH_DURATION = DOT_DURATION * 3  # ダッシュの長さ
PAUSE_DURATION = DOT_DURATION  # 文字間の休止時間
VOLUME = 0.3  # 音量（0.0 から 1.0）

# フィルタパラメータ
LOW_FREQ = 300  # 低域カットオフ周波数 (Hz)
HIGH_FREQ = 800  # 高域カットオフ周波数 (Hz)
FILTER_ORDER = 4  # フィルタの次数

def generate_wave_noise(duration):
    """波のようなノイズを生成"""
    # ホワイトノイズの生成
    samples = int(SAMPLE_RATE * duration)
    noise = np.random.normal(0, 1, samples)
    
    # バンドパスフィルタの設計
    nyquist = SAMPLE_RATE / 2
    low = LOW_FREQ / nyquist
    high = HIGH_FREQ / nyquist
    b, a = signal.butter(FILTER_ORDER, [low, high], btype='band')
    
    # フィルタの適用
    filtered_noise = signal.filtfilt(b, a, noise)
    
    # エンベロープの適用（なめらかな立ち上がりと減衰）
    envelope = np.ones_like(filtered_noise)
    attack_time = 0.02
    release_time = 0.02
    attack_samples = int(attack_time * SAMPLE_RATE)
    release_samples = int(release_time * SAMPLE_RATE)
    
    # 音の立ち上がり
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    # 音の減衰
    envelope[-release_samples:] = np.linspace(1, 0, release_samples)
    
    # 音量の正規化と調整
    wave = filtered_noise * envelope
    wave = wave / np.max(np.abs(wave)) * VOLUME
    
    return wave.astype(np.float32)

def play_wave_sound(duration):
    """波のような音を再生"""
    wave = generate_wave_noise(duration)
    sd.play(wave, SAMPLE_RATE)
    sd.wait()

def text_to_morse(text):
    """テキストをモールス信号に変換"""
    morse = ''
    text = text.upper()  # 英字を大文字に変換
    
    for char in text:
        if char in MORSE_CODE_DICT:
            morse += MORSE_CODE_DICT[char] + ' '
        elif char in JAPANESE_MORSE_DICT:
            morse += JAPANESE_MORSE_DICT[char] + ' '
        elif char in ['、', '。']:
            morse += JAPANESE_MORSE_DICT[char] + ' '
    return morse.strip()

def play_morse_sound(morse_code):
    """モールス信号を音声で再生"""
    for symbol in morse_code:
        if symbol == '.':
            play_wave_sound(DOT_DURATION)
        elif symbol == '-':
            play_wave_sound(DASH_DURATION)
        elif symbol == ' ':
            time.sleep(PAUSE_DURATION)
        time.sleep(PAUSE_DURATION / 2)

def main():
    print("モールス信号変換プログラム")
    print("注意: 英数字とカタカナに対応しています")
    print("終了するには 'q' を入力してください")
    
    while True:
        text = input('\n変換するテキストを入力してください: ')
        if text.lower() == 'q':
            break
        
        morse_code = text_to_morse(text)
        print(f'モールス信号: {morse_code}')
        play_morse_sound(morse_code)

if __name__ == '__main__':
    main()
