"""
Python code to do string-search using Grover's algorithm.
"""
import grover_pattern as gp
import str_utils as su
import numpy as np
import argparse

# Get arguments
parser = argparse.ArgumentParser()
parser.add_argument('filename', help='Filename to search.') # Get file to search
parser.add_argument('target', help='String to search for.') # Get string to search for
args = parser.parse_args()

# Get file data
file = args.filename

# Convert files to array of strings based on line numbers
lines = su.get_lines_from_file(file)

# Convert file and target to ints
target = su.encode_str(args.target)
encoding = su.strings2ints(lines)

# Get inputs for oracle creation
num_qubits = np.ceil(np.log2(encoding.max() + 1)).astype(int)
num_iter = 12
master_indices = []

for i, target_int in enumerate(target):
    # Create oracle
    qc = gp.grover_circuit(num_qubits, target_int, num_iter)

    # Simulate results
    probabilities = gp.match_ints(encoding.flatten(), qc, target_int)

    # Get indices of candidates
    indices = np.argwhere(probabilities >= np.mean(probabilities))[:,0].tolist()

    # Compare indices and see if sequential -- potential solutions
    indices_to_remove = []
    if i == 0:
        master_indices = indices
    else:
        for j in master_indices:
            if j+i not in indices:
                indices_to_remove.append(j)
    
    # Remove all failed comparisons
    for j in indices_to_remove:
        master_indices.remove(j)

# Turn simulated data into user-legible output
line_numbers = np.floor(np.asarray(master_indices) / encoding.shape[1]).astype(int)

# Print all lines to user
for i in line_numbers:
    print(lines[i])

print(f"{len(master_indices)} total lines found containing the target string. Results printed above.\n")
