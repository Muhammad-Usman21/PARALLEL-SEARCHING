import os
from concurrent.futures import ProcessPoolExecutor

def process_chunk(chunk, start_line, pattern):
    """
    Process a chunk of lines and search for a pattern.
    Prints the process ID and the matching lines.
    """
    matches = []
    print(f"Processing chunk starting at line {start_line} with Process ID: {os.getpid()}")
    for i, line in enumerate(chunk):
        if pattern in line:
            matches.append({
                "lineNumber": start_line + i,
                "line": line.strip(),
                "processId": os.getpid()
            })
            print(f"Process ID: {os.getpid()} - Line {start_line + i}")
    print(f"Processing chunk ending with Process ID: {os.getpid()}")

    return matches

def divide_into_chunks(lines, chunk_size):
    """
    Divide the list of lines into chunks of the specified size.
    """
    for i in range(0, len(lines), chunk_size):
        yield lines[i:i + chunk_size]

def parallel_search_in_file(filename, pattern):
    """
    Perform parallel search on a single file by dividing it into chunks
    based on the number of available processors.
    """
    try:
        # Read all lines from the file
        with open(filename, 'r') as file:
            lines = file.readlines()
        # lines = read_lines(filename)
        total_lines = len(lines)

        # Determine the number of available cores and calculate chunk size
        total_cores = os.cpu_count() or 1
        chunk_size = total_lines // total_cores

        # If there's a remainder, adjust chunk size for the last chunk
        if total_lines % total_cores != 0:
            chunk_size += 1

        results = []
        with ProcessPoolExecutor(max_workers=total_cores) as executor:
            futures = []
            start_line = 1

            # Divide the lines into chunks and submit tasks to process each chunk
            for chunk in divide_into_chunks(lines, chunk_size):
                futures.append(executor.submit(process_chunk, chunk, start_line, pattern))
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
    for match in matches:
        print(f"Process ID: {match['processId']}, "
              f"Line Number: {match['lineNumber']}")
