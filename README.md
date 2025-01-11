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

-----

## Installation

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/Muhammad-Usman21/PARALLEL-SEARCHING.git
cd PARALLEL-SEARCHING
```

### 2. Backend Installation

**Step 1:** Navigate to the backend directory

```bash
cd backend
```

**Step 2:** Create and activate a virtual environment (Optional but recommended)
  
```bash
# On Windows:
python -m venv venv  
venv\Scripts\activate
```

**Step 3:** Install dependencies

```bash
pip install -r requirements.txt
```

**Step 4:** Run the backend server

```bash
python run.py
```

### 3. Frontend Installation

**Step 1:** Navigate to the frontend directory

```bash
cd frontend
```

**Step 2:** Install dependencies

```bash
npm install
```

**Step 3:** Create an `.env` file in frontend directory

Add the following to the `.env` file:

```env
VITE_APP_BACKEND_HOST=http://127.0.0.1:5000
VITE_PORT=5173
```

**Step 4:** Run the frontend server

```bash
npm run dev
```

------

## Future Enhancements
- Enhance the pattern-matching algorithm with advanced NLP techniques.
- Implement user authentication for saving search preferences.


