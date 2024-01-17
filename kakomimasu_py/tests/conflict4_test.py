from ..kkmm import Game, Player, Action, Board, Field
from .util import tos


def test_conflict4():
    n_agent = 2
    total_turn = 30
    width, height = 3, 2
    points = [0 for _ in range(width * height)]
    board = Board(width, height, points, n_agent)

    game = Game(board)
    p1 = Player("test1")
    p2 = Player("test2")
    game.attach_player(p1)
    game.attach_player(p2)
    game.start()

    # put
    p1.set_actions([Action(0, Action.PUT, 0, 0), Action(1, Action.PUT, 1, 1)])
    p2.set_actions([Action(0, Action.PUT, 1, 0)])
    assert game.next_turn()
    assert tos(game) == "W00 W11 _..\n_.. W00 _.."

    # move
    p2.set_actions([Action(0, Action.MOVE, 2, 0)])
    assert game.next_turn()
    assert tos(game) == "W00 W1. W11\n_.. W00 _.."

    # remove move conflict
    p1.set_actions([Action(0, Action.REMOVE, 1, 0), Action(1, Action.MOVE, 1, 0)])
    assert game.next_turn()
    assert tos(game) == "W00 _.. W11\n_.. W00 _.."

    # move
    p1.set_actions([Action(0, Action.MOVE, 1, 0)])
    assert game.next_turn()
    assert tos(game) == "W0. W00 W11\n_.. W00 _.."

    # move remove conflict myself
    p1.set_actions([Action(0, Action.MOVE, 0, 0), Action(0, Action.REMOVE, 0, 0)])
    assert game.next_turn()
    assert tos(game) == "W0. W00 W11\n_.. W00 _.."

    # finish
    while game.next_turn():
        pass
