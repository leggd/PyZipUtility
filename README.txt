Overview
This Python script is a command-line tool designed to interact with ZIP files. It provides functionality to view metadata, list contents, and extract ZIP files, with an option to generate an HTML report of extracted file details.

Usage
Run the script from the command line with a ZIP file as an argument:

python3 d3764716.py <filename>.zip

Features
1. **View ZIP File Metadata**: Displays file path, size, creation date, last modified date, and last accessed date.
2. **View ZIP File Members**: Lists the contents of the ZIP file.
3. **Extract ZIP File**: Extracts contents to an `extracted_files` directory.
4. **Generate Report**: Creates an HTML report (`report.html`) with details of extracted files upon exit (if extraction occurred).

Requirements
- Python 3.x
- Standard Python libraries: `sys`, `pathlib`, `os`, `zipfile`, `datetime`

How It Works
1. Validates the input ZIP file.
2. Presents a menu for user interaction.
3. Performs selected actions on the ZIP file.
4. Optionally generates an HTML report with styled tables if files are extracted.

Notes
- The script overwrites the `extracted_files` directory if it exists.
- No AI was used in the planning, design, or creation of this code.
- See the source code for detailed comments and references.

Credits
Daniel Legg
Created for an assigned for the module 'Programming for Cyber Security'
