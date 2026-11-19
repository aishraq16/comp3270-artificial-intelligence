# Q4: Find the Cheapest Route Using UCS-GSA

## Measurements for branching

UCS moves in the returned path: 10

UCS total cost: 10

Cost of the Q2 BFS route using Q4's move costs: 12

## Explanation (at most 100 words)

Which route is cheaper? Why does BFS's fewest-moves guarantee not guarantee the cheapest route here? Why does UCS wait until a goal path is removed from the priority queue before returning it?

Answer: UCS route is cheaper. This is because BFS's fewest moves route goes through the state (1, 2) which has an expensive cost of 5, making the total cost of the path higher than that of UCS. 
UCS prioritizes cumulative cost and returns a goal only when its path is removed from the priority queue. With positive step costs, no remaining path can then lead to a cheaper goal. Returning when a goal is first generated could miss a cheaper route still waiting in the queue.

