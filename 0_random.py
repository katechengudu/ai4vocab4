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




# Delete all objects from math_text model
MathTextToken.objects.all().delete()

# Count all objects in math_text model to confirm deletion
total_count_text = MathTokenOrigin.objects.count()
print("Total count of math_text objects after deletion:", total_count_text)

all_math_texts = math_text.objects.all()
print(f"Found {all_math_texts.count()} MathText objects to process.")


# List of topics as provided earlier
topics = [
    "1-number",
    "1-number-operations-and-integers",
    "10-mensuration",
    "11-probability",
    "12-statistics",
    "2-algebra",
    "2-algebra-and-functions",
    "2-fractions-decimals-and-percentages",
    "3-coordinate-geometry",
    "3-indices-and-surds",
    "3-ratio-proportion-and-rates-of-change",
    "4-approximation-and-estimation",
    "4-calculus",
    "4-geometry-and-measures",
    "5-matrix-transformations",
    "5-probability",
    "5-ratio-proportion-and-rates-of-change",
    "6-algebra",
    "6-statistics",
    "7-graphs-of-equations-and-functions",
    "8-basic-geometry",
    "9-congruence-and-similarity"
]

# Corresponding section_merged values as listed
section_merged = [
    "Number and Operations",
    "Number and Operations",
    "Geometry and Measures",
    "Probability",
    "Statistics",
    "Algebra",
    "Algebra",
    "Fractions, Decimals, and Percentages",
    "Coordinate Geometry",
    "Algebra",
    "Ratio, Proportion, and Rates of Change",
    "Approximation and Estimation",
    "Calculus",
    "Geometry and Measures",
    "Matrix Transformations",
    "Probability",
    "Ratio, Proportion, and Rates of Change",
    "Algebra",
    "Statistics",
    "Graphs and Equations",
    "Geometry and Measures",
    "Congruence and Similarity"
]

# Create a dictionary by zipping the two lists together
topic_to_section = dict(zip(topics, section_merged))

# Print the resulting dictionary
print(topic_to_section)



# python 0_random.py