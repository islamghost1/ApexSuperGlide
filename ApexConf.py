import time
from pynput import keyboard, mouse
from pynput.keyboard import Controller as KeyboardController, Key, KeyCode
from pynput.mouse import Controller as MouseController, Button
import json
import os
import threading
from welcome import landingPage
from welcome import style

# Global variables
keys_dict = {}
start_cycle = None
perfrom_the_super_Glide = None
in_game_jump = None
in_game_crouch = None
stop_the_program = None
show_menu = None
running = True
in_menu = False
keyboard_listener = None
mouse_listener = None
current_config_key = None
new_key_value = ""
editing_config = False
key_list = ["start_cycle", "perfrom_the_super_Glide", "in_game_jump", "in_game_crouch", "stop_the_program"]
current_key_index = 0
waiting_for_input = False
mouse_button_pressed = None
mouse_scroll_direction = None

# Load config
def load_config():
    global keys_dict
    try:
        with open('./keyBoardConfig.json') as f:
            keys_dict = json.load(f)
    except FileNotFoundError:
        # Default config if file doesn't exist
        keys_dict = {
            "start_cycle": "space",
            "perfrom_the_super_Glide": "scroll_down",
            "in_game_jump": "space",
            "in_game_crouch": "c",
            "stop_the_program": "f12"
        }
        save_config()

# Save config to file
def save_config():
    with open('./keyBoardConfig.json', 'w') as f:
        json.dump(keys_dict, f, indent=4)

# Convert key string to KeyCode object
def get_key_code(key):
    if key in ["scroll_up", "scroll_down", "button_left", "button_right", "button_middle"]:
        return key
    elif len(key) == 1:
        return KeyCode.from_char(key)
    else:
        try:
            return getattr(Key, key)
        except AttributeError:
            return key

# Read and apply keyboard config
def readKeyBoardConfig():
    global start_cycle, perfrom_the_super_Glide, in_game_jump, in_game_crouch, stop_the_program, show_menu
    
    load_config()
    
    start_cycle = get_key_code(keys_dict["start_cycle"])
    perfrom_the_super_Glide = get_key_code(keys_dict["perfrom_the_super_Glide"])
    in_game_jump = get_key_code(keys_dict["in_game_jump"])
    in_game_crouch = get_key_code(keys_dict["in_game_crouch"])
    stop_the_program = get_key_code(keys_dict["stop_the_program"])
    show_menu = Key.f11  # F11 is hardcoded for menu functionality
    
    print(style.YELLOW + "Your config:\n start_cycle: {0}\n perfrom_the_super_Glide: {1}\n in_game_jump: {2}\n in_game_crouch: {3}\n stop_the_program: {4}"
          .format(keys_dict["start_cycle"], keys_dict["perfrom_the_super_Glide"], keys_dict["in_game_jump"], keys_dict["in_game_crouch"], keys_dict["stop_the_program"]))

# Clear terminal screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Display menu
def display_menu():
    clear_screen()
    print(style.CYAN + """
    ╔══════════════════════════════╗
    ║           MENU               ║
    ╠══════════════════════════════╣
    ║ 1) Edit Config               ║
    ║ 2) Return to Main View       ║
    ╚══════════════════════════════╝
    """ + style.RESET)
    print("Press 1 or 2 to select an option (ESC to exit):")

# Create a dynamic width box based on content
def create_dynamic_box(title, content_lines):
    # Find the longest line to determine box width
    max_length = max(len(title), max(len(line) for line in content_lines))
    box_width = max_length + 8  # Add padding
    
    # Create the box
    box_top = "╔" + "═" * box_width + "╗"
    title_line = "║" + title.center(box_width) + "║"
    separator = "╠" + "═" * box_width + "╣"
    box_bottom = "╚" + "═" * box_width + "╝"
    
    # Create content lines
    formatted_content = []
    for line in content_lines:
        formatted_content.append("║" + line.ljust(box_width) + "║")
    
    # Combine all parts
    box = [box_top, title_line, separator] + formatted_content + [box_bottom]
    return "\n".join(box)

# Display edit config screen
def display_edit_config(key_name):
    clear_screen()
    
    content_lines = [
        f"  Current setting for {style.YELLOW}{key_name}{style.RESET}: {style.GREEN}{keys_dict[key_name]}{style.RESET}",
        "",
        f"  * Press the {style.YELLOW}key{style.RESET} you want to use for this action.",
        f"  * For {style.YELLOW}mouse buttons{style.RESET}: click left/right/middle mouse button",
        f"  * For {style.YELLOW}scroll{style.RESET}: use mouse wheel up/down",
        f"  * Press {style.YELLOW}Backspace{style.RESET} to clear",
        f"  * Press {style.YELLOW}Enter{style.RESET} to confirm",
        f"  * Press {style.YELLOW}ESC{style.RESET} to cancel and return to menu"
    ]
    
    if new_key_value:
        content_lines.append("")
        content_lines.append(f"  New value: {style.GREEN}{new_key_value}{style.RESET}")
    
    box = create_dynamic_box("EDIT CONFIG", content_lines)
    print(style.CYAN + box + style.RESET)

# Function to get key name as string
def get_key_name(key):
    try:
        # Handle special keys
        if hasattr(key, 'char') and key.char:
            return key.char
        elif key == Key.space:
            return "space"
        elif key == Key.ctrl:
            return "ctrl"
        elif key == Key.ctrl_l:
            return "ctrl_l"
        elif key == Key.ctrl_r:
            return "ctrl_r"
        elif key == Key.shift:
            return "shift"
        elif key == Key.shift_l:
            return "shift_l"
        elif key == Key.shift_r:
            return "shift_r"
        elif key == Key.alt:
            return "alt"
        elif key == Key.alt_l:
            return "alt_l"
        elif key == Key.alt_r:
            return "alt_r"
        elif key == Key.tab:
            return "tab"
        elif key == Key.backspace:
            return "backspace"
        elif key == Key.enter:
            return "enter"
        elif key == Key.esc:
            return "esc"
        elif key == Key.f1:
            return "f1"
        elif key == Key.f2:
            return "f2"
        elif key == Key.f3:
            return "f3"
        elif key == Key.f4:
            return "f4"
        elif key == Key.f5:
            return "f5"
        elif key == Key.f6:
            return "f6"
        elif key == Key.f7:
            return "f7"
        elif key == Key.f8:
            return "f8"
        elif key == Key.f9:
            return "f9"
        elif key == Key.f10:
            return "f10"
        elif key == Key.f11:
            return "f11"
        elif key == Key.f12:
            return "f12"
        else:
            # Try to get string representation
            return str(key).replace("Key.", "")
    except:
        # Default fallback
        return str(key).replace("Key.", "")

# Function to handle mouse button events when editing config
def on_click(x, y, button, pressed):
    global mouse_button_pressed, waiting_for_input, new_key_value
    
    if not editing_config or not waiting_for_input:
        return
    
    if pressed:
        if button == Button.left:
            mouse_button_pressed = "button_left"
            new_key_value = "button_left"
        elif button == Button.right:
            mouse_button_pressed = "button_right"
            new_key_value = "button_right"
        elif button == Button.middle:
            mouse_button_pressed = "button_middle"
            new_key_value = "button_middle"
        
        # Update display
        if new_key_value:
            display_edit_config(current_config_key)

# Function to handle mouse scroll events when editing config
def on_scroll_config(x, y, dx, dy):
    global mouse_scroll_direction, waiting_for_input, new_key_value
    
    if not editing_config or not waiting_for_input:
        return
    
    if dy > 0:
        mouse_scroll_direction = "scroll_up"
        new_key_value = "scroll_up"
    elif dy < 0:
        mouse_scroll_direction = "scroll_down"
        new_key_value = "scroll_down"
    
    # Update display
    if new_key_value:
        display_edit_config(current_config_key)

# Setup the menu listeners
def setup_menu_listeners():
    global keyboard_listener, mouse_listener
    
    # Stop existing listeners
    if keyboard_listener:
        keyboard_listener.stop()
    if mouse_listener:
        mouse_listener.stop()
    
    # Create new listeners for menu
    keyboard_listener = keyboard.Listener(on_press=on_press_menu)
    mouse_listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll_config)
    
    keyboard_listener.start()
    mouse_listener.start()

# Setup the main game listeners
def setup_game_listeners():
    global keyboard_listener, mouse_listener
    
    # Stop existing listeners
    if keyboard_listener:
        keyboard_listener.stop()
    if mouse_listener:
        mouse_listener.stop()
    
    # Create new listeners for the game
    keyboard_listener = keyboard.Listener(on_press=on_press_game)
    mouse_listener = mouse.Listener(on_scroll=on_scroll_game)
    
    keyboard_listener.start()
    mouse_listener.start()

# Keyboard handler for menu mode
def on_press_menu(key):
    global in_menu, editing_config, current_config_key, new_key_value, current_key_index, waiting_for_input
    
    # Check if the key is a numpad key
    is_numpad_1 = False
    is_numpad_2 = False
    
    # Handle numpad keys - checking both vk codes and direct string representations
    if hasattr(key, 'vk') and key.vk == 97:  # Numpad 1 on some systems
        is_numpad_1 = True
    elif str(key) == "<96+1>" or str(key) == "<97>":  # Numpad 1 representation
        is_numpad_1 = True
    
    if hasattr(key, 'vk') and key.vk == 98:  # Numpad 2 on some systems
        is_numpad_2 = True
    elif str(key) == "<96+2>" or str(key) == "<98>":  # Numpad 2 representation
        is_numpad_2 = True
    
    if editing_config:
        # In edit config mode
        if key == Key.enter:
            # Save current key and move to next
            if new_key_value:
                keys_dict[current_config_key] = new_key_value
            
            current_key_index += 1
            if current_key_index >= len(key_list):
                # Finished editing all keys
                save_config()
                editing_config = False
                in_menu = True
                waiting_for_input = False
                new_key_value = ""
                current_key_index = 0
                display_menu()
                readKeyBoardConfig()  # Reload config to apply changes
            else:
                # Move to next key
                current_config_key = key_list[current_key_index]
                new_key_value = ""
                waiting_for_input = True
                display_edit_config(current_config_key)
            
        elif key == Key.backspace:
            # Clear current input
            new_key_value = ""
            display_edit_config(current_config_key)
        
        elif key == Key.esc:
            # Cancel editing
            editing_config = False
            in_menu = True
            waiting_for_input = False
            new_key_value = ""
            current_key_index = 0
            display_menu()
        
        else:
            # Record the key
            key_name = get_key_name(key)
            if key_name not in ["enter", "backspace", "esc"]:
                new_key_value = key_name
                display_edit_config(current_config_key)
    
    else:
        # Main menu mode
        if key == KeyCode.from_char('1') or is_numpad_1:
            # Enter edit config mode
            editing_config = True
            current_key_index = 0
            current_config_key = key_list[current_key_index]
            new_key_value = ""
            waiting_for_input = True
            display_edit_config(current_config_key)
        
        elif key == KeyCode.from_char('2') or is_numpad_2 or key == Key.esc:
            # Return to main view
            in_menu = False
            clear_screen()
            # Call welcome function before returning to main program
            landingPage()
            # Go back to main program
            setup_game_listeners()
            readKeyBoardConfig()
           

# Keyboard handler for game mode
def on_press_game(key):
    global running, in_menu, space_pressed
    
    if key == show_menu:
        # Show menu
        in_menu = True
        display_menu()
        setup_menu_listeners()
        return
    
    elif key == start_cycle:
        space_pressed = True
    
    elif key == stop_the_program:
        print(f'{stop_the_program} pressed, stopping...')
        running = False
        
    if space_pressed and key == perfrom_the_super_Glide:
        super_glide()

# Mouse scroll handler for game mode
def on_scroll_game(x, y, dx, dy):
    global space_pressed
    
    if perfrom_the_super_Glide == "scroll_up" and dy > 0 and space_pressed:
        super_glide()
    elif perfrom_the_super_Glide == "scroll_down" and dy < 0 and space_pressed:
        super_glide()

# Super glide function
def super_glide():
    global space_pressed
    # Simulate jump and crouch
    keyboard_controller = KeyboardController()
    
    keyboard_controller.press(in_game_jump)
    time.sleep(0.0069)
    keyboard_controller.release(in_game_jump)

    keyboard_controller.press(in_game_crouch)
    keyboard_controller.release(in_game_crouch)

    space_pressed = False

# Main program function
def run_in_thread():
    global running, in_menu, space_pressed
    
    # Initialize variables
    space_pressed = False
    
    # Setup initial game listeners
    setup_game_listeners()
    
    # Main loop
    try:
        while running:
            time.sleep(0.01)  # Small sleep to reduce CPU usage
    except KeyboardInterrupt:
        running = False
    
    # Stop listeners when program ends
    if keyboard_listener:
        keyboard_listener.stop()
    if mouse_listener:
        mouse_listener.stop()

# Main program entry
if __name__ == "__main__":
    landingPage()
    readKeyBoardConfig()
    run_in_thread()