"""
This is the actual agent, it will contain two parts:
- basic part, like move to a certain, or do an opertaion;
- avanced part, the AI brain that make the decision.
"""
from Map import Map

class Agent:
    def __init__(self, board: Map) -> None:
        self.board = board
        self.pos = (board.startpos[0], board.startpos[1])

    def __str__(self) -> str:
        return f"agent current at {self.pos}"

    def __repr__(self) -> str:
        return self.__str__()

    def move(self, dir: int):
        """
        try to move one case to the <dir>
        dir: 0 : right
             1 : down
             2 : left
             3 : up
        """
        if dir == 0:
            if self.pos[0] < self.board.side_len - 1:
                self.pos = (self.pos[0] + 1, self.pos[1])
        elif dir == 1:
            if self.pos[1] < self.board.side_len - 1:
                self.pos = (self.pos[0], self.pos[1] + 1)
        elif dir == 2:
            if self.pos[0] > 0:
                self.pos = (self.pos[0] - 1, self.pos[1])
        elif dir == 3:
            if self.pos[1] > 0:
                self.pos = (self.pos[0], self.pos[1] - 1)
        else:
            raise ValueError

if __name__ == '__main__':
    m = Map(4)
    a = Agent(m)
    print(m)
    print(a)
    a.move(0)
    print(a)
