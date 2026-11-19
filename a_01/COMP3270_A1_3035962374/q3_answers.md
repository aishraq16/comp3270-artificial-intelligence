# Q3: Find a Route Using DFS-GSA

## Measurements for branching

BFS expanded states: 14

BFS moves in the returned path: 8

DFS expanded states: 12

DFS moves in the returned path: 12

## Explanation (at most 100 words)

How does FIFO versus LIFO cause the different exploration orders? Does DFS find a shortest route in this maze? Why would examining fewer states not, by itself, imply a shorter returned path?

BFS uses a FIFO queue, exploring states level by level in increasing path depth. DFS uses a LIFO stack, exploring the most recently added state first and following a branch deeper before considering alternatives. Here, DFS does not find a shortest route: its path takes 12 moves, whereas BFS finds an 8-move route. Examining fewer states measures search effort, not solution length. DFS expands fewer states because it reaches the goal along a longer branch without exploring some alternatives; BFS explores more branches but guarantees a shortest route when every move has equal cost.
