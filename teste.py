import pyautogui
print(pyautogui.KEYBOARD_KEYS)
# Lista todos os títulos das janelas abertas
for window in pyautogui.getAllTitles():
    print(window)