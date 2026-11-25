# Yunuz's AutoTyper

A small Python desktop utility for typing text into the focused application. It includes a Tkinter interface, start and stop hotkeys, saved presets, a system-tray menu, and an optional helper that encrypts the Python source file.

## Features

- Type entered text with a configurable delay
- Save and reload a text and delay preset
- Start with `Ctrl + Alt + T` and stop with `Ctrl + Alt + S`
- Minimize to the system tray
- Optionally encrypt the source file using a user-provided Fernet key

## Run locally

Requirements: Python 3 and the packages below. Tkinter must also be available in your Python installation.

```bash
git clone https://github.com/itsyunus/AutoTyper.git
cd AutoTyper
python -m pip install pyautogui pynput pystray pillow cryptography
python autotyper.py
```

## Optional source encryption

The encryption helper reads a key from the `AUTOTYPER_FERNET_KEY` environment variable. Generate a key locally with:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Set the generated value in your local environment before using the **Encrypt Code** button. Keep it out of source control. This helper encrypts a copy of the source file; it is not a substitute for protecting credentials or distributing a secure application.

## Build

Install PyInstaller, then run:

```bash
python -m pip install pyinstaller
pyinstaller autotyper.spec
```

The generated application is placed in PyInstaller's output directory.
