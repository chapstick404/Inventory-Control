import curses

class CursesDisplay: # a container to connect window and widgets together
    def __init__(self):
        self.widgets = {}

    def draw(self, startWidget="root", inputWin=None, fg=None, bg=None): #draws the widgets
        if inputWin:
            self.cursesWindow = inputWin
        else:
            self.cursesWindow = curses.initscr()
        curses.cbreak()
        curses.noecho()
        curses.start_color()
        if fg is None:
            fg = curses.COLOR_WHITE
        if bg is None:
            bg = curses.COLOR_BLACK
        curses.init_pair(2, fg, bg)
        curses.init_pair(1, bg, fg)


class DisplayWidget:
    def __init__(self, type, onClose=None):
        class InvalidType(Exception):
            def __init__(self):
                Exception.__init__(self, "Invalid \"type\" parameter.")

        self.type = type
        if not self.type in ["text", "list_menu", "list"]:
            raise InvalidType()
        self.id = id
        self.onClose = onClose
