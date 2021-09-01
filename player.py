from interception.stroke import key_stroke
import time

# Scancodes for arrow and alphanumeric/modifier keys should be separated. They have different key-states.
SC_DECIMAL_ARROW = {
    "LEFT": 75, "RIGHT": 77, "DOWN": 80, "UP": 72,
}

SC_DECIMAL = {

"ESC": 1, "1": 2, "2": 3, "3": 4, "4": 5, "5": 6, "6": 7, "7": 8, "8": 9, "9": 10, "0": 11, 
"-": 12, "=": 13, "bs": 14, "Tab": 15, "Q": 16, "W": 17, "E": 18, "R": 19, "T": 20, "Y": 21, 
"U": 22, "I": 23, "O": 24, "P": 25, "[": 26, "]": 27, "ENTER": 28, "CTRL": 29, "A": 30, "S": 31, 
"D": 32, "F": 33, "G": 34, "H": 35, "J": 36, "K": 37, "L": 38, ";": 39, "'": 40, "`": 41, 
"SHIFT": 42, "Z": 44, "X": 45, "C": 46, "V": 47, "B": 48, "N": 49, "M": 50, 
",": 51, ".": 52, "/": 53, "RSHIFT": 54, "PrtSc": 55, "ALT": 56, "SPACE": 57, "CAPS": 58,
# something on this line bugged out the ms script. the sript would press when start.
# "F1": 59, "F2": 60, "F3": 61, "F4": 62, "F5": 63, "F6": 64, "F7": 65, "F8": 66, "F9": 67, 
"F10": 68, "NUM": 69, "SCROLL": 70, "HOME": 71, "PGUP": 73, "-": 74, 
"CENTER": 76,  "+": 78, "END": 79,  "PGDN": 81, "INS": 82, "DEL": 83 

# original scan code
# "ALT": 56, "SPACE": 57, "CTRL": 29, "SHIFT": 42,
# "A": 30, "S": 31, "D": 32, "F": 33,
# "Q": 16, "W": 17, "E": 18, "R": 19,
# "1": 2, "2": 3, "3": 4, "4": 5
}


# Change these to your own settings.
JUMP_KEY = "SPACE"
ROPE_LIFT_KEY = "SHIFT"


class Player:
    def __init__(self, context, device, game):
        self.game = game
        # interception
        self.context = context
        self.device = device

    def release_all(self):
        for key in SC_DECIMAL_ARROW:
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 3, 0))
        for key in SC_DECIMAL:
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 1, 0))

    def press(self, key):
        """
        Mimics a human key-press.
        Delay between down-stroke and up-stroke was tested to be around 50 ms.
        """
        if key in SC_DECIMAL_ARROW:
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 2, 0))
            time.sleep(0.05)
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 3, 0))
        else:
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 0, 0))
            time.sleep(0.05)
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 1, 0))

    def release(self, key):
        if key in SC_DECIMAL_ARROW:
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 3, 0))
        else:
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 1, 0))

    def hold(self, key):
        if key in SC_DECIMAL_ARROW:
            self.context.send(self.device, key_stroke(SC_DECIMAL_ARROW[key], 2, 0))
        else:
            self.context.send(self.device, key_stroke(SC_DECIMAL[key], 0, 0))

    def go_to(self, target):
        """
        Attempts to move player to a specific (x, y) location on the screen.
        """
        while True:
            player_location = self.game.get_player_location()
            if player_location is None:
                continue

            x1, y1 = player_location
            x2, y2 = target

            """
            There are delays between taking a screenshot, processing the image, sending the key press, and game server ping.
            Player should be within 2 pixels of x-destination and 7 pixels of y-destination.
            """
            if abs(x1 - x2) < 2:
                # Player has reached target x-destination, release all held keys.
                self.release_all()
                if abs(y2 - y1) < 7:
                    # Player has reached target y-destination, release all held keys.
                    self.release_all()
                    break
                # Player is above target y-position.
                elif y1 < y2:
                    self.hold("DOWN")
                    self.press(JUMP_KEY)
                # Player is below target y-position.
                else:
                    if y1 - y2 > 30:
                        self.press(ROPE_LIFT_KEY)
                    else:
                        self.press(ROPE_LIFT_KEY)  # small climb movement in most maps is not viable
                                                    # can always rope lift up and then jump down
                        # self.press("UP")
                        # self.press("UP")
                # Delay for player falling down or jumping up.
                time.sleep(1)
            else:
                # Player is to the left of target x-position.
                if x1 < x2:
                    self.hold("RIGHT")
                # Player is to the right of target x-position.
                else:
                    self.hold("LEFT")
                if abs(x2 - x1) > 30:
                    self.press(JUMP_KEY)
                    self.press(JUMP_KEY)
