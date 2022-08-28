import CursesDisplay
import curses


def main(stdscr):
   display = CursesDisplay.CursesDisplay(stdscr)
   display.add_widget(CursesDisplay.TitleWidget("test"), name="root")
   display.draw_scrn()
   while True:
       stdscr.getch()

curses.wrapper(main)