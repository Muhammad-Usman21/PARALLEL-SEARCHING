import os
from concurrent.futures import ProcessPoolExecutor
from itertools import islice

def search_in_chunk(chunk, pattern, start_line):
    """
    Searches for the pattern in a chunk of lines.
    Returns matches with line numbers and process IDs.
    Prints the PID to verify which process is handling the chunk.
    """
    print(f"Processing chunk starting at line {start_line} with Process ID: {os.getpid()}")
    matches = []
    for i, line in enumerate(chunk):
        if pattern in line:
            matches.append({
                "lineNumber": start_line + i,
                "line": line.strip(),
                "processId": os.getpid()
            })
            print(f"process id: {os.getpid()} line number: {start_line + i}")
    return matches



def read_file_in_chunks(filename, chunk_size):
    """
    Generator to read a file in chunks of lines.
    Prints the process ID to verify which process is handling the chunk.
    """
    with open(filename, 'r') as file:
        while True:
            chunk = list(islice(file, chunk_size))
            if not chunk:
                break
            # Print the process ID for every chunk processed
            print(f"Process ID: {os.getpid()} is reading a chunk.")
            yield chunk

def parallel_search_in_file(filename, pattern):
    """
    Perform parallel search on a single file by dividing it into chunks.
    """
    try:
        total_cores = os.cpu_count() or 1  # Number of available CPU cores
        chunk_size = 10  # Number of lines per chunk (adjust as needed)

        results = []
        with ProcessPoolExecutor(max_workers=total_cores) as executor:
            futures = []
            start_line = 1

            # Divide the file into chunks and submit search tasks
            for chunk in read_file_in_chunks(filename, chunk_size):
                futures.append(executor.submit(search_in_chunk, chunk, pattern, start_line))
                start_line += len(chunk)

            # Collect results as tasks complete
            for future in futures:
                results.extend(future.result())

        return results

    except FileNotFoundError:
        print(f"File not found: {filename}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage
if __name__ == "__main__":
    filename = "../Text Files/file1.txt"
    pattern = "is"

    # Perform the parallel search
    matches = parallel_search_in_file(filename, pattern)

    # Display the results
    # for match in matches:
    #     print(f"Process ID: {match['processId']}, "
    #           f"Line Number: {match['lineNumber']}, ")
