import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from functions import stream_sound_gemini
import base64
import io
from openai import OpenAI

# 環境変数の読み込み
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
OPENAI_API_KEY = os.getenv('OpenAI_API_KEY')

# API設定
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="gemini-exp-1206")
client = OpenAI(api_key=OPENAI_API_KEY)

def get_audio_html(audio_content):
    """音声データをHTML形式で再生可能にする"""
    b64 = base64.b64encode(audio_content).decode()
    return f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'

def text_to_speech(text):
    """テキストを音声に変換"""
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text
    )
    return response.content

def main():
    st.title("カタメニョウ - 富山の語り部AI")
    
    # チャット履歴の初期化
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])
        
        # システムプロンプトの設定
        system_prompt = """あなたは稲積みの「カタメニョウ」で，富山県山村の小院瀬見の語り部です．
        あなたは今から東京の人に話しかけられるので，2-3文でごく手短に簡潔に話してください．
        富山弁で（時折語尾が「っちゃ」「なが」となる）おじいちゃんみたいな口調がいいです．
        ちなみに今は冬の季節です．"""
        
        st.session_state.chat.send_message(
            f"あなたは以下の設定に従って応答してください：\n{system_prompt}"
        )

    # ユーザー入力
    user_input = st.text_input("メッセージを入力してください：")
    
    if st.button("送信"):
        if user_input:
            # ユーザーメッセージを表示
            st.write(f"あなた: {user_input}")
            
            try:
                # AIからの応答を取得
                response = st.session_state.chat.send_message(user_input)
                ai_message = response.text
                
                # AI応答を表示
                st.write(f"カタメニョウ: {ai_message}")
                
                # 音声変換と再生
                sentences = [s.strip() for s in ai_message.split('.') if s.strip()]
                for sentence in sentences:
                    if sentence:
                        audio_content = text_to_speech(sentence)
                        st.markdown(get_audio_html(audio_content), unsafe_allow_html=True)
                        
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main() 