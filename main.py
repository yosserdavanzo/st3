from game.SuperTickTackToe import SuperTickTackToe
from game.Player import Player

st3 = SuperTickTackToe(render_mode="human")
player1 = Player(st3)
player2 = Player(st3)
selectedBoard = st3.selectBoard(0, 0)
marked = st3.placeMark(1,0, 0)
marked2 = st3.placeMark(2, 0,1)
print(st3.textRepr())
st3._render_frame()

print("Hold")

