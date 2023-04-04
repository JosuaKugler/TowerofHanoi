# TowerofHanoi
This repository is written for the purpose of better understanding the Towers of Hanoi with multiple pegs.

For a short talk explaining the basic ideas, see `symposium_slides/main.pdf`

Therefore it contains several functions.
The bruteforce function simply tries all possibilities and finds the possibilities that are solving the problem in the minimum number of moves.

The adjustedUpsilon function computes the number of possibilities for solving the problem with the Frame-Stewart algorithm.

In addition, there is a visualize function that can visualize different types of data and create e.g. Tower of Hanoi pictures or tables with values.

With moves_FS, there is a Python script that creates all possible FS-movessequences
With createmoves, the history of a TH can be converted into a moveslist.
