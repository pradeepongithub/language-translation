from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware 
from typing import List
from pydantic import BaseModel
from googletrans import Translator

app = FastAPI()
translator = Translator()

class TranslationRequest(BaseModel):
    text: str

class TranslationResponse(BaseModel):
    translation: str

async def translate_text(text: str, target_language: str = "mi") -> str:
    translation = translator.translate(text, dest=target_language)
    translated_text = translation.text
    return translated_text

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.post("/translate/", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    translated_text = await translate_text(request.text)
    return {"translation": translated_text}

@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            translated_text = await translate_text(data)
            await websocket.send_text(translated_text)
    except WebSocketDisconnect:
        pass

