from game.TickTackToe import TickTackToe

class Cursor:
    board_x:int
    board_x:int
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.board_x = None
        self.board_y = None

    def isValid(self) -> bool:
        if self.board_x is None or self.board_y is None:
            return False
        else:
            return True
    
    def moveTo(self, y, x) -> bool:
        if (x<0 or 2<x) or (y<0 or 2<y):
            return False
        else:
            self.boardX = x
            self.boardY = y
            return True

class SuperTickTackToe():
    hyper_board:TickTackToe
    sub_boards:[[TickTackToe]]
    player_count:int = 0
    cursor:Cursor

    def __init__(self) -> None:
        self.hyper_board = TickTackToe()
        self.sub_boards = [[TickTackToe() for _ in range(3)] for _ in range(3)]
        self.cursor = Cursor()
    
    def __repr__(self) -> str:
        out = ""
        out += f"Hyper Board:\n{self.hyper_board}\n\nSub Boards:\n"
        for row in range(len(self.sub_boards)):
            for col in range(len(self.sub_boards[row])):
                out+= f"({row}, {col}):\n{self.sub_boards[row][col]}\n"
            out += "\n"
        out += "\n"
        return out

    def getNextMark(self) -> int:
        if self.player_count < 2:
            self.player_count+=1
            return self.player_count
        else:
            print("Only Two players there may be, no more no less")
    
    def selectBoard(self, y:int, x:int) -> bool:
        if (not self.cursor.isValid()) and self.hyper_board[y][x] == 0:
            self.cursor.moveTo(y, x)
            return True
        else:
            return False
        
    # (did the move work, did the sub_board win, who won the super game)
    def placeMark(self, mark:int, y:int, x:int) -> (bool, bool, int):
        valid_move = False
        sub_winner = False
        super_winner = 0

        if not self.cursor.isValid():
            return (valid_move, sub_winner, super_winner)
        (worked, winner) = self.sub_boards[self.cursor.board_y][self.cursor.board_x].placeMark(mark, y, x)
        if not worked:
            return (valid_move, sub_winner, super_winner)
        else:
            valid_move = True
            # update the hyper game
            if winner:
                sub_winner = True
                # update hyper board
                (should_have_worked, super_winner) = self.hyper_board.placeMark(mark,self.cursor.board_y, self.cursor.board_x)
                if not should_have_worked: raise RuntimeError("Hyper Game tried to place a mark where it shouldn't've")

                if super_winner != 0:
                    return (valid_move, sub_winner, super_winner)
            # move cursor to new sub board or make invalid
            if self.hyper_board[y][x] == 0:
                self.cursor.moveTo(y, x)
            else:
                self.cursor.reset()
