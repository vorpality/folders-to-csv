import csv
import re
import os
import sys
import glob

def extract_number(dir_name):
    """Extract the leading number from a directory name."""
    match = re.match(r'^(\d+)', dir_name)
    return int(match.group()) if match else float('inf')

def find_csv_files(root_folder):
    """Recursively find all CSV files in the folder and subfolders, sorted by directory numbers."""
    csv_files = []
    for root, dirs, files in os.walk(root_folder):
        # Extract numbers and sort directories based on these numbers
        dirs.sort(key=extract_number)
        files.sort()

        for file in files:
            if file.endswith('.csv'):
                csv_files.append(os.path.join(root, file))
    return csv_files

def extract_data_from_csv(csv_file):
    try:
        with open(csv_file, mode='r', newline='', encoding='utf-8', errors='ignore') as file:
            reader = csv.reader(file)
            data = list(reader)
            # Rest of your code to process data...
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError encountered in file: {csv_file}")
        print(f"Error details: {e}")
        return []  # Return an empty list or handle as needed

    """Extract the 3rd column from the 98th row onwards in the CSV file."""
    base_filename = os.path.splitext(os.path.basename(csv_file))[0]


        
    # Ensure the CSV file has at least 98 rows and the rows have a third column
    if len(data) >= 98:
        # Use a list comprehension with a conditional expression to provide a default value
        return [base_filename] + [row[2] if len(row) > 2 else "" for row in data[98:]]
    return []




def extract_column_from_csv(csv_file, row_idx, col_idx):
    try:
        with open(csv_file, mode='r', newline='', encoding='utf-8', errors='ignore') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if i == row_idx:
                    return row[col_idx] if len(row) > col_idx else None
    except UnicodeDecodeError as e:
        print(f"UnicodeDecodeError encountered in file: {csv_file}")
        print(f"Error details: {e}")
    return None

def compile_data_from_folder(folder_path, output_csv_path, output_txt_path):
    # Find all CSV files in the folder and subfolders
    csv_files = find_csv_files(folder_path)
    all_rows = []
    column_results = []
    
    # Open the text file for writing the paths
    with open(output_txt_path, 'w') as txt_file:
        # Process each CSV file
        for csv_file in csv_files:
            # Extract the specified column data from the specified row
            column_value = extract_column_from_csv(csv_file, 38, 1)  # 39th row, 2nd column
            
            if column_value != "Match":
                # Record the non-matching result as a comment in csv_paths.txt
                txt_file.write(f"{csv_file} - Skipped, Column value: {column_value}\n")
                continue  # Skip further processing for this file
            
            txt_file.write(csv_file + "\n")  # Write the path of the CSV file
            
            row = extract_data_from_csv(csv_file)
            if row:  # Only add if the row has data
                all_rows.append(row)
                
            
    # Write all rows to a single output CSV file
    with open(output_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(all_rows)

def main():
    folder_path = os.getcwd()
    output_csv_path = "reformed.csv"
    output_txt_path = "csv_paths.txt"

    # Check if reformed.csv exists and delete it
    if os.path.exists(output_csv_path):
        os.remove(output_csv_path)

    compile_data_from_folder(folder_path, output_csv_path, output_txt_path)
    print(f"Compiled CSV saved to {output_csv_path}")
    print(f"Paths of processed CSV files saved to {output_txt_path}")

if __name__ == "__main__":
    main()
