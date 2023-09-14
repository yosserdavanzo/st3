from typing import Any
from game.TickTackToe import TickTackToe
import numpy as np
import pygame
import gymnasium as gym
from gymnasium import spaces

class Cursor():
    board_x:int
    board_y:int
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
            self.board_y = y
            self.board_x = x
            return True

class SuperTickTackToe(gym.Env):
    ##############################################################
    #### Vars
    # pygame

    # gym env
    metadata = {"render_modes": ["rgb_array", "human"], "render_fps": 4}
    # The 9 actions are 9 hyper grid selectors, and 9 subgrid selectors 
    action_space = spaces.Discrete(9)
    
    # st3
    hyper_board:TickTackToe
    sub_boards:[[TickTackToe]]
    player_count:int = 0
    cursor:Cursor


    ##############################################################
    #### Dunders

    def __init__(self, render_mode=None, size=3) -> None:
        # Pygame data
        self.size = size
        self.window_size = 1800
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.window = None
        self.clock = None

        self.player1Color = pygame.Color(255, 0, 0)
        self.player2Color = pygame.Color(0, 0, 255)

        self.hyper_board = TickTackToe()
        self.sub_boards = [[TickTackToe() for _ in range(3)] for _ in range(3)]
        self.cursor = Cursor()
    
    def textRepr(self) -> str:
        out = ""
        out += f"Hyper Board:\n{self.hyper_board}\n\nSub Boards:\n"
        for row in range(len(self.sub_boards)):
            for col in range(len(self.sub_boards[row])):
                out+= f"({row}, {col}):\n{self.sub_boards[row][col]}\n"
            out += "\n"
        out += "\n"
        return out


    ##############################################################
    #### Actions

    def getNextMark(self) -> int:
        if self.player_count < 2:
            self.player_count+=1
            return self.player_count
        else:
            print("Only Two players there may be, no more no less")
    
    def selectBoard(self, y:int, x:int) -> bool:
        if (not self.cursor.isValid()) and self.hyper_board.board[y][x] == 0:
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
                # store the super winner
                (should_have_worked, super_winner) = self.hyper_board.placeMark(mark,self.cursor.board_y, self.cursor.board_x)
                # double check for weird states
                if not should_have_worked: raise RuntimeError("Hyper Game tried to place a mark where it shouldn't've")

            # move cursor to new sub board or make invalid
            if self.hyper_board.board[y][x] == 0:
                self.cursor.moveTo(y, x)
            else:
                self.cursor.reset()
            return (valid_move, sub_winner, super_winner)

    ##############################################################
    #### Drawing and Rendering

    def drawBoard(self, canvas, board:TickTackToe, y_0:int,  x_0:int, y_f:int, x_f:int, width=1):
        y_diff = y_f - y_0
        x_diff = x_f - x_0

        x_segment = x_diff//3
        y_segment = y_diff//3

        # Draw lines
        for i in range(1,3):
            pygame.draw.line(
                canvas, 
                0,
                (y_0, x_0 + (i*x_segment)),
                (y_f, x_0 + (i*x_segment)),
                width=width
            )
            pygame.draw.line(
                canvas, 
                0,
                (y_0 + (i*y_segment), x_0),
                (y_0 + (i*y_segment), x_f),
                width=width
            )

        # Draw marks
        y_mid_segment = y_segment//2
        x_mid_segment = x_segment//2
        for i in range(len(board.board)):
            for j in range(len(board.board[i])):
                mark = board.board[i][j]
                if mark:
                    color = self.player1Color if mark == 1 else self.player2Color
                    y_c = y_0 + (i * y_segment) + y_mid_segment
                    x_c = x_0 + (j * x_segment) + x_mid_segment
                    pygame.draw.circle(canvas, color, (x_c, y_c), y_mid_segment)
        
    def drawCursor(self, canvas):
        if not self.cursor.isValid():
            return
        yellow = (240,230,140)
        segment_width = self.window_size // 3
        y0 = self.cursor.board_y * segment_width
        x0 = self.cursor.board_x * segment_width

        pygame.draw.rect(canvas, yellow, ( x0, y0, segment_width, segment_width), width=9)

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()
    
    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode(
                (self.window_size, self.window_size)
            )
        
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()
        
        canvas = pygame.Surface((self.window_size, self.window_size))
        canvas.fill((255, 255, 255))

        ## Draw the board
        # Hyper Board
        self.drawBoard(canvas, self.hyper_board, 0, 0, self.window_size, self.window_size, width=9)

        self.drawCursor(canvas)
        # Sub Boards
        buffer = 20
        segment = self.window_size//3
        for i in range(3):
            i_0 = i*segment + buffer
            i_f = i_0 + segment - buffer
            for j in range(3):
                j_0 = j*segment + buffer 
                j_f = j_0 + segment - buffer
                self.drawBoard(canvas,self.sub_boards[i][j], i_0, j_0, i_f, j_f)

        # Send up the frame we rendered
        if self.render_mode == "human":
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        else:
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes = (1,0,2)
            )


    ##############################################################
    #### Gymnasium
    def _get_obs(self):
        return
    
    def _get_info(self):
        return

    def reset(self, *, seed: int | None = None, options: dict[str, Any] | None = None) -> tuple[Any, dict[str, Any]]:
        super().reset(seed=seed, options=options)

        self.__init__(self.render_mode, self.size)
        obs = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()
        
        return obs, info
