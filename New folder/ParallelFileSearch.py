import os
from concurrent.futures import ProcessPoolExecutor, as_completed, TimeoutError
from multiprocessing import current_process

# Function to search for a pattern in a single line within a file
def search_in_line(filename, pattern, line, line_number):
    if pattern in line:
        # Construct the output message
        message = (f"Process ID: {current_process().pid}, "
                   f"Filename: {filename}, Line number: {line_number}")
        print(message)

# Function to read a file and search for the pattern in each line using a separate ProcessPoolExecutor
def search_in_file(filename, pattern):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            # Spawn a separate ProcessPoolExecutor for line-level parallelism
            with ProcessPoolExecutor() as line_executor:
                futures = [line_executor.submit(search_in_line, filename, pattern, line, line_number + 1)
                           for line_number, line in enumerate(lines)]
                
                # Wait for all line-level tasks in this file to complete
                for future in as_completed(futures):
                    future.result()
    except FileNotFoundError:
        print(f"Could not open file: {filename}")

def main(pattern, files):
    # Outer ProcessPoolExecutor to process each file in parallel
    with ProcessPoolExecutor() as file_executor:
        futures = [file_executor.submit(search_in_file, filename, pattern) for filename in files]
        
        # Wait for all file-level tasks to complete
        for future in as_completed(futures):
            try:
                future.result()
            except TimeoutError:
                print("A file search task timed out.")

if __name__ == "__main__":
# Generate a list of files from file1.txt to file50.txt
    files = [f"../Text Files/file{i}.txt" for i in range(1, 21)]
    pattern = "programming"

    main(pattern, files)
