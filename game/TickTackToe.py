import numpy as np

class TickTackToe():
    board:[[int]]

    def __init__(self) -> None:
        self.board = [[0 for _ in range(3)] for _ in range(3)]

    def __repr__(self) -> str:
        out = ""
        for row in self.board:
            out+=(str(row) + "\n")
        return out

    def liniarize(self):
        out = np.array([], dtype=np.int8)
        for row in self.board:
            np.append(out, row)
        return out

    def _checkForWinner(self)-> int:
        # Top Left Group
        top_left = self.board[0][0]
        # Top row
        # Left col
        # \ Diag
        if ((top_left == self.board[0][1]) and (top_left == self.board[0][2])) or \
            ((top_left == self.board[1][0]) and (top_left == self.board[2][0])) or \
            ((top_left == self.board[1][1]) and (top_left == self.board[2][2])):
            return top_left
        
        # Mid Group
        mid = self.board[1][1]
        # Center Row
        # Center Col
        # / Diag
        if ((mid == self.board[1][0]) and (mid == self.board[1][2])) or \
            ((mid == self.board[0][1]) and (mid == self.board[0][1])) or \
            ((mid == self.board[2][2]) and (mid == self.board[2][0])):
            return mid
        
        # Bottom Left Group
        bottom_left = self.board[2][2]
        # Bottom Row
        # Right Col
        if ((bottom_left == self.board[2][0]) and (bottom_left == self.board[2][1])) or \
            ((bottom_left == self.board[0][2]) and (bottom_left == self.board[1][2])):
            return bottom_left
        
        return 0
        
    def placeMark(self, mark:int, y:int, x:int) -> (bool,int):
        # check if it's a valid move
        if self.board[y][x] != 0:
            return (False, None)
        
        self.board[y][x] = mark
        winner = self._checkForWinner()
        return (True, winner)

