from collections import namedtuple
from ways import load_map_from_csv, compute_distance
from ways import info
from ways import graph
from ways import tools
import heapq
import csv
import utilities

inf=1e15
Graph = namedtuple('Graph', 'edges weight target is_goal heuristic')

def find_idastar_route(source, target, roads=None):
    if roads is None:
        roads = load_map_from_csv()
    
    def weight(link):
        return utilities.cost_function(link)
    
    def heuristic(s):
        s_node = roads[s]
        t_node = roads[target]
        problem = utilities.RoutingProblem(s_node,t_node,roads,utilities.cost_function)
        return tools.compute_distance(problem.roads.get(s_node.index).lat,problem.roads.get(s_node.index).lon,
            problem.roads.get(t_node.index).lat,problem.roads.get(t_node.index).lon)/110

    def edges(v):
        junction = roads[v]
        edges = list(junction.links)
        # now sort it
        edges.sort(key=lambda edge: weight(edge) + heuristic(edge.target))
        return junction.links

    def edge_target(link):
        return link.target

    def is_goal(junction):
        return junction == target

    
    
    G = Graph(edges, weight, edge_target, is_goal, heuristic)

    return idastar(source, target, G)

def idastar(root, goal, G):
    bound = G.heuristic(root)
    path = [root]

    while True:
        t = idastar_iter(path, 0, G, bound)
        # t is none only when we find
        if t is None:
            # if have some insight about the search
            return path
        elif t == inf:
            print('not found')
            return []
        bound = t
    return None

def idastar_iter(path, curr_cost, G, bound):
    node = path[-1]
    f = curr_cost + G.heuristic(node)
    if f > bound:
        return f
    # found, return none
    if G.is_goal(node):
        return None
    
    minimum = inf
    for edge in G.edges(node):
        child = G.target(edge)
        # if child in path:
            # continue
        path.append(child)
        t = idastar_iter(path, curr_cost + G.weight(edge), G, bound)
        # if found
        if t is None:
            return None # return that its found.
        if t < minimum:
            minimum = t
        path.pop()
    return minimum

def path_idastar_cost (path,roads):
    cost = 0.0
    for i in range (len(path)-1):
        junction_link = roads.get(path[i]).links
        for j in junction_link:
            if j.target == path[i+1]:
               link_cost = utilities.cost_function(j)
               cost = cost + link_cost
               break
    return cost
    
# print idastar solution for 100 problems

def print_idastar_costs():
    roads = load_map_from_csv()
    with open("problems.csv") as problems_file:
       read_file = csv.reader(problems_file,delimiter=',')
       counter = 0
       for splited_line in read_file:
           if counter >= 5:
               break
           counter+=1
           source = int(splited_line[0])
           target = int(splited_line[1])
           path = find_idastar_route(source, target,roads)
           path_cost = path_idastar_cost(path,roads)
           with open('results/IDAstarRuns.txt', 'a') as output:
               problem = utilities.RoutingProblem(source,target,roads,utilities.cost_function)
               cost_h = utilities.h(problem,utilities.Node(problem.source),utilities.Node(problem.target))
               output.write(str(path_cost) +","+ str(cost_h) + '\n')

# print_idastar_costs()