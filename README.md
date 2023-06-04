# textlayout
Manipulate two dimensional blocks of text

The TextGrid object is a grid of characters with fixed dimensions. It's content
is updated with the `write()`, `set()`, and `clear()` methods.

The TextLayout object contains references to TextGrid objects which it arranges
in a non overlapping layout, in the order they are added, from top to bottom
and left to right.

# Usage
```
>>> from textlayout import TextLayout, TextGrid
>>> layout = TextLayout(8, 8)
>>> grid0 = TextGrid(4, 4)
>>> grid1 = TextGrid(4, 4)
>>> grid2 = TextGrid(4, 4)
>>> grid3 = TextGrid(4, 4)
>>> layout.add(grid0)
True
>>> layout.add(grid1)
True
>>> layout.add(grid2)
True
>>> layout.add(grid3)
True
>>> print(layout)








>>> grid0.write('aaaa')
True
>>> grid0.write('aaaa')
True
>>> grid0.write('aaaa')
True
>>> grid0.write('aaaa')
True
>>> grid1.set("bbbb\nbbbb\nbbbb\nbbbb")
>>> grid2.set(['cccc', 'cccc', 'cccc', 'cccc'])
>>> grid3.set(grid0)
>>> print(layout)
aaaabbbb
aaaabbbb
aaaabbbb
aaaabbbb
ccccaaaa
ccccaaaa
ccccaaaa
ccccaaaa
>>> grid0.set("dddd\ndddd\ndddd\ndddd")
>>> print(layout)
ddddbbbb
ddddbbbb
ddddbbbb
ddddbbbb
ccccaaaa
ccccaaaa
ccccaaaa
ccccaaaa
>>>
```
