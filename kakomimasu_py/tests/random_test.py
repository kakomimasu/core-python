from ..kkmm import Game, Player, Action, Board
import random
import pytest


def test_random():
    n_agent = 6
    width, height = n_agent * 2, n_agent * 2
    total_turn = 10000
    points = [0 for _ in range(width * height)]
    board = Board(width, height, points, n_agent)

    game = Game(board)
    p1 = Player("test1")
    p2 = Player("test2")
    game.attach_player(p1)
    game.attach_player(p2)
    game.start()

    actions = [Action.PUT, Action.MOVE, Action.REMOVE]

    def get_random_action(agent_number):
        return [
            agent_number,
            random.choice(actions),
            random.randint(0, n_agent - 1),
            random.randint(0, n_agent - 1),
        ]

    def check_agent():
        for i in range(height):
            for j in range(width):
                tile = game.field.get(j, i)
                for p, player in enumerate(game.players):
                    agent_on_tile = sum(
                        1 for a in player.agents if a.x == j and a.y == i
                    )
                    if agent_on_tile > 1:
                        raise AssertionError("Agent conflict!!")
                    if agent_on_tile == 1 and tile["player"] != p:
                        raise AssertionError(
                            f"Illegal field!! {j}x{i} {tile['player']} must be {p}"
                        )

    for i in range(1, total_turn + 1):
        act_p1 = [get_random_action(j) for j in range(n_agent)]
        act_p2 = [get_random_action(j) for j in range(n_agent)]

        p1.set_actions([Action(*a) for a in act_p1])
        p2.set_actions([Action(*a) for a in act_p2])

        game.next_turn()
        check_agent()

