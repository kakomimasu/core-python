from ..kkmm import Player
import pytest


def test_player_set_actions_before_game_attached():
    p1 = Player("test1")

    # ゲームにアタッチされる前に setActions を呼び出すと例外が発生することを確認
    with pytest.raises(ValueError) as excinfo:
        p1.set_actions([])

    assert "Game is not set" in str(excinfo.value)
