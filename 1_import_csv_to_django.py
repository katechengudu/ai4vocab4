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

file = 'sql.csv'

# Read the CSV file and write it back out without the BOM
with open(file, 'r', encoding='utf-8-sig') as infile, open('cleaned_sql.csv', 'w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    for row in csv.reader(infile):
        writer.writerow(row)

# Now read from the cleaned file
with open('cleaned_sql.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Create a new math_text instance and set its fields based on the CSV columns
        math_instance = math_text(
            level=row['level'],
            subject=row['subject'],
            section=row['section'],
            topic=row['topic'],
            haochen_database_id=row['id'],
            haochen_data_problem=row['problem'],
            haochen_data_solution=row['solution']
        )
        # Save the instance to the database
        math_instance.save()

print("Data imported successfully")


# python 1_import_csv_to_django.py



