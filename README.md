# PydokuSolver
PydokuSolver is Sudoku puzzle solver written in Python. It can find solutions to Sudoku fields of any dimensions and can find one or all possible solutions.

## Usage
You can run Pydoku with the following command line:

`python main.py <input>` 

where `<input>` is a text file containing one character per cell in the Sudoku puzzle you want to solve. 
Empty cells can be denoted with either spaces or zeroes, like so:

```
800406007
000000400
010000650
509030780
000070000
048020103
052000090
001000000
300902005
```

For example files, have a look at the files in the `ExampleInputs` folder and its sub-folders, or solve one of them using:

`python main.py ExampleInputs/9x9/easy1.txt`

The number of cells depends on the size of the Sudoku field that you have. Pydoku supports (almost) any size Sudoku such as 2x2, 4x4, 6x6, 9x9, 16x16, etc..., as long as it meets the classic Sudoku requirements that the field can be divided into blocks of equal size, where the number of blocks per side is the square root of the number of cells in each row and column.

### Additional parameters
Pydoku allows you to find all possible solutions to a given Sudoku puzzle using the `--intensive` parameter. To have Pydoku output a log of what's going on during the solving process, use `--show_process`:

`python main.py <input> --intensive --show_process`

You can find all the command line parameters that Pydoku supports by using:

`python main.py -h`
