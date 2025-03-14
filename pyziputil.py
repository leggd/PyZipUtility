import sys
from pathlib import Path
import os
import zipfile
import datetime

"""
input_validation() Function

Verifies the user has ran the program as intended and returns .zip file name

Returns:
    input_file (str): .zip file name if validation passes
    Boolean: False if any validation checks fail
"""
def input_validation():
    # Initialise/Declare Variables
    args = sys.argv # 
    input_file = None
    valid_zip = False

    # Check there is correct amount of command line arguments
    # If len correct, assign input_file variable to argument at index 1
    if len(args) != 2:
        print("Invalid argument amount (usage: python3 d3764716.py xxxx.zip)")
        return False
    else:
        input_file = args
    
    # Obtain list of files in current working directory
    files_in_cwd = os.listdir()   
    
    # Iterate through list to check if .zip file name doesn't exist
    # If file exists, assign Boolean value to valid_zip variable using is_zipfile()
    if not input_file in files_in_cwd:
        print("Zip filename does not exist in current directory")
        return False
    else:
        valid_zip = zipfile.is_zipfile(input_file)

    # Stop function from proceeding if input_file is not a .zip file
    if not valid_zip:
        print("Not a valid zip file, check the integrity of the file specified")
        return False
    
    # If all validation has passed, return .zip file name to main program
    return input_file

"""
menu() Function

Displays a text-based menu in terminal to direct the function of the program

Returns:
    selection (int): User selected option number
"""
def menu():
    # Declare selection list variable containing menu options
    valid_selections = [1 ,2 ,3 ,0]

    # Print menu elements with alignment
    # Infinite loop to obtain user input until valid selection is entered
    while True:
        print("\nMain Menu\n")
        print(" View Zip File Metadata\n".center(53))
        print("[2] View details of Zip File Members\n".center(63))
        print("[3] Extract Zip File\n".center(47))
        print("[0] Quit\n".center(35))

        selection = input("Please enter a selection: ")

        try:
            selection = int(selection)
        except:
            print("\n**** Your selection is not a number ****")
            
        if selection not in valid_selections:
            print("\n**** Invalid selection (1,2,3,0 only) ****")
        else:
            return selection

"""
zip_metadata() Function

Resolve and display .zip file metadata in terminal

Parameter:
    input_file (str): Input file name/path
"""
def zip_metadata(input_file):
    # Declare path object variable
    file_data = Path(input_file)

    # Obtain file path of zip file
    file_path = file_data.resolve()  

    # Obtain all file metadata values and assign to variable
    file_details = file_data.stat()  

    # Obtain individual metadata values from file_details variable using indicies
    file_size = file_details[6]
    file_creation_date = file_details[9]
    file_last_modified_date = file_details[8]
    file_last_accessed_date = file_details[7]

    # Convert Unix time variables to readable dates and reassign variables
    file_creation_date = datetime.datetime.fromtimestamp(file_creation_date).strftime('%d-%m-%Y')  
    file_last_modified_date = datetime.datetime.fromtimestamp(file_last_modified_date).strftime('%d-%m-%Y')  
    file_last_accessed_date = datetime.datetime.fromtimestamp(file_last_accessed_date).strftime('%d-%m-%Y')  

    # Print all metadata values in terminal
    print("\nZIP FILE INFORMATION\n")
    print("Path: ",file_path)
    print("Size: ",file_size,"bytes")
    print("Created: ",file_creation_date)
    print("Last Modified: ",file_last_modified_date)
    print("Last Accessed: ",file_last_accessed_date)

"""
zip_extraction Function

Extract files from user input .zip file to extracted_files sub directory

Parameter:
    input_file (str): Input file name/path
"""
def zip_extraction(input_file):
    # Resolve current working directory path and assign to str variable
    p = Path()
    p = p.resolve()
    cwd = str(p)
    
    # Initialise directory name variable
    directory = 'extracted_files'
    
    # Construct expected extracted files directory path
    extracted_files_dir = os.path.join(cwd, directory)
    
    # Iterate through working directory and store all directories as a list
    dir_list = [x for x in p.iterdir() if x.is_dir()]  

    # Convert list to string for easier interpretation
    dir_list_string = ''.join(str(dir_list))

    # Check if extracted_files directory is present in directory list
    # Create extracted_files directory if directory not already present
    if directory in dir_list_string:
        # Obtain list of file names in extracted_files directory
        files_in_dir = os.listdir(extracted_files_dir)  

        # Iterate through list of file names, removing a file each iteration
        for file in files_in_dir:     
            os.remove(f'{extracted_files_dir}/{file}')     

        # Delete the empty extracted_files directory
        os.rmdir(extracted_files_dir)    

        # Create empty extracted_files directory
        os.mkdir(extracted_files_dir)    
    else:
        os.mkdir(extracted_files_dir)    

    # Extract .zip file to empty extracted_files directory
    with zipfile.ZipFile(input_file) as archive:
        archive.extractall(extracted_files_dir)

    print("\nContents of", "'" + input_file + "'", "extracted to", extracted_files_dir)

    # Set Boolean value so main loop can identify that extraction has taken place
    extracted = True
    return extracted

"""
file_metadata() Function

Obtains file names and selected file metadata values from files
in the extracted_files sub directory and stores values in a dictionary

Returns:
    file_name (list): All string file names on their own
    file_details_dict (dict): File name strings as keys, with each value a list
                              containing metadata values
"""
def file_metadata():
    # Resolve current working directory
    p = Path()
    p = p.resolve()

    # Resolve path to extracted_files directory
    directory = 'extracted_files'
    cwd = str(p)
    dir = os.path.join(cwd, directory)

    # Create path object from extracted_files directory
    p = Path(dir)

    # Collect list of any files and their paths found in extracted_files directory
    file_list_raw = [x for x in p.iterdir() if x.is_file()]

    # Initialise list variable to store file names
    file_name_list = []

    # Iterate through raw file list and collect file names
    for file in file_list_raw:
        file_name = file.parts  
        file_name_list.append(file_name[-1])

    # Initialise dictionary variable to store file details
    file_details_dict = {}
    
    # Iterate through file name list
    # Create key for each file name and initialise empty list value
    for name in file_name_list:
        file_details_dict[name] = []

    # Initialise list variables to store different metadata values
    file_size_list = []
    file_creation_date_list = []
    file_modified_date_list = []

    # Iterate through raw file list
    # Create path and stat object from singular file
    # Obtain metadata from stat object
    # Append metadata values to appropriate lists
    for file in file_list_raw:
        file_data = Path(file)
        file_details = file_data.stat()

        file_size = file_details[6]
        file_creation_time = file_details[9]
        file_modified_time = file_details[8]

        file_size_list.append(file_size)

        file_creation_date = datetime.datetime.fromtimestamp(file_creation_time).strftime('%d-%m-%Y')   
        file_creation_date_list.append(file_creation_date)

        file_modified_date = datetime.datetime.fromtimestamp(file_modified_time).strftime('%d-%m-%Y')   
        file_modified_date_list.append(file_modified_date)

    # Initialise index variable to for proper assignment during iteration
    index = 0

    # Iterate through file name list again
    # Append processed metadata to each list within the dictionary
    # Increase index each iteration
    for file in file_name_list:
        file_details_dict[file].append(file_size_list[index])
        file_details_dict[file].append(file_creation_date_list[index])
        file_details_dict[file].append(file_modified_date_list[index])
        index += 1
    
    return file_name_list, file_details_dict

"""
table_formatter() Function

Creates a HTML table element to display file metadata 

Parameters:
    file_name (str): Name of the File
    file_size (str): Size of the file
    file_creation_date (str): Creation date of file
    file_modified_date (str): Modified date of file

Returns:
    table_entry (str): A concatenated string of all HTML tags and metadata values
"""
def table_formatter(file_name, file_size, file_creation_date, file_modified_date):
    # Declare variables with required HTML tags as strings
    table_open = '<table>'
    table_close = '</table>'

    table_row_header_open = '<tr>\n<th colspan="2">'
    table_row_header_close = '</th>\n</tr>'

    table_row_open = '\n<tr>'
    table_row_close = '\n</tr>'

    table_data_open = '\n<td class="label">'
    table_data_close = '</td>'

    # Elements of the table created using concatanation with input variables
    file_name_header = (table_row_header_open + file_name + 
                        table_row_header_close + table_row_open)
    
    file_size_label = table_data_open + 'File Size' + table_data_close
    
    file_size_data = (table_data_open + file_size + table_data_close + 
                      table_row_close  + table_row_open)

    file_creation_date_label = table_data_open + 'File Creation Date' + table_data_close

    file_creation_data = (table_data_open + file_creation_date + table_data_close + 
                          table_row_close  + table_row_open)

    file_modified_date_label = table_data_open + 'File Modified Date' + table_data_close

    file_modified_data = (table_data_open + file_modified_date + 
                          table_data_close + table_row_close)
    
    # Complete table entry created by concatenating tags and elements
    table_entry = (table_open + file_name_header + file_size_label + 
                   file_size_data + file_creation_date_label + 
                   file_creation_data + file_modified_date_label + 
                   file_modified_data + table_close + '\n')

    return table_entry

"""
create_tables() Function

Creates multiple tables using table_formatter() function

Returns: 
    formatted_tables (str): A string of all table elements formatted in HTML
"""
def create_tables():
    # Initialise list to store formatted HTML tables
    table_entries_list = []

    # Obtain file names list and file details dictionary and assign to variables
    file_names = file_metadata()[0]
    file_info = file_metadata()

    # Iterate through file name list obtaining file metadata values dictionary
    # Obtain singular formatted table entry by calling table_formatter()
    # Add table entry to list of table entries
    for file_name in file_names:
        file_size = str(file_info[file_name][0]) + ' bytes'
        file_creation_date = file_info[file_name]
        file_modified_date = file_info[file_name][2]
        
        table_entry = table_formatter(file_name, file_size, 
                                      file_creation_date, file_modified_date)
        
        table_entries_list.append(table_entry)
    
    # Convert all table entries to string
    formatted_tables = ''.join(table_entries_list)

    return formatted_tables

"""
generate_report() Function

Generates a formatted HTML document to display all data pertaining to files 
extracted from the input .zip file and writes HTML file to current working directory

Parameter:
    input_file(str): Name of the .zip file
"""
def generate_report(input_file):
    # Store CSS style in string variable
    css = """<style>
		body {
        background-color: #ECECEC;
        }
        #banner {
			background-color: #BACBA9;
			font-family: Verdana, sans-serif;
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            padding: 10px;
            margin-bottom: 20px;            
        }
        .label {
			font-family: Verdana, sans-serif;
            text-align: center;
            padding: 6px;
		}
		table {
			font-family: Verdana, sans-serif;
            width: 50%;
            border-collapse: collapse;
            margin: auto;
            margin-bottom: 8px;
            table-layout: fixed
        }
        th {
			border: 1px solid #000000;
            background-color: #BACBA9;
			font-family: Verdana, sans-serif;    
            font-weight: bold;
            text-align: center;
		}
        td {
            border: 1px solid #000000;
            padding: 5px;
			font-family: Verdana, sans-serif;   
			text-align: center;			     
		}
        .footer {
            text-align: center;
			font-family: Verdana, sans-serif;            
			margin-top: 20px;
            padding: 10px;
            background-color: #BACBA9;
        }
    </style>"""

    # Obtain current date and time
    now = datetime.datetime.now()     
    now = str(now)
    
    # String maniupulation to reformat datetime.now() output and strip time
    dd = now[8:10] + '-'
    mm = now[5:7] + '-'
    yyyy = now[0:4]

    # Store current date in DD-MM-YYYY Format
    date = dd + mm + yyyy

    # Create path object for current working directory
    p = Path()
    p = p.resolve()

    # Obtain list of files in current working directory
    files_in_cwd = os.listdir()

    # Check for existing report.html and delete if it exists
    if 'report.html' in files_in_cwd:
        os.remove('report.html')

    # Obtain fully formatted HTML table strings and assign to variable
    formatted_tables = create_tables()

    # Create entire HTML document with concatanation of CSS, tables, zip file name and date
    html_variable = ('<html><head><title>ZIP Extraction Report</title>' + css + 
                     '</head><body><div id="banner">' + input_file + '</div>' + 
                     formatted_tables + '<div class="footer">Daniel Legg - ' + 
                     '<a href="mailto: d3764716@live.tees.ac.uk">d3764716@live.tees.ac.uk</a> - ' +
                      date + '</div></body></html>')
    
    # Write html_variable to current working direcory as report.html in write only mode
    with open("report.html","w") as writer:
        writer.write(html_variable)

"""
main() Function

Contains the main loop of the program and handles user selections and behaviour
"""
# Initialise Boolean variable to track whether user has extracted this session
extracted = False
def main():
    global extracted
    # Obtain input file name from CLA
    input_file = input_validation()

    # Infinite loop while there is a string stored in input_file variable
    # Displays menu and obtains user selection
    # Functions called based on selection value
    # Program ends when input_file is set to None
    while input_file:
        selection = menu()
        if selection == 1:
            zip_metadata(input_file)

        if selection == 2:
            with zipfile.ZipFile(input_file) as archive:
                print("\nZIP FILE MEMBERS\n")
                zipfile.ZipFile.printdir(archive)

        if selection == 3:
            extracted = zip_extraction(input_file)

        if selection == 0:
            if extracted:
                generate_report(input_file)
                print("\nThe program will now end. See report.html for extraction summary\n")
                input_file = None
            else:
                print("\nThe program will now end. No files extracted so no report generated\n")
                input_file = None
         
if __name__ in "__main__":
    main()
