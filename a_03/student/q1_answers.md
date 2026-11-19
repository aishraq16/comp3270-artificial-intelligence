# Q1 Answers

## 1. Second-sweep North action at (0, 2)

## 1. Second-sweep North action at (0, 2)

| Next position | Probability | Immediate reward | Previous value | Contribution |
| --- | --- | --- | --- | --- |
| (0, 2) | 0.8 | -0.04 | -0.04 | -0.0608 |
| (0, 3) | 0.1 | -0.04 | 1 | 0.086 |
| (0, 1) | 0.1 | -0.04 | -0.04 | -0.0076 |

Action value: 0.0176

Why +1 is discounted: Entering exit (0, 3) only gives the -0.04 movement reward now; the +1 exit reward is received on the next step when taking Exit, so future value is discounted by 0.9.

## 2. Sweep comparison

| Sweeps | Start value | Greedy start action |
| --- | --- | --- |
| 2 | -0.07600000000000001 | North |
| 100 | 0.2964665410943774  | East |

Explanation (total Q1 prose limit: 120 words):

After k sweeps of synchronous value iteration, value information only propagates up to k steps away from the exit. From (2, 0), reaching (0, 3) and exiting takes more than 2 steps, so after only 2 sweeps the +1 exit reward hasn't propagated back to (2, 0) yet.  

Sources used, if any:
