"""
Python code for string and file-parsing utilities for compatibility
with Grover search.
"""
import numpy as np

def get_lines_from_file(filename):
    """
    Function to read an array of lines as strings from a file.

    :param filename: String representing filename to be read from

    :return line_arr: Array of strings representing each line of the file
    """
    # Get number of lines to allocate memory for array
    with open(filename, 'r') as fp:
        num_lines = sum(1 for line in fp)

    # Get length of longest line in file
    longest = len(max(open(filename), key=len))

    # Initialize array of lines
    line_arr = np.empty(num_lines, dtype=f'U{longest}')

    # Open file and get lines in array
    file = open(filename, 'r')
    for line_num in range(num_lines):
        line_arr[line_num] = file.readline()
    file.close()

    return line_arr

def encode_str(string):
    """
    Function to encode a string into an array of unicode values.

    :param string: String to encode

    :return uni_arr: Array of unicode values
    """
    # Convert string to array of chars
    str_arr = np.asarray(list(string))

    # Convert chars into their unicode values
    uni_arr = np.zeros(len(str_arr), dtype=int)
    for i in range(len(uni_arr)):   
        uni_arr[i] = ord(str_arr[i])

    return uni_arr

def strings2ints(arr_lines):
    """
    Function to turn an array of strings into a matrix of characters converted
    into Unicode values.

    :param arr_lines: Array of strings

    :return uni_mat: Matrix of unicode values for characters
    """
    # Get longest string length
    longest = len(max(arr_lines, key=len))

    # Initialize 2D matrix of unicode values
    uni_mat = np.zeros(shape=(len(arr_lines), longest), dtype=int)
    for i in range(len(arr_lines)):
        line = arr_lines[i]
        for j in range(len(line)):
            uni_mat[i][j] = ord(line[j])

    return uni_mat

