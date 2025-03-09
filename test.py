import asyncio
import websockets
import json

async def test_tts():
    uri = "ws://localhost:8000/ws/tts"
    
    async with websockets.connect(uri) as websocket:
        request_data = json.dumps({"text": "cook for me atleast", "speaker_wav": "female.wav"})
        await websocket.send(request_data)
        
        response = await websocket.recv()

asyncio.run(test_tts())