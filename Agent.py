"""
This is the actual agent, it will contain two parts:
- basic part, like move to a certain, or do an opertaion;
- avanced part, the AI brain that make the decision.
"""
from itertools import product

from Map import Map

class Agent:
    def __init__(self, board: Map) -> None:
        self.board = board
        self.pos = (board.startpos[0], board.startpos[1])
        self.list_past_pos = [self.pos, ]

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

        self.list_past_pos.append(self.pos)

    def legal_moves(self):
        """
        return a list of all legal move directions,
        these directions should be appliable using the function `move`
        """
        ret = list()
        if self.pos[0] < self.board.side_len - 1:
            ret.append(0)
        if self.pos[1] < self.board.side_len - 1:
            ret.append(1)
        if self.pos[0] > 0:
            ret.append(2)
        if self.pos[1] > 0:
            ret.append(3);
        return ret

    def detect(self, coord, detector):
        """
        detect the coordinate `coord` using a given detector.
        0: smell
        1: wind
        2: light
        """
        val = False
        if detector not in range(2):
            raise RuntimeError(f"Unexpected detector id {detector}, should be between 0 and 2")
        if detector == 0:
            val = self.board.is_has_smell(coord)
        elif detector == 1:
            val = self.board.is_windy(coord)
        else:
            val = self.board.is_has_light(coord)
        return val

    def detectable_coords(self):
        """
        return a list of coords based on current position
        """
        legal_moves = self.legal_moves()
        list_coord_x = [self.pos[0], ]
        list_coord_y = [self.pos[1], ]
        if 0 in legal_moves:
            list_coord_x.append(self.pos[0] + 1)
        if 1 in legal_moves:
            list_coord_y.append(self.pos[1] + 1)
        if 2 in legal_moves:
            list_coord_x.append(self.pos[0] - 1)
        if 3 in legal_moves:
            list_coord_y.append(self.pos[1] - 1)
        return list(product(list_coord_x, list_coord_y))

if __name__ == '__main__':
    m = Map(4)
    a = Agent(m)
    print(m)
    print(a)
    print(a.detectable_coords())
