#!/usr/bin/env python3
"""
    Unit tests for the TextGrid and TextLayout classes.

    Author: Dylan Doxey <dylan.doxey@gmail.com>
    Date: May 29, 2023
"""
import unittest
from textlayout import TextLayout, TextGrid


class TestTextLayout(unittest.TestCase):
    """These tests exercise and demonstrate the
       TextGrid and TextLayout behaviors.
    """

    def test_grid_emtpy1x1(self):
        """This test demonstrates creating a blank 1 by 1 grid."""
        grid = TextGrid(1, 1)
        lines = str(grid).split("\n")
        expect = [' ']
        self.assertEqual(lines, expect)

    def test_grid_emtpy3x3(self):
        """This test demonstrates creating a blank 3 by 3 grid."""
        grid = TextGrid(3, 3)
        lines = str(grid).split("\n")
        expect = ['   ',
                  '   ',
                  '   ']
        self.assertEqual(lines, expect)

    def test_grid_setstr3x3(self):
        """This test demonstrates setting the value of a 3 by 3 grid using
           a string of 4 four character strings separated by line breaks
           the source data.
        """
        grid = TextGrid(3, 3)
        grid.set("abcd\nefgh\nijkl\nmno")
        lines = str(grid).split("\n")
        expect = ['abc',
                  'efg',
                  'ijk']
        self.assertEqual(lines, expect)

    def test_grid_setlist3x3(self):
        """This test demonstrates setting the value of a 3 by 3 grid using
           a list of 4 four character strings as the source data.
        """
        grid = TextGrid(3, 3)
        grid.set(['abcd',
                  'efgh',
                  'ijkl'
                  'lmno'])
        lines = str(grid).split("\n")
        expect = ['abc',
                  'efg',
                  'ijk']
        self.assertEqual(lines, expect)

    def test_grid_setlargergrid3x3(self):
        """This test demonstrates setting the value of a 3 by 3 grid using
           a 4 x 4 grid as the source data.
        """
        grid = TextGrid(3, 3)
        grid4x4 = TextGrid(4, 4)
        grid4x4.set(['abcd',
                     'efgh',
                     'ijkl'
                     'lmno'])
        grid.set(grid4x4)
        lines = str(grid).split("\n")
        expect = ['abc',
                  'efg',
                  'ijk']
        self.assertEqual(lines, expect)

    def test_grid_setsmallergrid3x3(self):
        """This test demonstrates setting the value of a 3 by 3 grid using
           a 2 x 2 grid as the source data.
        """
        grid = TextGrid(3, 3)
        grid2x2 = TextGrid(2, 2)
        grid2x2.set(['ab',
                     'ef'])
        grid.set(grid2x2)
        lines = str(grid).split("\n")
        expect = ['ab ',
                  'ef ',
                  '   ']
        self.assertEqual(lines, expect)

    def test_grid_nonemtpy3x3_border(self):
        """This test demonstrates a text grid with border renders as
           a 3 x 3 grid with one character of text on stringification.
        """
        grid = TextGrid(3, 3, border=True)
        grid.write('aa')
        lines = str(grid).split("\n")
        expect = ['   ',
                  ' a ',
                  '   ']
        self.assertEqual(lines, expect)

    def test_grid_clear(self):
        """This test demonstrates the text grid clear() method."""
        grid = TextGrid(3, 3)
        grid.set("abc\ndef\nghi")
        lines = str(grid).split("\n")
        expect = ['abc',
                  'def',
                  'ghi']
        self.assertEqual(lines, expect)
        grid.clear()
        lines = str(grid).split("\n")
        expect = ['   ',
                  '   ',
                  '   ']
        self.assertEqual(lines, expect)

    def test_grid_setnone(self):
        """This test demonstrates a text grid will clear content
           if set with None.
        """
        grid = TextGrid(3, 3)
        grid.set("abc\ndef\nghi")
        lines = str(grid).split("\n")
        expect = ['abc',
                  'def',
                  'ghi']
        self.assertEqual(lines, expect)
        grid.set(None)
        lines = str(grid).split("\n")
        expect = ['   ',
                  '   ',
                  '   ']
        self.assertEqual(lines, expect)

    def test_layout_emtpy1x1(self):
        """This test demonstrates that a new one character layout with
           no text grids added will show zero reservations and no text
           on stringification.
        """
        layout = TextLayout(1, 1)
        lines = layout.reservations().split("\n")
        expect = ['+---+',
                  '| 0 |',
                  '+---+']
        self.assertEqual(lines, expect)
        expect = [' ']
        self.assertEqual(layout.lines, expect)

    def test_layout_bordered1x1(self):
        """This test demonstrates a 3 by 3 layout with
           a bordered 1 by 1 grid strififies correctly.
        """
        layout = TextLayout(3, 3)
        grid = TextGrid(3, 3, border=True)
        self.assertTrue(layout.add(grid))
        grid.set('a')
        lines = layout.reservations().split("\n")
        expect = ['+-------+',
                  f'| {grid.gid} {grid.gid} {grid.gid} |',
                  f'| {grid.gid} {grid.gid} {grid.gid} |',
                  f'| {grid.gid} {grid.gid} {grid.gid} |',
                  '+-------+']
        self.assertEqual(lines, expect)
        expect = ['   ',
                  ' a ',
                  '   ']
        self.assertEqual(layout.lines, expect)

    def test_layout_emtpy2x2(self):
        """This test demonstrates that a new 2 by 2 layout with
           no text grids added will show zero reservations and
           each position has no text on stringification.
        """
        layout = TextLayout(2, 2)
        lines = layout.reservations().split("\n")
        expect = ['+-----+',
                  '| 0 0 |',
                  '| 0 0 |',
                  '+-----+']
        self.assertEqual(lines, expect)
        expect = ['  ',
                  '  ']
        self.assertEqual(layout.lines, expect)

    def test_layout_2x2addblank4x1x1(self):
        """This test demonstrates that the text grids are added to
           to the layout in a left to right, top to bottom, sequence.
           The positions of each grid is verified after being added
           to the layout.
        """
        layout = TextLayout(2, 2)
        grid0x0 = TextGrid(1, 1)
        grid0x1 = TextGrid(1, 1)
        grid1x0 = TextGrid(1, 1)
        grid1x1 = TextGrid(1, 1)
        self.assertTrue(layout.add(grid0x0))
        self.assertTrue(layout.add(grid0x1))
        self.assertTrue(layout.add(grid1x0))
        self.assertTrue(layout.add(grid1x1))
        lines = layout.reservations().split("\n")
        expect = ['+-----+',
                  f'| {grid0x0.gid} {grid0x1.gid} |',
                  f'| {grid1x0.gid} {grid1x1.gid} |',
                  '+-----+']
        self.assertEqual(lines, expect)
        self.assertEqual(grid0x0.location(), {'y': 0, 'x': 0})
        self.assertEqual(grid0x1.location(), {'y': 0, 'x': 1})
        self.assertEqual(grid1x0.location(), {'y': 1, 'x': 0})
        self.assertEqual(grid1x1.location(), {'y': 1, 'x': 1})
        expect = ['  ',
                  '  ']
        self.assertEqual(layout.lines, expect)

    def test_layout_2x2add4x1x1(self):
        """This test demonstrates adding four text grids
           and shows that updates to those text grids are
           reflected on the stringified layout.
        """
        layout = TextLayout(2, 2)
        grid0x0 = TextGrid(1, 1)
        grid0x1 = TextGrid(1, 1)
        grid1x0 = TextGrid(1, 1)
        grid1x1 = TextGrid(1, 1)
        self.assertTrue(layout.add(grid0x0))
        self.assertTrue(layout.add(grid0x1))
        self.assertTrue(layout.add(grid1x0))
        self.assertTrue(layout.add(grid1x1))
        grid0x0.set(['aa', 'aa'])
        grid0x1.set(['bb', 'bb'])
        grid1x0.set(['cc', 'cc'])
        grid1x1.set(['dd', 'dd'])
        lines = layout.reservations().split("\n")
        expect = ['+-----+',
                  f'| {grid0x0.gid} {grid0x1.gid} |',
                  f'| {grid1x0.gid} {grid1x1.gid} |',
                  '+-----+']
        self.assertEqual(lines, expect)
        expect = ['ab',
                  'cd']
        self.assertEqual(layout.lines, expect)

    def test_layout_mixedgrids(self):
        """This test demonstrates a layout with mixed grids with
           borders and no borders.
        """
        layout = TextLayout(5, 5)
        grid0x0 = TextGrid(3, 3, border=True)
        grid0x3 = TextGrid(3, 2)
        grid3x0 = TextGrid(2, 3)
        grid3x3 = TextGrid(2, 2)
        self.assertTrue(layout.add(grid0x0))
        self.assertTrue(layout.add(grid0x3))
        self.assertTrue(layout.add(grid3x0))
        self.assertTrue(layout.add(grid3x3))
        grid0x0.set(['a'])
        grid0x3.set(['bb', 'bb', 'bb'])
        grid3x0.set(['ccc', 'ccc'])
        grid3x3.set(['dd', 'dd'])
        expect = ['   bb',
                  ' a bb',
                  '   bb',
                  'cccdd',
                  'cccdd']
        self.assertEqual(layout.lines, expect)


if __name__ == '__main__':
    unittest.main()
