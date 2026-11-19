# Q3: Multiple Agents and Turn Depth (2 written marks)

Name: Afzal Ishraq
University number: 3035962374

Run: python3 q3.py written_turns --inspect
Use the ghost labels from this map. Z is trapped and must pass. Assume the game
remains nonterminal during this turn-accounting exercise.

Faulty trace: (X, 2) -> (Z, 1) -> (P, 0)

Correct sequence from (X, 2) through the first depth-zero turn:

(X, 2) -> (Z, 2) -> (P, 1) -> (X, 1) -> (Z, 1) -> (P, 0)

In at most 80 words, identify the first incorrect transition, explain its effect
on the number of Pacman turns considered, and show where Z passes in your
corrected sequence.

Response:

The first incorrect transition is (X, 2) -> (Z, 1). X is not the last ghost, so depth stays 2 and the next turn is (Z, 2). Dropping depth early reaches (P, 0) before the next round, which removes one Pacman turn. Z is trapped and passes, but the pass still consumes the turn: (Z, 2) leads to (P, 1), and later (Z, 1) leads to (P, 0).
