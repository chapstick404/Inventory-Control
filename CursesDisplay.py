import curses

class DisplayWidget: #basic display widget
    def __init__(self, value: str, onClose=None):
        self.value = value
        self.id = id
        self.onClose = onClose
        self.widgets = [self]

    def draw(self, win: curses.window): #basic class to implement the function
        for widget in self.widgets:
            if widget is self:
                self.draw_self(win)
            else:
                widget.draw(win)

    def add_widget(self, widget):
        self.widget.append(widget)


    def draw_self(self, win: curses.window):
        win.addstr(self.value)

class TitleWidget(DisplayWidget):
    def __init__(self, title: str, onClose=None, pos=None):
        super().__init__(title, onClose)
        if pos is None:
            self.pos = "Top-Left"

    def draw_self(self, win: curses.window):
        if self.pos == "Top-Left":
            win.addstr(0, 0, self.value)
class  ListView(DisplayWidget):
    def __init__(self, value: list, onClose=None, pos=None):
        self.values = value
        self.onClose= onClose
        if not pos:
            self.pos="Top-Left"

    def draw_self(self, win: curses.window):
        lines = win.getmaxyx()[0]
        self.line_pos = 0
        for index in range(lines):
            if index < len(self.values):
                win.addstr(0, self.line_pos+index, self.values[index+self.line_pos])



class CursesDisplay: # a container to connect window and widgets together
    def __init__(self, scrn: curses.window):
        self.widgets = []
        self.scrn = scrn
    def add_widget(self, widget: DisplayWidget, name: str): #todo add position value
        self.widgets.append(widget)

    def draw_scrn(self):
        for widget in self.widgets:
            widget.draw(self.scrn)

