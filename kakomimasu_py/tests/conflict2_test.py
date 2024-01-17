from ..kkmm import Game, Player, Action, Board
from .util import tos


def test_conflict2():
    n_agent = 6
    width, height = 3, 3
    total_turn = 20
    points = [0 for _ in range(width * height)]
    board = Board(width, height, points, n_agent)

    game = Game(board)
    p1 = Player("test1")
    p2 = Player("test2")
    game.attach_player(p1)
    game.attach_player(p2)
    game.start()

    # put
    p1.set_actions(
        [
            Action(0, Action.PUT, 0, 0),
            Action(1, Action.PUT, 0, 1),
            Action(2, Action.PUT, 0, 2),
        ]
    )
    p2.set_actions(
        [
            Action(0, Action.PUT, 2, 0),
            Action(1, Action.PUT, 2, 1),
            Action(2, Action.PUT, 2, 2),
        ]
    )
    assert game.next_turn()
    assert tos(game) == "W00 _.. W11\nW00 _.. W11\nW00 _.. W11"

    # move conflict
    p1.set_actions(
        [
            Action(0, Action.MOVE, 1, 1),
            Action(1, Action.MOVE, 1, 1),
            Action(2, Action.MOVE, 1, 1),
        ]
    )
    p2.set_actions(
        [
            Action(0, Action.MOVE, 1, 1),
            Action(1, Action.MOVE, 1, 1),
            Action(2, Action.MOVE, 1, 1),
        ]
    )
    assert game.next_turn()
    assert tos(game) == "W00 _.. W11\nW00 _.. W11\nW00 _.. W11"

    # move remove put conflict
    p1.set_actions(
        [
            Action(0, Action.MOVE, 1, 1),
            Action(1, Action.REMOVE, 1, 1),
            Action(2, Action.REMOVE, 1, 1),
            Action(3, Action.PUT, 1, 1),
        ]
    )
    p2.set_actions(
        [
            Action(0, Action.MOVE, 1, 1),
            Action(1, Action.REMOVE, 1, 1),
            Action(2, Action.MOVE, 1, 1),
            Action(3, Action.PUT, 1, 1),
        ]
    )
    assert game.next_turn()
    assert tos(game) == "W00 _.. W11\nW00 _.. W11\nW00 _.. W11"

    # move no conflict
    p1.set_actions(
        [
            Action(0, Action.MOVE, 1, 0),
            Action(1, Action.MOVE, 1, 1),
            Action(2, Action.MOVE, 1, 2),
        ]
    )
    p2.set_actions([])
    assert game.next_turn()
    assert tos(game) == "W0. W00 W11\nW0. W00 W11\nW0. W00 W11"

    # move no other wall and agent
    p1.set_actions(
        [
            Action(0, Action.MOVE, 2, 0),
            Action(1, Action.MOVE, 2, 1),
            Action(2, Action.MOVE, 2, 2),
        ]
    )
    p2.set_actions([])
    assert game.next_turn()
    assert tos(game) == "W0. W00 W11\nW0. W00 W11\nW0. W00 W11"

    # finish
    while game.next_turn():
        pass
