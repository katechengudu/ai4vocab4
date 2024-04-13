import os
import django
import spacy
from django.db.models import Count
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4vocab4.settings')
django.setup()

print("Successfully imported Django and Passage model")

from passages.models import math_text, MathTextToken, MathTokenOrigin


# Finding duplicates based on 'section_merged', 'topic', 'english_text_problem', and 'english_text_solution'
duplicates = math_text.objects.values(
    'topic', 'english_text_problem', 'english_text_solution'
).annotate(
    count=Count('id')
).filter(count__gt=1)


# Initialize a counter for the total number of duplicates
total_duplicates = 0

# Check if there are any duplicates
if duplicates.exists():
    # Specify the CSV file name
    csv_file_name = 'duplicated_math_texts.csv'
    
    # Open the CSV file for writing
    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['ID', 'Section Merged', 'Topic', 'English Text Problem', 'English Text Solution', 'Section', 'Haochen Database ID'])
        
        # For each set of duplicate criteria, find, write, and delete the corresponding records
        for dup in duplicates:
            # Fetching detailed rows matching the duplicate criteria
            matching_rows = math_text.objects.filter(
                topic=dup['topic'],
                english_text_problem=dup['english_text_problem'],
                english_text_solution=dup['english_text_solution']
            ).order_by('id')
            
            # Counter for duplicates in the current set (excluding the first row)
            current_set_duplicates = matching_rows.count() - 1
            
            # Update the total counter
            total_duplicates += current_set_duplicates
            
            # Keep the first one and remove the rest
            first_row = True
            for row in matching_rows:
                if first_row:
                    # Skip the first row to keep it
                    first_row = False
                    continue
                
                # Write each row's details to the CSV file before deleting
                writer.writerow([
                    row.id,
                    row.section_merged, 
                    row.topic, 
                    row.english_text_problem, 
                    row.english_text_solution,
                    row.section,
                    row.haochen_database_id
                ])
                
                # Delete this duplicate row
                row.delete()
    
    print(f"Total duplicates found and deleted: {total_duplicates}")
    print(f"Duplicated rows have been successfully saved to {csv_file_name} and deleted from the database.")
else:
    print("No duplicated rows found.")


# python 3_check_and_delete_duplicates.py