from __future__ import print_function
from heapq import * #Hint: Use heappop and heappush

import math

ACTIONS = [(0,1),(1,0),(0,-1),(-1,0)]

class AI:
    def __init__(self, grid, type):
        self.grid = grid
        self.set_type(type)
        self.set_search()

    def set_type(self, type):
        self.final_cost = 0
        self.type = type

    def set_search(self):
        self.final_cost = 0
        self.grid.reset()
        self.finished = False
        self.failed = False
        self.previous = {}

        # Initialization of algorithms goes here
        if self.type == "dfs":
            self.frontier = [self.grid.start]
            #self.explored = []
            self.visited = set() # added tracker for visited nodes
        elif self.type == "bfs":
            self.frontier = [self.grid.start]
            self.visited = set()
        elif self.type == "ucs":
            self.frontier = [(0, self.grid.start)]
            self.visited = set()
        elif self.type == "astar":
            self.visited = set()
            self.frontier = [(0, self.grid.start)]

    def get_result(self):
        total_cost = 0
        current = self.grid.goal
        while not current == self.grid.start:
            total_cost += self.grid.nodes[current].cost()
            current = self.previous[current]
            self.grid.nodes[current].color_in_path = True #This turns the color of the node to red
        total_cost += self.grid.nodes[current].cost()
        self.final_cost = total_cost

    def make_step(self):
        if self.type == "dfs":
            self.dfs_step()
        elif self.type == "bfs":
            self.bfs_step()
        elif self.type == "ucs":
            self.ucs_step()
        elif self.type == "astar":
            self.astar_step()

    #DFS: BUGGY, fix it first
    def dfs_step(self):
        
        if not self.frontier:
            self.failed = True
            self.finished = True
            print("no path")
            return
        current = self.frontier.pop()
        #self.visited.add(current) # append the node popped from frontier (is now explored)

        # Finishes search if we've found the goal.
        if current == self.grid.goal:
            print("we've reached the end-goal-point!",print(self.previous[current]))
            self.finished = True
            return

        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        if current not in self.visited:
            self.visited.add(current)
            for n in children:
                if n not in self.visited and n not in self.frontier: # was missing this
                    # below checks boundries of map
                    if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                        if not self.grid.nodes[n].puddle:
                            self.previous[n] = current
                            self.frontier.append(n)
                            self.grid.nodes[n].color_frontier = True
                if n == self.grid.goal:
                    self.finished = True
                    return
    
    #Implement BFS here (Don't forget to implement initialization at line 23)
    def bfs_step(self):

        if not self.frontier:
            self.failed = True
            self.finished = True
            return
        current = self.frontier.pop(0)

        if current == self.grid.goal:
            self.finished = True
            return
        
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        if current not in self.visited:
            self.visited.add(current)
            for n in children:
                if n not in self.visited and n not in self.frontier:
                    if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                        if not self.grid.nodes[n].puddle:
                            self.previous[n] = current
                            self.frontier.append(n)
                            self.grid.nodes[n].color_frontier = True
                if n == self.grid.goal: # isn't actually needed, unlike in dfs, not sure why.
                    self.finished = True
                    return


    #Implement UCS here (Don't forget to implement initialization at line 23)
    def ucs_step(self):
        if not self.frontier:
            self.failed = True
            self.finished = True
            return
        cost, current = heappop(self.frontier)
        #print("++++++++++++++++++++++++++++++++++",current)
        if current == self.grid.goal:
            self.finished = True
            #print("FINAL >>>>>>>>>>>>>>>>>>>>>>>>>>",current)
            return current
        
        #if current not in self.visited:
        #self.visited.add(current) # could be referring to self.grid.goal?

        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        if current not in self.visited:
            self.visited.add(current)
            for n in children:
                #child_cost = n[1] # repetitive, but for label purpose
                '''
                print(current,"--------------") # current node is represented by coordinates (x,y)
                print(n,"--------------") # n representes current node + action to reach child node
                print(self.visited,"--------------") # contains visited nodes
                print(self.frontier,"--------------") # contains frontier nodes
                '''
                if n not in self.visited and n not in self.frontier:
                    if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                        if not self.grid.nodes[n].puddle:
                            if n not in [x[1] for x in self.frontier]:
                                self.previous[n] = current
                                heappush(self.frontier,(cost + self.grid.nodes[n].cost(), n))
                                self.grid.nodes[n].color_frontier = True
                if n == self.grid.goal:
                    self.finished = True
                    return
            

    # manhattan distance : test 1 fails, all success
    # euclidean distance : test 2 fails, all success
    def heuristic(self, a, b):
        # return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2) # euclid
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) # manhattan dist.
    
    # need way to switch btwn heuristic : not changing anything
    def dynamic_heuristic(self, a, b):
        manhattan = abs(a[0] - b[0]) + abs(a[1] - b[1])
        euclidean = math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
        if manhattan < euclidean:
            return manhattan
        else:
            return euclidean

    #Implement Astar here (Don't forget to implement initialization at line 23)
    # same implementation as UCS, but with heuristic cost on-top of UCS' path-cost.
    def astar_step(self):

        if not self.frontier:
            self.failed = True
            self.finished = True
            return
        
        cost, current = heappop(self.frontier)

        if current == self.grid.goal:
            self.finished = True
            return current
        
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        self.grid.nodes[current].color_checked = True
        self.grid.nodes[current].color_frontier = False

        if current not in self.visited:
            self.visited.add(current)
            for n in children:
                if n not in self.visited and n not in self.frontier:
                    if n[0] in range(self.grid.row_range) and n[1] in range(self.grid.col_range):
                        if not self.grid.nodes[n].puddle:
                            if n not in [x[1] for x in self.frontier]:       # double check n not in frontier
                                real_cost = cost + self.grid.nodes[n].cost() # just like in UCS
                                heuristic_cost = self.heuristic(self.grid.goal,n) # cost of frontier node
                                # heuristic_cost = self.dynamic_heuristic(self.grid.goal,n)

                                self.previous[n] = current
                                heappush(self.frontier,(real_cost + heuristic_cost, n))
                                self.grid.nodes[n].color_frontier = True
                # need to ensure goal is reached, on frontier. (enforced again)
                if n == self.grid.goal:
                    self.finished = True
                    return