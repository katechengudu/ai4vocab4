import os
import django
import spacy
from django.db.models import Count
import csv
from django.db import transaction
from django.db.models import Q
import pandas as pd


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4vocab4.settings')
django.setup()

print("Successfully imported Django and Passage model")

from passages.models import math_text, MathTextToken, MathTokenOrigin

# Increase the maximum field size limit
csv.field_size_limit(csv.field_size_limit() * 2)







# List of your CSV filenames
filenames = ['sql.csv', 'number.csv', 'algebra(2).csv','Probability.csv','Geometry and Measures.csv','Statistics.csv','the-rest.csv']

# Function to check headers and count empty values
def check_csv(file):
    try:
        # Load the CSV file
        data = pd.read_csv(file)

        # Print headers
        print(f"Headers in {file}:")
        print(data.columns.tolist())

        # Check for empty values
        empty_values_count = data.isnull().sum().sum()  # Sum of all empty values in the DataFrame
        print(f"Total empty values in {file}: {empty_values_count}")
        if empty_values_count > 0:
            print(f"Empty values by column in {file}:")
            print(data.isnull().sum())  # Empty values per column
        print("\n")

    except Exception as e:
        print(f"Error reading {file}: {e}\n")

# Apply the function to each file
for filename in filenames:
    check_csv(filename)


# Delete all objects from math_text model
MathTextToken.objects.all().delete()

# Count all objects in math_text model to confirm deletion
total_count_text = MathTokenOrigin.objects.count()
print("Total count of math_text objects after deletion:", total_count_text)

all_math_texts = math_text.objects.all()
print(f"Found {all_math_texts.count()} MathText objects to process.")

# python 0_random.py