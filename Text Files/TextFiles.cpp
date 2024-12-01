#include <iostream>
#include <fstream>
#include <vector>
#include <cstdlib>
#include <ctime>

using namespace std;

int main()
{
    const int numberOfFiles = 50;
    const int minLines = 200;
    const int maxLines = 400;
    const string repeatedLines[] = {
        "Hello, welcome to the world of programming. Programming is fun.",
        "Today is a beautiful day for coding. Coding helps improve skills.",
        "C++ is a powerful language for software development. Software development requires practice.",
        "Learning never exhausts the mind; the mind is always ready to learn.",
        "The best way to predict the future is to invent it; inventing takes creativity.",
        "Debugging is like being the detective in a crime movie. Every detective must solve a mystery.",
        "The only way to do great work is to love what you do; love for your work is essential.",
        "Success is not the key to happiness. Happiness is the key to success.",
        "Creativity is intelligence having fun. Fun can spark creativity.",
        "To be or not to be, that is the question. The question of existence.",
        "A journey of a thousand miles begins with a single step. Each step counts in a journey.",
        "In the end, we will remember not the words of our enemies, but the silence of our friends.",
        "Simplicity is the soul of efficiency; efficiency is key in our work.",
        "There are only two hard things in computer science: cache invalidation and naming things.",
        "Programming is thinking, not typing; typing is just a means to programming.",
        "The future belongs to those who believe in the beauty of their dreams; dreams inspire the future.",
        "Life is what happens when you're busy making other plans; plans can change.",
        "Every moment is a fresh beginning. A beginning can lead to great things.",
        "The mind is everything. What you think, you become. You become what you believe.",
        "You cannot change your future, but you can change your habits; habits shape your future.",
        "The only limit to our realization of tomorrow is our doubts of today; doubts can hinder progress.",
        "What we fear doing most is usually what we most need to do. Facing fears can lead to growth.",
        "Do not wait to strike till the iron is hot, but make it hot by striking; striking while the iron is hot.",
        "Success usually comes to those who are too busy to be looking for it; busy people often find success.",
        "Perseverance is not a long race; it is many short races one after the other; each race matters.",
        "It's not whether you get knocked down; it's whether you get up; getting up is important.",
        "Everything you’ve ever wanted is on the other side of fear; fear often holds us back.",
        "I find that the harder I work, the more luck I seem to have; luck often favors the hardworking.",
        "Opportunities don't happen; you create them; creating opportunities is essential.",
        "Success is not how high you have climbed, but how you make a positive difference to the world; making a difference is key.",
        "Debugging is like being the detective in a crime movie. Every detective must solve a mystery. The only way to do great work is to love what you do; love for your work is essential. Success is not the key to happiness. Happiness is the key to success. Creativity is intelligence having fun. Fun can spark creativity. To be or not to be, that is the question. The question of existence.",
        "Hello, welcome to the world of programming. Programming is fun. Today is a beautiful day for coding. Coding helps improve skills. C++ is a powerful language for software development. Software development requires practice. Learning never exhausts the mind; the mind is always ready to learn. The best way to predict the future is to invent it; inventing takes creativity. Debugging is like being the detective in a crime movie. Every detective must solve a mystery. The only way to do great work is to love what you do; love for your work is essential. Success is not the key to happiness. Happiness is the key to success. Creativity is intelligence having fun. Fun can spark creativity. To be or not to be, that is the question. The question of existence.",
    };

    srand(static_cast<unsigned>(time(0))); // Seed for random number generation

    for (int fileIndex = 1; fileIndex <= numberOfFiles; ++fileIndex)
    {
        string filename = "file" + to_string(fileIndex) + ".txt";
        ofstream outFile(filename);

        int totalLines = minLines + rand() % (maxLines - minLines + 1); // Random number of lines between 50 and 70

        for (int lineNumber = 0; lineNumber < totalLines; ++lineNumber)
        {
            // Randomly select a line from repeatedLines to add to the file
            outFile << repeatedLines[rand() % (sizeof(repeatedLines) / sizeof(repeatedLines[0]))] << endl;
        }

        outFile.close();
    }

    return 0;
}
