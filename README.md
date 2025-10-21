# Setup before first run

**First of all - install Python 3.10 or above**

1. Create virtual environment. For Windows and Macos/Linux: Navigate to your project folder and run: 
    ```
    python -m venv venv
    ```
2. Activate virtual environment:
    2.1. for Macos/Linux: Navigate to your project folder and run: 
    ```
    source venv/bin/activate
    ```
    2.2. for Windows (Command): Navigate to your project folder and run: 
    ```
    venv\Scripts\activate
    ```
3. Install required packages.
    3.1. if you have NVIDIA GPU run: 
    ```
    pip install -r cuda.txt
    ```
    3.2. if you have Intel GPU. Your device must be list id 1.1 Hardware [here](https://pytorch-extension.intel.com/installation?platform=gpu&version=v2.8.10%2Bxpu&os=windows&package=pip)
    ```
    pip install -r intel_gpu.txt
    ```
    3.3. for Mac
    ```
    pip install -r requirements.txt
    ```


# How to run Whisper client


1. Activate virtual environment - see step 2 of "Setup before first run"
2.1. Run desktop client (Tkinter):
```
    python whisper_ctkinter_client.py
```
2.2. Run via command shell as a script:
```
    python whisper_transformers.py model_name path_to_your_audio_file
```
example to run as script:
```
    python whisper_transformers.py openai/whisper-large-v3-turbo C:\audio.mp3
```
Whisper models listed here [Whisper models of Huggingface.com](https://huggingface.co/models?search=openai/whisper)



   
