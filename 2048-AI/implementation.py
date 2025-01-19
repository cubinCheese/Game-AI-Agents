from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1

# Tree node. To be used to construct a game tree.
class Node:
    def __init__(self, state, player_type):
        self.state = (state[0], state[1])
        self.children = [] # children nodes will be (move, child)
        self.player_type = player_type

    def is_terminal(self):
        return not bool(self.children)

class AI:
    def __init__(self, root_state, search_depth=3):
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    def build_tree(self, node=None, depth=0):

        # no root passed in
        if node is None:     
            node = self.root

        # depth 0 of game tree reached (starts at defined depth=3)
        if depth == 0:
            return

        # max and chance player cases
        # max player - 'make' a move to branch out onto every possible game state
        # chance player - place down random tiles on 'current' branch of game state
        if node.player_type == MAX_PLAYER:
            for move in MOVES.keys():
                self.simulator.set_state(node.state[0], node.state[1])
                if self.simulator.move(move):
                    new_state = self.simulator.current_state()
                    new_node = Node(new_state, CHANCE_PLAYER)
                    node.children.append((move, new_node))
                    self.build_tree(new_node, depth - 1)
        elif node.player_type == CHANCE_PLAYER:
            open_tiles = self.simulator.get_open_tiles() # blank tiles list
            for tile in open_tiles:
                child_state = copy.deepcopy(node.state)
                child_state[0][tile[0]][tile[1]] = 2
                child_node = Node(child_state, MAX_PLAYER)
                #print(child_state[1])
                node.children.append((None, child_node))
                self.build_tree(child_node, depth - 1) # depth-1 fixes game slowness
    
    def expectimax(self, node=None):
        #print("myScore: ",self.simulator.current_state()[1])

        if node is None:
            node = self.root

        if node.is_terminal(): 
            return None, node.state[1] # return payoff on terminal node
        
        # max player - determine optimal direction and its weighed value
        # chance player - calc. expected value of game state based on moves aval.
        if node.player_type == MAX_PLAYER: # determine optimal direction and its value
            best_value = float("-inf")
            best_direction = None
            for move, child_node in node.children:     # loop through children node
                _, value = self.expectimax(child_node) # recursively - det. best-value
                if value > best_value:                 # max(value,expectimax)
                    best_direction = move
                    best_value = value
            #print("best_direction and best_value: ", )
            return best_direction, best_value

        elif node.player_type == CHANCE_PLAYER: # return expectimax calculation
            total_value = 0
            count = 0
            #if len(node.children) == 0: return None, 0
            for _, child_node in node.children:
                _, value = self.expectimax(child_node)
                total_value += value
                count += 1
            #if count == 0: return None, 0  # previous div/zero error: fixed with terminal case
            #print("myScore: ",total_value)
            #print(node.children)
            return None, float(total_value) / count 

    # issue with build_tree? changing between expectimax and alphabeta changed nothing
    # limited by game_tree? makes no sense.
    def alphabeta(self, node=None, alpha=float('-inf'), beta=float('inf')):
        if node is None:
            node = self.root
            
        if node.player_type == MAX_PLAYER:
            best_direction = None
            best_value = float("-inf")
            
            for move, child_node in node.children:
                _, value = self.expectimax(child_node, alpha, beta)
                
                if value > best_value:
                    best_direction = move
                    best_value = value
                
                alpha = max(alpha, best_value)
                
                if alpha >= beta:
                    break
            
            return best_direction, best_value

        elif node.player_type == CHANCE_PLAYER:
            total_value = 0
            count = 0
            
            for _, child_node in node.children:
                _, value = self.expectimax(child_node, alpha, beta)
                total_value += value
                count += 1
            
            if count == 0:
                return None, 0
            
            return None, total_value / count


    def compute_decision(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        return direction

    def compute_decision_ec(self):
        return random.randint(0, 3)


