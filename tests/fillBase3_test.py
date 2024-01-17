from kakomimasu_py import Field, Board
import pytest


def test_fill2():
    n_agent = 6
    width, height = 3, 3
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
        for i in range(0, len(s), 2):
            c = Field.WALL if s[i] == "W" else Field.AREA
            n = None if s[i + 1] == "." else int(s[i + 1])
            f = field.tiles[i // 2]
            assert f["type"] == c and f["player"] == n

    set_field_layout(
        """
000
0.0
00.
"""
    )

    field.fill_area()

    check_field(
        """
W0W0W0
W0_.W0
W0W0_.
"""
    )
