"""
The Graph show save the hypothesis and the observation.
"""
from collections.abc import Iterable

from itertools import product
from sys import exit

import numpy as np 

from Map import Map
from Agent import Agent

class Assumption:
    def __init__(self, points: Iterable[tuple[int, int]], status: Iterable[int]) -> None:
        self.data = dict()
        for i, p in enumerate(points):
            self.data[p] = status[i]

    def __str__(self) -> str:
        ret =   "Assumption: vertex | status\n"
        for k, v in self.data.items():
            ret += f"   {k} | {Assumption.get_status_verbose(v)}\n"

        return ret

    @staticmethod
    def get_status_verbose(val):
        if val == 0:
            return "nothing"
        elif val == 1:
            return "monster"
        elif val == 2:
            return "hole"
        elif val == 3:
            return "exit"
        else:
            raise ValueError("unexpected value")

    def get_obseving_possibles():
        pass

class KnowledgeGraph:
    def __init__(self, map: Map, points: list[tuple[int, int]]) -> None:
        self.map = map
        self.input_list = points
        
        self.hypotheses_size = 4 ** len(points)
        self.hypotheses = np.empty(self.hypotheses_size, dtype=float)
        self.hypotheses.fill(1 / self.hypotheses_size)

    def encoding(self, status: Iterable[int]) -> int:
        depl = 0
        for value in reversed(status):
            depl *= 4
            depl += value
        return depl

    def decoding(self, value: int) -> list[int]:
        status = list()
        while value >= 4:
            status.append(value % 4)
            value = value // 4
        status.append(value)
        return list(status)

    def find_all(self, coord: tuple[int, int], status: int) -> list[tuple[int, int]]:
        """
        return the list of all corresponding indexs with <status> at <coord>
        """
        try:
            indexs = list()
            element_index = self.input_list.index(coord)

            for i in range(self.hypothese_size):
                value_at_element = i % (4 ** (element_index + 1))
                value_at_element = value_at_element // 4 ** element_index

                if status != value_at_element:
                    continue
                indexs.append(i)

            return indexs

        except ValueError:
            print(f"unable to get coordinate with given coord: {coord}")
            exit(1)

    def update(self, coord: tuple[int, int], observation: int) -> None:
        """
        observation:
        0: wind
        1: smell
        2: light
        """
        if coord not in self.input_list:
            return
        if observation not in range(2):
            return

        element_index = self.input_list.index(coord)

        if observation == 2:
            # find the exit
            old_validation = self.get_valid_hypotheses_number()

            for hypothesis in range(self.hypotheses_size):
                if self.decoding(hypothesis)[element_index] != 2:
                    self.hypotheses[hypothesis] = np.NaN
            
            new_validation = self.get_valid_hypotheses_number()

            for hypothesis in range(self.hypotheses_size):
                if self.decoding(hypothesis)[element_index] == 2:
                    self.hypotheses[hypothesis] *= old_validation
                    self.hypotheses[hypothesis] /= new_validation
            return

        else:
            pass

                

        neighbors = self.map.get_all_neighbor(coord)
        for neighbor in neighbors:
            pass
        
    def get_valid_hypotheses_number(self) -> int:
        return len([i for i in self.hypotheses if i != np.NaN])
        

if __name__ == '__main__':
    m = Map(4)
    a = Agent(m)
    k = KnowledgeGraph(m, a.detectable_coords())
    # for i in k.hypothesis_vertices:
    #     print(i)

    print(k.decoding(45))
