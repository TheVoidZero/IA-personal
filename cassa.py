import speech_recognition as sr
import pyttsx3, pywhatkit
name = "dinero"
listener = sr.Recognizer()
engine = pyttsx3.init()

#Voz escogida para el asistente
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()
#esto hara que sea posible que te esuche
def listen():
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            pc= listener.listen(source)
            rec=listener.recognize_google(pc)
            rec= rec.lower()
            if name in rec:
                rec = rec.replace(name,'')
    except:
        pass
    return rec
#reproducira lo que se menciona
def run_cas():
    rec=listen()
    if 'reproduce' in rec:
        music = rec.replace('reproduce','')
        print("Reproduciendo " + music)
        talk("Reproduciendo " + music)
        pywhatkit.playonyt(music)
#correra la funcion
if __name__== '__main__':
    run_cas()