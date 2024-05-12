import curses
import random
import time
from collections import deque
from curses import wrapper

FILE_NAME = "text.txt"  # Constant for the file name containing text
COLOR_GREEN = curses.COLOR_GREEN  # Color constant for green
COLOR_RED = curses.COLOR_RED  # Color constant for red
COLOR_WHITE = curses.COLOR_WHITE  # Color constant for white
COLOR_BLACK = curses.COLOR_BLACK  # Color constant for black


def load_texts():
    """
    Load and strip lines of text from a predefined text file.
    :return: list of stripped lines of text.
    """
    with open(FILE_NAME, "r") as f:
        return [line.strip() for line in f]


def start_screen(stdscr):
    """
    Display the welcome screen with instructions.
    :param stdscr: Curses window used to handle the screen.
    """
    stdscr.clear()
    stdscr.addstr("Welcome to the Swift_Stroke!\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):
    """
    Display the target text, current input by the user and the real-time WPM.
    :param stdscr: Curses window used to handle the screen.
    :param target: The target text for typing.
    :param current: The current text typed by the user.
    :param wpm: Words per minute speed.
    """
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1) if char == correct_char else curses.color_pair(2)
        stdscr.addstr(0, i, char, color)


def wpm_test(stdscr, texts):
    """
    Handle the typing test logic including displaying the text and processing input.
    :param stdscr: Curses window used to handle the screen.
    :param texts: List of texts to choose from for the typing test.
    """
    target_text = random.choice(texts)
    current_text = deque()
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = (
            round((len(current_text) / (time_elapsed / 60)) / 5) if current_text else 0
        )

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except curses.error:
            continue

        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if current_text:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    """
    Main function to initialize color pairs and start the typing test.
    :param stdscr: Curses window used to handle the screen.
    """
    curses.init_pair(1, COLOR_GREEN, COLOR_BLACK)
    curses.init_pair(2, COLOR_RED, COLOR_BLACK)
    curses.init_pair(3, COLOR_WHITE, COLOR_BLACK)

    texts = load_texts()
    start_screen(stdscr)
    while True:
        wpm_test(stdscr, texts)
        stdscr.addstr(2, 0, "You completed the text. Press any key to continue...")
        stdscr.refresh()
        key = stdscr.getkey()

        if ord(key) == 27:
            break


wrapper(main)
