import CursesDisplay
import curses


def main(stdscr):
   display = CursesDisplay.CursesDisplay(stdscr)
   mylines = ["Line {0} ".format(id)*3 for id in range(1,14)]
   display.add_widget(CursesDisplay.ListView(mylines))
   display.add_widget(CursesDisplay.ListView(mylines))
   display.add_widget(CursesDisplay.ListView(mylines))
   display.draw_scrn()
   while True:
       display.widget_input()

def test(stdscr):
   while True:
      keypress = stdscr.getch()
      stdscr.addstr(str(keypress))

curses.wrapper(main)