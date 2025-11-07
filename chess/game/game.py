from chess.environment.board import Board
from chess.environment.player import Player
from chess.environment.color import Color
from chess.game.agent import Agent

class Game:
    def __init__(self, agent_white: Agent, agent_black: Agent, display_board=True):
        p_white, p_black = Player(Color.WHITE), Player(Color.BLACK)
        self.board = Board(p_white, p_black)

        self.display_board = display_board
        self.agent_white = agent_white
        self.agent_black = agent_black
        self.agent_white.player = p_white
        self.agent_black.player = p_black
        self.agent_white.board = self.board
        self.agent_black.board = self.board

        self.agents = (self.agent_white, self.agent_black)
        self.n_turns = 0
        self.winner = None
        self.draw = False
        self.stalemate = False


    def gameplay_loop(self):
        self.board.print_board()
        while not self.winner:
            curr_agent = self.agents[self.n_turns % 2]
            if self.display_board:
                print(f"\nCurrent Player: {curr_agent}")

            if self.board.is_stalemate(curr_agent.player):
                print(f"Game ended in stalemate after {self.n_turns} turns")
                self.stalemate = True
                break
            
            curr_agent.act()
            self.board.print_board()

            self.n_turns += 1
            if self.board.is_draw():
                print(f"\nGame ended in draw after {self.n_turns} turns")
                self.draw = True
                break

            if self.board.has_checkmated(curr_agent.player):
                self.winner = curr_agent
                print(f'{self.winner} has checkmated after {self.n_turns} turns')
            
            elif self.board.has_checked(curr_agent.player):
                print(f'{curr_agent} has checked')
            
            print(f"{self.n_turns} turns passed\n")
            
                
