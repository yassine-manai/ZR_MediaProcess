import os
import csv

def detectDelimiter(csvFile):
    with open(csvFile, 'r') as myCsvfile:
        header = myCsvfile.readline()
        if ";" in header:
            return ";"
        if "," in header:
            return ","
    # Default delimiter (MS Office export)
    return ";"


def read_data(path, header):
    if not os.path.exists(path):
        return None, "File does not exist."
    
    try:
        if path.lower().endswith('.csv'):
            delimiter = ','
        elif path.lower().endswith('.psv'):
            with open(path, 'r') as file:
                first_line = file.readline()
                delimiter = '|' if '|' in first_line else ';'
        else:
            return None, "Unsupported file format. Please use a .csv file."

        delimiter = detectDelimiter(path)
        print("-----------------------------")
        
        with open(path, 'r') as file:
            if header:
                reader = csv.DictReader(file, delimiter=delimiter)
            else:
                reader = csv.reader(file, delimiter=delimiter)
                headers = next(reader)
                data = [row for row in reader]
                return data
        
            data = [row for row in reader]
            return data

    except csv.Error:
        return None, "Failed to read the file. Please ensure it's a valid CSV file."
    except Exception as e:
        return None, f"An error occurred: {str(e)}"



def read_data_with_header(path, header):
    if not os.path.exists(path):
        return None, "File does not exist."
    
    try:
        if path.lower().endswith('.csv'):
            delimiter = ','
        elif path.lower().endswith('.psv'):
            with open(path, 'r') as file:
                first_line = file.readline()
                delimiter = '|' if '|' in first_line else ';'
        else:
            return None, "Unsupported file format. Please use a .csv file."

        delimiter = detectDelimiter(path)
        
        with open(path, 'r') as file:
            if header == False:
                reader = csv.DictReader(file, delimiter=delimiter)
                data = [row for row in reader]
                
            if header == True:
                reader = csv.reader(file, delimiter=delimiter)
                headers = next(reader) 
                
                custom_headers = [f"colomn{i+1}" for i in range(len(headers))]
                data = [dict(zip(custom_headers, row)) for row in reader]
                
                return custom_headers, data
        
            return data

    except csv.Error:
        return None, "Failed to read the file. Please ensure it's a valid CSV file."
    except Exception as e:
        return None, f"An error occurred: {str(e)}"
