import torch
import time
import numpy as np
import soundfile as sf
from fastapi import FastAPI, WebSocket
from TTS.api import TTS
from huggingface_hub import snapshot_download
from torch.serialization import add_safe_globals
from TTS.tts.configs.xtts_config import XttsConfig, XttsAudioConfig
from TTS.config.shared_configs import BaseDatasetConfig
from TTS.tts.models.xtts import XttsArgs

import base64, io

if torch.cuda.is_available():
    print("GPU available")

add_safe_globals([XttsConfig])
add_safe_globals([XttsAudioConfig])
add_safe_globals([BaseDatasetConfig])
add_safe_globals([XttsArgs])

# Load the Coqui XTTS-v2 model
print("Loading Coqui XTTS-v2...")
# tts = TTS(MODEL_PATH).to("cuda")  # Ensure GPU is used
# tts = TTS("C:/Users/shalabh/.cache/huggingface/hub/models--coqui--XTTS-v2/snapshots/6c2b0d75eae4b7047358e3b6bd9325f857d43f77").to("cuda")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)

# FastAPI app
app = FastAPI()

def encode_audio_to_base64(file_path):
    """Reads the audio file and returns a Base64-encoded string."""
    with open(file_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode("utf-8")

# WebSocket endpoint for real-time TTS
@app.websocket("/ws/tts")
async def tts_websocket(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Receive text input
            data = await websocket.receive_json()
            print(data)
            text = data.get("text", "")
            speaker_wav = data.get("speaker_wav", None)

            if not text:
                await websocket.send_text("Error: No text received")
                continue

            start_time = time.time()

            # Generate speech and store in memory (BytesIO buffer)
            audio_buffer = io.BytesIO()
            tts.tts_to_file(text=text, file_path=audio_buffer, speaker_wav="female.wav", language="en")

            end_time = time.time()
            time_taken = round(end_time - start_time, 3)

            # Convert in-memory audio to Base64
            audio_buffer.seek(0)
            audio_base64 = base64.b64encode(audio_buffer.read()).decode("utf-8")

            # Send response
            await websocket.send_json({
                "status": "success",
                "time_taken": time_taken,
                "audio_base64": audio_base64
            })
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
