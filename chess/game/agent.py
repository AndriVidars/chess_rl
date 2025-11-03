from abc import abstractmethod
from chess.environment.board import Board
from chess.environment.player import Player

class Agent:
    def __init__(self, name: str):
        self.name = name
        self.board = None
        self.player = None

    @abstractmethod
    def act(self):
        pass
    
    def __str__(self):
        return f"{self.name} - {self.player.color}"