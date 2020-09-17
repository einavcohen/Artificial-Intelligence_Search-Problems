import utilities
from ways import info
from ways import graph
from ways import tools
from ways import load_map_from_csv
import heapq
import csv

#f = g: 
def find_ucs_rout(source, target,cost_function,roads=None):
    if roads is None:
        roads = load_map_from_csv()
    problem = utilities.RoutingProblem(source,target,roads,utilities.cost_function)
    path , cost = utilities.best_first_graph_search(problem,utilities.g)
    return path

def find_ucs_cost(source, target,cost_function,roads=None):
    if roads is None:
        roads = load_map_from_csv()
    problem = utilities.RoutingProblem(source,target,roads,utilities.cost_function)
    path , cost = utilities.best_first_graph_search(problem,utilities.g)
    return cost

# print ucs solution for 100 problems
def print_ucs_costs():
    roads = load_map_from_csv() 
    with open("problems.csv") as problems_file:
       read_file = csv.reader(problems_file,delimiter=',')
       for splited_line in read_file:
           source = int(splited_line[0])
           target = int(splited_line[1])
           cost = find_ucs_cost(source, target, utilities.cost_function,roads)
           with open('results/UCSRuns.txt', 'a') as output:
               output.write(str(cost)+'\n')

# print_ucs_costs()