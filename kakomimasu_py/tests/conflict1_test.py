from ..kkmm import Game, Player, Action, Board
from .util import tos


def test_conflict1():
    n_agent = 6
    width, height = 3, 1
    total_turn = 20
    points = [0 for _ in range(width * height)]
    board = Board(width, height, points, n_agent, total_turn)

    game = Game(board)
    p1 = Player("test1")
    p2 = Player("test2")
    game.attach_player(p1)
    game.attach_player(p2)
    game.start()

    # put
    p1.set_actions([Action(0, Action.PUT, 0, 0)])
    p2.set_actions([Action(0, Action.PUT, 2, 0)])
    assert game.next_turn()
    assert tos(game) == "W00 _.. W11"

    # move conflict
    p1.set_actions([Action(0, Action.MOVE, 1, 0)])
    p2.set_actions([Action(0, Action.MOVE, 1, 0)])
    assert game.next_turn()
    assert tos(game) == "W00 _.. W11"

    # put move conflict
    p1.set_actions([Action(1, Action.PUT, 1, 0)])
    p2.set_actions([Action(0, Action.MOVE, 1, 0)])
    assert game.next_turn()
    assert tos(game) == "W00 _.. W11"

    # move no conflict
    p1.set_actions([Action(0, Action.MOVE, 1, 0)])
    p2.set_actions([])
    assert game.next_turn()
    assert tos(game) == "W0. W00 W11"

    # move no conflict
    p1.set_actions([Action(0, Action.MOVE, 0, 0)])
    p2.set_actions([])
    assert game.next_turn()
    assert tos(game) == "W00 W0. W11"

    # move remove conflict
    p1.set_actions([Action(0, Action.MOVE, 1, 0)])
    p2.set_actions([Action(0, Action.REMOVE, 1, 0)])
    assert game.next_turn()
    assert tos(game) == "W00 W0. W11"

    # remove no conflict
    p1.set_actions([])
    p2.set_actions([Action(0, Action.REMOVE, 1, 0)])
    assert game.next_turn()
    assert tos(game) == "W00 _.. W11"

    # move no conflict
    p1.set_actions([])
    p2.set_actions([Action(0, Action.MOVE, 1, 0)])
    assert game.next_turn()
    assert tos(game) == "W00 W11 W1."

    # remove failed
    p1.set_actions([])
    p2.set_actions([Action(0, Action.REMOVE, 0, 0)])
    assert game.next_turn()
    assert tos(game) == "W00 W11 W1."

    # move failed
    p1.set_actions([])
    p2.set_actions([Action(0, Action.MOVE, 0, 0)])
    assert game.next_turn()
    assert tos(game) == "W00 W11 W1."

    # cross move failed
    p1.set_actions([Action(0, Action.MOVE, 1, 0)])
    p2.set_actions([Action(0, Action.MOVE, 0, 0)])
    assert game.next_turn()
    assert tos(game) == "W00 W11 W1."

    # finish
    while game.next_turn():
        pass
