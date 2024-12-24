# Parallel File Search Website

Check out the live website here: [https://file-search-frontend.onrender.com](https://file-search-frontend.onrender.com)

-------

## Overview
This project is a web application that performs ***parallel searching*** in files to extract:
1. Lines containing a specific ***pattern***.
2. Specific ***headings or sections*** from research papers (e.g., abstract, introduction, etc.).

The frontend is built with ***React***, and the backend is powered by ***Flask*** for efficient processing using parallel computing.

------

## How It Works
1. **Upload Files**: Users can upload ***multiple text files, word files, excel files or research papers (PDFs)***.
2. **Specify Search Criteria**: Provide a ***search pattern or choose specific headings*** to extract.
3. **Parallel Search**: The backend processes files in parallel to deliver fast results.
4. **View Results**: Results are displayed in a structured format on the frontend.
5. **Download Results**: Download the extracted results as a PDF file for future reference.

------

## Tech Stack
### Frontend
- **React**: For creating the user interface.
- **Tailwind CSS & Flowbite**: For responsive and modern styling.

### Backend
- **Flask**: For handling file search and data extraction.
- **Concurrent Programming**: Utilizes `concurrent.futures.ProcessPoolExecutor` for parallel searching.


------

## Future Enhancements
- Enhance the pattern-matching algorithm with advanced NLP techniques.
- Implement user authentication for saving search preferences.


