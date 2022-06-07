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

comandos = """
    Comandos que puedes utilizar:
    -Reproduce...(cancion)
    -Busca... (algo)
    -Alarma...(hora en 24H)
    -Archivo...(nombre)
    -Colores (rojo,azul,amarillo)
    -Detener
"""

#ventana del asistente
label_tittle = Label(main_window, text="Liz AV", bg="#6f0000", fg="#243B55",font=('Arial',"27", 'bold'))
#se ubicara enmedio
label_tittle.pack(pady=10)
#se pondra el apartado donde se muestra los comandos
canvas_comandos=Canvas(bg="#654ea3", height=200,width=195)
canvas_comandos.place(x=0,y=0)
canvas_comandos.create_text(90,80,text=comandos,fill="white",font='Arial 10')

#ventana donde se escribira
text_info = Text(main_window,bg="#654ea3",fg="white")
text_info.place(x=0,y=200,height=200,width=195)

text_info = Text(main_window, bg="#654ea3", fg="white")
text_info.place(x=0, y=200,height=400,width=200)



liz_photo=ImageTk.PhotoImage(Image.open("cc.jpg"))#abrimos la imagen que ocuparemos
window_photo= Label(main_window, image=liz_photo)#diremos donde se pondra la imagen
window_photo.pack(pady=5)#ubciaremos la iamgen

#dependiendo de las voces que tengas en tu computadora
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

def charge_data(name_dict,name_file):
    try:
        with open(name_file) as f:
            for line in f:
                (key,val)=line.split(",")
                val = val.rstrip("\n")
                name_dict[key]=val
    except FileNotFoundError as e:
        pass


sites = dict()
charge_data(sites, "Pages.txt")

files = dict()
charge_data(files, "Archivos.txt")

programas = dict()
charge_data(programas, "Apps.txt")

#guardara lo que digas
def talk(text):
    engine.say(text)
    engine.runAndWait()

def read_and_talk():
    text=text_info.get("1.0","end")
    talk(text)
#escribira lo que busque en la wiki
def write_text(text_wiki):
    text_info.insert(INSERT,text_wiki)
#harea que el microfono nos escuche
def listen():
    listener = sr.Recognizer()     
    with sr.Microphone() as source:
        print("Escuchando...")
        listener.adjust_for_ambient_noise(source)
        pc = listener.listen(source)

    try:
        rec = listener.recognize_google(pc, language="es")
        rec = rec.lower()
    except sr.UnknownValueError:
        print("No te entendí, intenta de nuevo")
        if name in rec:
            rec = rec.replace(name, '')
    return rec
# reproducira lo que se menciona si
def clock(rec):
    hora = rec.replace('alarma', '')
    hora = hora.strip()
    talk("Alarma activada a las " + hora + " horas")
    if hora[0] != '0' and len(hora)<5:
        hora = '0' + hora
    print(hora)
    while True:
        if datetime.datetime.now().strftime('%H:%M') == hora:
            print("Despierta")
            mixer.init()
            mixer.music.load("despierta.mp3")
            mixer.music.play()
        else:
            continue
        if keyboard.read_key() == "S":
            mixer.music.stop()
            break
#sucede la magia dependiendo lo que digas ella hara el resto
def run_liz():
    while True:
        try:
            rec = listen()
        except UnboundLocalError:
            print("No te entendí, intenta de nuevo")
            continue   
        if 'reproduce' in rec:
            music = rec.replace('reproduce', '')
            print("Reproduciendo " + music)
            talk("Reproduciendo " + music)
            pywhatkit.playonyt(music)
        elif 'busca' in rec: #hallar solucion
            search = rec.replace('busca', '')
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 2)
            write_text(search + ": " + wiki)
            talk(wiki)
            break
        elif 'alarma' in rec:
            t = tr.Thread(target=clock, args=(rec,))
            t.start()
        elif 'detener' in rec:
            talk("Nos vemos manco culiao")
            break
        elif 'colores' in rec:
            talk("Espere un momento")
            colors.capture()
        elif 'abre' in rec:
            task=rec.replace('abre', '').strip()
            if task in sites:
                for task in sites:
                    if task in rec:
                        sub.call(f'start {sites[task]}', shell=True)
                        talk(f'Abriendo {task}')
            elif task in sites:
                for task in programas:
                    if task in rec:
                        talk(f'Abriendo {task}')
                        os.startfile(programas[task])
            else:
                talk("Lo siento no hay nada con ese nombre, si lo necesita agregalo en el apartado correcto")
        elif 'archivo' in rec:
            file=rec.replace('archivo','').strip()
            if file in files:
                for file in files:
                    if file in rec:
                        sub.Popen([files[file]], shell=True)
                        talk(f'Abriendo {file}')
            else:
                talk("Lo siento no hay nada con ese nombre, si lo necesita agregalo en el apartado correcto")
        elif 'escribe' in rec:
            try:
                with open("nota.txt", 'a') as f:
                    write(f)
            except FileNotFoundError as e:
                file = open("nota.txt", 'w')
                write(file)

#escribe en un bloc no de notas
def write(f):
    talk("Que quieres que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, puedes revisarlo")
    sub.Popen("nota.txt", shell=True)
#sirve para añadir aplicaciones, programas y cosas
def open_files_w():
    global namefiles_entry,pathf_entry
    window_files=Toplevel()
    window_files.title("Agregar archivos")
    window_files.configure(bg= "#654ea3")
    window_files.geometry("300x200")
    window_files.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(window_files)} center')

    title_label= Label(window_files, text="Agrega un archivo", bg="#654ea3", fg="white",font=('Arial',"15", 'bold'))
    title_label.pack(pady=3)

    name_label= Label(window_files, text="Nombre del archivo", bg="#654ea3", fg="white",font=('Arial',"10", 'bold'))
    name_label.pack(pady=2)

    namefiles_entry= Entry(window_files)
    namefiles_entry.pack(pady=1)

    path_label= Label(window_files, text="Ruta del archivo", bg="#654ea3", fg="white",font=('Arial',"10", 'bold'))
    path_label.pack(pady=2)

    pathf_entry= Entry(window_files,width=35)
    pathf_entry.pack(pady=1)

    save_button= Button(window_files, text="Guardar", bg="#654ea3", fg="white",width=8,height=1,command=add_files)
    save_button.pack(pady=4)



def open_apps_w():
    global nameapps_entry, patha_entry
    window_apps=Toplevel()
    window_apps.title("Agregar apps")
    window_apps.configure(bg= "#654ea3")
    window_apps.geometry("300x200")
    window_apps.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(window_apps)} center')

    title_label= Label(window_apps, text="Agrega app", bg="#654ea3", fg="white",font=('Arial',"15", 'bold'))
    title_label.pack(pady=3)

    name_label= Label(window_apps, text="Nombre de la app", bg="#654ea3", fg="white",font=('Arial',"10", 'bold'))
    name_label.pack(pady=2)

    nameapps_entry= Entry(window_apps)
    nameapps_entry.pack(pady=1)

    path_label= Label(window_apps, text="Ruta de la app", bg="#654ea3", fg="white",font=('Arial',"10", 'bold'))
    path_label.pack(pady=2)

    patha_entry= Entry(window_apps,width=35)
    patha_entry.pack(pady=1)

    save_button= Button(window_apps, text="Guardar", bg="#654ea3", fg="white",width=8,height=1,command=add_apps)
    save_button.pack(pady=4)


def open_pages_w():
    global namepages_entry,pathp_entry
    window_pages=Toplevel()
    window_pages.title("Agregar paginas")
    window_pages.configure(bg= "#654ea3")
    window_pages.geometry("300x200")
    window_pages.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(window_pages)} center')

    title_label= Label(window_pages, text="Agrega una pagina", bg="#654ea3", fg="white",font=('Arial',"15", 'bold'))
    title_label.pack(pady=3)

    name_label= Label(window_pages, text="Nombre de la pagina", bg="#654ea3", fg="white",font=('Arial',"10", 'bold'))
    name_label.pack(pady=2)

    namepages_entry= Entry(window_pages)
    namepages_entry.pack(pady=1)

    path_label= Label(window_pages, text="Ruta de la pagina", bg="#654ea3", fg="white",font=('Arial',"10", 'bold'))
    path_label.pack(pady=2)

    pathp_entry= Entry(window_pages,width=35)
    pathp_entry.pack(pady=1)

    save_button= Button(window_pages, text="Guardar", bg="#654ea3", fg="white",width=8,height=1,command=add_pages)
    save_button.pack(pady=4)

def add_files():
    name_file = namefiles_entry.get().strip()
    path_file=pathf_entry.get().strip()
    files[name_file]=path_file
    save_data(name_file,path_file, "Archivos.txt")
    namefile_entry.delete(0,"end")
    pathf_entry.delete(0,"end")
def add_apps():
    name_file = nameapps_entry.get().strip()
    path_file=patha_entry.get().strip()
    programas[name_file]=path_file
    save_data(name_file,path_file, "Apps.txt")
    nameapps_entry.delete(0,"end")
    patha_entry.delete(0,"end")
def add_pages():
    name_page = namepages_entry.get().strip()
    url_pages=pathp_entry.get().strip()
    sites[name_page]=url_pages
    save_data(name_page,url_pages, "Pages.txt")
    namepages_entry.delete(0,"end")
    pathp_entry.delete(0,"end")

def save_data(key,value,file_name):
    try:
        with open(file_name, 'a') as f:
            f.write(key+ "," + value + "\n")
    except FileNotFoundError as f:
        file = open(file_name, "a")
        file.write(key+ "," + value + "\n")
            




button_voice_mx=Button(main_window, text="Voz mexicana", fg="white", bg="#348F50", font=("Arial",10,"bold"),command=mexican_voice)
button_voice_mx.place(x=625,y=90,width=100,height=30)
button_voice_es=Button(main_window, text="Voz española", fg="white", bg="#b92b27", font=("Arial",10,"bold"),command=spanish_voice)
button_voice_es.place(x=625,y=130,width=100,height=30)
button_voice_al=Button(main_window, text="Voz alemana", fg="white", bg="#f4791f", font=("Arial",10,"bold"),command=german_voice)
button_voice_al.place(x=625,y=170,width=100,height=30)
button_listen=Button(main_window, text="Escuchar", fg="white", bg="#c31432", font=("Arial",10,"bold"),width=10,height=4,command=run_liz)
button_listen.pack(pady=10)
button_speak=Button(main_window, text="Hablar", fg="white", bg="#654ea3", font=("Arial",10,"bold"),width=10,height=4,command=read_and_talk)
button_speak.place(x=625,y=210,width=100,height=30)
button_add_files=Button(main_window, text="Agregar archivos", fg="white", bg="#654ea3", font=("Arial",10,"bold"),width=10,height=4,command=open_files_w)
button_add_files.place(x=615,y=250,width=120,height=30)
button_add_apps=Button(main_window, text="Agregar aplicaciones", fg="white", bg="#654ea3", font=("Arial",10,"bold"),width=10,height=4,command=open_apps_w)
button_add_apps.place(x=615,y=290,width=150,height=30)
button_add_pages=Button(main_window, text="Agregar paginas", fg="white", bg="#654ea3", font=("Arial",10,"bold"),width=10,height=4,command=open_pages_w)
button_add_pages.place(x=615,y=330,width=120,height=30)



main_window.mainloop()
