import CursesWidgets
import CursesLayouts
import curses
import abc


class Display(abc.ABC):
    _layout: CursesLayouts.Layout

    def __init__(self, scrn: curses.window, log_level=0):
        self.log_level = log_level
        self.active_widget = None
        self.new_handle = None
        self.value = -1
        self.widgets = []
        self.scrn = scrn
        self.value = -1
        self.screen = []
        if self.log_level > 0:
            logfile = open("log.txt", "w")
            logfile.close()

    @property
    def layout(self):
        """The layout of the base screen"""
        return self._layout

    @layout.setter
    def layout(self, value: CursesLayouts.Layout): #todo change to make class here
        self._layout = value
        self._layout.win = self.scrn.derwin(0,0)

    def draw_scrn(self):
        self._layout.draw()
        self.log("Drawing Layout " + str(self._layout))
        self.scrn.refresh()
        self.log("Drawing screen")

    def clear_layout(self): #may cause memory leak
        self._layout.clear_widgets()
        self.scrn.clear()

    def log(self, log_string):
        if self.log_level < 1:
            return
        with open("log.txt", "a") as logfile:
            logfile.write(log_string)
            logfile.write("\n")
            if self.log_level > 1:
                logfile.write("Cursor Position: " + str(self.scrn.getyx()))
                logfile.write("\n")

    def handle_input(self, keypress=None):
        self.log("Handling Input")
        if keypress is None:
            keypress = self.scrn.getch()
        if keypress == 9:
            self._layout.change_active()
        else:
            self._layout.input(keypress)

    def wait_for_enter(self):
        keypress = self.scrn.getch()
        if str(curses.keyname(keypress)) == "b'^J'":
            return False
        else:
            self._layout.input(keypress)
            return True
