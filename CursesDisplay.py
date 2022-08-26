import curses

class DisplayWidget: #basic display widget
    def __init__(self, value: str, onClose=None):
        self.value = value
        self.id = id
        self.onClose = onClose

    def draw(self, win: curses.window): #basic class to implement the function
        win.addstr(self.value)
class CursesDisplay: # a container to connect window and widgets together
    def __init__(self):
        self.widgets = []

    def add_widget(self, widget: DisplayWidget, name: str): #todo add position value
        self.widgets.append(widget)


