import keyboard
import pyautogui

def getMainWindow():
    return pyautogui.getInfo()[3]

def generate_events():
    while True:
        yield keyboard.read_event()

def getLigne():
    strings = keyboard.get_typed_strings(generate_events())
    return next(strings)

def getWrotedText():
    text = ""
    while not "--" in text:
        text += getLigne()
        text += "\n"
    text = f"{getMainWindow()} - {text[:-3]}"
    return text

while True:
    print(getWrotedText())
