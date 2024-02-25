import time
from pynput import keyboard, mouse
from pynput.keyboard import Controller, Key, KeyCode
import json
from welcome import langingPage
from welcome import style

with open('./keyBoardConfig.json') as f:
    keys_dict = json.load(f)

# read json config
def readKeyBoardConfig():
    global climbe_an_object, perfrom_the_super_Glide, in_game_jump, in_game_crouch, stop_the_program

    def get_key_code(key):
        if len(key) == 1:
            return KeyCode.from_char(key)
        else:
            try:
                return getattr(Key, key)
            except AttributeError:
                return key  # If not a known key, assume it's a mouse event

    climbe_an_object = get_key_code(keys_dict["climbe_an_object"])
    perfrom_the_super_Glide = get_key_code(keys_dict["perfrom_the_super_Glide"])
    in_game_jump = get_key_code(keys_dict["in_game_jump"])
    in_game_crouch = get_key_code(keys_dict["in_game_crouch"])
    stop_the_program = get_key_code(keys_dict["stop_the_program"])

    print(style.YELLOW + "your config :\n climbe_an_object : {0} ,\n perfrom_the_super_Glide : {1} ,\n in_game_jump : {2} ,\n in_game_crouch : {3} ,\n stop_the_program : {4}"
          .format(climbe_an_object, perfrom_the_super_Glide, in_game_jump, in_game_crouch, stop_the_program))


def run_in_thread():
    # This boolean variable will control the execution of the listeners
    running = True

    # This boolean variable will track if the 'SPACE BAR' has been pressed
    space_pressed = False

    # This will simulate keyboard events
    keyboard_controller = Controller()

    def on_press(key):
        nonlocal running, space_pressed

        if key == climbe_an_object:
            space_pressed = True
        elif key == stop_the_program:
            print('{0} pressed, stopping...'.format(stop_the_program))
            running = False  # Stop the listeners
        if space_pressed and key == perfrom_the_super_Glide:
            super_glide()

    def on_scroll(x, y, dx, dy):
        nonlocal space_pressed

        if perfrom_the_super_Glide == "scroll_up" and dy > 0 and space_pressed:
            super_glide()
        elif perfrom_the_super_Glide == "scroll_down" and dy < 0 and space_pressed:
            super_glide()


    def super_glide():
        nonlocal space_pressed
        # Simulate jump and crouch
        keyboard_controller.press(in_game_jump)
        time.sleep(0.0069)
        keyboard_controller.release(in_game_jump)

        keyboard_controller.press(in_game_crouch)
        keyboard_controller.release(in_game_crouch)

        space_pressed = False

    # Setup the listener for the keyboard
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()

    # Setup the listener for the mouse
    mouse_listener = mouse.Listener(on_scroll=on_scroll)
    mouse_listener.start()

    # Keep the program running.
    while running:
        time.sleep(0.00000000000000000000001)  # Add a small sleep to reduce CPU usage
        continue

    # Once running becomes False, stop the listeners
    keyboard_listener.stop()
    mouse_listener.stop()

# langing page
langingPage()
# get config
readKeyBoardConfig()
# thread that runs the function
run_in_thread()
