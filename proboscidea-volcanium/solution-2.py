import functools
import itertools

input_file = open('proboscidea-volcanium/input.txt', 'r')
valve_lines = input_file.readlines()

class Valve:
    def __init__(self, name, rate, neighbors) -> None:
        self.name = name
        self.rate = rate
        self.neighbors = neighbors

def get_valves_and_dist():
    valves = {}
    dist = {}

    for valve_data in valve_lines:
        valve_data = valve_data.strip('\n').split(' ')
        valve_name = valve_data[1]
        valve_rate = int(valve_data[4][5:-1])
        valve_neighbors = []

        # dist to itself is zero
        dist[valve_name] = { valve_name: 0 }
        for valve_n in valve_data[9:]:
            valve_n = valve_n[:2]
            valve_neighbors.append(valve_n)
            # set dist to neighbor as travel time, in this case 1 second
            dist[valve_name][valve_n] = 1

        valves[valve_name] = Valve(valve_name, valve_rate, valve_neighbors)

    # init all edges of graph
    for valve_one in valves.keys():
        for valve_two in valves.keys():
            if valve_one not in dist[valve_two]:
                dist[valve_two][valve_one] = 99

    # relax edges of graph - floyd warshall
    for k in valves.keys():
        for i in valves.keys():
            for j in valves.keys():
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

    return valves, dist

# only consider visiting nonempty valves
def search(path_stack, valves, dist):
    results = []
    while len(path_stack) != 0:
        curr_valve, rest, t, score = path_stack.pop()
        if t < 0:
            print(t)
        for next in rest:
            remaining = rest - {next}
            if dist[curr_valve][next] < t:
                new_t = t - dist[curr_valve][next] - 1
                new_score = score + valves[next].rate * new_t
                path_stack.append((next, remaining, new_t, new_score))
            else:
                results.append(score)
        
        if len(rest) == 0:
            results.append(score)

    return max(results)

def solution():
    valves, dist = get_valves_and_dist()
    nonempty_valves = list(filter(lambda k: valves[k].rate != 0, valves.keys()))

    # create simplified/cached version of our search, memoization of the valves to traverse
    @functools.cache
    def get_subscores(unvisited_valves):
        return search([('AA', unvisited_valves, 26, 0)], valves, dist)

    results = set()
    half_way_point = len(nonempty_valves) // 2

    # idea: score is maximized with subsets of equal size since valves are opened asap
    # get equal size subsets or similar size subsets of at most size diff 1 for our nonempty valves
    subsets = itertools.combinations(nonempty_valves, half_way_point)
    for s in subsets:
        our_valves = frozenset(s)
        ele_valves = frozenset(nonempty_valves) - our_valves
        results.add(get_subscores(our_valves) + get_subscores(ele_valves))

    return max(results)

print(solution())
