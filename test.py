import librosa
import soundfile as sf
import numpy as np

def enhance_audio(input_file, output_file):
    # 音声ファイルの読み込み
    y, sr = librosa.load(input_file, sr=None)
    
    # ローパスフィルターの適用（低音強調）
    y_low = librosa.effects.preemphasis(y, coef=0.95)
    
    # イコライザー効果（低音域を増幅）
    stft = librosa.stft(y)
    frequencies = librosa.fft_frequencies(sr=sr, n_fft=2048)  # n_fftを指定
    
    # 低周波数帯域（100Hz以下）を強調
    freq_mask = frequencies <= 100
    freq_mask = np.repeat(freq_mask[:, np.newaxis], stft.shape[1], axis=1)  # マスクの形状を調整
    stft_modified = stft.copy()
    stft_modified[freq_mask] *= 1.5  # 低音を1.5倍に増幅
    
    # 音声をクリアにするためのノイズ削減
    y_clean = librosa.istft(stft_modified)
    
    # 音量の正規化
    y_normalized = librosa.util.normalize(y_clean)
    
    # 結果を保存
    sf.write(output_file, y_normalized, sr)

# 使用例
input_file = 'voice_20241210_110500.wav'
output_file = 'voice_20241210_110500_enhanced.wav'
enhance_audio(input_file, output_file) 