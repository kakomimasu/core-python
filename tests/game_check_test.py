from kakomimasu_py import Game, Player, Board
import pytest


def test_game_too_much_attach():
    width, height = 3, 1
    points = [0 for _ in range(width * height)]
    board = Board(width, height, points)

    game = Game(board)

    assert game.attach_player(Player("test1")) == True
    assert game.attach_player(Player("test2")) == True
    assert game.attach_player(Player("test3")) == False


def test_game_attach_same_player():
    width, height = 3, 1
    points = [0 for _ in range(width * height)]
    board = Board(width, height, points)

    game = Game(board)
    p = Player("test1")

    assert game.attach_player(p) == True
    assert game.attach_player(p) == False


def test_game_status_check():
    width, height = 3, 1
    points = [0 for _ in range(width * height)]
    board = Board(width, height, points)

    game = Game(board)

    def check_status(is_free, is_ready, is_gaming, is_ended):
        assert game.is_free() == is_free
        assert game.is_ready() == is_ready
        assert game.is_gaming() == is_gaming
        assert game.is_ended() == is_ended

    check_status(True, False, False, False)
    game.attach_player(Player("test1"))
    check_status(True, False, False, False)
    game.attach_player(Player("test2"))
    check_status(False, True, False, False)
    game.start()
    check_status(False, False, True, False)
    while game.next_turn():
        check_status(False, False, True, False)
    check_status(False, False, False, True)
