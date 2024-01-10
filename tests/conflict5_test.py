from kkmm import Game, Player, Action, Board
from .util import tos


def test_conflict5():
    n_agent = 2
    total_turn = 20
    width, height = 3, 1
    points = [1, 1, 1]
    board = Board(width, height, points, n_agent)

    game = Game(board)
    p1 = Player("test1")
    p2 = Player("test2")
    game.attach_player(p1)
    game.attach_player(p2)
    game.start()

    # put
    p1.set_actions([Action(0, Action.PUT, 0, 0)])
    assert game.next_turn()
    assert tos(game) == "W00 _.. _.."

    # conflict1
    p1.set_actions([Action(0, Action.MOVE, 1, 0), Action(0, Action.MOVE, 2, 0)])
    assert game.next_turn()
    assert tos(game) == "W00 _.. _.."
    actions = game.log[-1]["players"][0]["actions"]
    assert all(a.res == Action.ERR_ONLY_ONE_TURN for a in actions)

    # conflict2
    p1.set_actions([Action(0, Action.MOVE, 2, 0), Action(0, Action.MOVE, 1, 0)])
    assert game.next_turn()
    assert tos(game) == "W00 _.. _.."
    actions = game.log[-1]["players"][0]["actions"]
    assert all(a.res == Action.ERR_ONLY_ONE_TURN for a in actions)

    # conflict3
    p1.set_actions(
        [
            Action(0, Action.MOVE, 2, 0),
            Action(0, Action.MOVE, 1, 0),
            Action(0, Action.MOVE, 3, 0),
        ]
    )
    assert game.next_turn()
    assert tos(game) == "W00 _.. _.."
    actions = game.log[-1]["players"][0]["actions"]
    assert all(a.res == Action.ERR_ONLY_ONE_TURN for a in actions)

    # finish
    while game.next_turn():
        pass
