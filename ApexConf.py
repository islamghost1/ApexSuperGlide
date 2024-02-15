import time
from pynput import keyboard, mouse
from pynput.keyboard import Controller, Key

def run_in_thread():
    # This boolean variable will control the execution of the listeners
    running = True

    # This boolean variable will track if the 'SPACE BAR' has been pressed
    space_pressed = False

    # This will simulate keyboard events
    keyboard_controller = Controller()

    def on_press(key):
        nonlocal running, space_pressed
        if key == keyboard.Key.space:
            space_pressed = True
        elif key == keyboard.Key.esc:
            print('ESC pressed, stopping...')
            running = False  # Stop the listeners

    def on_scroll(x, y, dx, dy):
        nonlocal space_pressed
        if dy < 0 :#and space_pressed:
           # Simulate SPACE BAR click
            keyboard_controller.press(Key.space)
            time.sleep(0.0069)
            
            # c c  cctime.sleep(0.1)
            keyboard_controller.press('c')
            keyboard_controller.release(Key.space)
            keyboard_controller.release('c')
            
            space_pressed = False  

    # Setup the listener for the keyboard
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()

    # Setup the listener for the mouse
    mouse_listener = mouse.Listener(on_scroll=on_scroll)
    mouse_listener.start()

    # Keep the program running.
    while running:   
        time.sleep(0.00000000000000000000001)# Add a small sleep to reduce CPU usage
        continue

    # Once running becomes False, stop the listeners
    keyboard_listener.stop()
    mouse_listener.stop()


# thread that runs the function
run_in_thread()
