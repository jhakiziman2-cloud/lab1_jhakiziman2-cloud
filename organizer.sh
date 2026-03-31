#!/usr/bin/bash

# Creating archive folder if it doesn't exist
if [ ! -d "archive" ]; then
    mkdir archive
fi

# Checking if grades.csv exists
if [ ! -f "grades.csv" ]; then
    echo "No grades.csv file found."
    exit 1
fi

# Generating timestamp
timestamp=$(date +"%Y%m%d-%H%M%S")

# New filename
new_filename="grades_$timestamp.csv"

# Moving and renameing file
mv grades.csv archive/$new_filename

# Creating a new empty grades.csv
touch grades.csv

# Logging the operation
echo "$timestamp - grades.csv archived as $new_filename" >> organizer.log

echo "Archiving complete."
