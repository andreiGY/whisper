import customtkinter
from CTkMessagebox import CTkMessagebox
import CTkTable
from whisper_hf import get_devices, get_whisper_models, transcribe
from history import get_data, save_data
import os
import threading
import time

AUDIO_FILE = None

def get_data_view():
    table_headers = ("Audio file", "Transcription file", "Date of transcription")
    hist_data = get_data()
    #print(hist_data)
    hist_data.insert(0, table_headers)
    #print(hist_data)
    return hist_data


def button_choose_file():
    print("button pressed")
    filename = customtkinter.filedialog.askopenfilename()
    global AUDIO_FILE
    AUDIO_FILE = filename
    print(filename)
    audio_file_label.configure(text="File: " + filename)

def transcribition_run(label):
    if AUDIO_FILE is None:
        CTkMessagebox(title="No audio file", message="Please, select audio file first.")
        return
    label.configure(text="Transcribing...")
    audio_file_name, output_file_name, finished_time = transcribe(model_id=optionmenu_models.get(), audio_file=AUDIO_FILE, device=optionmenu_devices.get())
    if output_file_name is not None:
        label.configure(text="Saving history...")
        save_data(audio_file=audio_file_name, output_file=output_file_name, datetime=str(finished_time))
        #hist_table.configure(values = get_data_view())
    time.sleep(1) 
    label.configure(text="Transcribing finished")
    time.sleep(1)
    label.configure(text="")

def start_task(label):
    thread = threading.Thread(target=transcribition_run, args=(label,))
    thread.start()
    #thread.join()
    hist_table.configure(values = get_data_view())

app = customtkinter.CTk()
app.title("Whisper client application")
app.geometry("1000x450")

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("themes/breeze.json")

# frame for transcription options (left)
op_frame = customtkinter.CTkFrame(master=app, width=300, height=400)
op_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
op_frame.grid_propagate(False)


# выбор устройства
device_label = customtkinter.CTkLabel(op_frame, text="Device:")
device_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
def optionmenu_callback(choice):
    print("optionmenu devices dropdown clicked:", choice)

devices_list = get_devices()
optionmenu_devices_var = customtkinter.StringVar(value=devices_list[0])
optionmenu_devices = customtkinter.CTkOptionMenu(op_frame,values=devices_list,
                                         command=optionmenu_callback,
                                         variable=optionmenu_devices_var)
optionmenu_devices.grid(row=1, column=0, padx=20, pady=0, sticky="w")

# выбор модели
model_label = customtkinter.CTkLabel(op_frame, text="Model:")
model_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
def optionmenu_callback(choice):
    print("optionmenu models dropdown clicked:", choice)

models_list = get_whisper_models()
models =[]
for model in models_list:
    models.append(model["name"])
optionmenu_models_var = customtkinter.StringVar(value=models[0])
optionmenu_models = customtkinter.CTkOptionMenu(op_frame,values=models,
                                         command=optionmenu_callback,
                                         variable=optionmenu_models_var)
optionmenu_models.grid(row=3, column=0, padx=20, pady=0, sticky="w")

# выбор аудио файла
button_audio_file = customtkinter.CTkButton(op_frame, text="Load audio file", command=button_choose_file)
button_audio_file.grid(row=4, column=0, padx=20, pady=20, sticky="w")
audio_file_label = customtkinter.CTkLabel(op_frame, text="No file selected")
audio_file_label.grid(row=5, column=0, padx=20, pady=0, sticky="w")

# отображение прогресса
progress_label = customtkinter.CTkLabel(op_frame, text="")
progress_label.grid(row=7, column=0, padx=20, pady=50, sticky="w")
# запуск транскрибации
button_run = customtkinter.CTkButton(op_frame, text="Transcribe", corner_radius=20, command=lambda: start_task(progress_label))
button_run.grid(row=6, column=0, padx=20, pady=50, sticky="w")

# frame for history list of transcriptions
hist_frame = customtkinter.CTkScrollableFrame(master=app, width=650, height=400)
hist_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nw")
#hist_frame.grid_propagate(False)

hist_label = customtkinter.CTkLabel(hist_frame, text="Transcription history")
hist_label.grid(row=0, column=0, padx=20, pady=10)
#таблица с историей транаскрибации
def row_selected(selected):
    print(selected)
    if selected['column'] != 2:
        print(f"command is: start {selected['value']}")
        os.system(f"start {selected['value']}")
    return


values = get_data_view()
#    [ ["Audio file", "Transcription file", "Date of transcription"],
#     ["1.mp3", "file_name1.txt", "2025-10-04 11:00:00"], ["2.ogg", "file_name2.txt", "2025-12-04 11:00:00"], ["3.wav", "file_name3.txt", "2025-10-05 11:00:00"]]
hist_table = CTkTable.CTkTable(master=hist_frame, row=5, column=3, values=values, command=row_selected, wraplength=300, header_color="gray", hover_color="light steel blue")
hist_table.grid(row=1, column=0, padx=10, pady=10, sticky="nw")


app.mainloop()