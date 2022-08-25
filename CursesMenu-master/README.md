# CursesMenu
![PyPI](https://img.shields.io/pypi/v/CursesMenu)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/scoutchorton/CursesMenu)

## Description

CursesMenu is a GTK inspired widget engine using curses for use with command line interfaces. Also inspired by the Ubuntu Live Server installation menus.

## Installation

### Using pip:
```bash
pip3 install cursesmenu
```

### From source:
```bash
python3 setup.py install
```

## Tutorial
* Import the package into your script using:

```python
from CursesMenu import *
```

* Create a new `CursesMenu` object:

```python
myMenu = CursesMenu()
```

* Create widgets to add to the menu:

```python
#Creates a text widget that gets a string of text as input from the user
textInput = CursesWidget("text", title="My Text Widget", onClose="listWidget")

#Creates a list widget that gets an index and value of a list item from the user
listInput = CursesWidget("list", title="My List Widget", items=["Item 1", "Item 2", "Item 3"])
```

* Add widgets to the menu:

```python
myMenu.addWidget(textInput, id="root")
myMenu.addWidget(listInput, id="listWidget")
```

* Draw the menu using Curses:

```python
myMenu.draw()
```

## Documentation
### `CursesMenu()`
* Menu object to handle widgets and drawing with curses.

 #### **Methods**
 * **`CursesMenu.addWidget(widget, margin=0, id=None)`**
   * Adds a widget to the menu.
   * widget: An instance of `CursesWidget` to add to the menu.
   * margin: Empty space around the widget. Defaults to `0`.
   * id: Identification for use with the `onClose` property of `CursesWidget` and also for `CursesMenu.draw()`.
 * **`CursesMenu.quit(`)**
   * Exits curses in the menu. Intended for use within `CursesMenu` class.
 * **`CursesMenu.widgetHandler(widget)`**
   * Drawing process for the menu. Intended for use within `CursesMenu` class.
   * widget: Widget for the handler to draw.
 * **`CursesMenu.draw(startWidget="root", inputWin=None)`**
   * Initiates curses and hands off execution to `CursesMenu.widgetHandler()`.
   * startWidget: ID of the widget to start drawing. Defaults to `"root"`.
   * inputWin: Curses window object to use for drawing to. Indtended for use with `curses.wrapper()`, but can be used outside of `curses.wrapper()`. Defaults to `None`.

 #### Properties
 * **`CursesMenu.widgets`**
   * Python dictionary of widgets with their respective ID's.

### `CursesWidget(type, title="", onClose=None, items=[], hide=False)`
* Widget object to handle associated data with a widget.
* type: Type of widget to create. Accepts `"text"` and `"list"`.
* title: String to display above widget. Defaults to an empty string.
* onClose: String with the ID of a widget added to the same menu to go to after drawing the current widget. Defaults to `None`.
* items: For use with `"list"` widget. A Python list of items to be displayed. Converted to strings when displayed. Defaults to an empty list.
* hide: Boolean value for whether to hide input. Replaces text input for asterisks if set to `True`. Defaults to `False`.
#### Properties
 * **`CursesWidget.type`**
   * Parameter of original object.
 * **`CursesWidget.title`**
   * Parameter of original object.
 * **`CursesWidget.id`**
   * Parameter of original object.
 * **`CursesWidget.onClose`**
   * Parameter of original object.
 * **`CursesWidget.hide`**
   * Parameter of original object.
 * **`CursesWidget.data`**
   * `items` parameter of original object.
 * **`CursesWidget.value`**
   * Dependent on `CursesWidget.type`. If `CursesWidget.type == "text"`, `CursesWidget.value = {"text": ""}`. If `CursesWidget.type == "list"`, `CursesWidget.value = {"text": "", "index": 0}`. Updated during `CursesMenu.widgetHandler()`.
