import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
import pathlib
import sys
from datetime import datetime
import gc
import os

AUDIO_FILE = None

# directory for cached models of whisper
MODELS_CACHE_DIR = "models/"
# directory for transcribtion results (.txt files)
OUTPUTS_DIR = "outputs/"

def choose_device():
    device = "cpu"
    if torch.cuda.is_available():
        device = "cuda:0"
    elif torch.xpu.is_available():
        device = "xpu"
    elif torch.backends.mps.is_available():
        device = "mps"
    return device

def get_devices():
    devices = []
    if torch.cuda.is_available(): devices.append("cuda:0")
    if torch.xpu.is_available(): devices.append("xpu")
    if torch.backends.mps.is_available(): devices.append("mps")
    devices.append("cpu")
    return devices

dtype_dic = {
    "cpu": torch.float32,
    "cuda:0": torch.float16,
    "xpu": torch.float16,
    "mps": torch.float32
}

def get_whisper_models():
    whisper_models=[
        {
            "name": "openai/whisper-large-v3-turbo", "parameters": "809 M"
        },
        {
            "name": "openai/whisper-large-v2", "parameters": "1550 M"
        },
        {
            "name": "openai/whisper-medium", "parameters": "769 M"
        },
        {
            "name": "openai/whisper-small", "parameters": "244 M"
        },
        {
            "name": "openai/whisper-base", "parameters": "74 M"
        },
        {
            "name": "openai/whisper-tiny", "parameters": "39 M"
        },
        {
            "name": "distil-whisper/distil-large-v3", "parameters": "756 M"
        }
        ]
    return whisper_models

def transcribe(model_id, audio_file, device=None, torch_dtype=None):
    
    if device is None:
        device = choose_device()
        print(f"Device is {device}")
    if torch_dtype is None:
        torch_dtype = dtype_dic.get(device, torch.float32)
        print(f"torch_dtype is {torch_dtype}")

    # create directory for cached models if it not exists
    if not os.path.exists(MODELS_CACHE_DIR):
        os.makedirs(MODELS_CACHE_DIR)

    # create directory for output files if it not exists
    if not os.path.exists(OUTPUTS_DIR):
        os.makedirs(OUTPUTS_DIR)

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, cache_dir=MODELS_CACHE_DIR
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        chunk_length_s=30,
        batch_size=16,  # batch size for inference - set based on your device
        torch_dtype=torch_dtype,
        device=device,
    )
    AUDIO_FILE = audio_file
    file_path = pathlib.Path(AUDIO_FILE)
    if not file_path.is_file():
        print(f"{AUDIO_FILE} is not a file. Exiting...")
        sys.exit(1)


    generate_kwargs = {"return_timestamps": True}  # "language": "russian"
    start_time = datetime.now()

    result = pipe(AUDIO_FILE, generate_kwargs=generate_kwargs) # sample
    out_text = result["text"]
    #print(result)

    end_time = datetime.now()
    file_name = f"{OUTPUTS_DIR}{pathlib.Path(AUDIO_FILE).stem}_{end_time.strftime('%Y%m%d%H%M%S')}.txt"
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(out_text)

    print(f"Processing file {AUDIO_FILE} took {end_time - start_time}. Result saved into file {file_name}")
    gc.collect()
    return AUDIO_FILE, file_name, end_time


if __name__ == "__main__":
    transcribe(sys.argv[1], sys.argv[2])
    
