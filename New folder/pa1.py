import re  #The re module provides support for regular expressions in Python
from concurrent.futures import ProcessPoolExecutor

def search_file(file_path, pattern):
    matches = []
    print(f"Searching in {file_path}...")  #checking which file is accessed
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # print(f"Line read: {line.strip()}")  # Show each line read
                if re.search(pattern, line, re.IGNORECASE):  # Case-insensitive search
                    matches.append(line.strip()) # it appends only that specific line not the whole text
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return matches

def parallel_search(file_paths, pattern):
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(search_file, path, pattern): path for path in file_paths}
        for future in futures:
            file_path = futures[future]
            try:
                matches = future.result()
                if matches:
                    print(f"\nMatches in {file_path}:")
                    for match in matches:
                        print("line where match is found : "+match)
                else:
                    print(f"\nNo matches found in {file_path}.\n")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")


def search_chunk(lines, pattern):
    matches = []
    for line in lines:
        if re.search(pattern, line, re.IGNORECASE):
            matches.append(line.strip())
    return matches

# Function to divide a file into chunks of lines
def read_file_in_chunks(file_path, chunk_size=5):
    with open(file_path, 'r', encoding='utf-8') as file:
        while True:
            lines = [file.readline() for _ in range(chunk_size)]
            if not lines[0]:  
                break
            yield lines #If the end of the file has not been reached function can produce a series of results incrementally rather than returning all results at once.

# Parallel search function for a single large file
def parallel_search_single_file(file_path, pattern, chunk_size=5):
    results = []
    with ProcessPoolExecutor() as executor:
        threads = [executor.submit(search_chunk, lines, pattern) for lines in read_file_in_chunks(file_path, chunk_size)]
        
        for thread in threads:
            matches = thread.result()  # Get the result from the future
            if matches:
                results.extend(matches)
                for match in matches:
                    print(match)    
    if results:
        print(f"\nMatches in {file_path}:")
        for match in results:
            print(match)
    else:
        print(f"\nNo matches found in {file_path}.")

if __name__ == "__main__":
    
    file_paths = ["file1.txt"]
    # file_paths = ["file1.txt"]
    pattern = "."  # Search pattern
    if len(file_paths) > 1:
        parallel_search(file_paths, pattern)
    else:
        parallel_search_single_file(file_paths[0],pattern)