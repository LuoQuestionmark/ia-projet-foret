"""
The Graph show save the hypothesis and the observation.
"""
from collections.abc import Iterable
from collections import defaultdict

from itertools import chain, combinations, combinations_with_replacement, product, permutations

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
    def __init__(self, points: Iterable[tuple[int, int]]) -> None:
        # hypothesis_vertices are the hyp on
        # the points on map given as input.
        # each element in this dict is a valid hyp.
        # the key is encoded in a way so that a element
        # can be found based on a observation
        # the value is a value from 0 to 1
        # 1 is true, 0 is false, and the values between
        # are probabilities
        self.hypothesis_vertices = dict()

        # observng vertices are the collection of every
        # possible observation that can be done
        # each vertex is bound with one or more vertex
        # in the hypothesis_vertices, which are saved as
        # a set of value in as the value of this dict
        self.observing_vertices = defaultdict(set)

        # the exactly encoding of a vertex in the hypothesis_vertices
        # is the following:
        # [(<coordx>,<coordy>):<status>, ...]
        # which is saved in the class `Assumption`
        # with coordx, coordy in [0,edge_len] (edge_len < 10)
        # with status in [0, 1, 2, 3]
        #      with 0: nothing, safe
        #           1: monster
        #           2: hole
        #           3: exit

        possibilities = product(combinations_with_replacement(range(3), len(points) - 1), [3])
        possibilities = [chain(i[0], [i[1]]) for i in possibilities]

        for status in permutations(possibilities):
            assumption = Assumption(points, status)
            self.hypothesis_vertices[assumption] = 1 / (4 ** len(points))

if __name__ == '__main__':
    m = Map(4)
    a = Agent(m)
    k = KnowledgeGraph(a.detectable_coords())
    for i in k.hypothesis_vertices:
        print(i)
    print(len(k.hypothesis_vertices))
