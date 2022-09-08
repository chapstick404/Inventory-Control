import CursesDisplay
import curses


def main(stdscr):
   display = CursesDisplay.CursesDisplay(stdscr)
   mylines = ["Line {0} ".format(id)*3 for id in range(1,14)]
   display.add_widget(CursesDisplay.ListMenu(mylines))

   display.draw_scrn()
   while display.get_value_of_widget(0) == None:
       display.widget_input()

   selcetion = display.get_value_of_widget(0)
   display.clear_widgets()
   display.add_widget(CursesDisplay.TitleWidget(str(selcetion)))
   display.draw_scrn()
   while True:
       display.widget_input()
def test(stdscr):
   while True:
      keypress = stdscr.getch()
      stdscr.addstr(str(curses.keyname(keypress)))

curses.wrapper(main)