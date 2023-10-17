'''
Still a TODO for now. 
Will add the players position, draft year and overall pick number, origin country, amateur team to the player data table.
'''
import mysql.connector
import csv
import re

def main():
    # see where there are duplicates
    path = "C:/Users/Owner/OneDrive/Documents/DataWebsite/csv_data/nhldraft.csv"
    
    name_counts = {}

    with open(path) as f:
        reader = csv.reader(f)
        next(reader)  # Skip header row if present
    
        for row in reader:
            # Replace 'name_column_index' with the actual index of the name column
            name = row[4]
            
            # Count occurrences of each name
            if name in name_counts:
                name_counts[name] += 1
            else:
                name_counts[name] = 1

    # Print duplicate names
    for name, count in name_counts.items():
        if count > 1:
            print(f"Duplicate name: {name} (Count: {count})")





if __name__ == "__main__":
    main()