from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import soundfile as sf
import numpy as np
import io
from scipy.signal import resample

app = FastAPI()

@app.get("/")
async def welcome():
    return "Process Audio"

@app.post("/process_audio")
async def process_audio(file: UploadFile = File(...)):
    try:
        # Read the uploaded file
        contents = await file.read()
        
        # Use BytesIO to create a file-like object from the contents
        audio_file = io.BytesIO(contents)
        
        # Load the audio file using soundfile
        audio_array, sample_rate = sf.read(audio_file)
        
        # Resample the audio to 16000 Hz
        target_sample_rate = 16000
        number_of_samples = round(len(audio_array) * float(target_sample_rate) / sample_rate)
        audio_array_resampled = resample(audio_array, number_of_samples)
        
        # Convert the numpy array to a list for JSON serialization
        audio_list = audio_array_resampled.tolist()
        
        # Return the audio array and sample rate
        return JSONResponse({
            "audio_array": audio_list,
            "sample_rate": target_sample_rate
        })

    except Exception as e:
        # Logging the error for debugging
        print(f"Error processing audio file: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

