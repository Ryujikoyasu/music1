from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai_key = os.environ['OpenAI_API_KEY']
client = OpenAI(api_key=openai_key)

with open("./media/output.mp3", "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )
            
print("Transcription:", transcription)