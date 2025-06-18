import tkinter as tk
from tkinter import messagebox, filedialog
import pyautogui
import threading
import time
from pynput import keyboard
from pystray import Icon, MenuItem, Menu
from PIL import Image
import json
import os
from cryptography.fernet import Fernet

# === Configuration ===
APP_NAME = "Yunuz's AutoTyper"
PRESET_FILE = "src/presets.json"
ENCRYPTION_KEY = b'ZmRoZXdvcmxkeXVudXp9ZmRoZXdvcmxkeXVudXp9ZA=='  # 'ftheworldyunuz' padded to 32 bytes and base64-encoded
ENCRYPTED_FILE = "src/encrypted.py"

# === Global Variables ===
running = False
hotkey_listener = None

# === Auto Typer Logic ===
def start_typing(text, delay):
    global running
    running = True
    time.sleep(2)  # 2 seconds delay before starting
    while running:
        pyautogui.typewrite(text)
        time.sleep(delay)

def stop_typing():
    global running
    running = False

# === Encryption Utility ===
def encrypt_code():
    try:
        cipher = Fernet(ENCRYPTION_KEY)
        with open(__file__, 'rb') as f:
            data = f.read()
        encrypted = cipher.encrypt(data)
        with open(ENCRYPTED_FILE, 'wb') as f:
            f.write(encrypted)
        messagebox.showinfo("Encrypted", f"Code encrypted to {ENCRYPTED_FILE}")
    except Exception as e:
        messagebox.showerror("Encryption Error", str(e))

# === GUI ===
class AutoTyperApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)

        tk.Label(root, text="Text to Type:").pack()
        self.text_entry = tk.Text(root, height=5, width=40)
        self.text_entry.pack()

        tk.Label(root, text="Typing Delay (seconds):").pack()
        self.delay_entry = tk.Entry(root)
        self.delay_entry.insert(0, "1")
        self.delay_entry.pack()

        tk.Button(root, text="Start", command=self.start_typing_thread).pack(pady=5)
        tk.Button(root, text="Stop", command=stop_typing).pack(pady=5)
        tk.Button(root, text="Save Preset", command=self.save_preset).pack()
        tk.Button(root, text="Load Preset", command=self.load_preset).pack()
        tk.Button(root, text="Encrypt Code", command=encrypt_code).pack(pady=5)

        # Minimize to tray
        self.root.protocol("WM_DELETE_WINDOW", self.minimize_to_tray)

        self.register_hotkeys()

    def start_typing_thread(self):
        try:
            text = self.text_entry.get("1.0", tk.END).strip()
            delay = float(self.delay_entry.get())
            threading.Thread(target=start_typing, args=(text, delay), daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def save_preset(self):
        preset_data = {
            "text": self.text_entry.get("1.0", tk.END),
            "delay": self.delay_entry.get()
        }
        with open(PRESET_FILE, "w") as f:
            json.dump(preset_data, f)
        messagebox.showinfo("Saved", "Preset saved successfully.")

    def load_preset(self):
        try:
            with open(PRESET_FILE, "r") as f:
                preset_data = json.load(f)
                self.text_entry.delete("1.0", tk.END)
                self.text_entry.insert(tk.END, preset_data["text"])
                self.delay_entry.delete(0, tk.END)
                self.delay_entry.insert(0, preset_data["delay"])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def minimize_to_tray(self):
        self.root.withdraw()
        menu = Menu(MenuItem('Show', self.restore), MenuItem('Exit', self.exit_app))
        self.icon = Icon(APP_NAME, menu=menu)
        threading.Thread(target=self.icon.run).start()

    def restore(self):
        self.root.deiconify()
        self.icon.stop()

    def exit_app(self):
        self.icon.stop()
        self.root.quit()

    def register_hotkeys(self):
        def on_press(key):
            try:
                if key.ctrl and key.alt and key.char == 't':
                    self.start_typing_thread()
                elif key.ctrl and key.alt and key.char == 's':
                    stop_typing()
            except AttributeError:
                pass

        global hotkey_listener
        hotkey_listener = keyboard.Listener(on_press=on_press)
        hotkey_listener.start()

# === Main ===
def run_ui():
    root = tk.Tk()
    app = AutoTyperApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_ui()
