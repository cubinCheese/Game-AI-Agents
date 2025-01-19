import copy
import random
from game import Game, states

HIT = 0
STAND = 1
DISCOUNT = 0.95 #This is the gamma value for all value calculations

class Agent:
    def __init__(self):
        # For MC values
        self.MC_values = {}
        self.S_MC = {}
        self.N_MC = {}

        # For TD values
        self.TD_values = {}
        self.N_TD = {}

        # For Q-learning values
        self.Q_values = {}
        self.N_Q = {}

        # Initialization of the values
        for s in states:
            self.MC_values[s] = 0
            self.S_MC[s] = 0
            self.N_MC[s] = 0
            self.TD_values[s] = 0
            self.N_TD[s] = 0
            self.Q_values[s] = [0, 0] # First element is the Q value of "Hit", second element is the Q value of "Stand"
            self.N_Q[s] = [0, 0] # First element is the number of visits of "Hit" at state s, second element is the number of visits of "Stand" at s

        # Game simulator
        self.simulator = Game()

    @staticmethod
    def default_policy(state):
        user_sum = state[0]
        user_A_active = state[1]
        actual_user_sum = user_sum + user_A_active * 10
        if actual_user_sum < 14:
            return 0
        else:
            return 1

    @staticmethod
    def alpha(n):
        return 10.0 / (9 + n)
    

    def make_one_transition_forTD(self, action): # return current reward       # can return None
        if self.simulator.game_over():
            #print("Got here.")
            return self.simulator.check_reward(), None
        

        state = self.simulator.state
        #reward = None
        #print(action) # actions are valid, but not entering if-else???
        reward = self.simulator.check_reward() # difference is we return current reward

        if action == HIT:
            #print("here1")
            self.simulator.act_hit()
        elif action == STAND:
            self.simulator.act_stand()
        
        next_state = self.simulator.state
        #reward = self.simulator.check_reward() # difference is we return current reward

        # enforced reward returns
        if (reward == -1):
            #print("reached lost state")
            return reward, next_state
        if (reward == 0):
            #print("reached draw state")
            return reward, next_state
        if (reward == 1): 
            #print("reached win state")
            return reward, next_state
    
    def make_one_transition(self, action): # for MC # return next_state reward # can't return None
        '''
        if self.simulator.game_over():
            print("Got here.")
            return None
        '''

        state = self.simulator.state
        #reward = None
        #print(action) # actions are valid, but not entering if-else???
        if action == HIT:
            #print("here1")
            self.simulator.act_hit()
        elif action == STAND:
            self.simulator.act_stand()

        next_state = self.simulator.state
        reward = self.simulator.check_reward()

        # enforced reward return, can't return None ever
        if (reward == -1):
            #print("reached lost state")
            return reward, next_state
        if (reward == 0):
            #print("reached draw state")
            return reward, next_state
        if (reward == 1): 
            #print("reached win state")
            return reward, next_state

    # monte carlo policy eval.
    def MC_run(self, num_simulation, tester=False,):
        # Perform num_simulation rounds of simulations in each cycle of the overall game loop
        for simulation in range(num_simulation):
            # Do not modify the following three lines
            if tester:
                self.tester_print(simulation, num_simulation, "MC")
            self.simulator.reset()  # The simulator is already reset for you for each new trajectory

            # TODO
            # Note: Do not reset the simulator again in the rest of this simulation
            # Hint: self.simulator.state gives you the current state of the trajectory
            # Hint: Use the "make_one_transition" function to take steps in the simulator, and keep track of the states
            # Hint: Go through game.py file and figure out which functions will be useful
            # Make sure to update self.MC_values, self.S_MC, self.N_MC for the autograder
            # Don't forget the DISCOUNT
            #states_visited = []
            states_visited = [self.simulator.state]
            rewards = [self.simulator.check_reward()] #rewards = []
            while not self.simulator.game_over():
                s = self.simulator.state # State representation: (user_sum, user_has_Ace, dealer_first)
                #action = self.pick_action(s,0.2)
                # use defualt policy
                action = self.default_policy(s)
                r, next_state = self.make_one_transition(action)
                ##states_visited.append(s) # stores state we left after transition
                states_visited.append(next_state) # list of states visited should include terminal states *hence the next_state
                ##print("visited states in whileLoop: ",states_visited)
                #TEMPCOUNT += 1
                ##print("times while-loop ran: ",TEMPCOUNT)
                #print("before: ",rewards,r)
                rewards.append(r)
                ##print("after: ",rewards)
            ##print(rewards)
            ##print("after populating states list: ",states_visited)
            G = 0
            for t in range(len(states_visited)-1, -1, -1): # reverse order iterate lists' indicies
                #s = self.simulator.state 
                s = states_visited[t]
                ##print("this is what state we are at (initially): ",s)
                ##print("Our rewards array: ",rewards," | Our rewards[t]: ",rewards[t])
                r = rewards[t]
                G = DISCOUNT * G + r
                self.N_MC[s] += 1
                ##print("we are on state (after N_MC): ",s," with (MC_val): ",self.N_MC[s])
                self.S_MC[s] += G
                ##print("we are on state (after S_MC): ",s," with (MC_val): ",self.S_MC[s])
                self.MC_values[s] = self.S_MC[s] / self.N_MC[s]
                ##print("we are on state (after MC_val): ",s," with (MC_val): ",self.MC_values[s])
                
            #print("current states_visited: ", states_visited) # this print only shows last visited state, not timeline of...
            #print("for the state: ",s," we have: ",self.MC_values[s])

    # temporal difference policy eval
    def TD_run(self, num_simulation, tester=False):
        for simulation in range(num_simulation):
            if tester:
                self.tester_print(simulation, num_simulation, "TD")
            self.simulator.reset()
            
            state = self.simulator.state
            states_visited = [self.simulator.state]
            rewards = [self.simulator.check_reward()]

            while state is not None:
                action = self.default_policy(state)
                reward, next_state = self.make_one_transition_forTD(action)
                ##print("was I ever None: ", next_state)
                
                states_visited.append(next_state)
                rewards.append(reward)
                #print("rewards: ",rewards[])
                ##print("after populating states list: ",states_visited)
                #self.N_TD[state] += 1
                #state = next_state

                if next_state is not None:                    
                    self.TD_values[state] += self.alpha(self.N_TD[state]) * (reward + DISCOUNT * self.TD_values[next_state] - self.TD_values[state])
                    
                    ##print("next_state is not None: ",next_state) # terminal state should be 1,0,0
                    ##print("TD_value: ",self.TD_values[state])
                    ##print("reward: ",reward)
                    #state = next_state 
                    #self.N_TD[state] += 1 # fixed issue: this was misplaced below calculation...
                    #self.TD_values[state] += self.alpha(self.N_TD[state]) * (reward + DISCOUNT * self.TD_values[next_state] - self.TD_values[state])
                    ##print("Here are the rewards: ",rewards)
                    ##print("and the corresponding states: ",states_visited)
                    ##print("current state is: ",state," next_state is: ",next_state)
                    ##print("for the current state: ",state," you have the TD_value of: ",self.TD_values[state])
                    ##print("for the next_state: ",next_state," you have the TD_value of: ",self.TD_values[next_state])

                if next_state is None:
                    ##print("DOES THIS RUNEEEEEEEEEEEEEEEEEEEEEEEEEEEEEVER")
                    self.TD_values[state] += self.alpha(self.N_TD[state]) * (reward + DISCOUNT * 0 - self.TD_values[state])
                    
                    #print("for the state: ",state," you have the TD_value of: ",self.TD_values[next_state])
                    #print("for the next_state: ",next_state," you have the TD_value of: ",self.TD_values[next_state])

                #print("all td_values: ",self.TD_values)
                self.N_TD[state] += 1
                state = next_state
            
    # similar implementation to TD_run, modified (1) policy-action choice (2) Q_values calculation based on max()
    def Q_run(self, num_simulation, tester=False, epsilon=0.4):
        for simulation in range(num_simulation):
            if tester:
                self.tester_print(simulation, num_simulation, "TD")
            self.simulator.reset()

            state = self.simulator.state
            #states_visited = [self.simulator.state]
            #rewards = [self.simulator.check_reward()]

            while state is not None:
                
                #N_Q # is [# visits of Hit, # visits of Stand]
                # # First element is the number of visits of "Hit" at state s, second element is the number of visits of "Stand" at s
                # what should be given to self.alpha(n)? the sum of these two?

                #action = self.default_policy(state)
                action = self.pick_action(state,epsilon)
                reward, next_state = self.make_one_transition_forTD(action)
                
                #states_visited.append(next_state)
                #rewards.append(reward)

                if next_state is not None:
                    # max() picks value corresponding to next_state : hence Q_val[next_state] not [next_state][action]
                    self.Q_values[state][action] += self.alpha(self.N_Q[state][action]) * (reward + DISCOUNT * max(self.Q_values[next_state]) - self.Q_values[state][action])
                    
                if next_state is None:
                    self.Q_values[state][action] += self.alpha(self.N_Q[state][action]) * (reward + DISCOUNT * 0 - self.Q_values[state][action])

                self.N_Q[state][action] += 1
                state = next_state
    
    # TODO: Implement epsilon-greedy policy
    def pick_action(self, s, epsilon):
        if random.random() < epsilon:     # probability of epsilon - pick random action
            value = random.randint(0, 1)  # Select a random action - hit or stand
            #print(value)
            return value
        else:                         # probability of 1-epsilon - maximize Q-value
            # Select the action with the highest Q-value for the current state
            max_q_value = max(self.Q_values[s])
            #print(max_q_value)
            #print(self.Q_values[s].index(max_q_value))
            return self.Q_values[s].index(max_q_value)
