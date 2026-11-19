# Q4: Reflex Pacman with Multiple Ghosts (3 written marks)

Name: Afzal Ishraq
University number: 3035962374

Run: python3 q4.py written_feature --inspect --ablate
Copy all legal actions from your output; add rows if necessary and leave unused rows blank.

| Action | Full evaluation | Without additional feature |
| --- | --- | --- |
| North | -11.0 | -56.0 |
| East | -41.0 | -71.0 |
| South | -26.0 | -71.0 |
| West | -6.0 | -66.0 |

Selected action, full evaluation: West
Selected action, without feature: North

In at most 120 words, explain your food/all-ghost features and what the added
feature measures. Explain the observed change in values or ranking. An unchanged
selected move is valid; explain why. Keep all other weights/features unchanged.

Response:

The food terms subtract 5 times the nearest-food distance and 2 per remaining dot. Every ghost then subtracts 60 divided by its own distance, so a second ghost still changes the value. The extra feature adds 15 per legal exit after the move. West has four exits and North has three. Without that bonus North leads, -56 against West at -66, because West steps closer to W. The exit term is worth 15 more on West than on North, which exceeds that 10-point gap, so the full evaluation switches to West at -6.
