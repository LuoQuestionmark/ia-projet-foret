"""
The Graph show save the hypothesis and the observation.
"""
from collections.abc import Iterable

from itertools import product
from sys import exit

import numpy as np 

from Map import Map
from Agent import Agent

VERBOSE = 1

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
        self.hypotheses = np.ones(self.hypotheses_size, dtype=float)
        
        self.exit_coord = None

        self.deal_impossible()

    def encoding(self, status: Iterable[int]) -> int:
        depl = 0
        for value in reversed(status):
            depl *= 4
            depl += value
        return depl

    def decoding(self, value: int) -> list[int]:
        status = list()
        for _ in self.input_list:
            status.append(value % 4)
            value = value // 4
        return list(status)

    def deal_impossible(self) -> None:
        if VERBOSE > 0:
            print("delete case with multiple exit")
        for hypothesis in range(self.hypotheses_size):
            exits = [i == 3 for i in self.decoding(hypothesis)]
            if sum(exits) > 1:
                self.hypotheses[hypothesis] = 0
        if VERBOSE > 0:
            print("delete case with startpos = exit")
        startpos = self.map.startpos
        index = self.input_list.index(startpos)
        for hypothesis in self.possible_hypotheses():
            if self.decoding(hypothesis)[index] != 0:
                self.hypotheses[hypothesis] = 0

    def find_all(self, coord: tuple[int, int], status: int) -> list[int]:
        """
        return the list of all corresponding index with <status> at <coord>
        """
        try:
            indexs = list()
            element_index = self.input_list.index(coord)

            for i in range(self.hypotheses_size):
                value_at_element = i % (4 ** (element_index + 1))
                value_at_element = value_at_element // 4 ** element_index

                if status != value_at_element:
                    continue
                indexs.append(i)

            return indexs

        except ValueError:
            print(f"unable to get coordinate with given coord: {coord}")
            exit(1)

    def possible_hypotheses(self):
        for hypothesis in range(self.hypotheses_size):
            if self.hypotheses[hypothesis] <= 0:
                continue
            yield hypothesis

    def is_coherent(self, hypothesis: int, coord_index: int, observation: int) -> bool:
        """
        see if the given hypothsis is cohrent with observation.

        observation:
        0: smell
        1: wind
        2: light
        """
        if observation not in range(3):
            raise ValueError
        if observation == 0:
            status = 1
        elif observation == 1:
            status = 2
        else:
            status = 3

        if self.decoding(hypothesis)[coord_index] != status:
            return False
        else:
            return True


    def update(self, coord: tuple[int, int], observation: int) -> None:
        """
        observation:
        0: smell
        1: wind
        2: light
        3: nothing above
        """
        if coord not in self.input_list:
            return
        if observation not in range(4):
            return

        element_index = self.input_list.index(coord)

        if observation == 2:
            if VERBOSE > 0:
                print(f"find exit at coord {coord}")

            self.exit_coord = coord

            for hypothesis in self.possible_hypotheses():
                if self.decoding(hypothesis)[element_index] != 3:
                    self.hypotheses[hypothesis] = 0
            return

        if observation == 1 or observation == 0:
            if VERBOSE > 0:
                if observation == 0:
                    print(f"find smell at coord {coord}")
                else: # observation == 1
                    print(f"find wind at coord {coord}")

            neighbors = self.map.get_all_neighbor(coord)
            neighbor_index = set()
            for neighbor in neighbors:
                if neighbor not in self.input_list:
                    continue
                neighbor_index.add(self.input_list.index(neighbor))

            for hypothesis in self.possible_hypotheses():
                # if self.decoding(hypothesis)[neighbor_index] != 1:
                if all([self.is_coherent(hypothesis, index, observation) for index in neighbor_index]) is False:
                    if VERBOSE > 1:
                        if observation == 0:
                            print(f"hypothesis #{hypothesis} with the possibility in coord {coord} has no monster is decreased")
                        else:
                            print(f"hypothesis #{hypothesis} with the possibility in coord {coord} has no hole is decreased")
                    self.hypotheses[hypothesis] = min(0.5, self.hypotheses[hypothesis])
            return

        if observation == 3:
            if VERBOSE > 0:
                print(f"detect \"nothing\" at coord {coord}")
            
            neighbors = self.map.get_all_neighbor(coord)
            neighbor_index = set()
            for neighbor in neighbors:
                if neighbor not in self.input_list:
                    continue
                neighbor_index.add(self.input_list.index(neighbor))

            for observation, hypothesis in product(range(2), self.possible_hypotheses()):
                if any([self.is_coherent(hypothesis, index, observation) for index in neighbor_index]) is True:
                    if VERBOSE > 1:
                        if observation == 0:
                            print(f"hypothesis #{hypothesis} with the possibility in coord {neighbor} has monster is decreased")
                        else:
                            print(f"hypothesis #{hypothesis} with the possibility in coord {neighbor} has hole is decreased")
                    self.hypotheses[hypothesis] = 0

        
    def get_valid_hypothese(self) -> Iterable[int]:
        return [i for i, v in enumerate(self.hypotheses) if v > 0]

    def get_probable_hypothese(self) -> Iterable[int]:
        """
        return the index of all probable hypothese
        """
        return [i for i, v in enumerate(self.hypotheses) if v == 1]

    def get_safe_coords(self) -> Iterable[tuple[int, int]]:
        coords = {coord: 0 for coord in self.input_list}

        for coord in coords.keys():
            potential_problematic_hypothese = set(self.find_all(coord, 1))
            potential_problematic_hypothese = potential_problematic_hypothese.union(set(self.find_all(coord, 2)))
            valid_hypothese = set(self.get_valid_hypothese())
            coords[coord] = len(potential_problematic_hypothese.intersection(valid_hypothese))
                
        # output = sorted(coords.keys(), key=lambda i: coords[i], reverse=True)
        coords = sorted(coords.items(), key=lambda i: i[1])

        coords = [i[0] for i in coords if i[1] == 0]

        if VERBOSE > 0:
            print(f"find safe coords: {coords}")

        return coords

    def get_low_risk_coords(self) -> Iterable[tuple[int, int]]:
        coords = {coord: 0 for coord in self.input_list}

        for coord in coords.keys():
            potential_problematic_hypothese = set(self.find_all(coord, 1))
            potential_problematic_hypothese = potential_problematic_hypothese.union(set(self.find_all(coord, 2)))
            valid_hypothese = set(self.get_probable_hypothese())
            coords[coord] = len(potential_problematic_hypothese.intersection(valid_hypothese))
                
        # output = sorted(coords.keys(), key=lambda i: coords[i], reverse=True)
        coords = sorted(coords.items(), key=lambda i: i[1])

        if VERBOSE > 0:
            print(f"find low risk coords: {coords}")

        return coords

    def __call__(self, agent: Agent):
        for coord in self.input_list:
            if agent.detect(coord, 0):
                self.update(coord, 0)
                if VERBOSE > 0:
                    print(self)

            if agent.detect(coord, 1):
                self.update(coord, 1)
                if VERBOSE > 0:
                    print(self)

            if agent.detect(coord, 2):
                self.update(coord, 2)
                if VERBOSE > 0:
                    print(self)

            if not (agent.detect(coord, 0) or agent.detect(coord, 1)):
                self.update(coord, 3)
                if VERBOSE > 0:
                    print(self)

    def __str__(self) -> str:
        string = ""
        string += f"Knowledge Graph:\n"
        string += f"total hypothese size: {self.hypotheses_size}\n"
        string += f"legal hypothese size: {len(self.get_valid_hypothese())}\n"
        string += f"probable hypothese size: {len(self.get_probable_hypothese())}\n"
        string += f"exit coord: {self.exit_coord}\n"

        return string
        

if __name__ == '__main__':
    m = Map(4)
    a = Agent(m)
    k = KnowledgeGraph(m, a.detectable_coords())

    print(k.map)

    print(k)

    # for coord in a.detectable_coords():
    #     if a.detect(coord, 0):
    #         k.update(coord, 0)
    #         print(k)

    #     if a.detect(coord, 1):
    #         k.update(coord, 1)
    #         print(k)

    #     if a.detect(coord, 2):
    #         k.update(coord, 2)
    #         print(k)

    #     if not (a.detect(coord, 0) or a.detect(coord, 1)):
    #         k.update(coord, 3)
    #         print(k)

    k(a)

    k.get_low_risk_coords()
    k.get_safe_coords()

    print(k.map)
