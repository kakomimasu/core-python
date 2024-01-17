from kakomimasu_py import Game, Player, Action, Board, Field
import pytest


def prepare():
    width, height = 3, 3
    points = list(range(width * height))
    n_agent = 9
    board = Board(width, height, points, n_agent, total_turn=30)

    game = Game(board)
    p1 = Player("test1")
    p2 = Player("test2")
    game.attach_player(p1)
    game.attach_player(p2)
    game.start()
    return game, p1, p2


def test_action_put():
    game, p1, _ = prepare()
    p1.set_actions([Action(0, Action.PUT, 0, 0)])
    game.next_turn()
    assert game.field.tiles[0] == {"type": Field.WALL, "player": 0}


def test_action_cant_put():
    game, p1, _ = prepare()
    p1.set_actions([Action(0, Action.PUT, 1000, 0)])
    game.next_turn()
    assert game.field.tiles[0] == {"type": Field.AREA, "player": None}
    assert game.log[0]["players"][0]["actions"][0].res == Action.ERR_ILLEGAL_ACTION


def test_action_move():
    game, p1, _ = prepare()
    p1.set_actions([Action(0, Action.PUT, 0, 0)])
    game.next_turn()
    p1.set_actions([Action(0, Action.MOVE, 1, 0)])
    game.next_turn()
    assert game.field.tiles[0] == {"type": Field.WALL, "player": 0}


def test_action_move_series():
    game, p1, _ = prepare()
    p1.set_actions([Action(0, Action.PUT, 0, 0), Action(1, Action.PUT, 1, 0)])
    game.next_turn()
    p1.set_actions([Action(0, Action.MOVE, 1, 0), Action(1, Action.MOVE, 2, 0)])
    game.next_turn()
    assert game.field.tiles[2] == {"type": Field.WALL, "player": 0}


def test_action_cant_move_series():
    game, p1, p2 = prepare()
    p1.set_actions([Action(0, Action.PUT, 0, 0), Action(1, Action.PUT, 1, 0)])
    game.next_turn()
    p1.set_actions([Action(0, Action.MOVE, 1, 0), Action(1, Action.MOVE, 2, 0)])
    p2.set_actions([Action(0, Action.PUT, 2, 0)])
    game.next_turn()
    assert game.field.tiles[2] == {"type": Field.AREA, "player": None}


def test_action_cant_move():
    game, p1, _ = prepare()
    p1.set_actions([Action(0, Action.PUT, 0, 0)])
    game.next_turn()
    p1.set_actions([Action(0, Action.MOVE, 2, 0)])
    game.next_turn()
    assert game.field.tiles[2] == {"type": Field.AREA, "player": None}
    assert game.log[1]["players"][0]["actions"][0].res == Action.ERR_ILLEGAL_ACTION


def test_fill():
    game, p1, _ = prepare()
    p1.set_actions(
        [
            Action(0, Action.PUT, 0, 0),
            Action(1, Action.PUT, 1, 0),
            Action(2, Action.PUT, 2, 0),
            Action(3, Action.PUT, 0, 1),
            Action(4, Action.PUT, 2, 1),
            Action(5, Action.PUT, 0, 2),
            Action(6, Action.PUT, 1, 2),
            Action(7, Action.PUT, 2, 2),
        ]
    )
    game.next_turn()
    assert game.field.tiles[4] == {"type": Field.AREA, "player": 0}


def test_action_remove():
    game, p1, _ = prepare()
    p1.set_actions([Action(0, Action.PUT, 0, 0)])
    game.next_turn()
    assert game.field.tiles[0] == {"type": Field.WALL, "player": 0}
    p1.set_actions([Action(0, Action.MOVE, 1, 0)])
    game.next_turn()
    p1.set_actions([Action(0, Action.REMOVE, 0, 0)])
    game.next_turn()
    assert game.field.tiles[0] == {"type": Field.AREA, "player": None}


def test_action_cant_remove():
    game, p1, _ = prepare()
    p1.set_actions([Action(0, Action.PUT, 0, 0)])
    game.next_turn()
    p1.set_actions([Action(0, Action.REMOVE, 1, 0)])
    game.next_turn()
    assert game.field.tiles[1] == {"type": Field.AREA, "player": None}
    assert game.log[1]["players"][0]["actions"][0].res == Action.ERR_ILLEGAL_ACTION


def test_wall_point():
    game, p1, _ = prepare()
    p1.set_actions([Action(0, Action.PUT, 1, 0), Action(1, Action.PUT, 2, 0)])
    game.next_turn()
    assert vars(game.log[0]["players"][0]["point"]) == {
        "area_point": 0,
        "wall_point": 1 + 2,
    }


def test_area_point():
    game, p1, _ = prepare()
    p1.set_actions(
        [
            Action(0, Action.PUT, 0, 0),
            Action(1, Action.PUT, 1, 0),
            Action(2, Action.PUT, 2, 0),
            Action(3, Action.PUT, 0, 1),
            Action(4, Action.PUT, 2, 1),
            Action(5, Action.PUT, 0, 2),
            Action(6, Action.PUT, 1, 2),
            Action(7, Action.PUT, 2, 2),
        ]
    )
    game.next_turn()
    status = game
    assert status.field.tiles[4] == {"type": Field.AREA, "player": 0}
    assert vars(game.log[0]["players"][0]["point"]) == {
        "area_point": 4,
        "wall_point": 0 + 1 + 2 + 3 + 5 + 6 + 7 + 8,
    }


def test_remove_on_agent():
    game, p1, p2 = prepare()
    p1.set_actions([Action(0, Action.PUT, 0, 0)])
    p2.set_actions([Action(0, Action.PUT, 1, 0)])
    game.next_turn()
    p1.set_actions([Action(0, Action.REMOVE, 1, 0)])
    game.next_turn()
    assert game.field.tiles[1] == {"type": Field.WALL, "player": 1}
    assert game.log[1]["players"][0]["actions"][0].res == Action.REVERT


def test_conflict_put():
    game, p1, p2 = prepare()
    p1.set_actions([Action(0, Action.PUT, 0, 0)])
    p2.set_actions([Action(0, Action.PUT, 0, 0)])
    game.next_turn()
    assert game.field.tiles[0] == {"type": Field.AREA, "player": None}
    assert game.log[0]["players"][0]["actions"][0].res == Action.CONFLICT
    assert game.log[0]["players"][1]["actions"][0].res == Action.CONFLICT


def test_conflict_move():
    game, p1, p2 = prepare()
    p1.set_actions([Action(0, Action.PUT, 0, 0)])
    p2.set_actions([Action(0, Action.PUT, 2, 0)])
    game.next_turn()
    p1.set_actions([Action(0, Action.MOVE, 1, 0)])
    p2.set_actions([Action(0, Action.MOVE, 1, 0)])
    game.next_turn()
    assert game.field.tiles[1] == {"type": Field.AREA, "player": None}
    assert game.log[1]["players"][0]["actions"][0].res == Action.CONFLICT
    assert game.log[1]["players"][1]["actions"][0].res == Action.CONFLICT


def test_conflict_remove():
    game, p1, p2 = prepare()
    p1.set_actions([Action(0, Action.PUT, 0, 0)])
    p2.set_actions(
        [
            Action(0, Action.PUT, 2, 0),
            Action(1, Action.PUT, 1, 0),
        ]
    )
    game.next_turn()
    p2.set_actions([Action(1, Action.MOVE, 1, 1)])
    assert game.field.tiles[1] == {"type": Field.WALL, "player": 1}
    game.next_turn()
    p1.set_actions([Action(0, Action.REMOVE, 1, 0)])
    p2.set_actions([Action(0, Action.REMOVE, 1, 0)])
    game.next_turn()
    assert game.field.tiles[1] == {"type": Field.WALL, "player": 1}
    assert game.log[2]["players"][0]["actions"][0].res == Action.CONFLICT
    assert game.log[2]["players"][1]["actions"][0].res == Action.CONFLICT


def test_conflict_remove_move():
    game, p1, p2 = prepare()
    p1.set_actions([Action(0, Action.PUT, 0, 0)])
    p2.set_actions([Action(0, Action.PUT, 2, 0)])
    game.next_turn()
    p1.set_actions([Action(0, Action.REMOVE, 1, 0)])
    p2.set_actions([Action(0, Action.MOVE, 1, 0)])
    game.next_turn()
    assert game.field.tiles[1] == {"type": Field.WALL, "player": 1}
    assert game.log[1]["players"][0]["actions"][0].res == Action.ERR_ILLEGAL_ACTION
    assert game.log[1]["players"][1]["actions"][0].res == Action.SUCCESS


def test_conflict_remove_move2():
    game, p1, p2 = prepare()
    p1.set_actions([Action(0, Action.PUT, 0, 0)])
    game.next_turn()
    p1.set_actions([Action(0, Action.REMOVE, 1, 0)])
    p2.set_actions([Action(0, Action.PUT, 1, 0)])
    game.next_turn()
    assert game.field.tiles[1] == {"type": Field.WALL, "player": 1}
    assert game.log[1]["players"][0]["actions"][0].res == Action.ERR_ILLEGAL_ACTION
    assert game.log[1]["players"][1]["actions"][0].res == Action.SUCCESS
