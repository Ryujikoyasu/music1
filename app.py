import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from openai import OpenAI
import base64
import io

# 環境変数の読み込み
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
OPENAI_API_KEY = os.getenv('OpenAI_API_KEY')

# API設定
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="gemini-exp-1206")
client = OpenAI(api_key=OPENAI_API_KEY)

def text_to_speech(text):
    """テキストを音声に変換"""
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text
        )
        return response.content
    except Exception as e:
        st.error(f"音声変換エラー: {e}")
        return None

def main():
    st.title("カタメニョウ - 富山の語り部AI")
    
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])
        system_prompt = """あなたは稲積みの「カタメニョウ」で，富山県山村の小院瀬見の語り部です．
        簡潔に2-3文で話してください．富山弁で語ってください．"""
        st.session_state.chat.send_message(system_prompt)

    user_input = st.text_input("メッセージを入力してください：")
    
    if st.button("送信", key="send"):
        if user_input:
            with st.chat_message("user"):
                st.write(user_input)
            
            try:
                response = st.session_state.chat.send_message(user_input)
                ai_message = response.text
                
                with st.chat_message("assistant"):
                    st.write(ai_message)
                    
                    # 音声生成と再生
                    audio = text_to_speech(ai_message)
                    if audio:
                        b64 = base64.b64encode(audio).decode()
                        st.audio(audio, format='audio/mp3')
                        
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main() 