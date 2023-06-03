"""
    The TextLayout and TextGrid classes address the need to work with stirngs
    in two dimentional grids, as opposed to the usual one dimensional string.

    The TextGrid is a two dimentional string which is pre-populated with spaces
    if it is uninitialized.

    The TextLayout is a similar to the TextGrid in that it is a two dimentional
    text object with fixed dimensions. However, the content of the TextLayout
    object is derived from its component TextGrid instances which are written
    two separately.

    Author: Dylan Doxey <dylan.doxey@gmail.com>
    Date: May 29, 2023
"""


class TextLayout:
    """TextLayout is a composition of TextGrid instances where the layout of
       how the grids render is determined at the time they are added to the
       layout.
    """
    def __init__(self, height, width, border=False):
        if (height < 3 or width < 3) and (height == 0 or width == 0 or border):
            raise Exception(f'height: {height}, width: {width}, '
                            f'border: {border} -- invalid')
        self.height = height
        self.width = width
        self.border = border
        self.reserved_ = [[0 for x in range(width)] for y in range(height)]
        self.data = {}

    def __str__(self):
        return "\n".join(self.lines)

    @property
    def lines(self):
        """The lines property provides a list of strings which represent the
           content of the TextLayout as populated by its component TextGrid
           instances.
        """
        lines = []
        b_char = ""
        if self.border:
            b_char = " "
            border = b_char * self.width
            lines.append(border)
        for ypos, row in enumerate(self.reserved_):
            line = ""
            for xpos, grid_id in enumerate(row):
                if grid_id == 0:
                    line += " "
                else:
                    line += self.data[grid_id].read(ypos, xpos)
            lines.append(f'{b_char}{line}{b_char}')
        if self.border:
            lines.append(lines[0])
        return lines

    def reservations(self):
        """Produces a text representation of the grid reservations on the
           layout. Useful for debugging.
        """
        lines = ['+' + ('-' * (1 + self.width * 2)) + '+']
        b_char = ""
        if self.border:
            b_char = " "
            border = b_char * self.width
            lines.append(border)
        for row in self.reserved_:
            line = " ".join([str(c) for c in row])
            lines.append(f'|{b_char} {line} {b_char}|')
        if self.border:
            lines.append(lines[1])
        lines.append(lines[0])
        return "\n".join(lines)

    def inquire(self, ypos, xpos, grid):
        """Inquire if a given grid can fit at the proposed y/x position.
            Return None if the answer is no, or a loss score greater than
            zero if the grid would overlap the edges of the screen.
        """
        loss = 0
        for row in range(grid.height):
            r_index = row + ypos
            if r_index >= len(self.reserved_):
                loss += grid.width
                continue
            c_index = xpos
            c_end = c_index + grid.width
            c_index = max(c_index, 0)
            collisions = sum(self.reserved_[r_index][c_index:c_end])
            if collisions > 0:
                return None
            overhang = grid.width - len(self.reserved_[r_index][c_index:])
            loss += overhang
        return loss

    def search(self, grid):
        """Search for the nearest available place to position the grid by
            scanning from left to right and top to bottom.
        """
        border_offset = 1 if self.border else 0
        positions = []
        for row in range(self.height):
            for col in range(self.width):
                loss = self.inquire(row, col, grid)
                if loss is not None:
                    positions.append({'ypos': row + border_offset,
                                      'xpos': col + border_offset,
                                      'loss': loss})
                    if loss == 0:
                        break
            if len(positions) > 0 and positions[-1]['loss'] == 0:
                break
        if len(positions) > 0:
            return sorted(positions, key=lambda c: c['loss'])[0]
        return None

    def reserve(self, grid):
        """Reserve a spot on the layout for the grid."""
        for row in range(grid.ypos, grid.ypos + grid.height):
            for col in range(grid.xpos, grid.xpos + grid.width):
                if row < len(self.reserved_) and \
                   col < len(self.reserved_[row]):
                    if self.reserved_[row][col] > 0:
                        raise AssertionError(f'{row},{col} already reserved')
                    self.reserved_[row][col] = grid.gid
        self.data[grid.gid] = grid

    def add(self, grid):
        """Find a position on the layout for the given grid and assign the
           position properties on the grid and retains a reference to the
           grid so that updates to the grid content will be reflected when
           the layout lines are rendered.
        """
        position = self.search(grid)
        if position is not None:
            grid.locate(position['ypos'], position['xpos'])
            self.reserve(grid)
            return True
        return False


class TextGrid(TextLayout):
    """The TextGrid is a two dimentional collection of characters."""
    gid_ = 1

    def __init__(self, height, width, border=False):
        super().__init__(height, width, border)
        self.ypos = 0
        self.xpos = 0
        self.rows = []
        self.gid = __class__.gid_
        __class__.gid_ += 1

    def __str__(self):
        text = ""
        for row_i in range(self.height):
            for col_i in range(self.width):
                text += self.read(self.ypos + row_i, self.xpos + col_i)
            text += '\n'
        return text.rstrip("\n")

    def locate(self, ypos, xpos):
        """Set the x and y position attributes of the TextGrid."""
        self.ypos = ypos
        self.xpos = xpos

    def location(self):
        """Get a dict with the x and y position attributes."""
        if self.ypos is None or self.xpos is None:
            return None
        return {'y': self.ypos, 'x': self.xpos}

    def write(self, line):
        """Write a line to the grid. Any lines or characters that are
           out of bounds will be discarded.
        """
        max_height, max_width = self.height, self.width
        if self.border:
            max_height -= 2
            max_width -= 2
        if len(self.rows) < max_height:
            self.rows.append(line[0:max_width])
            return True
        return False

    def set(self, text):
        """Set the content of the grid. The source data can be a list of
           strings, or a string with newlines, or an object that can be
           stringified.
        """
        if text is None:
            self.rows = []
            return
        lines = None
        if isinstance(text, list):
            lines = text
        elif isinstance(text, str):
            lines = text.split("\n")
        else:
            lines = str(text).split("\n")
        for line in lines:
            if not self.write(line):
                break

    def read(self, y_coord, x_coord):
        """Read the character for the given x and y coordinates of the grid.
           The x and y given are for the coordinates of the grid according to
           its location in the layout.
        """
        if self.border:
            if y_coord == 0 or y_coord == self.height - 1 or \
               x_coord == 0 or x_coord == self.width - 1:
                return " "
        ypos = y_coord - self.ypos
        xpos = x_coord - self.xpos
        if ypos >= self.height or xpos >= self.width:
            raise Exception(f'{ypos} >= {self.height}, '
                            f'{xpos} >= {self.width}: out of range')
        if self.border:
            ypos -= 1
            xpos -= 1
        if ypos < len(self.rows) and xpos < len(self.rows[ypos]):
            return self.rows[ypos][xpos]
        return " "
