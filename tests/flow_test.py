from kakomimasu_py import Game, Player, Action, Board
import pytest


def test_flow():
    width, height = 8, 8
    points = list(range(width * height))
    n_agent = 6
    total_turn = 10
    board = Board(width, height, points, n_agent, total_turn=total_turn)

    game = Game(board)
    p1 = Player("test1")
    p2 = Player("test2")
    game.attach_player(p1)
    game.attach_player(p2)
    game.start()

    while True:
        p1.set_actions([Action(0, Action.PUT, 1, 1), Action(0, Action.MOVE, 2, 2)])
        p2.set_actions(
            [
                Action(0, Action.PUT, 1, 1),
                Action(1, Action.PUT, 1, 2),
                Action(2, Action.PUT, 1, 3),
                Action(10, Action.PUT, 2, 2),
            ]
        )
        if not game.next_turn():
            break

    assert len(game.log) == total_turn
    final_points = [vars(a["point"]) for a in game.log[-1]["players"]]
    assert final_points == [
        {"area_point": 0, "wall_point": 0},
        {"area_point": 0, "wall_point": 51},
    ]
