# Q5: Eat All the Food

Keep your full answer within 200 words, excluding these supplied prompts.

## State Representation

Why is position alone no longer a sufficient state? Describe your chosen representation and explain how it meets the assignment's state requirements.

Answer: Position alone is insufficient because Pacman can revisit the same junction with different food remaining. These situations have different remaining tasks and must be treated as distinct states. If the explored set tracked only position, it could skip a necessary revisit after food has been eaten. Therefore, each state must record both Pacman’s position and which food remains.

My state is a tuple containing a position tuple and a frozenset of remaining food coordinates. It is immutable and hashable. Equal positions and food sets compare equal and hash identically regardless of eating order; changing either produces a distinct state. Successors create new states without modifying the parent or problem.

## Search on long_route

Moves in the returned path: 38

Why did BFS itself need no change?

Answer: BFS itself needed no change because it treats states as complete, hashable objects and uses the supplied goal and successor functions. Q5 changes what a state represents, which successors it has, and when it satisfies the goal: no food remains. The queue and explored-set logic remain unchanged. Since every move costs 1, BFS still finds a route that collects all food in the fewest moves.