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

# Get the total number of objects for progress tracking
total_objects = math_text.objects.count()
print(f"Total objects to process: {total_objects}")

# Loop through all math_text objects
for index, obj in enumerate(math_text.objects.all(), start=1):
    # Parsing 'haochen_data_problem'
    problem_data_json = json.loads(obj.haochen_data_problem)
    problem_text = ' '.join([strip_tags(item['body']) for item in problem_data_json])
    
    # Parsing 'haochen_data_solution'
    solution_data_json = json.loads(obj.haochen_data_solution)
    solution_text = ' '.join([strip_tags(item['body']) for item in solution_data_json])
    
    # Save the cleaned text to the math_text object
    obj.english_text_problem = problem_text
    obj.english_text_solution = solution_text
    obj.save()

    print(f"Processed {index}/{total_objects}: Updated object ID {obj.id}")
    print("-" * 80)  # Print a separator line for readability
    
# python 2_get_p_tag_text.py