# Q2: Reflex Pacman with One Ghost (5 written marks)

Name: Afzal Ishraq
University number: 3035962374

Run each command from student/ after completing Q0/Q1/Q2. Record your own results.

| Command | Wins | Losses | Unfinished |
| --- | --- | --- | --- |
| python3 q1.py corridor --trials 10 --seed 8 --max-rounds 40 | 6 | 4 | 0 |
| python3 q2.py corridor --trials 10 --seed 8 --max-rounds 40 | 10 | 0 | 0 |
| python3 q2.py race --trials 10 --seed 8 --max-rounds 40 | 10 | 0 | 0 |

In at most 150 words, describe your evaluation formula (features, signs and
weights), explain one measured difference from random play, and identify a
limitation of one-step reasoning. Sources, if used, should be acknowledged.

Response:

A nonterminal move uses the successor score, minus 5 times the nearest-food Manhattan distance, minus 2 per remaining food, minus 80 divided by the nearest-ghost distance. An adjacent ghost therefore costs 80, while one step closer to food is worth only 5, so staying away from the ghost outweighs a slightly shorter path. Terminal children return the exact final score, so an immediate win beats every other move and an immediate capture loses when a safe move exists. On corridor this player won 10/10, each time in two turns with score 518. Random play won 6/10 and lost 4. Its wins took 2 to 6 Pacman turns, while this player always finished in 2. One step still cannot see a ghost move that blocks the only exit on the next turn.
