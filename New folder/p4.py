import os
from concurrent.futures import ProcessPoolExecutor

def process_chunk(chunk, start_line, pattern, filename):
    """
    Process a chunk of lines and search for a pattern.
    Prints the process ID, the file being processed, and the matching lines.
    """
    matches = []
    print(f"Process {os.getpid()} starting to process file '{filename}' from line {start_line}")
    
    for i, line in enumerate(chunk):
        if pattern in line:
            matches.append({
                "lineNumber": start_line + i,
                "line": line.strip(),
                "processId": os.getpid(),
                "fileName": filename
            })
            # print(f"Process {os.getpid()} found pattern in file '{filename}', line {start_line + i}")
    
    print(f"Process {os.getpid()} finished processing file '{filename}' up to line {start_line + len(chunk)}")
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
                futures.append(executor.submit(process_chunk, chunk, start_line, pattern, filename))
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

def parallel_search_in_multiple_files(file_list, pattern):
    """
    Perform parallel search across multiple files, and within each file.
    """
    try:
        total_files = len(file_list)
        results = []

        # Outer parallelism: Process each file in parallel
        with ProcessPoolExecutor(max_workers=total_files) as executor:
            futures = []

            # Submit each file for processing
            for filename in file_list:
                print(f"Submitting {filename} for processing with Process ID: {os.getpid()}")
                futures.append(executor.submit(parallel_search_in_file, filename, pattern))

            # Collect results as tasks complete
            for future in futures:
                results.extend(future.result())

        return results

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Example usage
if __name__ == "__main__":
    # List of files to process
    file_list = ["../Text Files/file1.txt", "../Text Files/file2.txt", "../Text Files/file3.txt", "../Text Files/file4.txt", "../Text Files/file5.txt", "../Text Files/file6.txt", "../Text Files/file7.txt", "../Text Files/file8.txt", "../Text Files/file9.txt", "../Text Files/file10.txt"]
    pattern = "prog"

    # Perform the parallel search across multiple files
    matches = parallel_search_in_multiple_files(file_list, pattern)

    # Display the results
    for match in matches:
        print(f"Process ID: {match['processId']}, "
              f"File: {match['fileName']}, "
              f"Line Number: {match['lineNumber']}")
