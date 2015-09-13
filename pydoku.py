##############################################################################
# Pydoku Solver 
# This Python script can solve Sudoku fields of any dimension and can find 
# multiple solutions if the input field has them.
# For usage, use the following command line:
#	python pydoku.py -h
##############################################################################

import math
import argparse
import time

class Solver:
	def __init__(self):
		self.field_size = 0
		self.block_size = 0
		self.cell_options = set()
		self.solutions = list(list())
		self.intensive = False
		self.show_process = False


	# Attempts to load file inputFilePath and construct a Sudoku field from it.
	# The input field may have any size as long as the square root of the size is a whole integer. For example,
	# 4x4, 6x6, 9x9, ... 16x16, etc. are all allowed, but not 5x5. This is because it is not possible to divide a 5x5 grid into equally
	# sized blocks.
	def loadInput(self, inputFilePath):
		if len(inputFilePath) <= 0:
			print "No input file was specified."
			return

		sudoku = list()
		chars = set(' 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
		empty_cell_char = '0'
		with open(inputFilePath) as f:
			while True:
				c = f.read(1)
				if not c:
					break
				elif c in chars:
					if c == ' ':
						c = empty_cell_char
					sudoku.append(c)

		field_size_float = math.sqrt(len(sudoku))

		if not field_size_float.is_integer():
			print "Sudoku field is incorrectly formed with " + str(len(sudoku)) + " entries."
			return None

		self.field_size = int(field_size_float)
		self.block_size = int(math.sqrt(self.field_size))

		all_cell_options = list('123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ');
		self.cell_options.clear()
		for i in range(self.field_size):
			self.cell_options.add(all_cell_options[i])

		for y in range(self.field_size):
			for x in range(self.field_size):
				c = self.getCell(sudoku, x, y)
				if c != empty_cell_char and c not in self.cell_options:
					print "Cell [%i, %i] has a value (%s) that is outside the accepted range for %ix%i fields. Accepted values are %s" % (x + 1, y + 1, c, field_size, field_size, cell_options)
					return None

		return sudoku


	# Get the sequential index of cell [x, y] (because we store our field in a single-dimensional array)
	def getIdx(self, x, y):
		return x + y * self.field_size


	# Get the value in cell [x, y] in field.
	def getCell(self, field, x, y):
		return field[self.getIdx(x, y)]


	# Get the indices of the cell that comes after cell [x, y]. If [x] is at the end of a row
	# then y is incremented properly and x is set to 0.
	def getNextIndices(self, x, y):
		next_x = 0 if x == (self.field_size - 1) else x + 1
		next_y = y if x < (self.field_size - 1) else y + 1
		return next_x, next_y


	# Print a single formatted row of the field.
	def printFieldRow(self, field, y):
		hor_cell_spacing = "  "
		vert_cell_spacing = "\n"
		hor_block_spacing = "   "
		vert_block_spacing = "\n\n"
		fieldStr = ""
		i = y
		for j in range(self.field_size):
			c = self.getCell(field, j, i)
			fieldStr = fieldStr + (c if c != '0' else '.')
			if j < self.field_size:
				fieldStr = fieldStr + hor_cell_spacing
			if j % self.block_size == (block_size - 1):
				fieldStr = fieldStr + hor_block_spacing
		print fieldStr


	# Print the field as a nicely formatted grid with spacing between blocks.
	def printField(self, field):
		hor_cell_spacing = "  "
		vert_cell_spacing = "\n"
		hor_block_spacing = "   "
		vert_block_spacing = "\n\n"
		fieldStr = ""
		for i in range(self.field_size):
			for j in range(self.field_size):
				c = self.getCell(field, j, i)
				fieldStr = fieldStr + (c if c != '0' else '.')
				if j < self.field_size:
					fieldStr = fieldStr + hor_cell_spacing
				if j % self.block_size == (self.block_size - 1):
					fieldStr = fieldStr + hor_block_spacing
			fieldStr = fieldStr + vert_cell_spacing
			if i % self.block_size == (self.block_size - 1) and i < (self.field_size - 1):
				fieldStr = fieldStr + vert_block_spacing
		print fieldStr


	# Parse the field to find the remaing options for cell at [x, y].
	def getRemaining(self, field, x, y):
		remaining = set(self.cell_options)

		# Visit all cells in the same row and the same column and discard entries that have been filled in.
		for i in range(self.field_size):
			ver = self.getCell(field, x, i)
			hor = self.getCell(field, i, y)
			remaining.discard(ver)
			remaining.discard(hor)

		# Also remove all entries that already exist in the same block.
		block_start_x = int(math.floor(float(x) / self.block_size) * self.block_size)
		block_start_y = int(math.floor(float(y) / self.block_size) * self.block_size)
		for i in range(self.block_size):
			for j in range(self.block_size):
				c = self.getCell(field, block_start_x + i, block_start_y + j)
				remaining.discard(c)

		return remaining


	# Helper function that constructs an indentation string that indicates the current solve depth.
	def getDepthPrefixStr(self, depth):
		prefix = ""
		for i in range(depth):
			prefix = prefix + " "
		return prefix


	# Helper function to conditionally print a line to the console to indicate the current state of the solve function.
	def printProcessLine(self, depth, line):
		if self.show_process:
			print self.getDepthPrefixStr(depth) + line;


	# This function visits the cell at [x, y] and recurses as neccessary to the next cell.
	# If the current cell is empty it will first find all remaining possible options for the cell, then fill in the first option and recurse to the next cell.
	# Should control return to the function without having found a valid solution for the filled in option, or if we are performing an intensive search, the function
	# will try the second option and recurse again. This process is repeated until all options are depleted.
	def visitCell(self, field, x, y, depth):
		tmpField = list(field)

		if x == 0 and y == self.field_size:
			# We have found the solution (hopefully).
			self.solutions.append(list(tmpField))
			return self.intensive

		self.printProcessLine(depth, "Visiting cell @ [%i, %i]" % (x + 1, y + 1))

		c = self.getCell(tmpField, x, y)
		res = True
		if c == '0':
			remaining = self.getRemaining(tmpField, x, y)

			self.printProcessLine(depth, "Cell is empty, have %i options remaining: %s" % (len(remaining), str(remaining)))

			if len(remaining) > 0:
				for option in remaining:
					self.printProcessLine(depth, "Trying option %s" % (option))

					tmpField[self.getIdx(x, y)] = option

					next_idcs = self.getNextIndices(x, y)

					self.printProcessLine(depth, "Next cell: [%i, %i]" % (next_idcs[0] + 1, next_idcs[1] + 1))

					res = self.visitCell(tmpField, next_idcs[0], next_idcs[1], depth + 1)
					if not res:
						break
			else:
				self.printProcessLine(depth, "No options remaining")
		else:
			next_idcs = self.getNextIndices(x, y)
			res = self.visitCell(tmpField, next_idcs[0], next_idcs[1], depth + 1)

		self.printProcessLine(depth, "Going back")

		return res


	# The starting point of the algorithm. This functon simply starts visiting the cells in the field at cell [0, 0]
	def solve(self, filepath, intensive, show_process):
		field = self.loadInput(filepath)

		if field is None:
			print "No valid sudoku field was generated from the input file."
			return False

		self.printField(field)

		self.intensive = intensive
		self.show_process = show_process
		self.solutions = list(list())

		print "Solve(intensive=%r)... (started @ %s)" % (self.intensive, time.strftime("%X %x"))

		time_start = time.clock()

		res = self.visitCell(field, 0, 0, 0)

		time_end = time.clock()
		print "...completed in %f seconds." % (time_end - time_start)

		return res


# The main function is not placed within the if __name__ == "__main__" construct because this allows us to easily exit the function with a return statement.
def main():	
	parser = argparse.ArgumentParser(description='Solve an unsolved Sudoku field.')
	parser.add_argument("input", metavar="i", nargs=1, type=str, 
	                   	help="Input file containing the input unsolved Sudoku field as (1 character per cell: '001320600...'. Line breaks are ignored. Whitespace or zeroes denote empty cells. Depending on the size of the sudoku field, the set of accepted characters for cells is [123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ]. A 9x9 field accepts characters [1..9], a 16x16 field accepts [1..G], etc.).")
	parser.add_argument("--intensive", action="store_true", help="Perform an intensive solve and find all possible solutions to the input field.")
	parser.add_argument("--show_process", action="store_true", help="Display log entries during solving to visualise the process.")

	args = parser.parse_args()

	solver = Solver()
	solver.solve(args.input[0], args.intensive, args.show_process)

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