import re
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed


def search_chunk(lines_with_numbers, pattern,file_path):
    """Searches for the pattern in a chunk of lines, and includes line numbers."""
    matches = []
    for line_number, line in lines_with_numbers:
        if re.search(pattern, line, re.IGNORECASE):  # Case-insensitive search
            matches.append(f"{line_number}: {line.strip()}")  # Format with line number, remove whitespace
            print(f"In {file_path} line where match is found: {line_number} and line is {line}" )
    return matches

def read_file_in_chunks(file_path, chunk_size):
    """Reads a file in chunks of lines, including line numbers."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            line_number = 1
            while True:
                lines_with_numbers = [(line_number + i, file.readline()) for i in range(chunk_size)]
                if not lines_with_numbers[0][1]:  # If the first line is empty, end of file reached
                    break
                yield lines_with_numbers
                line_number += chunk_size
    except Exception as e:
        print(f"Error reading {file_path}: {e}")


def search_file_in_chunks(file_path, pattern, chunk_size):
    """Splits the file into chunks and searches each chunk for the pattern using threads."""
    matches = []
    chunks = read_file_in_chunks(file_path, chunk_size)

    # Use ThreadPoolExecutor to search each chunk in parallel
    with ThreadPoolExecutor() as thread_executor:
        futures = [thread_executor.submit(search_chunk, chunk, pattern,file_path) for chunk in chunks]
        for future in futures:
            try:
                chunk_matches = future.result()  # Get the result from the future
                matches.extend(chunk_matches)    # Add matches to the overall list
            except Exception as e:
                print(f"Error processing chunk in {file_path}: {e}")

    return matches


def parallel_search(file_paths, pattern, chunk_size):
    """Performs parallel search across multiple files, using chunk-based logic."""
    with ProcessPoolExecutor() as process_executor:
        futures = {process_executor.submit(search_file_in_chunks, path, pattern, chunk_size): path for path in file_paths}
        
        for future in as_completed(futures):
            file_path = futures[future]
            try:
                matches = future.result()
                if len(matches) == 0:
                    # print(f"\nMatches in {file_path}:")
                    # # for match in matches:
                    # #     print("Line where match is found: " + match)
                    print(f"\nNo matches found in {file_path}.\n")
                # else:
                    # print(f"\nNo matches found in {file_path}.\n")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")


if __name__ == "__main__":
    # pattern = "chin tapak dum dum"
    # file_paths = []
    file_paths = [f"file{i}.txt" for i in range(1, 51)]
    pattern = "pro"
    
    # while True:
    #     file_name = input("Enter name of file with .txt or press 'z' to go for search: \n")
    #     if file_name == 'z':
    #         break
    #     else:
    #         file_paths.append(file_name)
    
    if len(file_paths) <= 0:
        print("Please enter name of file")
    else:
        parallel_search(file_paths, pattern, chunk_size=5)
