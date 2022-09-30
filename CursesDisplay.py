import curses
import curses.textpad
import types


class DisplayWidget:  # basic display widget

    def __init__(self, text: str, onClose: types.BuiltinFunctionType):
        self.win = None
        self.onClose = onClose
        self.text = text

    def add_win(self, win: curses.window):
        self.win = win

    def draw(self):  # basic class to implement the function
        self.draw_self()

    def draw_self(self):
        self.win.addstr(self.text)

    def handle_input(self, keypress):  # here because all need to have method, may need to change
        return True

    def resize(self, y: int, x: int):
        self.win.resize(y,x)


class TitleWidget(DisplayWidget):
    def __init__(self, title: str, onClose=None):
        super().__init__(title, onClose)

    def draw_self(self):
        self.win.addstr(self.text)



class LabelWidget(TitleWidget):
    def __init__(self, text: str, onClose=None):
        super().__init__(text, onClose)
        self.value_changed = True

    def draw_self(self):
        if self.win is not None:
            if self.value_changed:
                self.win.addstr(0, 0, self.text)
                self.value_changed = False
                self.win.refresh()  # had to be here to update the screen

    def change_value(self, value):
        self.text = str(value)
        self.value_changed = True
        self.draw_self()


class ListView(DisplayWidget):
    def __init__(self, values: list, onClose=None):
        # noinspection PyTypeChecker
        super().__init__(None, onClose)
        self.line_pos = 0
        self.cursor = 0
        self.values = values

    def draw_self(self):
        self.win.clear()
        if self.win.getmaxyx()[0] > len(self.values):
            lines = len(self.values)
        else:
            lines = self.win.getmaxyx()[0]
        if self.line_pos < 0:
            self.line_pos = 0
        elif self.line_pos + lines > len(self.values):
            self.line_pos = len(self.values) - lines
        for index in range(lines):
            if index < len(self.values):
                self.win.addstr(index, 1, self.values[index + self.line_pos])

        self.win.refresh()

    def handle_input(self, keypressed):

        keypressed = str(curses.keyname(keypressed))  # is a byte object
        if keypressed == "b'KEY_DOWN'":
            self.line_pos += 1

        elif keypressed == "b'KEY_UP'":
            self.line_pos -= 1

        elif keypressed == "b'^J'":
            if self.onClose is None:
                return True
            else:
                self.onClose()


class MultiColumnList(ListView):
    def __init__(self, values: list, onClose=None):
        super().__init__(values, onClose)
        self.lists = []

    def add_win(self, win: curses.window):
        self.win = win
        columns = len(self.values[0])
        spacing = int(self.win.getmaxyx()[1] / columns) -1
        self.lists = []
        for row in self.values:
            complete_row = ''
            for item in row:
                item = str(item)
                if len(item) > spacing:
                    complete_row += item[:spacing]
                elif len(item) < spacing:
                    spaces = " " * (spacing - len(item))
                    complete_row += item + spaces
                else:
                    complete_row = item
            self.lists.append(complete_row)
        self.values = self.lists


class ListMenu(ListView):

    def __init__(self, values: list, onClose=None):
        super().__init__(values, onClose)
        self.value = None
        self.list_pos = 0
        self.cursor = 1

    def draw_self(self):
        self.win.clear()
        if self.win.getmaxyx()[0] > len(
                self.values):  # makes sure the list wont wrap around if the screen is bigger then the values
            lines = len(self.values)
        else:
            lines = self.win.getmaxyx()[0]

        if self.cursor > lines:
            self.list_pos += 1
            self.cursor = lines
        elif self.cursor < 1:
            self.list_pos -= 1
            if self.list_pos < 0:
                self.list_pos = 0
            self.cursor = 1

        if self.list_pos + lines > len(self.values):
            self.list_pos = len(self.values) - lines
        for index in range(0, lines):
            if index + 1 == self.cursor:
                self.win.addstr(index, 1, self.values[index + self.list_pos], curses.A_STANDOUT)
            else:
                self.win.addstr(index, 1, self.values[index + self.list_pos])

        self.win.refresh()

    def handle_input(self, keypressed):
        keypressed = str(curses.keyname(keypressed))
        if keypressed == "b'KEY_DOWN'":

            self.cursor += 1

        elif keypressed == "b'KEY_UP'":
            self.cursor -= 1

        elif keypressed == "b'^J'":
            if self.onClose is None:
                self.value = self.cursor + self.list_pos - 1
            else:
                self.value = self.cursor + self.list_pos - 1
                self.onClose(self.cursor + self.list_pos - 1)


class TextBox(DisplayWidget):
    def __init__(self, text = None, onClose=None):
        # noinspection PyTypeChecker
        super().__init__(text, onClose)
        self.value = None
        self.text_box = None
        self.onClose = onClose
        self.editwin = None

    def add_win(self, win: curses.window):
        self.win = win
        self.win.box()
        self.editwin = self.win.derwin(1, 1)

        self.text_box = curses.textpad.Textbox(self.editwin)
        self.editwin.refresh()

    def draw_self(self):  # todo change size

        self.editwin.refresh()

        self.editwin.cursyncup()

    def handle_input(self, keypress):
        if self.text_box.do_command(keypress) == 0:
            self.value = self.text_box.gather()
            if self.onClose is not None:
                self.onClose(self.value)

        pos = self.editwin.getyx()
        self.editwin.addstr(4,4,curses.keyname(keypress))
        self.editwin.move(pos[0], pos[1])
        self.editwin.refresh()


class TextInput(TextBox):
    def add_win(self, win: curses.window):
        self.win = win

        y, x = self.win.getmaxyx()
        self.win.resize(3, x)
        self.editwin = self.win.derwin(1, 1)
        if self.text is not None:
            self.editwin.addstr(self.text)
        self.text_box = curses.textpad.Textbox(self.editwin)
        self.editwin.refresh()

    def handle_input(self, keypress):
        if str(curses.keyname(keypress)) == "b'^J'":
            self.value = self.text_box.gather()
        if self.text_box.do_command(keypress) == 0:
            self.value = self.text_box.gather()
            if self.onClose is not None:
                self.onClose(self.value)
        self.editwin.refresh()

    def resize(self, y: int, x: int):
        self.win.clear()
        self.win.resize(3, x)
        self.win.box()
        self.editwin.resize(1, x-3)
        if self.text is not None:
            self.editwin.addstr(0, 0, self.text)
        self.win.refresh()

class CursesDisplay:  # a container to connect window and widgets together
    def __init__(self, scrn: curses.window):
        self.active_widget = None
        self.new_handle = None
        self.value = -1
        self.widgets = []
        self.scrn = scrn
        self.horizontals = 0
        self.value = -1
        self.screen = []

    def add_widget(self, widget: DisplayWidget, color_pair=None):  # adds widgets then creates the pads for them

        self.horizontals += 1
        self.widgets.append(widget)

        for index in range(len(self.widgets)):  # todo copy to layout widget
            # creates a basic horizontal layout
            if self.widgets[index].win is not None:
                self.widgets[index].win.mvwin(0, int(self.scrn.getmaxyx()[1] / self.horizontals) * index)
                self.widgets[index].resize(self.scrn.getmaxyx()[0], int(self.scrn.getmaxyx()[1] / self.horizontals))
            else:
                win = self.scrn.derwin(0, int(self.scrn.getmaxyx()[1] / self.horizontals)*(self.horizontals - 1))
                self.widgets[index].add_win(win)
                self.widgets[index].resize(self.scrn.getmaxyx()[0], int(self.scrn.getmaxyx()[1]/self.horizontals))

        return widget

    def clear_widgets(self):
        self.horizontals = 0
        for item in self.widgets:
            del item
        self.widgets = []
        self.scrn.clear()

    def clear_widget(self, pos):
        del self.widgets[pos]
        self.widgets.pop(pos)

    def draw_scrn(self):
        for widget in self.widgets:
            # widget.win.clear()
            self.new_handle = widget.draw()

        self.active_widget = len(self.widgets) - 1
        # if type(self.widgets[self.active_widget]) is not TextBox:
        #     self.scrn.move(self.widgets[self.active_widget].win.getbegyx()[0],
        #                    self.widgets[self.active_widget].win.getbegyx()[1])
        self.scrn.refresh()

    def refresh_widgets(self):  # here because im too lazy to add a call back function
        for widget in self.widgets:
            widget.win.clear()
            self.new_handle = widget.draw()

    def widget_input(self, keypress=None):
        if keypress is None:
            keypress = self.scrn.getch()
        if self.new_handle is type(DisplayWidget):
            self.new_handle.handle_input(keypress)

        if keypress == 9:  # todo add way for layout widget to switch subwidgets
            self.active_widget += 1
            if self.active_widget > len(self.widgets) - 1:
                self.active_widget = 0
            self.scrn.move(self.widgets[self.active_widget].win.getbegyx()[0],
                           self.widgets[self.active_widget].win.getbegyx()[1])

        self.widgets[self.active_widget].handle_input(keypress)

        if hasattr(self.widgets[self.active_widget], "value"):
            if self.widgets[self.active_widget].text != -1:
                self.value = self.widgets[self.active_widget].text
        self.widgets[self.active_widget].draw()

        self.scrn.refresh()

    def wait_for_enter(self):
        keypress = self.scrn.getch()
        if str(curses.keyname(keypress)) == "b'^J'":
            return False
        else:
            self.widget_input(keypress)
            return True

    def get_widget(self, pos):
        return self.widgets[pos]

    def get_value_of_widget(self, pos):
        if hasattr(self.widgets[pos], "value"):
            if self.widgets[pos].value is not None:
                return self.widgets[pos].value
        return None

    def save_screen(self):
        self.screen.append(self.widgets)
        return len(self.screen) - 1

    def load_screen(self, pos):
        self.widgets = self.screen[pos]
        self.scrn.clear()
        self.draw_scrn()
