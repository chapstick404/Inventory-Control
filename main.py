import sqlite3
import curses
from curses.textpad import Textbox, rectangle
import CursesMenu
import database
def text_menu(win, text):
    win.box('|', '_')
    win.addstr(2,5, "CTRL-G to Enter")
    rows, cols = win.getmaxyx()
    input_win = curses.newwin(1,cols-6,3,3)
    rectangle(win, 2,2, 1+2+1, cols=3)
    win.refresh()
    box = Textbox(input_win)
    box.edit()
    usr_in = box.gather()
    return usr_in
def start_menu(win, rows, cols):
    win.box('|', '_')
    win.addstr(1,1, "Database Control System")
    win.addstr(2,5, "Ctrl-G to Enter")
    file_input_win = curses.newwin(1,cols-6,3,3)
    rectangle(win, 2, 2, 1+2+1, cols-3)
    win.refresh()
    box = Textbox(file_input_win)
    box.edit()
    file = box.gather()
    return file

def database_control_menu(rows, cols, win):
    menu = CursesMenu.CursesMenu()
    listInput = CursesMenu.CursesWidget("list", title = "Select An Option", items=["Add Items", "Find Item Location", "Inspect Container", "Read Containers"])
    menu.addWidget(listInput, id="root")
    menu.draw(inputWin=win)
    return listInput.value['index']

def view_container(win):
    container = text_menu(win, 'Input container')
    contents = connector.read_container(container)
    #todo add scrolling menu
def add_items_menu(rows, cols, win):
    win.addstr(1,1,"Adding Object")
    win.addstr(2,1,"Scan Container, or hit enter")
    container = win.getstr(3,1)
    if container == "":
        container = "-1"
    win.refresh()
    win.move(2,1)
    win.clrtobot()
    win.addstr(2,1,"Scan Item")
    item = win.getstr(3,1)
    win.refresh()
    win.clear()
    return(container, item)

def main(stdscr):
    stdscr.clear()
    rows, cols = stdscr.getmaxyx()

    stdscr.keypad(True)
    curses.start_color()
    curses.use_default_colors()

    curses.init_pair(5, -1, curses.COLOR_BLUE)
    stdscr.bkgd(' ', curses.color_pair(5))

    stdscr.refresh()

    file = start_menu(stdscr, rows, cols)
    stdscr.clear()
    global connector
    connector = database.DataConnector(file)

    menu_option = database_control_menu(rows, cols, stdscr)

    if menu_option == 0:
        stdscr.clear()
        add_items_menu(rows, cols, stdscr)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    curses.wrapper(main)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
