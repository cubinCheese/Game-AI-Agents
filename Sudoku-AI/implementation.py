from __future__ import print_function
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy


class AI:
    def __init__(self):
        pass

    def solve(self, problem):

        domains = init_domains()
        restrict_domain(domains, problem)

        solution = self.Backtrack(domains)

        if solution is None:
            return None
        return solution
    
    def Backtrack(self, domains):

        if self.is_complete(domains):
            return domains

        spot = self.select_unassigned_spot(domains)
        values = self.sort_domain_values(domains, spot)

        for value in values:

            if self.board_isValid(domains, spot, value):
                domains_copy = copy.deepcopy(domains)
                domains_copy[spot] = [value]
                
                if self.propagate(domains_copy):
                    result = self.Backtrack(domains_copy)
                    if result is not None:
                        return result

        return None

    # verifies domains (solution) is filled-in # i.e. solution produced
    def is_complete(self, domains):
        
        for spot in sd_spots:
            if len(domains[spot]) != 1:
                return False
            
        return True

    # next 'spot' within domain to be filled - during backtrack
    def select_unassigned_spot(self, domains):
        
        min_domain_size = float('inf')
        selected_spot = None
        for spot in sd_spots:
            if len(domains[spot]) > 1 and len(domains[spot]) < min_domain_size:
                min_domain_size = len(domains[spot])
                selected_spot = spot
        
        return selected_spot

    # setup for heuristics to prioritize specific values 
    def sort_domain_values(self, domains, spot):
        
        values = domains[spot]
        # just returns those sorted 
        return sorted(values, key=lambda value: self.count_restricted_domains(domains, spot, value))

    # counts # of values (1-9) eliminated as candidates for particular spot
    def count_restricted_domains(self, domains, spot, value):
        
        count = 0
        for peer in sd_peers[spot]:
            # check if target 'value' is in domain of each peer
            if value in domains[peer] and len(domains[peer]) > 1:
                count += 1
        
        return count

    # verifies that new assignments of (value) to (spot) keep the current Sudoku board valid
    # i.e. unique value per row,box
    def board_isValid(self, domains, spot, value):

        for peer in sd_peers[spot]:
            if len(domains[peer]) == 1 and domains[peer][0] == value:
                return False
            
        return True

    # tldr. removes values already assigned to spots from domains of peers
    def propagate(self, domains):
        # queue of (spot,peer), where only spots of domain len is 1
        queue = [(spot, peer) for spot in sd_spots for peer in sd_peers[spot] if len(domains[spot]) == 1]
        
        # propagate till empty queue
        while queue:
            
            spot, peer = queue.pop(0) # pop pair from queue
            value = domains[spot][0]  # retrieve value of spot
            
            # verify domain of peer spot has value
            if value in domains[peer]: 

                domains[peer].remove(value) # remove that value
                
                if len(domains[peer]) == 0: # invalid if empty domain in peer spot
                    return False
                elif len(domains[peer]) == 1:
                    # add peers to queue
                    queue.extend([(peer, p) for p in sd_peers[peer] if len(domains[p]) == 1])
        
        return True

