# Q6: Guide the Search with A*-GSA

## Measurements

| Maze | Algorithm | Moves | Expanded states |
| --- | --- | --- | --- |
| playground | BFS (Q5) | 34 | 3327 |
| playground | A* (Q6) | 34 | 1180 |
| corridor | BFS (Q5) | 2 | 2 |
| corridor | A* (Q6) | 2 | 2 |

## Explanation (at most 200 words)

Does A* always expand fewer states? Use your corridor comparison.

Would summing the Manhattan distances to all remaining food always be admissible? Justify with a small maze in your written answer. Keep the maximum-distance heuristic in q6.py.

Why does the original maximum-distance heuristic satisfy h(state) <= 1 + h(child), including when a move eats a food dot?

How does g + h change the search effort compared with BFS on playground?

Answer:

A* does not always expand fewer states. On corridor, both BFS and A* find a 2-move solution and expand 2 states.

Summing Manhattan distances is not always admissible, because distances to different food dots can count overlapping travel. Consider a straight corridor P··, with Pacman at (0,0) and food at (0,1) and (0,2). The sum is 
1+2=3, but collecting both foods requires only 2 moves. Thus, the sum overestimates the optimal remaining cost.

The maximum-distance heuristic is consistent. For every food dot still remaining after a move, its Manhattan distance from the parent is at most its distance from the child plus 1. Its child distance is at most h(child). If the move eats a food dot, that dot’s distance from the parent was exactly 1, which is also at most 1 + h(child). Taking the maximum preserves this inequality, including when the last food is eaten.

On playground, both searches find 34-move solutions, but BFS expands 3,327 states versus A*’s 1,180. BFS explores by depth; A* prioritizes g+h, combining moves already made with estimated remaining cost to explore more selectively.




