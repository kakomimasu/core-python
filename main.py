from typing import List
from kkmm import Game, Player, Action  # 仮のモジュール名を game_module としています

# ボードの設定
width = 8
height = 8
points = [i for i in range(width * height)]  # Pythonのリスト内包表記を使用
n_agent = 6
total_turn = 10
board = {
    "width": width,
    "height": height,
    "points": points,
    "n_agent": n_agent,
    "total_turn": total_turn,
}

# ゲームとプレイヤーの初期化
game = Game(total_turn, width, height, points, n_agent, 2)  # Playerの数は2としています
p1 = Player("test1")
p2 = Player("test2")
game.attach_player(p1)
game.attach_player(p2)
game.start()

# ゲームのターン処理
while True:
    p1_actions = [
        Action(0, Action.PUT, 1, 1),
        Action(0, Action.MOVE, 2, 2),
    ]
    p2_actions = [
        Action(0, Action.PUT, 1, 1),
        Action(1, Action.PUT, 1, 2),
    ]
    p1.set_actions(p1_actions)
    p2.set_actions(p2_actions)

    if not game.next_turn():
        break

# ゲーム状態の出力
print(game.field.tiles)
