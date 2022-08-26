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
                win.addstr(self.value)
            else:
                widget.draw(win)

    def add_widget(self, widget):
        self.widget.append(widget)

class TitleWidget(DisplayWidget):
    def __int__(self, title: str, onClose=None, pos=None):
        super.__init__(self, title, onClose)
        if not pos:
            pos = "Top-Left"

    def draw(self, win: curses.window):
        if self.pos == "Top-left":
            win.addstr(self.value)

class CursesDisplay: # a container to connect window and widgets together
    def __init__(self, scrn: curses.window):
        self.widgets = []
        self.scrn = scrn
    def add_widget(self, widget: DisplayWidget, name: str): #todo add position value
        self.widgets.append(widget)

    def draw_scrn(self):
        for widget in self.widgets:
            widget.draw(self.scrn)

