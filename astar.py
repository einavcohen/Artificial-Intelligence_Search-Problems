from ways import info
from ways import graph
from ways import tools
from ways import load_map_from_csv
import heapq
import csv
import utilities

def find_astar_route(source,target,g,h,roads=None):
  if roads is None:
      roads = load_map_from_csv()
  problem = utilities.RoutingProblem(source,target,roads,utilities.cost_function)
  path , cost = utilities.best_first_graph_search(problem, f=lambda n: utilities.g(n)+utilities.h(problem,n,utilities.Node(problem.target)))
  return path

def find_astar_cost(source,target,g,h,roads=None):
  if roads is None:
      roads = load_map_from_csv()
  problem = utilities.RoutingProblem(source,target,roads,utilities.cost_function)
  path , cost = utilities.best_first_graph_search(problem, f=lambda n: utilities.g(n)+utilities.h(problem,n,utilities.Node(problem.target)))
  return cost
# print astar solution for 100 problems

def print_astar_costs():
    roads = load_map_from_csv()
    with open("problems.csv") as problems_file:
       read_file = csv.reader(problems_file,delimiter=',')
       for splited_line in read_file:
           source = int(splited_line[0])
           target = int(splited_line[1])
           cost = find_astar_cost(source, target, utilities.g,utilities.h,roads)
           with open('results/AStarRuns.txt', 'a') as output:
               problem = utilities.RoutingProblem(source,target,roads,utilities.cost_function)
               cost_h = utilities.h(problem,utilities.Node(problem.source),utilities.Node(problem.target))
               output.write(str(cost) +","+ str(cost_h) + '\n')

# print_astar_costs()
