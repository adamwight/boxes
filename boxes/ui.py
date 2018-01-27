class ui(object):
    def __init__(self, screen):
        self.screen = screen
        self.screen.border(0)

    def clear(self):
        self.screen.clear()

    def print_block(self, text, x=4):
        y = 4
        (height, width) = self.screen.getmaxyx()
        lines = text.splitlines()
        pages = self._page(lines, height - y)

        for page_num, page in enumerate(pages):
            if page_num > 0:
                self.prompt("Press any key to scroll...")
                # FIXME: clear section
                self.clear()

            cur_y = y

            for line in page:
                self.screen.addstr(cur_y, x, line)
                cur_y += 1
            self.screen.refresh()

    def _page(self, lines, height):
        for i in range(0, len(lines), height):
            yield lines[i:i + height]

    def log_action(self, text):
        # TODO: Reserve screen areas for each type of output.
        text = "Action result:\n" + text
        self.print_block(text, x=40)

    def prompt(self, message):
        (height, width) = self.screen.getmaxyx()
        self.screen.addstr(height - 2, 4, message)
        self.screen.refresh()
        return self.screen.getkey()

    # def menu(self, items, numbered=False):
