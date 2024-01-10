from kkmm import Game, Player, Action, Board
from .util import tos


def test_action_none():
    width, height = 3, 1
    points = [0 for _ in range(width * height)]
    board = Board(width, height, points)

    game = Game(board)
    p1 = Player("test1")
    p2 = Player("test2")
    game.attach_player(p1)
    game.attach_player(p2)
    game.start()

    p1.set_actions([Action(0, Action.NONE, 0, 0)])
    assert game.next_turn()
    assert tos(game) == "_.. _.. _.."


def test_action_remove_check_on_board():
    width, height = 3, 1
    points = [0 for _ in range(width * height)]
    board = Board(width, height, points)

    game = Game(board)
    p1 = Player("test1")
    p2 = Player("test2")
    game.attach_player(p1)
    game.attach_player(p2)
    game.start()

    p1.set_actions([Action(0, Action.PUT, 2, 0)])
    assert game.next_turn()
    assert tos(game) == "_.. _.. W00"

    action = Action(0, Action.REMOVE, 3, 0)
    p1.set_actions([action])
    assert game.next_turn()
    assert action.res == Action.ERR_ILLEGAL_ACTION
    assert tos(game) == "_.. _.. W00"
