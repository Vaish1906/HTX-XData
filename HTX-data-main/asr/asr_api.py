from litestar import Litestar, get, post, Request
from litestar.datastructures import UploadFile
from pydantic import BaseModel
from typing import Annotated
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from datasets import load_dataset
import torch
import librosa, io
import soundfile as sf


# Respond to GET requests at the ping endpoint with pong
@get("/ping")
async def ping_pong() -> str:
    return "pong"


# Define a class for the response that ASR endpoint returns
class ASRResponse(BaseModel):
    transcription: str
    duration: str


# Respond to POST requests at the ASR endpoint with the transcription and duration
@post(path="/asr")
async def transcribe_audio(request: Request) -> ASRResponse:

    data = await request.form()
    audio_file: UploadFile = data.get("file")

    file_content = await audio_file.read()

    # load model and processor
    processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")

    try:
        # Load audio data from the file content
        with io.BytesIO(file_content) as bio:
            audio_input, sample_rate = sf.read(bio)

        # Ensure the audio is at the correct sample rate (16kHz)
        target_sample_rate = processor.feature_extractor.sampling_rate
        print(target_sample_rate)
        if sample_rate != target_sample_rate:
            audio_input = librosa.resample(
                audio_input, orig_sr=sample_rate, target_sr=target_sample_rate
            )
            sample_rate = target_sample_rate

        # Tokenize the audio input
        input_values = processor(
            audio_input,
            return_tensors="pt",
            padding="longest",
            sampling_rate=sample_rate,
        ).input_values  # Batch size 1

        # Retrieve logits
        logits = model(input_values).logits

        # Take argmax and decode
        predicted_ids = torch.argmax(logits, dim=-1)
        transcribed_text = processor.batch_decode(predicted_ids)[
            0
        ]  # Get the first element of the list

        # Calculate audio duration
        audio_duration = librosa.get_duration(y=audio_input, sr=sample_rate)

        return ASRResponse(transcription=transcribed_text, duration=str(audio_duration))

    except Exception as e:
        return {"error": f"Error processing audio: {e}"}


app = Litestar([ping_pong, transcribe_audio])
