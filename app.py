import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from openai import OpenAI

# 環境変数の読み込み
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
OPENAI_API_KEY = os.getenv('OpenAI_API_KEY')

# API設定
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="gemini-pro")
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

def initialize_chat():
    """チャットの初期化"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    if "chat" not in st.session_state:
        st.session_state.chat = model.start_chat(history=[])
        system_prompt = """あなたは稲積みの「カタメニョウ」で，富山県山村の小院瀬見の語り部です．
        簡潔に2-3文で話してください．富山弁で語ってください．"""
        st.session_state.chat.send_message(system_prompt)

def main():
    st.title("カタメニョウ - 富山の語り部AI")
    
    initialize_chat()

    # チャット履歴の表示
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if message["role"] == "assistant" and "audio" in message:
                st.audio(message["audio"], format='audio/mp3')

    # ユーザー入力
    user_input = st.chat_input("メッセージを入力してください")
    
    if user_input:
        # ユーザーメッセージを表示・保存
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        
        try:
            # AIの応答を取得
            response = st.session_state.chat.send_message(user_input)
            ai_message = response.text
            
            # 音声生成
            audio = text_to_speech(ai_message)
            
            # メッセージと音声を保存・表示
            message_data = {
                "role": "assistant",
                "content": ai_message
            }
            if audio:
                message_data["audio"] = audio
            
            st.session_state.messages.append(message_data)
            
            with st.chat_message("assistant"):
                st.write(ai_message)
                if audio:
                    st.audio(audio, format='audio/mp3')
                    
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main() 