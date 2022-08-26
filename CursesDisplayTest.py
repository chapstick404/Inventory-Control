import CursesDisplay
import curses


def main(stdscr):
    widget = CursesDisplay.DisplayWidget("Everyn")
    widget.draw(stdscr)
    while True:
        stdscr.getch()

curses.wrapper(main)