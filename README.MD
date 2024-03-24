# Game-AI-Agents


## Navigate to ./2048-AI/2048-AI.exe

<img src="https://github.com/cubinCheese/Game-AI-Agents/assets/93562548/783609f6-3505-4df9-b0a0-c1efe3eb8b8a" width="300">

In 2048, the game state switches between the computer placing down tiles and (you) the player utilizing arrow keys to select a direction to move the tiles. Your goal is to merge as many tiles as possible until you can no longer continue.
Our AI Agent for 2048 acts as (you) the player and treats the (computer) as its opponent. The method by which our AI Agent maximizes its obtainable score is as follows:
- Building the depth 3 game tree: This game tree represents all possible states of the game, i.e. all possible moves of the player-computer-player sequence are stored/represented in the game tree.
- Our agent then explores possible moves from its current game state, simulating the resulting game states and evaluating its potential outcome. Imagine this as being able to look into the future, and choosing the most beneficial move you can.
- Expectimax Algorithm: This is used to evaluate the potential outcomes of each move. Considers both deterministic actions of the AI (max player - player that wants to maximize the score) and random events (chance player - random tile placements).

## Navigate to ./Blackjack-AI/Blackjack-AI.exe

![blackjack](https://github.com/cubinCheese/Game-AI-Agents/assets/93562548/11c82a35-615f-4f06-885a-f61aac065385)

Here, similar to how a person practices in a sport, our AI agent wants to maximize its probability of winning by playing more and more games. This way, it can further refine the choices it makes in future games.

AI Agent implements the following:
- Monte Carlo Policy Evaluation: The AI agent plays many blackjack games following a particular policy (e.g., hit on a sum of 16 or less, stand otherwise) and observes the outcomes. By averaging the rewards obtained over these episodes, the agent estimates the value of following that policy.
- Temporal-Difference Policy Evaluation: In blackjack, the AI agent updates its value estimates for states based on the difference between the current estimate and the sum of the immediate reward and the estimated value of the next state.
- Q-Learning: The AI agent maintains a Q-table that stores the estimated value (Q-value) for each action in each state. During gameplay, the agent selects actions based on a policy derived from the Q-values and then updates the Q-values based on the rewards obtained and the estimated value of the next state.
  Note. Q-learning is a model-free reinforcement learning algorithm that learns to make decisions by estimating the value of taking a particular action in a given state. It updates the Q-values (action-value function) based on observed rewards and transitions.


## Navigate to ./Gomoku-AI/Gomoku-AI.exe

![gomoku](https://github.com/cubinCheese/Game-AI-Agents/assets/93562548/f68fad88-2d1c-4f5e-b00c-4a7c0f56e50e)

Here, our AI Agent's goal is to get 5 white pieces in a connected sequence before we do. 

Implementation wise: Our AI implements the Monte Carlo Tree Search Algorithm (MCTS) to determine the best move it can make. So, by exploring different actions and their outcomes we can maximize our chances of winning.
Specifically, our MCTS utilizes the following:
- Selection: The AI agent selects a child node to explore from the current node. It does this by using the Upper Confidence Bound (UCB) formula to balance between nodes that have high potential (based on past performance) and nodes that have not been explored much.
- Expansion: Once a node is selected for exploration, the AI agent expands the tree by adding a new child node corresponding to an untried action from the selected node. This simulates taking that action and moves to the resulting state.
- Rollout (Simulation): The AI agent performs a rollout or simulation from the newly expanded node to a terminal state (end of the game) by randomly selecting actions until the game ends. This simulates possible future states and outcomes.
- Backpropagation: After the rollout, the AI agent backpropagates the outcome of the simulation (win or loss) back up the tree. It updates the statistics of the nodes along the path from the expanded node to the root, incrementing the visit count and win count of each node.
- Repeat: Steps 1-4 are repeated iteratively (for a specified number of iterations or budget) to gradually build up statistics about the quality of different actions and their outcomes.

## Navigate to ./Maze-AI/Maze-AI

![maze](https://github.com/cubinCheese/Game-AI-Agents/assets/93562548/a9961cd2-ee8c-42b4-8ed3-c7588b73cbde)

We implemented the following path finding algorithms:
- BFS: BFS ensures that it finds the shortest path to the exit, as it explores cells in order of their distance from the entrance.
- DFS: DFS may find a path to the exit faster than BFS in some cases but does not guarantee the shortest path.
- UCS: UCS guarantees finding the shortest path if the cost of moving from one cell to another is uniform.
- A*: A* Search would efficiently find the shortest path to the exit, leveraging an admissible and consistent heuristic, such as Manhattan distance or Euclidean distance to the exit. (Utilizes heuristics to know the rough direction of where the ending goal is).

## Navigate to ./Sudoku-AI/Sudoku-AI

How to Run Sudoku AI Agent.

In your terminal navigate to where this file is located.

```./Sudoku -h``` 🡆 ```to see a range of flag options```

```./Sudoku -t 0``` 🡆 ```Propagation only```

```./Sudoku -t 1``` 🡆 ```Propagation and Search```

```./Sudoku -t 2``` 🡆 ```50 Easy Cases```

```./Sudoku -t 3``` 🡆 ```50 Hard Cases```


![screenshot](https://github.com/cubinCheese/Game-AI-Agents/assets/93562548/bf9979c4-7fc5-49dd-a1a1-a3544058525d)

At a high level, the Sudoku AI agent is attempting to solve Sudoku puzzles using the Backtracking algorithm. It iteratively selects unassigned spots on the Sudoku board, assigns values to them, and checks if these assignments satisfy the Sudoku constraints. If the assignments violate any constraints, it backtracks and tries a different value. This process continues until a valid solution to the Sudoku puzzle is found. The agent uses propagation to maintain consistency by removing assigned values from the domains of their peers.

To see additional details of test cases passed, use "-d True".
