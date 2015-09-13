##############################################################################
# Pydoku Solver 
# This Python script can solve Sudoku fields of any dimension and can find 
# multiple solutions if the input field has them.
# For usage, use the following command line:
#	python main.py -h
##############################################################################

import math
import argparse
import time
import pydoku


# The main function is not placed within the if __name__ == "__main__" construct because this allows us to easily exit the function with a return statement.
def main():	
	parser = argparse.ArgumentParser(description='Solve an unsolved Sudoku field.')
	parser.add_argument("input", metavar="i", nargs=1, type=str, 
	                   	help="Input file containing the input unsolved Sudoku field as (1 character per cell: '001320600...'. Line breaks are ignored. Whitespace or zeroes denote empty cells. Depending on the size of the sudoku field, the set of accepted characters for cells is [123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ]. A 9x9 field accepts characters [1..9], a 16x16 field accepts [1..G], etc.).")
	parser.add_argument("--intensive", action="store_true", help="Perform an intensive solve and find all possible solutions to the input field.")
	parser.add_argument("--show_process", action="store_true", help="Display log entries during solving to visualise the process.")

	# Parse the command line arguments.
	args = parser.parse_args()

	# Instantiate our Pydoku solver.
	solver = pydoku.Solver(args.input[0], args.intensive, args.show_process)

	# Keep track of the start time.
	print "Solve(intensive=%r)... (started @ %s)" % (solver.intensive, time.strftime("%X %x"))
	time_start = time.clock()

	# Perform our solve.
	solver.solve()

	# Keep track of the end time
	time_end = time.clock()
	print "...completed in %f seconds." % (time_end - time_start)

	# Print output.
	if len(solver.solutions) == 0:
		print "No solution was found."
	else:
		if args.intensive:
			print "Found %i solutions:" % len(solver.solutions)
		for i in range(len(solver.solutions)):
			if args.intensive:
				print "           Solution %i:" % (i + 1)
			print "               |\n               V\n"
			solver.printField(solver.solutions[i])


# Main
if __name__ == "__main__":
	main()