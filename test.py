#!/usr/bin/env python3
import unittest
from textlayout import TextLayout, TextGrid


class TestTextLayout(unittest.TestCase):

    def test_grid_emtpy1x1(self):
        grid = TextGrid(1, 1)
        lines = str(grid).split("\n")
        expect = [' ']
        self.assertEqual(lines, expect)

    def test_grid_emtpy3x3_border(self):
        grid = TextGrid(3, 3, border=True)
        lines = str(grid).split("\n")
        expect = ['   ',
                  '   ',
                  '   ']
        self.assertEqual(lines, expect)

    def test_layout_emtpy1x1(self):
        layout = TextLayout(1, 1)
        lines = layout.reservations().split("\n")
        expect = ['+---+',
                  '| 0 |',
                  '+---+']
        self.assertEqual(lines, expect)
        lines = str(layout).split("\n")
        expect = [' ']
        self.assertEqual(lines, expect)

    def test_layout_emtpy2x2(self):
        layout = TextLayout(2, 2)
        lines = layout.reservations().split("\n")
        expect = ['+-----+',
                  '| 0 0 |',
                  '| 0 0 |',
                  '+-----+']
        self.assertEqual(lines, expect)
        lines = str(layout).split("\n")
        expect = ['  ',
                  '  ']
        self.assertEqual(lines, expect)

    def test_layout_2x2addblank4x1x1(self):
        layout = TextLayout(2, 2)
        grid0x0 = TextGrid(1, 1)
        grid0x1 = TextGrid(1, 1)
        grid1x0 = TextGrid(1, 1)
        grid1x1 = TextGrid(1, 1)
        layout.add(grid0x0)
        layout.add(grid0x1)
        layout.add(grid1x0)
        layout.add(grid1x1)
        lines = layout.reservations().split("\n")
        expect = ['+-----+',
                  f'| {grid0x0.id} {grid0x1.id} |',
                  f'| {grid1x0.id} {grid1x1.id} |',
                  '+-----+']
        self.assertEqual(lines, expect)
        self.assertEqual(grid0x0.location(), {'y': 0, 'x': 0})
        self.assertEqual(grid0x1.location(), {'y': 0, 'x': 1})
        self.assertEqual(grid1x0.location(), {'y': 1, 'x': 0})
        self.assertEqual(grid1x1.location(), {'y': 1, 'x': 1})
        lines = str(layout).split("\n")
        expect = ['  ',
                  '  ']
        self.assertEqual(lines, expect)

    def test_layout_2x2add4x1x1(self):
        layout = TextLayout(2, 2)
        grid0x0 = TextGrid(1, 1)
        grid0x1 = TextGrid(1, 1)
        grid1x0 = TextGrid(1, 1)
        grid1x1 = TextGrid(1, 1)
        layout.add(grid0x0)
        layout.add(grid0x1)
        layout.add(grid1x0)
        layout.add(grid1x1)
        grid0x0.write('aa')
        grid0x0.write('aa')
        grid0x1.write('bb')
        grid0x1.write('bb')
        grid1x0.write('cc')
        grid1x0.write('cc')
        grid1x1.write('dd')
        grid1x1.write('dd')
        lines = layout.reservations().split("\n")
        expect = ['+-----+',
                  f'| {grid0x0.id} {grid0x1.id} |',
                  f'| {grid1x0.id} {grid1x1.id} |',
                  '+-----+']
        self.assertEqual(lines, expect)
        lines = str(layout).split("\n")
        expect = ['ab',
                  'cd']
        self.assertEqual(lines, expect)


if __name__ == '__main__':
    unittest.main()
