from kakomimasu_py import Game, Player, Action, Board, Field
from .util import tos


def test_conflict3():
    n_agent = 2
    total_turn = 20
    width, height = 3, 1
    points = [0 for _ in range(width * height)]
    board = Board(width, height, points, n_agent)

    game = Game(board)
    p1 = Player("test1")
    p2 = Player("test2")
    game.attach_player(p1)
    game.attach_player(p2)
    game.start()

    # 各シナリオについてのテスト
    # put
    p1.set_actions([Action(0, Action.PUT, 0, 0)])
    p2.set_actions([])
    assert game.next_turn()
    assert tos(game) == "W00 _.. _.."

    # move
    p1.set_actions([Action(0, Action.MOVE, 1, 0)])
    p2.set_actions([])
    assert game.next_turn()
    assert tos(game) == "W0. W00 _.."

    # put conflict myself
    p1.set_actions([Action(1, Action.PUT, 1, 0)])
    p2.set_actions([])
    assert game.next_turn()
    assert tos(game) == "W0. W00 _.."

    # put conflict
    p1.set_actions([])
    p2.set_actions([Action(0, Action.PUT, 0, 0)])
    assert game.next_turn()
    assert tos(game) == "W0. W00 _.."

    # move put conflict myself
    p1.set_actions([Action(0, Action.MOVE, 2, 0), Action(1, Action.PUT, 2, 0)])
    p2.set_actions([])
    assert game.next_turn()
    assert tos(game) == "W0. W00 _.."

    # move put conflict
    p1.set_actions([Action(0, Action.MOVE, 2, 0)])
    p2.set_actions([Action(0, Action.PUT, 2, 0)])
    assert game.next_turn()
    assert tos(game) == "W0. W00 _.."

    # put no conflict
    p1.set_actions([])
    p2.set_actions([Action(0, Action.PUT, 2, 0)])
    assert game.next_turn()
    assert tos(game) == "W0. W00 W11"

    # remove
    p1.set_actions([Action(0, Action.REMOVE, 0, 0)])
    p2.set_actions([])
    assert game.next_turn()
    assert tos(game) == "_.. W00 W11"

    # put
    p1.set_actions([Action(1, Action.PUT, 0, 0)])
    p2.set_actions([])
    assert game.next_turn()
    assert tos(game) == "W00 W00 W11"

    # remove move conflict
    p1.set_actions([Action(0, Action.MOVE, 0, 0), Action(1, Action.REMOVE, 1, 0)])
    p2.set_actions([])
    assert game.next_turn()
    assert tos(game) == "W00 W00 W11"

    # finish
    while game.next_turn():
        pass
