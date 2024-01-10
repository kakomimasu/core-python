def tos(game):
    def is_on_agent(p, x, y):
        cnt = sum(1 for a in game.players[p].agents if a.x == x and a.y == y)
        if cnt == 1:
            return True
        elif cnt == 0:
            return False
        else:
            raise AssertionError("Agent conflict!! cnt: " + str(cnt))

    res = []
    for i in range(game.field.height):
        s = []
        for j in range(game.field.width):
            n = game.field.get(j, i)
            a0 = is_on_agent(0, j, i)
            a1 = is_on_agent(1, j, i)
            if a0 and a1:
                raise AssertionError("Agent conflict!!")
            a = "0" if a0 else ("1" if a1 else ".")
            s.append(
                f"{['_', 'W'][n['type']]}{n['player'] if n['player'] is not None else '.'}{a}"
            )
        res.append(" ".join(s))
    return "\n".join(res)
