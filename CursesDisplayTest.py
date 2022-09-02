import CursesDisplay
import curses


def main(stdscr):
   display = CursesDisplay.CursesDisplay(stdscr)
   mylines = ["Line {0} ".format(id)*3 for id in range(1,14)]
   display.add_widget(CursesDisplay.ListMenu(mylines))

   display.draw_scrn()
   while display.value == -1:
       display.widget_input()

def test(stdscr):
   while True:
      keypress = stdscr.getch()
      stdscr.addstr(str(curses.keyname(keypress)))

curses.wrapper(main)