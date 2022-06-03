import speech_recognition as sr
import subprocess as sub
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import keyboard
import colors
import os
import tkinter
from pygame import mixer
import threading as tr
from tkinter import *
from PIL import Image, ImageTk

main_window = Tk()
main_window.title("Liz AV")
main_window.geometry("800x600")
main_window.resizable(0,0)
main_window.configure(bg='#302b63')


label_tittle = Label(main_window, text="Liz AV", bg="#6f0000", fg="#243B55",font=('Arial',"27", 'bold'))

label_tittle.pack(pady=10)

liz_photo=ImageTk.PhotoImage(Image.open("cc.jpg"))
window_photo= Label(main_window, image=liz_photo)
window_photo.pack(pady=5)
def mexican_voice():
    change_voice(0)
def spanish_voice():
    change_voice(3)
def german_voice():
    change_voice(4)
def change_voice(id):
    engine.setProperty('voice', voices[id].id)
    engine.setProperty('rate', 145)
    talk("Hola soy liz")



name = "liz"
listener = sr.Recognizer()
engine = pyttsx3.init()

# Voz escogida para el asistente
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 145)

sites = {
    'google': 'https://www.google.com.mx/',
    'youtube': 'https://www.youtube.com/',
    'facebook': 'https://www.facebook.com/',
    'whatsapp': 'https://web.whatsapp.com/',
    'tu manga': 'https://lectortmo.com/',
}

files = {
    'carta': 'Carta pasantia-Aldo Hernadnez.pdf',
    'cedula': 'Cedula y papeleta-aldo hernandez.docx',
    'foto': 'aldo.jpg'

}

programas = {
    'steam': r'D:\Steam\steam.exe'  # la r nos indica que lo ocuparemos como un solo string por el \

}


def talk(text):
    engine.say(text)
    engine.runAndWait()
# esto hara que sea posible que te esuche


def listen():

    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language="es")
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name, '')
    except:
        pass
    return rec
# reproducira lo que se menciona si


def run_liz():
    while True:
        try:
            rec = listen()
        except:
            print("Podrias repetirlo?")
            continue
        if 'reproduce' in rec:
            music = rec.replace('reproduce', '')
            print("Reproduciendo " + music)
            talk("Reproduciendo " + music)
            pywhatkit.playonyt(music)
        elif 'busca' in rec:
            search = rec.replace('busca', '')
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 2)
            print(search + ": " + wiki)
            talk(wiki)
        elif 'alarma' in rec:
            hora = rec.replace('alarma', '')
            hora = hora.strip()
            talk("Alarma activada a las " + hora + " horas")
            while True:
                if datetime.datetime.now().strftime('%H:%M') == hora:
                    print("Despierta")
                    mixer.init()
                    mixer.music.load("despierta.mp3")
                    mixer.music.play()
                    if keyboard.read_key() == "S":
                        mixer.music.stop()
                        break
        elif 'detener' in rec:
            talk("Nos vemos manco culiao")
            break
        elif 'colores' in rec:
            talk("Espere un momento")
            colors.capture()
        elif 'abre' in rec:
            for site in sites:
                if site in rec:
                    sub.call(f'start {sites[site]}', shell=True)
                    talk(f'Abriendo {site}')
            for app in programas:
                if app in rec:
                    talk(f'Abriendo {app}')
                    os.startfile(programas[app])
        elif 'archivo' in rec:
            for file in files:
                if file in rec:
                    sub.Popen([files[file]], shell=True)
                    talk(f'Abriendo {file}')
        elif 'escribe' in rec:
            try:
                with open("nota.txt", 'a') as f:
                    write(f)
            except FileNotFoundError as e:
                file = open("nota.txt", 'w')
                write(file)


def write(f):
    talk("Que quieres que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, puedes revisarlo")
    sub.Popen("nota.txt", shell=True)

button_voice_mx=Button(main_window, text="Voz mexicana", fg="white", bg="#348F50", font=("Arial",10,"bold"),command=mexican_voice)
button_voice_mx.place(x=625,y=90,width=100,height=30)
button_voice_es=Button(main_window, text="Voz española", fg="white", bg="#b92b27", font=("Arial",10,"bold"),command=spanish_voice)
button_voice_es.place(x=625,y=130,width=100,height=30)
button_voice_al=Button(main_window, text="Voz alemana", fg="white", bg="#f4791f", font=("Arial",10,"bold"),command=german_voice)
button_voice_al.place(x=625,y=170,width=100,height=30)


main_window.mainloop()
