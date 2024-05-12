import curses
from curses import wrapper
import time
import random
from collections import deque

# Константы
FILE_NAME = "text.txt"
COLOR_GREEN = curses.COLOR_GREEN
COLOR_RED = curses.COLOR_RED
COLOR_WHITE = curses.COLOR_WHITE
COLOR_BLACK = curses.COLOR_BLACK


def load_texts():
    with open(FILE_NAME, "r") as f:
        return [line.strip() for line in f]


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()


def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1) if char == correct_char else curses.color_pair(2)
        stdscr.addstr(0, i, char, color)


def wpm_test(stdscr, texts):
    target_text = random.choice(texts)
    current_text = deque()
    wpm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except Exception:
            continue

        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if current_text:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    curses.init_pair(1, COLOR_GREEN, COLOR_BLACK)
    curses.init_pair(2, COLOR_RED, COLOR_BLACK)
    curses.init_pair(3, COLOR_WHITE, COLOR_BLACK)

    texts = load_texts()
    start_screen(stdscr)
    while True:
        wpm_test(stdscr, texts)
        stdscr.addstr(2, 0, "You completed the text Press any key to continue...")
        key = stdscr.getkey()

        if ord(key) == 27:
            break


wrapper(main)
