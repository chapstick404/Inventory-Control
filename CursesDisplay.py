import curses


class DisplayWidget:  # basic display widget
    def __init__(self, value: str, onClose=None, bg=None, fg=None):
        self.value = value
        self.id = id
        self.onClose = onClose
        self.widgets = [self]
        if fg is None:
            fg = curses.COLOR_WHITE
        if bg is None:
            bg = curses.COLOR_BLACK
        #curses.init_pair(2, fg, bg)
        #curses.init_pair(1, bg, fg)

    def draw(self, win: curses.window):  # basic class to implement the function
        self.draw_self(win)
        return None

    def draw_self(self, win: curses.window):
        win.addstr(self.value)

    def handle_input(self, win: curses.window, keypress):
        None


class TitleWidget(DisplayWidget):
    def __init__(self, title: str, onClose=None, fg=None, bg=None):
        super().__init__(title, onClose, fg, bg)

    def draw_self(self, win: curses.window):
        win.addstr(self.value)


class ListView(DisplayWidget):
    def __init__(self, values: list, onClose=None, fg=None, bg=None):
        super().__init__(None, onClose, fg, bg)
        self.cursor = 0
        self.values = values


    def draw_self(self, win: curses.window):
        win.clear()
        lines = win.getmaxyx()[0]
        if self.line_pos < 0:
            self.line_pos = 0
        elif self.line_pos + (lines) > len(self.values):
            self.line_pos = len(self.values) - lines
        for index in range(lines):
            if index < len(self.values):
                win.addstr(index, 1, self.values[index + self.line_pos])
        win.refresh()

    def handle_input(self, win: curses.window, keypressed):


        keypressed = str(curses.keyname(keypressed)) #is a byte object
        if keypressed == "b'KEY_DOWN'":
            self.line_pos += 1

        if keypressed == "b'KEY_UP'":
            self.line_pos -= 1

class ListMenu(ListView):


    def __init__(self, values: list, onClose=None, fg=None, bg=None):
        super().__init__(values, onClose, fg, bg)
        self.list_pos = 0
        self.cursor = 1
        self.value = -1

    def draw_self(self, win: curses.window):
        win.clear()
        lines = win.getmaxyx()[0]
        if self.cursor > lines:
            self.list_pos += 1
            self.cursor = lines
        elif self.cursor < 1:
            self.list_pos -= 1
            if self.list_pos < 0:
                self.list_pos = 0
            self.cursor = 1

        if self.list_pos+lines > len(self.values):
            self.list_pos = len(self.values)-lines
        win.addstr(3, 25, str(self.cursor))
        win.addstr(4,25,str(self.list_pos))
        for index in range(0,lines):
            if index+1 == self.cursor:
                win.addstr(index, 1, self.values[index+self.list_pos], curses.A_STANDOUT)
            else:
                win.addstr(index, 1, self.values[index+self.list_pos])

        win.refresh()


    def handle_input(self, win: curses.window, keypressed):
        keypressed = str(curses.keyname(keypressed))
        if keypressed == "b'KEY_DOWN'":

            self.cursor += 1

        elif keypressed == "b'KEY_UP'":
            self.cursor -= 1

        elif keypressed == "b'^J'":
            if self.onClose is None:
                self.value = self.cursor+self.list_pos-1
            else:
                self.onClose(self.cursor+self.list_pos-1)




class CursesDisplay:  # a container to connect window and widgets together
    def __init__(self, scrn: curses.window):
        self.value = -1
        self.widgets = []
        self.scrn = scrn
        self.horizontals = 0

    def add_widget(self, widget: DisplayWidget, pos=None):  # adds widgets then creates the pads for them
        if pos is None:
            pos = "Top"
        self.horizontals += 1
        for index in range(self.horizontals-1):  # todo copy to layout widget
            # creates a basic horizontal layout
            self.widgets[index][1].mvwin(0, int(self.scrn.getmaxyx()[1]/self.horizontals)*index)
            self.widgets[index][1].resize(self.scrn.getmaxyx()[0], int(self.scrn.getmaxyx()[1]/self.horizontals))


        self.widgets.append([widget,
                             self.scrn.derwin(self.scrn.getmaxyx()[0], int(self.scrn.getmaxyx()[1]/self.horizontals), 0, (int(self.scrn.getmaxyx()[1]/self.horizontals)*(self.horizontals-1)))])

    def clear_widgets(self):
        self.horizontals = 0
        self.widgets = []

    def clear_widget(self, pos):
        self.widgets.pop(pos)


    def draw_scrn(self):
        for index in range(len(self.widgets)):
            self.widgets[index][1].clear()
            self.new_handle = self.widgets[index][0].draw(self.widgets[index][1])
            self.active_widget = index

        self.scrn.move(self.widgets[self.active_widget][1].getbegyx()[0], self.widgets[self.active_widget][1].getbegyx()[1])
        self.scrn.refresh()

    def widget_input(self):
        keypress = self.scrn.getch()
        if self.new_handle is type(DisplayWidget):
            self.new_handle.handle_input(keypress)
        else:
            if keypress == 9: #todo add way for layout widget to switch subwidgets
                self.active_widget += 1
                if self.active_widget > len(self.widgets)-1:
                    self.active_widget = 0

        self.widgets[self.active_widget][0].handle_input(self.widgets[self.active_widget][1], keypress)
        if hasattr(self.widgets[self.active_widget][0], "value"):
            if self.widgets[self.active_widget][0].value != -1:
                self.value = self.widgets[self.active_widget][0].value
        self.widgets[self.active_widget][0].draw(self.widgets[self.active_widget][1])
        self.scrn.move(self.widgets[self.active_widget][1].getbegyx()[0],
                       self.widgets[self.active_widget][1].getbegyx()[1])
        self.scrn.refresh()
