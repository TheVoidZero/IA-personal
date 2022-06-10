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
import whatsapp as whapp

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

contacts = dict()
charge_data(contacts, "Contactos.txt")
###########################################################################################################################
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
        listener.adjust_for_ambient_noise(source)
        talk("Te escucho señor")
        pc = listener.listen(source)
    try:
        rec = listener.recognize_google(pc, language="es")
        rec = rec.lower()
    except sr.UnknownValueError:
        print("No te entendí, intenta de nuevo")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return rec
###################################################################################################################
def reproduce(rec):
    music = rec.replace('reproduce', '')
    print("Reproduciendo " + music)
    talk("Reproduciendo " + music)
    pywhatkit.playonyt(music)
def busca(rec):
    search = rec.replace('busca', '')
    wikipedia.set_lang("es")
    wiki = wikipedia.summary(search, 2)
    write_text(search + ": " + wiki)
    talk(wiki)
def thread_alarma(rec):
    t = tr.Thread(target=clock, args=(rec,))
    t.start()
def colores(rec):
    talk("Espere un momento")
    colors.capture()
def abre(rec):
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
def archivo(rec):
    file=rec.replace('archivo','').strip()
    if file in files:
        for file in files:
            if file in rec:
                sub.Popen([files[file]], shell=True)
                talk(f'Abriendo {file}')
    else:
            talk("Lo siento no hay nada con ese nombre, si lo necesita agregalo en el apartado correcto")
def escribe(rec):
    try:
        with open("nota.txt", 'a') as f:
            write(f)
    except FileNotFoundError as e:
        file = open("nota.txt", 'w')
        write(file)
def enviar_mensaje(rec):
    talk("A quien queires enviar el mensaje")
    contact=listen()
    contact=contact.strip()
    if contact in contacts:
        for cont in contacts:
            if cont == contact:
                contact = contacts[cont]
                talk("que mensaje quieres enviar")
                message=listen()
                talk("Enviando mensaje")
                whapp.send_message(contact,message)
    else:
        talk("No has agregado ningun contacto")
###################################################################################################################
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
#########################################################################################################################################
key_words={
    'reproduce' : reproduce,
    'busca' : busca,
    'alarma' : thread_alarma, 
    'colores' : colores,
    'abre' : abre,
    'archivo' : archivo,
    'escribe' : escribe,
    'mensaje' : enviar_mensaje
}
#########################################################################################################################################
#sucede la magia dependiendo lo que digas ella hara el resto
def run_liz():
    while True:
        try:
            rec = listen()
        except UnboundLocalError:
            talk("No te entendi, intetna de nuevo")
            continue
        rec = listen()
        if 'busca' in rec:
            key_words['busca'](rec)
            break
        else:
            for word in key_words:
                if word in rec:
                    key_words[word](rec)
        if 'detener' in rec:
            talk("Nos vemos manco culiao")
            break
    main_window.update()
        
####################################################################################################################
#escribe en un bloc no de notas
def write(f):
    talk("Que quieres que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, puedes revisarlo")
    sub.Popen("nota.txt", shell=True)
    ##################################################################################################################
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
def open_contacts_w():
    global namecontact_entry,phone_entry
    window_contacts=Toplevel()
    window_contacts.title("Agregar contacto")
    window_contacts.configure(bg= "#654ea3")
    window_contacts.geometry("300x200")
    window_contacts.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(window_contacts)} center')

    title_label= Label(window_contacts, text="Agrega un contacto", bg="#654ea3", fg="white",font=('Arial',"15", 'bold'))
    title_label.pack(pady=3)

    name_label= Label(window_contacts, text="Nombre del contacto", bg="#654ea3", fg="white",font=('Arial',"10", 'bold'))
    name_label.pack(pady=2)

    namecontact_entry= Entry(window_contacts)
    namecontact_entry.pack(pady=1)

    path_label= Label(window_contacts, text="Ruta del archivo", bg="#654ea3", fg="white",font=('Arial',"10", 'bold'))
    path_label.pack(pady=2)

    phone_entry= Entry(window_contacts,width=35)
    phone_entry.pack(pady=1)

    save_button= Button(window_contacts, text="Guardar", bg="#654ea3", fg="white",width=8,height=1,command=add_contacts)
    save_button.pack(pady=4)


#######################################################################################
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
def add_contacts():
    name_contact = namecontact_entry.get().strip()
    phone=phone_entry.get().strip()
    contacts[name_contact]=phone
    save_data(name_contact,phone, "Contactos.txt")
    namecontact_entry.delete(0,"end")
    phone_entry.delete(0,"end")

def save_data(key,value,file_name):
    try:
        with open(file_name, 'a') as f:
            f.write(key+ "," + value + "\n")
    except FileNotFoundError as f:
        file = open(file_name, "a")
        file.write(key+ "," + value + "\n")
            
######################################################################################################################################

def talk_pages():
    if bool(sites) == True:
        talk("Has agregado las siguientes paginas")
        for site in sites:
            talk(site)
    else:
        talk("No has agregado paginas web") 
def talk_apps():
    if bool(programas) == True:
        talk("Has agregado las siguientes aplicaciones")
        for app in programas:
            talk(app)
    else:
        talk("No has agregado aplicaciones") 
def talk_files():
    if bool(files) == True:
        talk("Has agregado los siguientes archivos")
        for file in files:
            talk(file)
    else:
        talk("No has agregado archivos") 
def talk_contacts():
    if bool(contacts) == True:
        talk("Has agregado los siguientes contactos")
        for cont in contacts:
            talk(cont)
    else:
        talk("No has agregado contactos") 
##################################################################################################################################
def give_me_name():
    talk("Hola cual es tu nombre")
    name=listen()
    name=name.strip()
    talk(f"Bienvenido {name}")

    try:
        with open("Name.txt",'w') as f:
            f.write(name)
    except FileNotFoundError:
        file = open("Name.txt", 'w')
        file.write(name)

def say_hello():
        if os.path.exists("Name.txt"):
            with open("Name.txt") as f:
                for name in f:
                    talk(f"Hola bienvenido, {name}")
        else:
            give_me_name()

def thread_hello():
    t=tr.Thread(target=say_hello)
    t.start()

thread_hello()
##################################################################################################################################
button_voice_mx=Button(main_window, text="Voz mexicana", fg="white", bg="#348F50", font=("Arial",10,"bold"),command=mexican_voice)
button_voice_mx.place(x=625,y=90,width=100,height=30)
button_voice_es=Button(main_window, text="Voz española", fg="white", bg="#b92b27", font=("Arial",10,"bold"),command=spanish_voice)
button_voice_es.place(x=625,y=130,width=100,height=30)
button_voice_al=Button(main_window, text="Voz alemana", fg="white", bg="#f4791f", font=("Arial",10,"bold"),command=german_voice)
button_voice_al.place(x=625,y=170,width=100,height=30)

button_listen=Button(main_window, text="Escuchar", fg="white", bg="#c31432", font=("Arial",10,"bold"),width=10,height=4,command=run_liz)
button_listen.pack(side=BOTTOM, pady=10)

button_speak=Button(main_window, text="Hablar", fg="white", bg="#654ea3", font=("Arial",10,"bold"),width=10,height=4,command=read_and_talk)
button_speak.place(x=625,y=210,width=100,height=30)


button_add_files=Button(main_window, text="Agregar archivos", fg="white", bg="#654ea3", font=("Arial",10,"bold"),width=10,height=4,command=open_files_w)
button_add_files.place(x=615,y=250,width=120,height=30)
button_add_apps=Button(main_window, text="Agregar aplicaciones", fg="white", bg="#654ea3", font=("Arial",10,"bold"),width=10,height=4,command=open_apps_w)
button_add_apps.place(x=615,y=290,width=150,height=30)
button_add_pages=Button(main_window, text="Agregar paginas", fg="white", bg="#654ea3", font=("Arial",10,"bold"),width=10,height=4,command=open_pages_w)
button_add_pages.place(x=615,y=330,width=120,height=30)
button_add_contacts=Button(main_window, text="Agregar contactos", fg="white", bg="#654ea3", font=("Arial",10,"bold"),width=10,height=4,command=open_contacts_w)
button_add_contacts.place(x=615,y=370,width=120,height=30)


button_tell_files=Button(main_window, text="Archivos agregadas", fg="white", bg="#2c3e50", font=("Arial",10,"bold"),width=10,height=4,command=talk_files)
button_tell_files.place(x=210,y=400,width=130,height=30)
button_tell_app=Button(main_window, text="Apps agregadas", fg="white", bg="#2c3e50", font=("Arial",10,"bold"),width=10,height=4,command=talk_apps)
button_tell_app.place(x=500,y=400,width=130,height=30)
button_tell_pages=Button(main_window, text="Paginas agregadas", fg="white", bg="#2c3e50", font=("Arial",10,"bold"),width=10,height=4,command=talk_pages)
button_tell_pages.place(x=355,y=400,width=130,height=30)
button_tell_contacts=Button(main_window, text="Contactos agregadas", fg="white", bg="#2c3e50", font=("Arial",10,"bold"),width=10,height=4,command=talk_contacts)
button_tell_contacts.place(x=210,y=450,width=130,height=30)



main_window.mainloop()
