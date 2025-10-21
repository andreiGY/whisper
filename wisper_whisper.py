import whisper

def split_audio_file(audio_file):
    # splitting of long audio file should be implemented here
    return

def transcribe_audio(model, audio_file):

    model = whisper.load_model(model) # "turbo" for example

    # load audio and pad/trim it to fit 30 seconds
    audio_file = whisper.load_audio(audio_file)
    split_audio_file(audio_file)

    audio = whisper.pad_or_trim(audio_file)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio, n_mels=model.dims.n_mels).to(model.device)

    # detect the spoken language
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)

    # print the recognized text
    print(result.text)

if __name__ == "__main__":
    transcribe_audio()

