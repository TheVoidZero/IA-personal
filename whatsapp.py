import webbrowser
import pyautogui as activada
import time

def send_message(contact, message):
    webbrowser.open(f"https://web.whatsapp.com/send?phone={contact}&text={message}")
    time.sleep(100)
    at.press('enter')