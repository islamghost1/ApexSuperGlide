import time
from pynput import keyboard, mouse
from pynput.keyboard import Controller, Key , KeyCode
import json
from welcome import langingPage
from welcome import  style


with open('./keyBoardConfig.json') as f:
  keys_dict = json.load(f)

#read json config
def readKeyBoardConfig():
    global start_the_cycle, jump, crouch, stop_the_program

    def get_key_code(key):
        if len(key) == 1:
            return KeyCode.from_char(key)
        else:
            try:
                return getattr(Key, key)
            except AttributeError:
                raise ValueError(f"Invalid key name: {key}")

    start_the_cycle = get_key_code(keys_dict["start_the_cycle"])
    jump = get_key_code(keys_dict["jump"])
    crouch = get_key_code(keys_dict["crouch"])
    stop_the_program = get_key_code(keys_dict["stop_the_program"])


    print(style.YELLOW+"your config :\n start_the_cycle : {0} ,\n jump : {1} ,\n crouch : {2} ,\n stop_the_program : {3}".format(start_the_cycle, jump, crouch, stop_the_program))



def run_in_thread():
    # This boolean variable will control the execution of the listeners
    running = True

    # This boolean variable will track if the 'SPACE BAR' has been pressed
    space_pressed = False

    # This will simulate keyboard events
    keyboard_controller = Controller()

    def on_press(key):
        nonlocal running, space_pressed
         
        if key == start_the_cycle:
            space_pressed = True
        elif key == stop_the_program:
            print('{0} pressed, stopping...'.format(stop_the_program))
            running = False  # Stop the listeners

    def on_scroll(x, y, dx, dy):
        nonlocal space_pressed
        if dy < 0 and space_pressed:
           # Simulate SPACE BAR click  
            keyboard_controller.press(jump)
            time.sleep(0.0069)
            keyboard_controller.release(jump)        

            keyboard_controller.press(crouch)
            keyboard_controller.release(crouch)
            
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

#langing page 
langingPage()
# get config
readKeyBoardConfig()
# thread that runs the function
run_in_thread()


