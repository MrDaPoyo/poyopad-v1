from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.rgb import RGB
from kmk.handlers.sequences import send_string

keyboard = KMKKeyboard()

keyboard.row_pins = (26, 27, 28, 29, 6, 7)
keyboard.col_pins = (0,)
keyboard.diode_orientation = DiodeOrientation.ROW2COL

keyboard.modules.append(Layers())
keyboard.extensions.append(MediaKeys())
keyboard.extensions.append(RGB(pixel_pin=3, num_pixels=2, val_limit=255))

COPY = KC.LCTL(KC.C)
PASTE = KC.LCTL(KC.V)
LMAO = send_string("LMAO")
DISCORD = send_string("\u001b" + "r" + "discord" + KC.ENTER.terminal_keycode)
SPOTIFY = send_string("\u001b" + "r" + "spotify" + KC.ENTER.terminal_keycode)

keyboard.keymap = [
    [COPY, PASTE, LMAO, DISCORD, SPOTIFY, KC.NO],
]

if __name__ == '__main__':
    keyboard.go()
