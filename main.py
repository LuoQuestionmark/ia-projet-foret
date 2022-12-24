from matplotlib import pyplot as plt
from time import sleep

import numpy as np

from Map import Map
from Agent import Agent
from KnowledgeGraph import KnowledgeGraph

VERBOSE = 1

def get_best_move(agent: Agent):
    graph = KnowledgeGraph(agent.board, agent.detectable_coords())
    graph(agent) #run

    indexs = agent.legal_moves()
    coords = agent.legal_move_coords()

    target = None
    if graph.exit_coord is not None:
        target = graph.exit_coord
        if target in coords:
            return indexs[coords.index(target)]
    else:
        positions = set(agent.board.get_all_coords())
        positions.difference_update(agent.list_past_pos)
        target = sorted(positions, key=lambda i: abs(i[0] + i[1] - agent.board.side_len))[0] # a central point

    tmp = set(coords)
    safe = set(graph.get_safe_coords())
    tmp.intersection_update(safe)

    if (len(tmp)) == 0:
        tmp = set(coords)
        low_risk = set(graph.get_low_risk_coords())
        tmp = tmp.intersection(low_risk)

    out = sorted(tmp, key=lambda i: abs(i[0] - target[0]) + abs(i[1] - target[1]))[0]
    return indexs[coords.index(out)]




if __name__ == '__main__':
    map = Map(4, 0, 0)
    agent = Agent(map)

    # fig, (ax, ax2) = plt.subplots(1, 2, figsize=(15,10))
    data = np.copy(map.data) % 10
    data[agent.pos] = -1
    # display = ax.matshow(np.rot90(data))
    # plt.pause(0.1)
    
    # fig.canvas.show()
    # fig.canvas.flush_events()

    last_move = None
    # fig.canvas.show()
    # fig.canvas.flush_events()
    # plt.show(block=False)
    while not map.is_out(last_move):
        move = get_best_move(agent)
        if VERBOSE > 0:
            if move == 0:
                direction = "right"
            elif move == 1:
                direction = "down"
            elif move == 2:
                direction = "left"
            else:
                direction = "right"
            print("get best move: " + direction)

        last_move = agent.move(move)
        print(agent)

        data = np.copy(map.data) % 10
        data[agent.pos] = -1
        # display.set_data(np.rot90(data))

        print(np.rot90(data))

        # fig.canvas.show()
        # plt.pause(1)

    print("out")
