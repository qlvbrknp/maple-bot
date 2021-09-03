import cv2 as cv
import os
import numpy as np


def find_arrow_directions(img, debug=False):
    """
    Given an image in BGRA format, will attempt to find "arrows" through
    classifying the directions of gradients that start and end at certain HSV values.
    Debugging will show parsed pictures of the image.
    """
    bgr = cv.cvtColor(img, cv.COLOR_BGRA2BGR)
    hsv = cv.cvtColor(bgr, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)
    m, n = len(h), len(h[0])
    valid_gradient = []
    directions = []

    if debug:
        visited = [[False for _ in range(n)] for _ in range(m)]
        canvas = np.zeros(img.shape[:2], dtype="uint8")

    def hue_is_red(r, c):
        """
        Returns a boolean value based on whether a certain pixel is a "red" color.
        """
        return 5 <= h[r][c] <= 12 and s[r][c] >= 65 and v[r][c] >= 128

    def hue_is_valid(r1, c1, r2, c2, diff):
        """
        Returns a boolean value based on whether two pixels are within a certain HSV range of each other.
        """
        return abs(int(h[r1][c1]) - int(h[r2][c2])) <= diff and s[r2][c2] >= 150 and v[r2][c2] >= 150 and h[r2][c2] <= 70

    def near_gradient(r, c):
        """
        Returns a boolean value based on whether or not a certain pixel is around an already discovered gradient.
        """
        for i, j in valid_gradient:
            if abs(i-r) < 15 and abs(c-j) < 15:
                return True
        return False

    def gradient_exists(r1, c1, delta_r, delta_c):
        """
        Given a starting pixel and unit value representing a direction, check if a gradient exists.
        """
        if near_gradient(r1, c1):
            return False

        tmp_r1, tmp_c1 = r1, c1
        rune_gradient = False
        # The directional arrows that appear in runes are around 30 pixels long.
        for _ in range(30):
            r2 = tmp_r1 + delta_r
            c2 = tmp_c1 + delta_c
            if 0 <= r2 < m and 0 <= c2 < n:
                # Check if the next pixel maintains the gradient.
                if hue_is_valid(tmp_r1, tmp_c1, r2, c2, 10):
                    # If the pixel is a green-ish color, it is a possible arrow.
                    if 50 <= h[r2][c2] <= 70:
                        rune_gradient = True
                        valid_gradient.append((r1, c1))
                        break
                    tmp_r1 = r2
                    tmp_c1 = c2
                else:
                    break
            else:
                break

        return rune_gradient

    def expand_gradient(r1, c1, direction):
        """
        Given a starting pixel and gradient direction, we can DFS to expand the gradient.
        Arrow(s) had horizontal hue changes of 10 and vertical hue changes of 2.
        """
        stack = [(r1, c1)]
        while stack:
            r2, c2 = stack.pop()
            visited[r2][c2] = True
            if r2 + 1 < m:
                if not visited[r2 + 1][c2] and hue_is_valid(r2, c2, r2 + 1, c2, 2 if direction else 10):
                    stack.append((r2 + 1, c2))
            if r2 - 1 >= 0:
                if not visited[r2 - 1][c2] and hue_is_valid(r2, c2, r2 - 1, c2, 2 if direction else 10):
                    stack.append((r2 - 1, c2))
            if c2 + 1 < n:
                if not visited[r2][c2 + 1] and hue_is_valid(r2, c2, r2, c2 + 1, 10 if direction else 2):
                    stack.append((r2, c2 + 1))
            if c2 - 1 >= 0:
                if not visited[r2][c2 - 1] and hue_is_valid(r2, c2, r2, c2 - 1, 10 if direction else 2):
                    stack.append((r2, c2 - 1))
            canvas[r2][c2] = 180

    def find_direction(r, c):
        """
        Given a starting pixel, returns the direction of any gradients found to exist.
        """
        if gradient_exists(r, c, 0, -1):
            return "RIGHT"
        elif gradient_exists(r, c, 0, 1):
            return "LEFT"
        elif gradient_exists(r, c, -1, 0):
            return "DOWN"
        elif gradient_exists(r, c, 1, 0):
            return "UP"
        else:
            return None

    # The rune captcha was observed to appear within this part of the application window on 800x600 resolution.
    for r in range(150, 275):
        for c in range(150, 650):
            # Arrows start at a red-ish color and are around 15 pixels apart.
            if hue_is_red(r, c) and not near_gradient(r, c):
                direction = find_direction(r, c)
                if direction:
                    directions.append((direction, (r, c)))
                    if debug:
                        if direction == "LEFT" or direction == "RIGHT":
                            expand_gradient(r, c, 1)
                        else:
                            expand_gradient(r, c, 0)

    if debug:
        cv.imshow("Hue", h)
        cv.imshow("Saturation", s)
        cv.imshow("Value", v)
        cv.imshow("Original", img)
        cv.imshow("Parsed", canvas)
        cv.waitKey(0)

    return sorted(directions, key=lambda x: x[1][1])


if __name__ == "__main__":
    for file_name in os.listdir("docs/rune_screenshots"):
        if file_name.endswith(".png"):
            img = cv.imread("docs/rune_screenshots/" + file_name)
            print(f'File:{file_name}, Directions={find_arrow_directions(img, True)}')
