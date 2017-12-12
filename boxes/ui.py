import curses


class ui(object):
	def __init__(self, screen):
		self.screen = screen
		self.screen.border(0)

	def print_block(self, text):
		y = 4
		for line in text.split('\n'):
			self.screen.addstr(y, 4, line)
			y += 1
		self.screen.refresh()

	def prompt(self, message):
		(height, width) = self.screen.getmaxyx()
		self.screen.addstr(height - 2, 4, message)
		self.screen.refresh()
		return self.screen.getkey()

	#def menu(self, items, numbered=False):
