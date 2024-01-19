# RunDeck Job Processing Application

Welcome to the RunDeck Job Processing Application! This tool is designed to handle RunDeck Job descriptions stored as XML files, providing an efficient process to convert, analyze, and document the information.

## Overview

### Input XML Processing

- The application reads all XML files present in the "Input_XML" folder, containing RunDeck Job descriptions.
- For each XML file, it extracts relevant information and converts it into JSON format.

### JSON Output

- Converted JSON files are stored in the "Json_File" folder, in a file named "input_json.json".

### Cron Expression Generation

- The application traverses through each generated JSON file.
- Using the extracted information, it creates Cron Expressions, a scheduling format used in Unix-like operating systems.

### Description Assignment

- For each Cron Expression generated, the application associates descriptive information, including details about the scheduled task and its purpose.

### Output Storage

- The final processed information, including Cron Expressions and associated descriptions, is stored in the "final_json.json" file within the "Json_File" folder.

### Result Summary

- A comprehensive summary is compiled in an "output_jobs.xlsx" file.
- This Excel file serves as structured output, providing a clear overview of the extracted data, generated Cron Expressions, and their corresponding descriptions.

## Usage

Follow these simple steps to make the most of the RunDeck Job Processing Application:

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/G-Balamurugan/RunDeck_Interpretation.git
    ```
    Clone the application repository to your local machine using the provided command.

2. **Input XML Files:**
    - Place your RunDeck Job XML files in the designated **"Input_XML" folder**.

3. **Run the Application:**
    - Execute the `main.py` file to seamlessly process and analyze the RunDeck Job descriptions.

Feel free to explore this RunDeck Job Processing Application!

