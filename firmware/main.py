import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.rgb import RGB
from kmk.handlers.sequences import send_string
from functools import partial

keyboard = KMKKeyboard()

# these row pins correspond to SW1-SW6 (GPIO26, GP27, GP28, GP29, GP6, GP7)
keyboard.row_pins = (board.GP26, board.GP27, board.GP28, board.GP29, board.GP6, board.GP7)
# now, the column pin.
keyboard.col_pins = (board.GP0,)
keyboard.diode_orientation = DiodeOrientation.ROW2COL

keyboard.modules.append(Layers())
keyboard.extensions.append(MediaKeys())

rgb_ext = RGB(
    pixel_pin=board.GP3,
    num_pixels=6,
    val_limit=100,
    hue_default=0,
    sat_default=0,
    val_default=0,
    rgb_order=(1, 0, 2),
)
keyboard.extensions.append(rgb_ext)

LED_PRESSED_COLOR = (255, 255, 255)
LED_RELEASED_COLOR = (0, 0, 0)

def _set_led_and_call_handler(key_index, color, original_handler, key, keyboard_obj, *args):
    '''Helper to set LED color and then call the original key handler.'''
    if hasattr(keyboard_obj, 'rgb') and keyboard_obj.rgb.pixels:
        keyboard_obj.rgb.set_pixel(key_index, *color)
        keyboard_obj.rgb.show()
    
    if original_handler:
        original_handler(key, keyboard_obj, *args)

def led_on_press_handler(key_index, original_handler, key, keyboard_obj, *args):
    _set_led_and_call_handler(key_index, LED_PRESSED_COLOR, original_handler, key, keyboard_obj, *args)

def led_on_release_handler(key_index, original_handler, key, keyboard_obj, *args):
    _set_led_and_call_handler(key_index, LED_RELEASED_COLOR, original_handler, key, keyboard_obj, *args)

def create_led_reactive_key(key_index, base_action):
    original_press_handler = None
    original_release_handler = None

    if hasattr(base_action, 'on_press') and callable(base_action.on_press):
        original_press_handler = base_action.on_press
        if hasattr(base_action, 'on_release') and callable(base_action.on_release):
            original_release_handler = base_action.on_release
    elif callable(base_action):
        original_press_handler = base_action
    else:
        pass

    return KC.make_key(
        on_press=partial(led_on_press_handler, key_index, original_press_handler),
        on_release=partial(led_on_release_handler, key_index, original_release_handler)
    )

ACTION_COPY = KC.LCTL(KC.C)
ACTION_PASTE = KC.LCTL(KC.V)
ACTION_LMAO = send_string("LMAO")
ACTION_DISCORD = send_string("\u001b" + "r" + "discord" + KC.ENTER.terminal_keycode)
ACTION_SPOTIFY = send_string("\u001b" + "r" + "spotif" + "y" + KC.ENTER.terminal_keycode)
ACTION_NO = KC.MACRO(":3")

KEY_COPY    = create_led_reactive_key(0, ACTION_COPY)
KEY_PASTE   = create_led_reactive_key(1, ACTION_PASTE)
KEY_LMAO    = create_led_reactive_key(2, ACTION_LMAO)
KEY_DISCORD = create_led_reactive_key(3, ACTION_DISCORD)
KEY_SPOTIFY = create_led_reactive_key(4, ACTION_SPOTIFY)
KEY_NO      = create_led_reactive_key(5, ACTION_NO)

keyboard.keymap = [
    [KEY_COPY, KEY_PASTE, KEY_LMAO, KEY_DISCORD, KEY_SPOTIFY, KEY_NO],
]

if __name__ == '__main__':
    keyboard.go()
