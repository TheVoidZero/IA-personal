import speech_recognition as sr
import subprocess as sub 
import pyttsx3, pywhatkit, wikipedia, datetime, keyboard, colors, os
from pygame import mixer

name = "liz"
listener = sr.Recognizer()
engine = pyttsx3.init()

#Voz escogida para el asistente
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate',145)

def talk(text):
    engine.say(text)
    engine.runAndWait()
#esto hara que sea posible que te esuche
def listen():
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            pc= listener.listen(source)
            rec=listener.recognize_google(pc, language="es")
            rec= rec.lower()
            if name in rec:
                rec = rec.replace(name,'')
    except:
        pass
    return rec
#reproducira lo que se menciona si
def run_cas():
    while True:
        rec=listen()
        if 'reproduce' in rec:
            music = rec.replace('reproduce','')
            print("Reproduciendo " + music)
            talk("Reproduciendo " + music)
            pywhatkit.playonyt(music)
        elif 'busca' in rec:
            search = rec.replace('busca','')
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 2)
            print(search +": "+ wiki)
            talk(wiki)
        elif 'alarma' in rec:
            hora = rec.replace('alarma','')
            hora= hora.strip()
            talk("Alarma activada a las "+ hora + " horas")
            while True:
                if datetime.datetime.now().strftime('%H:%M')==hora:
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
#correra la funcion
if __name__== '__main__':
    run_cas()