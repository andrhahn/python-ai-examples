# main.py - FastAPI endpoint
import os

from anthropic import Anthropic
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
conversation_history = []

MODEL = os.environ["ANTHROPIC_MODEL"]


@app.post("/chat")
async def chat(message: str):
    conversation_history.append({"role": "user", "content": message})

    def event_stream():
        with client.messages.stream(
            model=MODEL,
            max_tokens=1024,
            messages=conversation_history,
        ) as stream:
            for text in stream.text_stream:
                encoded = text.replace("\n", "\ndata: ")
                yield f"data: {encoded}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
