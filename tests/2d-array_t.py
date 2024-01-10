from kkmm import Game, Player, Action, Board

# def test_2d_array(obj, prev_key="", prev_value=None):
#     if not isinstance(obj, dict):
#         return
#     for k, v in obj.items():
#         if isinstance(v, dict):
#             test_2d_array(v, prev_key=k, prev_value=v)
#         elif isinstance(v, list):
#             if isinstance(prev_value, list):
#                 raise ValueError(f"Found 2d-array: {prev_key}")
#             else:
#                 test_2d_array(v, prev_key=k, prev_value=v)


def test_two_dimensional_array_check():
    width = 8
    height = 8
    points = list(range(width * height))
    n_agent = 6
    total_turn = 10
    board = Board(width, height, points, n_agent, total_turn=total_turn)

    game = Game(total_turn, width, height, points, n_agent, 2)
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

    final_points = [vars(log_p["point"]) for log_p in game.log[-1]["players"]]
    assert final_points == [
        {"area_point": 0, "wall_point": 0},
        {"area_point": 0, "wall_point": 51},
    ]

    # log = game  # Assuming game can be treated as a serializable object
    # test_2d_array(log)
