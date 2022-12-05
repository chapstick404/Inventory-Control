import CursesDisplay
import CursesWidgets
import CursesLayouts
import curses


def main(stdscr):
    curses.start_color()
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLUE)
    display = CursesDisplay.Display(stdscr, log_level=1)
    mylines = ["Line {0} ".format(id) * 3 for id in range(14)]
    myMultiLines = [['test0', 'test0b', 'test0c'], ['test1', 'test1b', 'test1c'], ['test2', 'test2b']]
    label = CursesWidgets.LabelWidget("")
    textinput = CursesWidgets.TextBox()
    layout = CursesLayouts.HorizonalLayout()
    display.layout = layout

    layout.add_widget(label)
    layout.add_widget(CursesWidgets.ListView(mylines))
    layout.add_widget(textinput)

    # display.add_widget(CursesDisplay.ListMenu(mylines, onClose=label.change_value))
    # display.add_widget(label)
    # display.add_widget(CursesDisplay.ListView(mylines))
    # display.add_widget(CursesDisplay.MultiColumnList(myMultiLines))
    # display.add_widget(textinput)

    display.draw_scrn()
    while display.wait_for_enter():
        display.draw_scrn()

    selcetion = display.get_value_of_widget(0)
    display.clear_widgets()
    display.add_widget(CursesWidgets.TitleWidget(str(selcetion)))
    display.draw_scrn()
    while True:
        display.widget_input()


def test(stdscr):
    curses.start_color()
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLUE)

    stdscr.bkgd(' ', curses.color_pair(7))
    stdscr.addstr(str(curses.color_pair(5)))
    while True:
        keypress = stdscr.getch()
        stdscr.addstr(str(curses.keyname(keypress)))


curses.wrapper(main)
