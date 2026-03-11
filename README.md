# SQL Window Functions Mastery

> [!CAUTION]
> **⚠️ Disclaimer**
> 1. This entire project (code, tutorials, exercises, solutions, and documentation) is **auto-generated** using various AI tools, including **Antigravity**, **Gemini**, and **ChatGPT**.
> 2. While the exercises have been **manually verified by humans**, there is **no guarantee of correctness, completeness, or safety**.
> 3. **Use at your own risk.** The developers assume no responsibility for any issues, errors, or damages arising from the use of this repository.
> 4. This is NOT intended to be a serious production or academic project; it is a **personal learning journey** and experimentation with AI-assisted coding.

Welcome to the **SQL Window Functions Mastery** project! This repository contains a comprehensive set of tutorials, interactive exercises, and interview questions designed to help you master SQL Window Functions using **DuckDB** and **Python**. 

Why **DuckDB**? Normally it is cumbersome to setup/connect to a database server. DuckDB allows us to work on data using SQL from within Python. It is the simplest approach for learning and practicing the Window functions here.  

## 📖 Overview

Window functions are a powerful feature in SQL that allow you to perform calculations across a set of table rows that are related to the current row, without collapsing the results like standard aggregate functions do.

This project covers the most important window functions categorized into the following modules:

- **Ranking Functions**: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`
- **Value Functions**: `LAG()`, `LEAD()`, `FIRST_VALUE()`, `LAST_VALUE()`
- **Aggregate Functions**: `SUM() OVER()`, `AVG() OVER()`, `COUNT() OVER()`, `MIN() OVER()`, `MAX() OVER()`
- **Distribution & Statistical Functions**: `NTILE()`, `CUME_DIST()`, `PERCENT_RANK()`

### 🏆 The End Goal: Interview Questions
All the modules above serve as preparation for the **Interview Questions** suite. This is where you put your skills to the test with 20 common SQL interview challenges that require combining multiple window function techniques.

## 📂 Project Structure

Each module (e.g., `ranking_functions`, `value_functions`) is organized into an easy-to-follow structure:

- `tutorials/`: Contains Python scripts that guide you through the concepts with functioning SQL examples.
- `exercises/`: Contains interactive exercises where you fill in the missing SQL queries.
- `solutions/`: Contains the correct SQL solutions for all exercises.
- `setup.py` / `validators.py`: Utility scripts for setting up the DuckDB in-memory database, generating sample data, and validating your exercise solutions.
- `run_all.py`: A convenient script to execute all tutorials or exercises within a module at once.

## 🚀 Getting Started

### Prerequisites

You need Python 3 installed. The project relies on a few external libraries, primarily **DuckDB** for executing the SQL queries locally and fast, and **pandas** for data manipulation/display.

### Installation

1. Clone this repository or download the source code.
2. It's recommended to create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   # .venv\Scripts\activate   # On Windows
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

### Running Tutorials
To learn about a specific function, run its corresponding tutorial script. For example:
```bash
python value_functions/tutorials/lag.py
```

### Solving Exercises
Navigate to the `exercises/` folder of the module you are studying. Open a file, find the placeholder for the SQL query, and implement your solution. Then, run the script to test your query against the automated validation logic:
```bash
python value_functions/exercises/lag.py
```
If your output matches the expected results, the script will let you know you passed!

#### 💡 Need a Hint?
For the **Interview Questions**, if you're stuck, you can get a conceptual hint by adding `hint` to the command:
```bash
python interview_questions/exercises/01_top_n_records.py hint
```

### Running Everything
You can also run all tutorials or exercises in a module using the `run_all.py` script:
```bash
python aggregate_functions/run_all.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
