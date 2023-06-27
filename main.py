import tkinter as tk
from tkinter import ttk
from pydub import AudioSegment
from PIL import Image, ImageTk
import wave
from pathlib import Path
import winsound
from auto_tune import main
from pydub.effects import speedup



try:
    song = "plik.wav"
    file_wave = wave.open(song, "rb")
except:
    warning = tk.Tk()
    warning.title("Warning")
    warning.geometry("600x150")
    warning.configure(bg="light blue")
    warning_text = ttk.Label(warning, anchor="center", text="Dodaj do folderu utwór w formacie wav o nazwie plik.", font="Constantia 20 ")
    warning_text.pack()
    warning.mainloop()
    quit()







#zmina głośności
def volumeIncrease():
    file = AudioSegment.from_wav(song)
    value = int(slider.get())
    file = file + value
    file.export("new_test.wav", format="wav")

def volumeDecrease():
    file = AudioSegment.from_wav(song)
    value = int(slider.get())
    file = file - value
    file.export("new_test.wav", format="wav")

#przyśpieszenie
def speed():
    file = AudioSegment.from_wav(song)
    value = float(speed_entry.get())
    new_file = speedup(file, value, 150)
    new_file.export("new_test.wav", format="wav")  



isplaying = False

#playing
def play():
        if isplaying:
            winsound.PlaySound(None, winsound.SND_PURGE)
            return False
        else:
            path_to_file = "new_test.wav"
            path = Path(path_to_file)
            if path.is_file():
                winsound.PlaySound("new_test.wav", winsound.SND_ASYNC) 
            else:
                winsound.PlaySound(song, winsound.SND_ASYNC) 
            return True

def change():
    global isplaying
    isplaying = play()






#interfejs

window = tk.Tk()
window.title("Music App")
window.geometry("600x600")
window.configure(bg="light blue")

leftframe = ttk.Frame(window)
leftframe.pack(side="left", fill="y")

rightframe = ttk.Frame(window)
rightframe.pack()


# parameters
parameters_frame = ttk.Frame(leftframe)
parameters_label = ttk.Label(parameters_frame, text="PARAMETERS", font="Constantia 24 bold underline")
channels_label = ttk.Label(parameters_frame, text = f"channels: {file_wave.getnchannels()}", font="Constantia 20")
frame_rate_label = ttk.Label(parameters_frame, text = f"frame rate: {file_wave.getframerate()}", font="Constantia 20 ")
frames_label = ttk.Label(parameters_frame, text = f"frames: {file_wave.getnframes()}", font="Constantia 20") 
time_label = ttk.Label(parameters_frame, text = f"time: {round(file_wave.getnframes() / file_wave.getframerate())} s", font="Constantia 20") 



#player
img = Image.open("img_player.jpg").resize((150,150))
img_player = ImageTk.PhotoImage(img)
button_player = ttk.Button(leftframe, text="Play", image=img_player, compound="top", command = change)
button_player.pack(padx=100, pady=100)

parameters_frame.pack()
parameters_label.pack()
channels_label.pack()
frame_rate_label.pack()
frames_label.pack()
time_label.pack()



#speeding
speed_entry = ttk.Entry(rightframe, width=25)
speed_button = ttk.Button(rightframe, text = "Speed up", command = speed)
speed_button.pack(pady=20)
speed_entry.pack(pady=20)




#autotune
button_at = ttk.Button(rightframe, text="AUTOTUNE", command = main)
button_at.pack(pady=50)

#voluming
volumeinc_button = ttk.Button(rightframe, text = "Increase", command = volumeIncrease)
volumedec_button = ttk.Button(rightframe, text = "Decrease", command = volumeDecrease)

volume_frame = ttk.Frame(rightframe)
decibles = ttk.Label(volume_frame, text="Decibles: 0")
decibels_value = tk.DoubleVar()

def decibles_change(value):
    decibles.config(text=f"Decibles: {int(slider.get())}")


slider = ttk.Scale(volume_frame, from_=0, to=40, orient='horizontal', variable=decibels_value, command=decibles_change)
slider.pack(pady=30)
decibles.pack()
volume_frame.pack()



volumeinc_button.pack(pady=10)
volumedec_button.pack(pady=10)










window.mainloop()
