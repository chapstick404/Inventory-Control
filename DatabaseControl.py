import curses
import CursesWidgets
import CursesDisplay
import CursesLayouts
import database


class InventoryControl:
    def __init__(self, scrn):
        self.scrn = scrn
        self.display = CursesDisplay.Display(scrn, log_level=2)
        self.layout = CursesLayouts.HorizonalLayout()
        self.display.layout = self.layout
        self.start_menu()

    def start_menu(self):
        menu = self.layout.add_widget(CursesWidgets.TextInput())
        self.display.draw_scrn()
        while menu.value is None:
            self.display.handle_input()
        self.database = database.DataConnector(menu.value)
        self.database_control_menu()

    def database_control_menu(self):

        while True:
            self.layout.clear_widgets()
            list_menu = CursesWidgets.ListMenu(
                ["Add Items", "Find Item Location", "Inspect Container", "Read Containers"])

            self.layout.add_widget(list_menu)
            self.display.draw_scrn()
            while list_menu.value is None:
                self.display.handle_input()
                self.display.draw_scrn()
            if list_menu.value == 0:
                self.add_item_menu()
            if list_menu.value == 1:
                self.find_item()
            if list_menu.value == 2:
                self.inspect_menu()
            if list_menu.value == 3:
                self.list_containers()

    def add_item_menu(self):
        container = self.single_input("Container ID")
        item = self.single_input("Item ID")
        title = self.single_input("Title")
        desc = self.single_input("Desc")
        self.database.add_item(item, container, title, desc)
        if container not in self.database.read_container(container):
            pos = self.layout.save_screen()
            if self.confirm_dialog("Add New Container?"):
                self.add_container_prefilled(container)
            self.layout.load_screen(pos)


    def confirm_dialog(self, dialog):
        self.layout.clear_widgets()
        menu = CursesWidgets.ListMenu(["No", "Yes"])
        self.layout.add_widget(CursesWidgets.TitleWidget(dialog))
        self.layout.add_widget(menu)
        self.display.draw_scrn()
        while menu.value is None:
            self.display.handle_input()
            self.display.draw_scrn()
        return menu.value

    def single_input(self, label=None, prefill = None):
        self.layout.clear_widgets()
        text_input = CursesWidgets.TextInput()

        if label is not None:
            self.layout.add_widget(CursesWidgets.TitleWidget(label))

        self.layout.add_widget(text_input)
        self.display.draw_scrn()
        while text_input.value is None:
            self.display.handle_input()
        return text_input.value

    def find_item(self):
        item_id = self.single_input()
        found = self.database.locate_item(item_id)

        self.layout.clear_widgets()
        if len(found) == 0:
            self.layout.add_widget(CursesWidgets.TitleWidget("No Such Item"))
        else:
            list_display = CursesWidgets.MultiColumnList(found)
            self.layout.add_widget(list_display)
        self.display.draw_scrn()
        while self.display.wait_for_enter():
            self.display.draw_scrn()

    def inspect_menu(self):
        self.layout.clear_widgets()
        text_input = CursesWidgets.TextInput()
        self.layout.add_widget(text_input)
        self.display.draw_scrn()
        while text_input.value is None:
            self.display.handle_input()
        input_value = text_input.value
        self.read_container(input_value)

    def read_container(self, container):
        self.layout.clear_widgets()
        containers = self.database.read_container(container)
        if len(containers) == 0:
            widget = CursesWidgets.LabelWidget("No/Empty Container")
        else:
            widget = CursesWidgets.MultiColumnList(list(containers))
        self.layout.add_widget(widget)
        self.display.draw_scrn()
        while self.display.wait_for_enter():
            None

    def list_containers(self):
        self.layout.clear_widgets()
        containers = self.database.readvalues('containers')
        list_view = CursesWidgets.MultiColumnList(containers)
        self.layout.add_widget(list_view)
        self.display.draw_scrn()
        while self.display.wait_for_enter():
            self.display.draw_scrn()

    def add_container(self):
        self.layout.clear_widgets()
        container = self.single_input("Container ID")
        title = self.single_input("Title")
        desc = self.single_input("Desc")
        self.database.add_container(container, title, desc)

    def add_container_prefilled(self, prefill: str):
        self.layout.clear_widgets()
        container = self.single_input("Container ID", prefill)
        title = self.single_input("Title")
        desc = self.single_input("Desc")
        self.database.add_container(container, title, desc)

if __name__ == '__main__':
    curses.wrapper(InventoryControl)
