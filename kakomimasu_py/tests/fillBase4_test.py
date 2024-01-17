from ..kkmm import Field, Board
import pytest


def test_fill1():
    n_agent = 6
    width, height = 3, 4
    points = [0 for _ in range(width * height)]

    field = Field(width=width, height=height, points=points, n_agent=n_agent)

    def set_field_layout(s):
        s = s.replace("\n", "")
        for i, c in enumerate(s):
            if c == "0":
                field.tiles[i] = {"type": Field.WALL, "player": 0}
            elif c == "1":
                field.tiles[i] = {"type": Field.WALL, "player": 1}
            else:
                field.tiles[i] = {"type": Field.AREA, "player": None}

    def check_field(s):
        s = s.replace("\n", "")
        for i, c in enumerate(s):
            if c != ".":
                n = int(c)
                f = field.tiles[i]
                assert f["type"] == Field.AREA and f["player"] == n

    set_field_layout(
        """
000
0.0
000
...
"""
    )

    field.fill_area()

    check_field(
        """
...
.0.
...
...
"""
    )
