from chess.game.game import Game
from chess.game.agent_random import AgentRandom

if __name__ == '__main__':
    a_w = AgentRandom('P1')
    a_b = AgentRandom('P2')
    game = Game(a_w, a_b)
    game.gameplay_loop()