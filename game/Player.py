from game.SuperTickTackToe import SuperTickTackToe
class Player():
    mark:int
    board:SuperTickTackToe
    def __init__(self, board:SuperTickTackToe) -> None:
        self.board = board
        self.mark = self.board.getNextMark()

    