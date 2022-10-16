# sudoku-solver

Only tested for 3x3 and 4x4 grids, but should work for an perfect square matrix sizes <br />

Requires tkinter library <br />

Script takes 3 command line arguments: <br />
  &emsp;[-a] will animate the solution <br />
  &emsp;[-f [filename]] will read in a csv of puzzles,solution. All puzzles and solutions are num only strings. Will default to inbuilt puzzle if none is provided <br />
  &emsp;[-s [int]] This is how you set grid size, default is 9 for a normal sudoku for perfect squares only, grids larger than 9 replace 10 with A etc. <br /><br />
  &emsp; [-i [int]] The number of puzzles to be test. Any average time and interations required to solve each puzzle will be printed. <br /><br />
Easy dataset can be found at https://www.kaggle.com/datasets/bryanpark/sudoku?resource=download <br />
<br />
Hard dataset and 4x4 attached
