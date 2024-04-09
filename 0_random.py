import os
import django
import spacy
from django.db.models import Count
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4vocab4.settings')
django.setup()

print("Successfully imported Django and Passage model")

from passages.models import math_text, MathTextToken, MathTokenOrigin

# Update the 'section_merged' field for all math_text objects
math_text.objects.update(section_merged="algebra")

print("All math_text objects have been updated with 'algebra' as the section_merged value.")





# python 0_random.py