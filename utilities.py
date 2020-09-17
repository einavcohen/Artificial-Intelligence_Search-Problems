from ways import info
from ways import graph
from ways import tools
from ways import load_map_from_csv
import heapq
import csv

def cost_function(link):
    cost = link.distance / info.SPEED_RANGES[link.highway_type][1]
    cost = cost / 1000
    return cost 

def h (problem,node1,node2):
    return tools.compute_distance(problem.roads.get(node1.state).lat,problem.roads.get(node1.state).lon,
    problem.roads.get(node2.state).lat,problem.roads.get(node2.state).lon)/110

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
      self.state = state
      self.parent = parent
      self.action = action
      self.path_cost = path_cost
      self.depth = 0
      if parent:
        self.depth = parent.depth + 1

    def expand(self, problem):
      return [self.child_node(problem, link) for link in problem.roads.get(self.state).links]

    def child_node(self, problem, action):
      next_state = action.target
      next_node = Node(next_state, self, action,
                  self.path_cost+problem.cost_function(action))
      return next_node
    
    def solution(self):
      return self.path(),self.path_cost

    def path(self):
      node, path_back = self, []
      while node:
          path_back.append(node.state)
          node = node.parent
      return list(reversed(path_back))

    def __repr__(self):
      return f"<{self.state}>"

    def __lt__(self, node):
      return self.state < node.state
    
    def __eq__(self, other):
      return isinstance(other, Node) and self.state == other.state

    def __ne__(self, other):
      return not (self == other)

    def __hash__(self):
        return hash(self.state)

class PriorityQueue:

    def __init__(self, f=lambda x: x):
        self.heap = []
        self.f = f

    def append(self, item):
        heapq.heappush(self.heap, (self.f(item), item))

    def extend(self, items):
        for item in items:
            self.append(item)

    def pop(self):
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            raise Exception('Trying to pop from empty PriorityQueue.')

    def __len__(self):
        return len(self.heap)

    def __contains__(self, key):
        return any([item == key for _, item in self.heap])

    def __getitem__(self, key):
        for value, item in self.heap:
            if item == key:
                return value
        raise KeyError(str(key) + " is not in the priority queue")

    def __delitem__(self, key):
        try:
            del self.heap[[item == key for _, item in self.heap].index(True)]
        except ValueError:
            raise KeyError(str(key) + " is not in the priority queue")
        heapq.heapify(self.heap)
    def __repr__(self):
      return str(self.heap)

class RoutingProblem:
 
  def __init__(self, source, target, roads,cost_function):
    self.source = source
    self.target = target
    self.roads = roads
    self.cost_function = cost_function  

  def step_cost(self, link):
    return self.cost_function(link)

  def is_target(self, node):
    return node == self.target

def best_first_graph_search(problem, f):

    source_node = Node(problem.source)
    frontier = PriorityQueue(f) #Priority Queue
    frontier.append(source_node)
    closed_list = set()
    while frontier:
        node = frontier.pop()
        if problem.is_target(node.state):
            return node.solution()

        closed_list.add(node.state)
        for child in node.expand(problem):
            if child.state not in closed_list and child not in frontier:
                frontier.append(child)
            elif child in frontier and f(child) < frontier[child]:
                del frontier[child]
                frontier.append(child)
    return None

def g(node):
    return node.path_cost
