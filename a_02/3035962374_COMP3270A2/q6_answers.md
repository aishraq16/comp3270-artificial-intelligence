# Q6: Expectimax (9 written marks)

Name: Afzal Ishraq
University number: 3035962374

| Command | Action | Value | Expanded nodes |
| --- | --- | --- | --- |
| python3 q5.py written_two_ghosts --inspect --depth 2 | North | -502 | 28 |
| python3 q6.py written_two_ghosts --inspect --depth 2 | West | -311.11111111111114 | 28 |
| python3 q5.py written_trap --inspect --depth 2 | West | -32 | 365 |
| python3 q6.py written_trap --inspect --depth 2 | West | -32.0 | 365 |

Run both:
python3 q5.py written_backup --inspect --branches
python3 q6.py written_backup --inspect --branches

| Root action | Q5 child value | Q6 child value | Q6 child expanded nodes | Uniform probability |
| --- | --- | --- | --- | --- |
| North | -12 | -12.0 | 5 | 1/3 |
| East | -12 | -12.0 | 6 | 1/3 |
| South | -502 | -257.0 | 6 | 1/3 |

Uniform expectation (show calculation using Q6 values):
(-12.0 + -12.0 + -257.0) / 3 = -281/3 = -93.66666666666667
Reported Q6 root action and value: None, -93.66666666666667
Lowest Q5 child value and associated action: South, -502

Change only this root's probabilities: first legal action in the stated
direction order gets 1/2; the remaining actions equally share the other 1/2.
Keep the Q6 child values unchanged; descendant ghosts remain uniform.

New root expectation (show probabilities and calculation):
North 1/2, East 1/4, South 1/4.
(1/2)(-12.0) + (1/4)(-12.0) + (1/4)(-257.0) = -6 + -3 + -64.25 = -73.25
Q6 root expanded count reconstructed from child counts: 1 + 5 + 6 + 6 = 18
Reported Q6 root expanded count: 18

In at most 220 words, use measured branch values to explain how MIN and chance
treat the risky branch. Connect this to an observed action/value difference in
the first table. Explain whether changing only the root probabilities requires
visiting a different set of nodes under the required full-tree search. Tables
and arithmetic do not count towards the word limit.

Response:

South is the risky branch. Minimax values that child at -502 and, because W minimises, uses -502 as the node value, so the ghost is treated as certain to capture. Expectimax values the same South child at -257, because ghosts deeper in that branch are averaged rather than minimised, and values North and East at -12 each. Their uniform mean is about -93.67, matching the reported root; the action stays None because a ghost node is a distribution. Shifting only this root to probabilities 1/2, 1/4 and 1/4 changes the weights to -73.25 and still expands every child. The reconstructed count, 1 + 5 + 6 + 6, equals the reported 18, so the new probabilities do not visit a different set of nodes. The same contrast appears on two ghosts. Minimax values North and West both at -502, so it keeps North, the first action. Expectimax values North at about -460.33 and West at about -311.11, so it chooses West. On the trap map both still choose West at -32, with 365 nodes either way. East and South do separate, at -501 and -502 for minimax against about -149.25 and -168.83 for expectimax, but West stays -32 either way.
