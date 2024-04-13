import os
import django
import json
from html.parser import HTMLParser

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4vocab4.settings')
django.setup()

print("Successfully imported Django and Passage model")

from passages.models import math_text


# HTML Stripper class
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = []
    def handle_data(self, d):
        self.text.append(d)
    def get_data(self):
        return ''.join(self.text)

# Function to strip tags from a string
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# Dictionary mapping 'section' to 'section_merged'
section_to_section_merged = {
    '1-number': 'Number and Operations', '1-number-operations-and-integers': 'Number and Operations', 
    '10-mensuration': 'Geometry and Measures', '11-probability': 'Probability', 
    '12-statistics': 'Statistics', '2-algebra': 'Algebra', '2-algebra-and-functions': 'Algebra', 
    '2-fractions-decimals-and-percentages': 'Fractions, Decimals, and Percentages', 
    '3-coordinate-geometry': 'Coordinate Geometry', '3-indices-and-surds': 'Algebra', 
    '3-ratio-proportion-and-rates-of-change': 'Ratio, Proportion, and Rates of Change', 
    '4-approximation-and-estimation': 'Approximation and Estimation', '4-calculus': 'Calculus', 
    '4-geometry-and-measures': 'Geometry and Measures', '5-matrix-transformations': 'Matrix Transformations', 
    '5-probability': 'Probability', '5-ratio-proportion-and-rates-of-change': 'Ratio, Proportion, and Rates of Change', 
    '6-algebra': 'Algebra', '6-statistics': 'Statistics', '7-graphs-of-equations-and-functions': 'Graphs and Equations', 
    '8-basic-geometry': 'Geometry and Measures', '9-congruence-and-similarity': 'Congruence and Similarity'
}

# Get the total number of objects for progress tracking
total_objects = math_text.objects.count()
print(f"Total objects to process: {total_objects}")

# Loop through all math_text objects
for index, obj in enumerate(math_text.objects.all(), start=1):
    # Update 'section_merged' from the dictionary if the section is a key in the dictionary
    if obj.section in section_to_section_merged:
        obj.section_merged = section_to_section_merged[obj.section]

    # Parsing 'haochen_data_problem'
    problem_data_json = json.loads(obj.haochen_data_problem)
    problem_text = ' '.join([strip_tags(item['body']) for item in problem_data_json])

    # Parsing 'haochen_data_solution'
    solution_data_json = json.loads(obj.haochen_data_solution)
    solution_text = ' '.join([strip_tags(item['body']) for item in solution_data_json])

    # Save the cleaned text and updated 'section_merged' to the math_text object
    obj.english_text_problem = problem_text
    obj.english_text_solution = solution_text
    obj.save()

    print(f"Processed {index}/{total_objects}: Updated object ID {obj.id}")
    print("-" * 80)  # Print a separator line for readability




    
# python 2_get_p_tag_text.py