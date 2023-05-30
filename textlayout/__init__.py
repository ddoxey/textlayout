class TextLayout:
    """TextLayout
    """
    def __init__(self, height, width, border=False):
        if (height < 3 or width < 3) and (height == 0 or width == 0 or border):
            raise Exception(f'height: {height}, width: {width}, border: {border} -- invalid')
        self.height = height
        self.width = width
        self.border = border
        self.reserved_ = [[0 for x in range(width)] for y in range(height)]
        self.data = {}

    def __str__(self):
        lines = []
        b = ""
        if self.border:
            b = " "
            lines.append('{}{}{}'.format(b, " " * self.width - 2, b))
        for ypos, row in enumerate(self.reserved_):
            line = ""
            for xpos, grid_id in enumerate(row):
                if grid_id == 0:
                    line += " "
                else:
                    line += self.data[grid_id].read(ypos, xpos)
            lines.append('{}{}{}'.format(b, line, b))
        if self.border:
            lines.append(lines[0])
        return "\n".join(lines)

    def reservations(self):
        lines = ['+' + ('-' * (1 + self.width * 2)) + '+']
        b = ""
        if self.border:
            b = " "
            lines.append('|{} {} {}|'.format(b, " " * self.width, b))
        for row in self.reserved_:
            lines.append('|{} {} {}|'.format(b, " ".join([str(c) for c in row]), b))
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
                if row < len(self.reserved_) and col < len(self.reserved_[row]):
                    if self.reserved_[row][col] > 0:
                        raise AssertionError(f'{row},{col} is already reserved')
                    self.reserved_[row][col] = grid.id
        self.data[grid.id] = grid

    def add(self, grid):
        position = self.search(grid)
        if position is not None:
            grid.locate(position)
            self.reserve(grid)
            return True
        return False


class TextGrid(TextLayout):
    id_ = 1

    def __init__(self, height, width, border=False):
        super().__init__(height, width, border)
        self.ypos = 0
        self.xpos = 0
        self.lines = []
        self.id = __class__.id_
        __class__.id_ += 1

    def __str__(self):
        text, b = "", ""
        yend = self.ypos + self.height
        xend = self.xpos + self.width
        if self.border:
            b = " "
            yend -= 2
            xend -= 2
            text += b * self.width + "\n"
        for ypos in range(self.ypos, yend):
            text += b
            for xpos in range(self.xpos, xend):
                text += self.read(ypos, xpos)
            text += f'{b}\n'
        if self.border:
            text += b * self.width + "\n"
        return text.rstrip("\n")

    def locate(self, position):
        self.ypos = position['ypos']
        self.xpos = position['xpos']

    def location(self):
        if self.ypos is None or self.xpos is None:
            return None
        return {'y': self.ypos, 'x': self.xpos}

    def write(self, line):
        if len(self.lines) < self.height:
            self.lines.append(line[0:self.width])

    def read(self, y, x):
        ypos = y - self.ypos
        xpos = x - self.xpos
        if ypos >= self.height or xpos >= self.width:
            raise Exception(f'{ypos} >= {self.height}, '
                            f'{xpos} >= {self.width}: out of range')
        if ypos < len(self.lines) and xpos < len(self.lines[ypos]):
            return self.lines[ypos][xpos]
        return " "

