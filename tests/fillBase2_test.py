from kakomimasu_py import Field, Board


def test_fill2():
    n_agent = 6
    width, height = 8, 8
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

    # Test 1
    set_field_layout(
        """
.00000..
00...00.
0.1..00.
0.....00
0.1...0.
0.....0.
00..000.
.00000..
"""
    )

    field.fill_area()

    check_field(
        """
........
..000...
.0.00...
.00000..
.0.000..
.00000..
..00....
........
"""
    )

    # Test 2
    set_field_layout(
        """
.00000..
00...00.
0.1..00.
0......0
0.1...0.
0.....0.
00..000.
.00000..
"""
    )

    field.fill_area()

    check_field(
        """
........
........
........
........
........
........
........
........
"""
    )

    # Test 3
    set_field_layout(
        """
.00000..
00...00.
0.11100.
0.1.1.00
0.1.1.0.
0.111.0.
00..000.
.00000..
"""
    )

    field.fill_area()

    check_field(
        """
........
..000...
.0......
.0.1.0..
.0.1.0..
.0...0..
..00....
........
"""
    )
