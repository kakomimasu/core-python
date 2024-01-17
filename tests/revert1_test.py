from ..kkmm import Game, Player, Action, Board
import pytest


def test_revert1():
    n_agent = 6
    width, height = 3, 1
    total_turn = 20
    points = [0 for _ in range(width * height)]
    board = Board(width, height, points, n_agent)

    game = Game(board)
    p1 = Player("test1")
    p2 = Player("test2")
    game.attach_player(p1)
    game.attach_player(p2)
    game.start()

    def tos():
        res = []
        for i in range(height):
            s = []
            for j in range(width):
                tile = game.field.get(j, i)
                a0 = any(a.x == j and a.y == i for a in game.players[0].agents)
                a1 = any(a.x == j and a.y == i for a in game.players[1].agents)
                a = "0" if a0 else ("1" if a1 else ".")
                s.append(
                    f"{['_', 'W'][tile['type']]}{tile['player'] if tile['player'] is not None else '.'}{a}"
                )
            res.append(" ".join(s))
        return "\n".join(res)

    # put
    p1.set_actions([Action(0, Action.PUT, 0, 0), Action(1, Action.PUT, 1, 0)])
    assert game.next_turn()
    assert tos() == "W00 W00 _.."

    # move x2
    p1.set_actions([Action(0, Action.MOVE, 1, 0), Action(1, Action.MOVE, 2, 0)])
    assert game.next_turn()
    assert tos() == "W0. W00 W00"

    # move x2 revert
    p1.set_actions([Action(0, Action.MOVE, 2, 0), Action(1, Action.MOVE, 3, 0)])
    assert game.next_turn()
    assert tos() == "W0. W00 W00"

    # finish
    while game.next_turn():
        pass
