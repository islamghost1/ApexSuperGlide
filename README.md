# Apex super glide :99%  success rate

Sure, here's a README for your script:

# Keyboard and Mouse Listener

This script sets up listeners for both keyboard and mouse events. It uses the `pynput` library to monitor and control input devices.

## Features

- **Keyboard Listener**: Detects when the 'SPACE BAR' and 'ESC' keys are pressed.
- **Mouse Listener**: Detects when the mouse wheel is scrolled.
- **Key Simulation**: Simulates the pressing of the 'SPACE BAR' and 'c' keys when the mouse wheel is scrolled.

## How it works

1. The script starts by setting up listeners for both the keyboard and mouse.
2. The keyboard listener detects when the 'SPACE BAR' and 'ESC' keys are pressed. If the 'SPACE BAR' is pressed, it sets a flag (`space_pressed`) to True. If the 'ESC' key is pressed, it stops the listeners and ends the program.
3. The mouse listener detects when the mouse wheel is scrolled. If the wheel is scrolled down, it simulates the pressing of the 'SPACE BAR' and 'c' keys, then sets the `space_pressed` flag back to False.
4. The script runs in a loop, continuously listening for keyboard and mouse events until the 'ESC' key is pressed.

## Usage

To run the script, simply execute it in a Python environment where the `pynput` library is installed. The script will start listening for keyboard and mouse events.

## Dependencies

- Python
- pynput library

Please note that this script uses the `pynput` library, which may not work in some environments due to restrictions on controlling input devices. Always use scripts that control input devices responsibly.
