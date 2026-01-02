from engine import database
from config import query_engine
from model import Transcription, Query

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/transcriptions")
def store_transcription(transcription: Transcription) -> str:
    database.save_transcribed_recording(transcription.transcription)
    return "Transcription saved successfully."

@app.post("/chat")
async def chat_stream(query: Query):
    def response_streamer(query):
        streaming_response = query_engine.query(query)
        for token in streaming_response.response_gen:
            print(token)
            yield token.encode("utf-8")

    return StreamingResponse(response_streamer(query.query), media_type="text/plain")