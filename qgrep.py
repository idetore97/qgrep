"""
Python code to do string-search using Grover's algorithm.
"""
import grover_pattern as gp
import str_utils as su
import argparse

# Get arguments
parser = argparse.ArgumentParser()
parser.add_argument('filename', help='Filename to search.') # Get file to search
parser.add_argument('target', help='String to search for.') # Get string to search for
args = parser.parse_args()

# Get file data
file = open(args.filename)

# Convert files to array of strings based on line numbers
lines = su.get_lines_from_file(file)

# Convert file to array of ints
encoding = su.strings2ints(lines)
target = su.encode_str(args.target)

# Create oracle
num_qubits = 10
integer_to_find = target
num_iter = 20
qc = gp.grover_circuit(num_qubits, integer_to_find, num_iter)
gp.bypass_draw(qc, bypass=True)

# Simulate results
gp.simulate_results(qc, show_hist=False)

# Turn simulated data into user-legible output




