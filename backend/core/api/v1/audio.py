from fastapi import APIRouter, UploadFile, File
from services.audio_service import AudioService
from pydub import AudioSegment
from io import BytesIO

router = APIRouter(prefix="/audio")

router = APIRouter(prefix="/audio")

@router.post("/")
def send_audio(file: bytes = File(...)):
    webm_audio = BytesIO(file)

    # Конвертация webm → wav
    audio = AudioSegment.from_file(webm_audio, format="webm")
    wav_io = BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)

    wav_bytes = wav_io.read()

    # Отправка в AudioService
    AudioService.send_audio(wav_bytes)

    return {"status": "ok"}