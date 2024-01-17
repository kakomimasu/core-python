from ..kkmm import Field, Board
import pytest


def test_field_set_invalid_playerid():
    width, height = 3, 1
    points = [0 for _ in range(width * height)]

    field = Field(width=width, height=height, points=points)

    # 無効なプレイヤーIDを設定しようとしたときに例外が投げられるかをテスト
    with pytest.raises(ValueError):
        field.set(0, 0, Field.WALL, -1)


def test_field_invalid_points_length():
    # pointsの長さが無効である場合に例外が投げられるかをテスト
    with pytest.raises(ValueError):
        Field(width=3, height=3, points=[0, 0])  # 長さが不十分
