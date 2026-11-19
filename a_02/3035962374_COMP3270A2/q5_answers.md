# Q5: Minimax (5 written marks)

Name: Afzal Ishraq
University number: 3035962374

Use --inspect, not game totals. Both cases use maps/written_lookahead.json.

| Command | Action | Value | Expanded nodes |
| --- | --- | --- | --- |
| python3 q5.py written_shallow --inspect | South | -31 | 12 |
| python3 q5.py written_deep --inspect | West | -32 | 186 |

Run: python3 q5.py written_backup --inspect --branches

| Root action | Child value |
| --- | --- |
| North | -12 |
| East | -12 |
| South | -502 |

Calculated minimum: -502
First minimising action: South
Reported root action and value: South, -502

In at most 150 words, explain this MIN backup, the additional turns depth 2
considers, and why a deeper finite search cannot guarantee a win. If the horizon
comparison retains the same action, explain the changed values and horizon.

Response:

W minimises Pacman's utility. North and East both return -12, and South returns -502, so the minimum is -502 and the root action is South. That value comes from a later capture, so the tie between the other two never decides the node. On the lookahead map, depth 1 ties South and West at -31, with East at -501, and keeps South because it comes first. Depth 2 adds a second full round, another Pacman turn and another turn for each ghost, expanding 186 nodes rather than 12. South then falls to -502 while West is -32, so the choice switches to West. The search still cannot guarantee a win: it stops at a finite depth, and a cutoff leaf is only the score minus 10 per remaining food. A later capture is invisible, and -32 is not itself a win.
