import curses
import curses.textpad
import types
from functools import singledispatch, singledispatchmethod

import CursesLogger
import CursesWidgets
import abc


class Layout(abc.ABC):
    win: curses.window
    logger: CursesLogger.Logger

    def __init__(self, log_level: int = 0):
        self.log_level = log_level
        self.active_widget = None
        self.new_handle = None
        self.value = -1
        self.widgets = []
        self.value = -1
        self.screen = []
        self.colorlist = (("red", curses.COLOR_RED),
                     ("green", curses.COLOR_GREEN),
                     ("yellow", curses.COLOR_YELLOW),
                     ("blue", curses.COLOR_BLUE),
                     ("cyan", curses.COLOR_CYAN),
                     ("magenta", curses.COLOR_MAGENTA),
                     ("black", curses.COLOR_BLACK),
                     ("white", curses.COLOR_WHITE))
        self.colors = {}
        colorpairs = 0
        for name, i in self.colorlist:
            colorpairs += 1
            curses.init_pair(colorpairs, curses.COLOR_WHITE, i)
            self.colors[name] = curses.color_pair(i)

    @abc.abstractmethod
    def add_widget_to_layout(self, widget: CursesWidgets.DisplayWidget):
        pass

    def get_widget(self, pos):
        return self.widgets[pos]

    def clear_widgets(self):
        for item in self.widgets:
            del item
        self.widgets = []
        self.win.clear()

    def add_widget(self, widget: CursesWidgets.DisplayWidget,
                   color_pair=None):  # adds widgets then creates the pads for them
        self.widgets.append(widget)
        self.active_widget = 0
        self.add_widget_to_layout(widget)
        return widget

    def draw(self, logger=None):
        for widget in self.widgets:
            self.logger.log("Drawing Widget", str(widget.win.getbkgd()))
            self.new_handle = widget.draw()
        self.win.refresh()

    def change_active(self):
        self.active_widget += 1
        if self.active_widget > len(self.widgets) - 1:
            self.active_widget = 0
        self.move_to_active()

    def move_to_active(self):  # todo tell widget to move cursor
        self.win.move(self.widgets[self.active_widget].win.getbegyx()[0],
                      self.widgets[self.active_widget].win.getbegyx()[1])
        self.win.cursyncup()

    def update_to_active(self):  # todo remove
        if hasattr(self.widgets[self.active_widget], "value"):
            if self.widgets[self.active_widget].text != -1:
                self.value = self.widgets[self.active_widget].text

    def input(self, keypress):
        if self.new_handle is type(CursesWidgets.DisplayWidget):  # todo allow for layout switching
            self.new_handle.handle_input(keypress)  # if widget is a display widget send input in
        if keypress == 9:
            self.change_active()
        else:
            self.widget_input(keypress)

    def widget_input(self, keypress):  # todo send input for any widget
        self.widgets[self.active_widget].handle_input(keypress)

    def save_screen(self):
        self.screen.append(self.widgets)
        return len(self.screen) - 1

    def load_screen(self, pos):
        self.widgets = self.screen[pos]
        self.win.clear()
        self.draw()

class HorizonalLayout(Layout):

    def add_widget_to_layout(self, widget: CursesWidgets.DisplayWidget):
        num_widgets = len(self.widgets)
        widget_win_size = [self.win.getmaxyx()[0], int(self.win.getmaxyx()[1] / num_widgets)]
        for index in range(num_widgets):
            # creates a basic horizontal layout
            if hasattr(self.widgets[index], "win"):
                self.logger.log("Moving Window", str((0, int(self.win.getmaxyx()[1] / num_widgets) * index)))
                self.widgets[index].win.mvderwin(0, widget_win_size[1] * index)
                self.widgets[index].resize(widget_win_size[0], widget_win_size[1])
            else:
                self.logger.log("Making window", str((0, int(self.win.getmaxyx()[1] / num_widgets) * (num_widgets - 1))))
                new_win = self.win.derwin(0, int(self.win.getmaxyx()[1] / num_widgets) * (num_widgets - 1))
                self.widgets[index].add_win(new_win)
                self.widgets[index].resize(self.win.getmaxyx()[0], int(self.win.getmaxyx()[1] / num_widgets))
                self.widgets[index].win.bkgd(' ',list(self.colors.values())[index])
                self.active_widget = index


class CursesDisplay:  # a container to connect window and widgets together
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

    def draw_scrn(self):
        for widget in self.widgets:
            self.new_handle = widget.draw()
            self.log("Drawing Widget " + str(widget))
        self.scrn.refresh()
        self.log("Drawing screen")

    def save_screen(self):
        self.screen.append(self.widgets)
        return len(self.screen) - 1

    def load_screen(self, pos):
        self.widgets = self.screen[pos]
        self.scrn.clear()
        self.draw_scrn()

    def clear_widgets(self):
        for item in self.widgets:
            del item
        self.widgets = []
        self.scrn.clear()

    def add_widget(self, widget: CursesWidgets.DisplayWidget,
                   color_pair=None):  # adds widgets then creates the pads for them
        self.widgets.append(widget)
        self.active_widget = 0
        self.add_widget_to_layout(widget)
        return widget

    def add_widget_to_layout(self, widget: CursesWidgets.DisplayWidget):
        num_widgets = len(self.widgets)
        for index in range(num_widgets):  # todo copy to layout widget
            # creates a basic horizontal layout
            if self.widgets[index].win is not None:
                self.widgets[index].win.mvwin(0, int(self.scrn.getmaxyx()[1] / num_widgets) * index)
                self.widgets[index].resize(self.scrn.getmaxyx()[0], int(self.scrn.getmaxyx()[1] / num_widgets))
            else:
                win = self.scrn.derwin(0, int(self.scrn.getmaxyx()[1] / num_widgets) * (num_widgets - 1))
                self.widgets[index].add_win(win)
                self.widgets[index].resize(self.scrn.getmaxyx()[0], int(self.scrn.getmaxyx()[1] / num_widgets))

    def get_widget(self, pos):
        return self.widgets[pos]

    def refresh_widgets(self):  # here because im too lazy to add a call back function
        # should be a part of member classes
        for widget in self.widgets:
            widget.win.clear()
            self.new_handle = widget.draw()

    def clear_widget(self, pos):
        del self.widgets[pos]
        self.widgets.pop(pos)

    def log(self, log_string):
        if self.log_level < 1:
            return
        with open("log.txt", "a") as logfile:
            logfile.write(log_string)
            logfile.write("\n")
            if self.log_level > 1:
                logfile.write("Cursor Position: " + str(self.scrn.getyx()))
                logfile.write("\n")

    def change_active(self):
        self.active_widget += 1
        if self.active_widget > len(self.widgets) - 1:
            self.active_widget = 0
        self.move_to_active()

    def move_to_active(self):
        self.log("Updating Active Location: " + str(self.active_widget))
        self.scrn.move(self.widgets[self.active_widget].win.getbegyx()[0],
                       self.widgets[self.active_widget].win.getbegyx()[1])

    def update_to_active(self):
        if hasattr(self.widgets[self.active_widget], "value"):
            if self.widgets[self.active_widget].text != -1:
                self.value = self.widgets[self.active_widget].text

    def handle_input(self, keypress=None):
        self.log("Handling Input")
        if keypress is None:
            keypress = self.scrn.getch()
        if self.new_handle is type(CursesWidgets.DisplayWidget):  # todo allow for layout switching
            self.new_handle.handle_input(keypress)  # if widget is a display widget send input in
        if keypress == 9:
            self.change_active()
        else:
            self.widget_input(keypress)
            self.update_to_active()

    def widget_input(self, keypress):  # todo send input for any widget
        self.widgets[self.active_widget].handle_input(keypress)

    def wait_for_enter(self):
        keypress = self.scrn.getch()
        if str(curses.keyname(keypress)) == "b'^J'":
            return False
        else:
            self.handle_input(keypress)
            return True

    def get_value_of_widget(self, pos):
        if hasattr(self.widgets[pos], "value"):
            if self.widgets[pos].value is not None:
                return self.widgets[pos].value
        return None


# todo update verticallayout
class VerticalLayout(CursesWidgets.DisplayWidget):
    def __init__(self, win: curses.window = None, selectable=True, onClose=None):
        super().__init__(win, onClose)
        self.widgets = []
        self.verticals = 0
        self.selectable = selectable

    def add_widget(self, widget: CursesWidgets.DisplayWidget,
                   color_pair=None):  # adds widgets then creates the pads for them

        self.verticals += 1
        self.widgets.append(widget)

        for index in range(len(self.widgets)):
            # creates a basic vertical layout
            if self.widgets[index].win is not None:
                self.widgets[index].win.mvwin(int(self.win.getmaxyx()[0] / self.verticals) * index, 0)
                self.widgets[index].resize(int(self.win.getmaxyx()[0] / self.verticals), self.win.getmaxyx()[1])
            else:
                win = self.win.derwin(int(self.win.getmaxyx()[0] / self.verticals) * (self.verticals - 1), 0)
                self.widgets[index].add_win(win)
                self.widgets[index].resize(int(self.win.getmaxyx()[0] / self.verticals), self.win.getmaxyx()[1])

        return widget

    def handle_input(self, keypress):
        if keypress is None:
            keypress = self.win.getch()
        if self.new_handle is type(CursesWidgets.DisplayWidget):
            self.new_handle.handle_input(keypress)

        if keypress == 9:  # todo add way for layout widget to switch subwidgets
            self.active_widget += 1
            if self.active_widget > len(self.widgets) - 1:
                self.active_widget = 0
            self.win.move(self.widgets[self.active_widget].win.getbegyx()[0],
                          self.widgets[self.active_widget].win.getbegyx()[1])
        else:
            self.widgets[self.active_widget].handle_input(keypress)

        if hasattr(self.widgets[self.active_widget], "value"):
            if self.widgets[self.active_widget].text != -1:
                self.value = self.widgets[self.active_widget].text
        self.widgets[self.active_widget].draw()

        self.win.refresh()

    def add_win(self, win: curses.window):
        self.win = win

    def resize(self, y: int, x: int):
        self.win.resize(y, x)

    def draw(self):
        for widget in self.widgets:
            self.new_handle = widget.draw()
        self.active_widget = len(self.widgets) - 1
        self.win.refresh()
