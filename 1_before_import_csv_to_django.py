import os
import django
import spacy
from django.db.models import Count
import csv
from django.db import transaction
from django.db.models import Q


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4vocab4.settings')
django.setup()

print("Successfully imported Django and Passage model")

from passages.models import math_text, MathTextToken, MathTokenOrigin

# Increase the maximum field size limit
csv.field_size_limit(csv.field_size_limit() * 2)

# Path to your CSV file
csv_file_path = 'Geometry and Measures.csv'

# Open the CSV file and read it
with open(csv_file_path, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    # Read the first row and assume it's the header
    headers = next(reader)
    
    # Print out the headers
    print("CSV Headers:")
    for header in headers:
        print(header)



# Set to store unique values from the 'section' column
unique_sections = set()

# Open the CSV file and read it
with open(csv_file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    # Iterate through each row in the CSV
    for row in reader:
        # Assuming 'section' is the name of the column you're interested in
        section = row['section']
        unique_sections.add(section)

# Print out the unique sections
print("Unique sections:")
for section in unique_sections:
    print(section)





# python 1_before_import_csv_to_django.py