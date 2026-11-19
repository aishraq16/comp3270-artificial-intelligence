# Q2: Find a Route Using BFS-GSA

## Measurements for branching

Expanded states: 14

Moves in the returned path: 8

## Explanation (at most 100 words)

Why does BFS find a shortest route here? Name one expanded state outside your returned route and explain why BFS examined it.

Answer: BFS expanded 14 states and returned a path of 8 moves. It finds a shortest route because its FIFO queue processes paths in nondecreasing move count. Since every move costs 1, the first goal removed from the queue has a minimum-length path. State (2, 1) was expanded but is not on the returned route. It is one move from the start, so BFS examines it while exploring the shallowest pending paths. BFS explores multiple branches rather than only the branch that eventually reaches the goal.

