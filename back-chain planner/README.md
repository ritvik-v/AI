# AI Planning

A program that backward-chains from the GOAL state and finds a set of operators that, performed in (reverse) sequence, will result in the GOAL being reached from the INITIAL state. 

## Implementation

The program first parses the text file "operators.txt" and then runs the backward-chaining process, and prints the contents of 'open-goals' and 'achievable'
as well as the chosen operator at each iteration. 

If successful, the correct sequence of operators will be printed.
If the algorithm was unsuccessful, the program will print "FAILURE" to the console.

The program then prints the story constructed from the sequence of operators.

## Author

Ritvik Vaish
