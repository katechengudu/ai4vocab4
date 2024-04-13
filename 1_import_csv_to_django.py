import requests
import json
import os
import django
import csv


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4vocab4.settings')
django.setup()

print("Successfully imported Django and Passage model")

from passages.models import math_text  


# Increase the maximum field size limit
csv.field_size_limit(csv.field_size_limit() * 2)

file = 'Geometry and Measures.csv'


# Open the CSV file
with open(file, newline='', encoding='utf-8') as csvfile:
    # Use csv.reader to read the file
    reader = csv.reader(csvfile)
    # Read and strip the first row (headers)
    headers = [header.strip() for header in next(reader)]
    
    # Print each column name
    print("Stripped column names in the CSV file:")
    for header in headers:
        print(f"'{header}'")  # Using single quotes to visualize spaces



# Now read from the cleaned file, applying strip() to headers
with open(file, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader((line.strip() for line in csvfile))  # Strip potential newline characters
    
    for row in reader:
        # Use get() method to avoid KeyError and strip() to handle potential leading/trailing spaces
        math_instance = math_text(
            level=row.get('level', '').strip(),
            subject=row.get('subject', '').strip(),
            section=row.get('section', '').strip(),
            topic=row.get('topic', '').strip(),
            haochen_database_id=row.get('id', '').strip(),
            haochen_data_problem=row.get('problem', '').strip(),
            haochen_data_solution=row.get('solution', '').strip()
        )
        # Save the instance to the database
        math_instance.save()

print("Data imported successfully")


# python 1_import_csv_to_django.py



