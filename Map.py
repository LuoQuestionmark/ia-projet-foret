from matplotlib import pyplot as plt
from scipy.signal import convolve2d as conv

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

        self.data = np.zeros((side_len, side_len), dtype=int)
        
        start_x, start_y, end_x, end_y = [np.random.randint(side_len) for _ in range(4)]

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

    @property
    def startpos(self):
        return self._startpos

if __name__ == '__main__':
    m = Map(4)
    print(m)
    print(m.startpos)