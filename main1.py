import serial  # Serial imported for Serial communication
import time  # Required to use delay functions
import pyautogui
import ctypes

ArduinoSerial = serial.Serial('com4', 9600)  # Create Serial port object called arduinoSerialData
time.sleep(2)  # wait for 2 seconds for the communication to get established

while 1:

    incoming = str(ArduinoSerial.readline())  # read the serial data and print it as line
    print(incoming)

    if 'down' in incoming:
        pyautogui.move(0, 20)

    if 'high' in incoming:
        pyautogui.move(0, -20)

    if 'left' in incoming:
        pyautogui.move(-20, 0)

    if 'right' in incoming:
        pyautogui.move(20, 0)

    if 'click' in incoming:
        pyautogui.click()

    if 'center' in incoming:
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0)
        screensize_1 = user32.GetSystemMetrics(1)
        center_x = screensize / 2
        center_y = screensize_1 / 2
        pyautogui.moveTo(center_x, center_y)

        # 2 датчик
    if 'Play/Pause' in incoming:
        pyautogui.typewrite(['space'], 0.2)

    if 'Vdown' in incoming:
        pyautogui.press('volumedown')

    if 'Vup' in incoming:
        pyautogui.press('volumeup')

    if 'language' in incoming:
        pyautogui.hotkey('shift', 'alt')

    if 'Rewind' in incoming:
        pyautogui.hotkey('left')

    if 'Forward' in incoming:
        pyautogui.hotkey('right')

    if 'Win+d' in incoming:
        pyautogui.hotkey('win', 'd')

    if 'ctrl+z' in incoming:
        pyautogui.hotkey('ctrl', 'z')

    if 'click_r' in incoming:
        pyautogui.rightClick()

    if 'Sdown' in incoming:
        pyautogui.scroll(-40)

    if 'Sup' in incoming:
        pyautogui.scroll(40)

    if 'ctrl+alt+delete' in incoming:
        pyautogui.hotkey('ctrl', 'shift', 'esc')
