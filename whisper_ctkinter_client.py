import customtkinter
from CTkMessagebox import CTkMessagebox
from whisper_hf import get_devices, get_whisper_models, transcribe

AUDIO_FILE = None


def button_choose_file():
    print("button pressed")
    filename = customtkinter.filedialog.askopenfilename()
    global AUDIO_FILE
    AUDIO_FILE = filename
    print(filename)
    audio_file_label.configure(text=filename)
def button_run():
    if AUDIO_FILE is None:
        CTkMessagebox(title="No audio file", message="Please, select audio file first.")
        return
    transcribe(model_id=optionmenu_models.get(), audio_file=AUDIO_FILE, device=optionmenu_devices.get())

app = customtkinter.CTk()
app.title("Whisper client application")
app.geometry("600x300")

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("themes/breeze.json")

# выбор аудио файла
button_audio_file = customtkinter.CTkButton(app, text="Load audio file", command=button_choose_file)
button_audio_file.grid(row=0, column=1, padx=20, pady=0, sticky="w")
audio_file_label = customtkinter.CTkLabel(app, text="No file selected")
audio_file_label.grid(row=1, column=1, padx=20, pady=0, sticky="w")

# запуск транскрибации
button_run = customtkinter.CTkButton(app, text="Transcribe", command=button_run)
button_run.grid(row=2, column=1, padx=20, pady=0, sticky="w")


# выбор устройства
device_label = customtkinter.CTkLabel(app, text="Device:")
device_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
def optionmenu_callback(choice):
    print("optionmenu devices dropdown clicked:", choice)

devices_list = get_devices()
optionmenu_devices_var = customtkinter.StringVar(value=devices_list[0])
optionmenu_devices = customtkinter.CTkOptionMenu(app,values=devices_list,
                                         command=optionmenu_callback,
                                         variable=optionmenu_devices_var)
optionmenu_devices.grid(row=1, column=0, padx=20, pady=0, sticky="w")

# выбор модели
model_label = customtkinter.CTkLabel(app, text="Model:")
model_label.grid(row=2, column=0, padx=20, pady=20, sticky="w")
def optionmenu_callback(choice):
    print("optionmenu models dropdown clicked:", choice)

models_list = get_whisper_models()
models =[]
for model in models_list:
    models.append(model["name"])
optionmenu_models_var = customtkinter.StringVar(value=models[0])
optionmenu_models = customtkinter.CTkOptionMenu(app,values=models,
                                         command=optionmenu_callback,
                                         variable=optionmenu_models_var)
optionmenu_models.grid(row=3, column=0, padx=20, pady=0, sticky="w")

app.mainloop()