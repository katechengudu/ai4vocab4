import requests
import json
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4vocab4.settings')
django.setup()

from passages.models import Passage, AcademicTerm

import ast  # To safely evaluate string representations of dictionaries


def process_passage(passage, error_log):
    if passage.gpt_response_academic_terms:
        try:
            # Safely evaluate the string to a dictionary
            terms_dict = ast.literal_eval(passage.gpt_response_academic_terms)
        except (ValueError, SyntaxError) as e:
            print(f"Error parsing gpt_response_academic_terms for Passage ID {passage.id}: {e}")
            error_log.append(passage.id)  # Log the Passage ID for later review
            return  # Stop processing this Passage and return

        for term, chinese_meaning in terms_dict.items():
            try:
                AcademicTerm.objects.get_or_create(
                    term=term,
                    chinese_meaning=chinese_meaning,
                    source=passage
                )
                print(passage.id)
                print(term)
                print(chinese_meaning)
                print("****************************************************")
            except Exception as e:
                print(f"Error creating AcademicTerm for Passage ID {passage.id}, Term: '{term}', Error: {e}")
                error_log.append(passage.id)  # Log the Passage ID for later review
                break  # Stop processing further terms for this Passage

if __name__ == "__main__":
    print("Starting to process passages...")
    error_log = []  # Initialize an empty list to track Passages with errors
    for passage in Passage.objects.all():
        process_passage(passage, error_log)

    print("Finished processing passages.")
    if error_log:
        print(f"Errors occurred with the following Passage IDs: {error_log}")
        # Optionally, handle the errored Passages here (retry, inspect, etc.)
