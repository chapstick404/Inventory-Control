import curses
import random
class CursesMenu:
	def __init__(self):
		self.widgets = {}
	def draw(self, startWidget="root", inputWin=None, fg=None, bg=None):
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


		self.widgetHandler(self.widgets[startWidget])


	def widgetHandler(self, widget):
		if widget["widgetObject"].type == "text":
			winDim = self.cursesWindow.getmaxyx()
			cursor = {"p": 0, "s": 0, "e": 0}
			textBuff = []
			keyPressed = ""
			wrapper = self.cursesWindow.derwin(winDim[0], winDim[1], 0, 0)
			textBox = wrapper.derwin(1, winDim[1] - widget["margin"] - 4, widget["margin"] + 1, widget["margin"] + 2)
			textboxLength = textBox.getmaxyx()[1]
			wrapper.bkgd(" ", curses.color_pair(2))
			wrapper.addstr(widget["margin"], widget["margin"], widget["widgetObject"].title, curses.color_pair(2))
			wrapper.refresh()
			curses.curs_set(1)
			textBox.keypad(True)
			while keyPressed != "\n":
				if keyPressed == "KEY_BACKSPACE" and len(textBuff) and cursor["p"] > 0:
					cursor["p"] -= 1
					if cursor["e"] > len(textBuff):
						cursor["e"] = len(textBuff)
					if cursor["p"] < cursor["s"] or (cursor["e"] == len(textBuff) and cursor["s"] > 0):
						cursor["s"] -= 1
					if cursor["e"] - cursor["s"] >= textboxLength:
						cursor["e"] = cursor["s"] + textboxLength
					if cursor["s"] < 0:
						cursor["s"] = 0
					textBuff.pop(cursor["p"])
				elif keyPressed == "KEY_DC" and len(textBuff) and cursor["p"] < len(textBuff):
					if cursor["e"] > len(textBuff):
						cursor["e"] = len(textBuff)
					if cursor["p"] < cursor["s"] or (cursor["e"] == len(textBuff) and cursor["s"] > 0):
						cursor["s"] -= 1
					if cursor["e"] - cursor["s"] >= textboxLength:
						cursor["e"] = cursor["s"] + textboxLength
					if cursor["s"] < 0:
						cursor["s"] = 0
					textBuff.pop(cursor["p"])
				elif keyPressed == "KEY_HOME":
					cursor["p"] = cursor["s"] = 0
					cursor["e"] = len(textBuff)
					if cursor["e"] >= textboxLength:
						cursor["e"] = textboxLength - 1
				elif keyPressed == "KEY_LEFT" and cursor["p"] > 0:
					cursor["p"] -= 1
					if cursor["p"] < cursor["s"]:
						cursor["s"] = cursor["p"]
					if cursor["e"] - cursor["s"] >= textboxLength:
						cursor["e"] = cursor["s"] + textboxLength - 1
				elif keyPressed == "KEY_RIGHT" and cursor["p"] < len(textBuff):
					cursor["p"] += 1
					if cursor["p"] > cursor["e"]:
						cursor["e"] = cursor["p"]
					if cursor["e"] - cursor["s"] >= textboxLength:
						cursor["s"] = cursor["e"] - textboxLength + 1
						if cursor["s"] < 0:
							cursor["s"] = 0
				elif keyPressed == "KEY_END":
					cursor["p"] = cursor["e"] = len(textBuff)
					cursor["s"] = cursor["e"] - textboxLength + 1
					if cursor["s"] < 0:
						cursor["s"] = 0
				elif len(keyPressed) == 1 and keyPressed != "\t":
					textBuff.insert(cursor["p"], keyPressed)
					cursor["p"] += 1
					if cursor["e"] < textboxLength - 1:
						cursor["e"] += 1
					if cursor["p"] > cursor["e"]:
						cursor["e"] = cursor["p"]
					if cursor["e"] - cursor["s"] >= textboxLength:
						cursor["s"] = cursor["e"] - textboxLength + 1
						if cursor["s"] < 0:
							cursor["s"] = 0
				textBox.bkgd(" ", curses.color_pair(1))
				textBox.addstr(0, 0, ("*" * (cursor["e"] - cursor["s"])).ljust(textboxLength - 1, " ") if widget["widgetObject"].hide else "".join(textBuff[cursor["s"]:cursor["e"]]).ljust(textboxLength - 1, " "), curses.color_pair(1))
				textBox.move(0, cursor["p"] - cursor["s"])
				textBox.refresh()
				keyPressed = textBox.getkey()
			widget["widgetObject"].value["text"] = "".join(textBuff)
			wrapper.erase()
		elif widget["widgetObject"].type == "list":
			winDim = self.cursesWindow.getmaxyx()
			data = widget["widgetObject"].data
			cursor = {"p": 0, "s": 0, "e": 0}
			maxLength = 0
			for i in data:
				maxLength = len(i) if maxLength < len(i) else maxLength
			keyPressed = ""
			wrapper =  self.cursesWindow.derwin(winDim[0], winDim[1], 0, 0)
			listWin = wrapper.derwin(((winDim[0] - (widget["margin"] * 2) - 1) if len(data) > (winDim[0] - (widget["margin"] * 2) - 1) else len(data)), ((winDim[1] - (widget["margin"] * 2) - 2) if (maxLength + 1) > (winDim[1] - (widget["margin"] * 2) - 2) else maxLength), widget["margin"] + 1, widget["margin"] + 2)
			listLength = listWin.getmaxyx()[0]
			listWidth = listWin.getmaxyx()[1]
			if len(data) > listLength:
				cursor["e"] = listLength
			else:
				cursor["e"] = len(data)
			cursor["e"] -= 1
			cursor["p"] = cursor["e"] - 2
			wrapper.bkgd(" ", curses.color_pair(2))
			wrapper.addstr(widget["margin"], widget["margin"], widget["widgetObject"].title, curses.color_pair(2))
			wrapper.refresh()
			curses.curs_set(0)
			listWin.keypad(True)
			while keyPressed != "\n":
				if keyPressed == "KEY_DOWN"and cursor["p"] < len(data) - 1:
					cursor["p"] += 1
					if cursor["p"] > cursor["e"]:
						cursor["e"] = cursor["p"]
						cursor["s"] = cursor["e"] - listLength + 1
				elif keyPressed == "KEY_UP" and cursor["p"] > 0:
					cursor["p"] -= 1
					if cursor["p"] < cursor["s"]:
						cursor["s"] = cursor["p"]
						cursor["e"] = cursor["s"] + listLength - 1
				elif keyPressed == "KEY_HOME":
					cursor["p"] = cursor["s"] = 0
					cursor["e"] = listLength - 1
				elif keyPressed == "KEY_END":
					cursor["p"] = cursor["e"] = len(data) - 1
					cursor["s"] = cursor["e"] - listLength + 1
				listWin.bkgd(" ", curses.color_pair(1))
				for i in range(cursor["s"], cursor["e"] + 1):
					listWin.insstr(i - cursor["s"], 0, str(data[i])[0:listWidth].ljust(listWidth, " "), curses.color_pair(2 if i == cursor["p"] else 1))
				listWin.refresh()
				keyPressed = listWin.getkey()
			widget["widgetObject"].value["text"] = data[cursor["p"]]
			widget["widgetObject"].value["index"] = cursor["p"]
			wrapper.erase()
		if widget["widgetObject"].onClose:
			self.widgetHandler(self.widgets[widget["widgetObject"].onClose])
		else:
			self.quit()
	def quit(self):
		curses.nocbreak()
		self.cursesWindow.keypad(False)
		curses.echo()
		curses.endwin()
	def addWidget(self, widget, margin=0, id=None):
		if id:
			self.widgets[id] = {"widgetObject": widget, "margin": margin}
			return id
		else:
			id = f"wid{str(random.randint(0,99999)).ljust(5, '0')}"
			if id in self.widgets.keys():
				self.addWidget(widget, padding)
			else:
				self.widgets[id] = {"widgetObject": widget, "margin": margin}
				return id

class CursesWidget:
	def __init__(self, type, title="", onClose=None, items=[], hide=False):
		class InvalidType(Exception):
			def __init__(self):
				Exception.__init__(self, "Invalid \"type\" parameter.")
		self.type = type
		if not self.type in ["text", "list"]:
			raise InvalidType()
		self.title = title
		self.id = id
		self.onClose = onClose
		if self.type in ["text", "list"]:
			self.value = {}
		if self.type in ["text"]:
			self.hide = hide
		if self.type in ["list"]:
			self.data = items
		if not self.type in ["label"]:
			if self.type in ["text"]:
				self.value = {"text":""}
			elif self.type in ["list"]:
				self.value = {"text":"", "index":0}
