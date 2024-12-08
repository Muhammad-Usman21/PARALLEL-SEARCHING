def count_total_lines(filename):
    """
    Counts the total number of lines in the file using readlines().
    """
    try:
        with open(filename, 'r') as file:
            list_of_lines = file.readlines()
            print(list_of_lines)
            return len(list_of_lines)  # Count lines by reading all into a list
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return 0

def count_total_lines(filename):
    """
    Counts the total number of lines in the file using read() and splitlines().
    """
    try:
        with open(filename, 'r') as file:
            list_of_lines = file.read().splitlines()
            print(list_of_lines)
            return len(list_of_lines)  # Count lines by splitting content
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return 0


filename = "../Text Files/file1.txt"

# Using readlines()
# total_lines = count_total_lines(filename)
# print(f"Total lines in {filename} using readlines(): {total_lines}")

# Using read() + splitlines()
# total_lines = count_total_lines(filename)
# print(f"Total lines in {filename} using read().splitlines(): {total_lines}")
