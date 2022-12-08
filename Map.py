from matplotlib import pyplot as plt
from scipy.signal import convolve2d as conv
from itertools import combinations

import numpy as np

class Map:
    def __init__(self, side_len=3, hole_proba=0.1, monster_proba=0.1):
        """
        side_len     : the size of the map, 3 for 3*3
        hole_proba   : the probability of generate a hole on a random case, if there isn't a player, or an exit
        monster_proba: the probability of generate a monster on a random case, 
                       if there isn't a player, an exit or a hole
        """
        # define the ground type as the following
        # the very last digit:
        # 0 = nothing from the env
        # 1 = hole  2 = monster  3 = exit
        # 4 = player_start point, or the player trace
        # the second from left:
        # 0 = nothing  1 = has wind
        # the third from left:
        # 0 = nothing 1 = has smell

        if side_len < 1: raise ValueError("impossible side length")

        self._side_len = side_len
        self.data = np.zeros((side_len, side_len), dtype=int)
        
        coords = list(combinations(range(side_len), 2))
        np.random.shuffle(coords)

        start_x, start_y = coords.pop()
        end_x, end_y = coords.pop()

        self.data[start_x, start_y] = 4
        self.data[end_x, end_y] = 3

        generated_mask = (self.data == 0)
        self.hole_mask = np.random.rand(*self.data.shape) < hole_proba
        self.hole_mask = np.bitwise_and(self.hole_mask, generated_mask)
        self.data += 1 * self.hole_mask

        generated_mask = (self.data == 0)
        self.monster_mask = np.random.rand(*self.data.shape) < monster_proba
        self.monster_mask = np.bitwise_and(self.monster_mask, generated_mask)
        self.data += 2 * self.monster_mask

        wind_mask = conv(self.hole_mask, np.ones((3, 3)), mode='same')
        self.data += 10 * (wind_mask > 0)

        smell_mask = conv(self.monster_mask, np.ones((3, 3)), mode='same')
        self.data += 100 * (smell_mask > 0)

        self._startpos = (start_x, start_y)

    def __str__(self) -> str:
        return str(np.rot90(self.data))

    def kill_monster(self, coord):
        if self.data[coord]%10 != 2: return
        # remove the monster
        self.data[coord] -= 2
        # remove the old smell
        self.data += -100 * (self.data >= 100)

        self.monster_mask[coord] = 0
        smell_mask = conv(self.monster_mask, np.ones((3, 3)), mode='same')
        self.data += 100 * (smell_mask > 0)

    def is_out(self, coord):
        if self.data[coord] == 3:
            return True
        else:
            return False

    def is_has_smell(self, coord):
        if self.data[coord] & 100 != 0:
            return True
        else:
            return False

    def is_windy(self, coord):
        if self.data[coord] & 10 != 0:
            return True
        else:
            return False

    def is_has_light(self, coord):
        """
        this function is the copy of "is_out", the reason of creating
        this function is purely for better semantic.
        """
        return self.is_out(coord)

    @property
    def startpos(self) -> tuple:
        return self._startpos

    @property
    def side_len(self) -> int:
        return self._side_len

if __name__ == '__main__':
    m = Map(4)
    print(m)
    print(m.startpos)
