import time
import random
from rune_solver import find_arrow_directions
from interception import *
from game import Game
from player import Player
from pynput.mouse import Button, Controller

mouse = Controller()


def bind(context):
    context.set_filter(interception.is_keyboard, interception_filter_key_state.INTERCEPTION_FILTER_KEY_ALL.value)
    print("Click any key on your keyboard.")
    device = None
    while True:
        device = context.wait()
        if interception.is_keyboard(device):
            print(f"Bound to keyboard: {context.get_HWID(device)}.")
            c.set_filter(interception.is_keyboard, 0)
            break
    return device

def solve_rune(g, p, target):
    """
    Given the (x, y) location of a rune, the bot will attempt to move the player to the rune and solve it.
    """
    while True:
        print("Pathing towards rune...")
        p.go_to(target)
        # Activate the rune.
        time.sleep(1)
        p.press("N")
        # Take a picture of the rune.
        time.sleep(1)
        img = g.get_rune_image()
        print("Attempting to solve rune...")
        directions = find_arrow_directions(img)

        if len(directions) == 4:
            print(f"Directions: {directions}.")
            for d, _ in directions:
                p.press(d)

            # The player dot will be blocking the rune dot, attempt to move left/right to unblock it.
            p.hold("LEFT")
            time.sleep(random.uniform(0.5, 1.25))
            p.release("LEFT")

            p.hold("RIGHT")
            time.sleep(random.uniform(0.5, 1.25))
            p.release("RIGHT")

            rune_location = g.get_rune_location()
            if rune_location is None:
                print("Rune has been solved.")
                break
            else:
                print("Trying again...")


if __name__ == "__main__":
    # This setup is required for Interception to mimic your keyboard.
    c = interception()
    d = bind(c)

    # Example Script for Hayato @ SS4.
    g = Game((5, 60, 250, 145))   # labyr suffering deep core 1
  
    p = Player(c, d, g)

    target_left = (195, 65)    # labyr suffering deep core 1
 

    while True:
        other_location = g.get_other_location()
        if other_location > 0:
            print("A player has entered your map.")

            #######  auto changing map when ppl enter ##### 
            # so far works fine, might need to improve
            print("Changing channel now.")
            time.sleep(4)
            p.press("ESC")
            time.sleep(0.5)
            p.press("ENTER")
            time.sleep(0.5)
            p.press("RIGHT")
            time.sleep(0.5)
            p.press("UP")
            time.sleep(0.5)
            p.press("ENTER")

            p.press("ESC")
            time.sleep(0.5)
            p.press("ENTER")
            time.sleep(0.5)
            p.press("RIGHT")
            time.sleep(0.5)
            p.press("UP")
            time.sleep(0.5)
            p.press("ENTER")

            p.press("ESC")
            time.sleep(0.5)
            p.press("ENTER")
            time.sleep(0.5)
            p.press("RIGHT")
            time.sleep(0.5)
            p.press("DOWN")
            time.sleep(0.5)
            p.press("ENTER")


        rune_location = g.get_rune_location()
        if rune_location is not None:
            print("A rune has appeared.")
            solve_rune(g, p, rune_location)


        print("Running...")

        p.go_to(target_left)


# mimic mouse move
        for i in range(5):
            mouse.move(2, -2)   # it just set a meaningless 1 and loop 5 times
        for i in range(5):
            mouse.move(-2, 2)


# buff

        
        # p.press("=")
        # time.sleep(3)
        p.press("8")
        time.sleep(1)
        # p.press("9")
        # time.sleep(1.5)
        p.press("0")
        time.sleep(1)

 # raising rage
 # arachid reflection
 # WORLD reaver
 # cry blade
 # soul blade
 # Sheild

        # time.sleep(2)

# first iternation

        p.press("R")   # soul blade
        time.sleep(1)

        p.press("LEFT")
        time.sleep(0.3)

        p.press("SPACE")
        p.press("SPACE")
        time.sleep(0.1)
        p.press("D")
        time.sleep(0.8)

        p.press("SPACE")
        p.press("SPACE")
        time.sleep(0.1)
        p.press("D")
        time.sleep(0.8)

        p.press("SPACE")
        p.press("SPACE")
        time.sleep(0.1)
        p.press("D")
        time.sleep(0.8)

        p.press("SPACE")
        p.press("SPACE")
        time.sleep(0.1)
        p.press("D")
        time.sleep(0.8)

        p.press("RIGHT")
        time.sleep(0.3)

        p.press("S")         # raising rage
        time.sleep(1)

        p.press("F")         # Sheild
        time.sleep(1)

        p.press("SHIFT")         # rope
        time.sleep(1)
        p.press("A")             # WORLD reaver
        time.sleep(2)
####  
      
        p.press("SPACE")
        p.press("SPACE")
        time.sleep(0.1)
        p.press("D")
        time.sleep(0.8)

        p.press("W") # arachid reflection
        time.sleep(1)

        p.press("SPACE")
        p.press("SPACE")
        time.sleep(0.1)
        p.press("D")
        time.sleep(0.8)

        p.press("SPACE")
        p.press("SPACE")
        time.sleep(0.1)
        p.press("D")
        time.sleep(0.8)

        p.press("SPACE")
        p.press("SPACE")
        time.sleep(0.1)
        p.press("D")
        time.sleep(0.8)

        p.go_to(target_left)

########### insert other player check here

        other_location = g.get_other_location()
        if other_location > 0:
            print("A player has entered your map.")

            #######  auto changing map when ppl enter ##### 
            # so far works fine, might need to improve
            print("Changing channel now.")
            time.sleep(4)
            p.press("ESC")
            time.sleep(0.5)
            p.press("ENTER")
            time.sleep(0.5)
            p.press("RIGHT")
            time.sleep(0.5)
            p.press("UP")
            time.sleep(0.5)
            p.press("ENTER")

            p.press("ESC")
            time.sleep(0.5)
            p.press("ENTER")
            time.sleep(0.5)
            p.press("RIGHT")
            time.sleep(0.5)
            p.press("UP")
            time.sleep(0.5)
            p.press("ENTER")

            p.press("ESC")
            time.sleep(0.5)
            p.press("ENTER")
            time.sleep(0.5)
            p.press("RIGHT")
            time.sleep(0.5)
            p.press("DOWN")
            time.sleep(0.5)
            p.press("ENTER")



##########

### second round; jump to upper platform

        p.press("LEFT")
        time.sleep(0.3)


        p.press("SPACE")
        p.press("SPACE")
        time.sleep(0.1)
        p.press("D")
        time.sleep(0.8)

        p.press("SPACE")
        p.press("SPACE")
        time.sleep(0.1)
        p.press("D")
        time.sleep(0.8)

        p.press("SPACE")
        p.press("SPACE")
        time.sleep(0.1)
        p.press("D")
        time.sleep(0.8)

        p.press("RIGHT")
        time.sleep(0.3)

        p.press("S")         # raising rage
        time.sleep(1)

        p.press("F")         # Sheild
        time.sleep(1)

        p.press("V")         # Skill jump
        time.sleep(0.5)
        p.press("SHIFT")         # rope
        time.sleep(1)

        p.press("A")             # WORLD reaver
        time.sleep(2)

### 

        p.press("2") #  instin combo
        time.sleep(0.8)

        p.press("SPACE")
        p.press("SPACE")
        time.sleep(0.1)
        p.press("D")
        time.sleep(0.8)

        p.press("E") #  cry blade
        time.sleep(1)

        p.press("B") #  rush to edge
        time.sleep(1)

        p.press("SPACE")
        p.press("SPACE")
        time.sleep(0.1)
        p.press("D")
        time.sleep(0.8)

        p.press("SPACE")
        p.press("SPACE")
        time.sleep(0.1)
        p.press("D")
        time.sleep(0.8)

        p.go_to(target_left)

