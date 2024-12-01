#include <iostream>
#include <fstream>
#include <string>
#include <omp.h>

using namespace std;

// Function to count the total lines in a file
int countLines(const string &filename)
{
    ifstream file(filename);
    if (!file.is_open())
    {
        cout << "Could not open file: " << filename << endl;
        return 0;
    }

    int lineCount = 0;
    string line;
    while (getline(file, line))
    {
        ++lineCount;
    }

    file.close();
    return lineCount;
}

// Function to search for a pattern in a file's lines using the line count
void searchInFile(const string &filename, const string &pattern, int totalLines)
{
    // Allocate an array to store lines
    string *results = new string[totalLines];

    // Open the file and read all lines into the results array
    ifstream file(filename);
    if (!file.is_open())
    {
        cout << "Could not open file: " << filename << endl;
        delete[] results; // Clean up allocated memory
        return;
    }

    // Read all lines into the results array
    for (int i = 0; i < totalLines; ++i)
    {
        getline(file, results[i]);
    }
    file.close();

// Parallel processing of lines
#pragma omp parallel for
    for (int lineNumber = 0; lineNumber < totalLines; ++lineNumber)
    {
        // Check if the pattern is found in the current line
        if (results[lineNumber].find(pattern) != string::npos)
        {
            // Construct the output message as a string
            string message = "\nThread number:" + to_string(omp_get_thread_num()) +
                             ", Filename: " + filename +
                             ", Line number: " + to_string(lineNumber + 1) +
                             ", Line: " + results[lineNumber];
            cout << message;
        }
    }

    delete[] results; // Clean up the allocated memory
}

int main(int argc, char *argv[])
{
    if (argc < 3)
    {
        cout << "Usage: " << argv[0] << " <pattern> [<file1> <file2> ...]" << endl;
        return 1;
    }

    string pattern = argv[1];

    omp_set_nested(1);

// Parallelize the file processing
#pragma omp parallel for
    for (int i = 2; i < argc; ++i)
    {
        string filename = argv[i];
        int totalLines = countLines(filename); // Count lines first

        if (totalLines > 0)
        {
            searchInFile(filename, pattern, totalLines); // Store lines and search
        }
    }

    return 0;
}
