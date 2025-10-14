import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from datasets import load_dataset
import pathlib
import sys
from datetime import datetime

AUDIO_FILE = "D:\\torrents\\ORWELL\\Orwell-skot1.mp3"

MODELS_CACHE_DIR = "models/"

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
    devices = ["cpu"]
    if torch.cuda.is_available(): devices.append("cuda:0")
    if torch.xpu.is_available(): devices.append("xpu")
    if torch.backends.mps.is_available(): devices.append("mps")
    return devices

#device = "cuda:0" if torch.cuda.is_available() else "cpu"
dtype_dic = {
    "cpu": torch.float32,
    "cuda:0": torch.float16,
    "xpu": torch.float16,
    "mps": torch.float32
}
#torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

device = choose_device()
print(f"Device is {device}")
torch_dtype = dtype_dic.get(device, torch.float32)
print(f"torch_dtype is {torch_dtype}")

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

model_id = "distil-whisper/distil-large-v3"

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
file_path = pathlib.Path(AUDIO_FILE)
if not file_path.is_file():
    print(f"{AUDIO_FILE} is not a file. Exiting...")
    sys.exit(1)


generate_kwargs = {"language": "russian", "return_timestamps": True}
start_time = datetime.now()

result = pipe(AUDIO_FILE, generate_kwargs=generate_kwargs) # sample
out_text = result["text"]
print(out_text)

end_time = datetime.now()
file_name = f"outputs/{pathlib.Path(AUDIO_FILE).stem}_{end_time.strftime('%Y%m%d%H%M%S')}"
with open(file_name, 'w') as f:
    f.write(out_text)

print(f"Processing file {AUDIO_FILE} took {end_time - start_time}. Result saved into file {file_name}")
