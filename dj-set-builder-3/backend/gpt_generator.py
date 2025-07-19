
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import openai
import os

# Define a tua chave da OpenAI aqui ou usa variável de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-OPENAI-PLACEHOLDER")

router = APIRouter()

class PlaylistRequest(BaseModel):
    mood: str
    genres: list[str]
    bpm: int | None = None

@router.post("/generate-playlist")
def generate_playlist(req: PlaylistRequest):
    prompt = f"""
    Cria uma playlist de 10 músicas para o mood '{req.mood}' nos géneros {', '.join(req.genres)}.
    {f"Cada música deve ter entre {req.bpm - 5} e {req.bpm + 5} BPM." if req.bpm else ""}
    Lista título - artista - link Spotify (fictício).
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                { "role": "system", "content": "És um DJ especialista em criar playlists." },
                { "role": "user", "content": prompt }
            ],
            temperature=0.7
        )
        return { "playlist": response["choices"][0]["message"]["content"] }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
