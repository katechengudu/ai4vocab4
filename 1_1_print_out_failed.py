
# there are TWO situations to be checked in this script:
# 1. chinese_translation = "Error in response" [gpt did not return a response]
# 2. passage.gpt_response_parsing_failed has value in it

import csv
import os
import django



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4vocab4.settings')
django.setup()

from passages.models import Passage

# Situation 1: Counting and recording Passage objects where the chinese_translation field has the value "Error in response" or is an empty string.

# Query to find passages with the specific conditions
passages_with_translation_errors = Passage.objects.filter(
    chinese_translation__in=["Error in response", '']
)

# Count the passages
count_chinese_translation_error = passages_with_translation_errors.count()



# CSV file setup for Situation 1
csv_filename_1 = 'passages_with_gpt_failed.csv'
with open(csv_filename_1, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Writing the header of the CSV file
    writer.writerow(['Passage ID', 'English Text', 'Chinese Translation','gpt_response_parsing_failed'])

    # Iterate through the passages to write their ids and the chinese_translation values to CSV
    for passage in passages_with_translation_errors.only('id', 'english_text', 'chinese_translation'):
        # Write to the CSV file
        writer.writerow([passage.id, passage.english_text, passage.chinese_translation,passage.gpt_response_parsing_failed])

# Print the results
print(f"Number of Passage objects with chinese_translation value 'Error in response' or empty: {count_chinese_translation_error}")







# Situation 2: Counting and recording Passage objects where the gpt_response_parsing_failed field has some value other than null and is not an exact empty string.

# Query to find passages with the specific conditions
passages_with_parsing_failed = Passage.objects.filter(
    gpt_response_parsing_failed__isnull=False
).exclude(
    gpt_response_parsing_failed__exact=''
)

# Count the passages
count_gpt_response_parsing_failed = passages_with_parsing_failed.count()


# CSV file setup
csv_filename_2 = 'passages_with_gpt_parsing_failed.csv'
with open(csv_filename_2, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Writing the header of the CSV file
    writer.writerow(['Passage ID', 'English Text', 'Parsing Failed Message','chinese_translation','academic_terms'])
    
    # Iterate through the passages to print and write their ids and the gpt_response_parsing_failed values to CSV
    for passage in passages_with_parsing_failed.only('id', 'english_text', 'gpt_response_parsing_failed'):       
        # Write to the CSV file
        writer.writerow([passage.id, passage.english_text, passage.gpt_response_parsing_failed,passage.chinese_translation,passage.gpt_response_academic_terms])

# Print the count of passages again
print(f"Number of Passage objects with Situation 2 gpt_response_parsing_failed: {count_gpt_response_parsing_failed}")


# python 1_1_print_out_failed.py