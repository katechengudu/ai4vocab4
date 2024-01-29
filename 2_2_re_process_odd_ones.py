import requests
import json
import os
import django
import ast


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4vocab4.settings')
django.setup()

from passages.models import Passage, AcademicTerm

def process_passage(passage, error_log):
    if passage.gpt_response_academic_terms:
        try:
            # Safely evaluate the string to a dictionary
            data = ast.literal_eval(passage.gpt_response_academic_terms)
            # Extract the list of terms from the 'terms' key
            terms_list = data.get('terms', [])
        except (ValueError, SyntaxError) as e:
            print(f"Error parsing gpt_response_academic_terms for Passage ID {passage.id}: {e}")
            error_log.append(passage.id)  # Log the Passage ID for later review
            return  # Stop processing this Passage and return

        for term_dict in terms_list:
            # Attempt to extract 'english' and 'chinese' values with both lowercase and capitalized keys
            english_term = term_dict.get('english') or term_dict.get('English')
            chinese_meaning = term_dict.get('chinese') or term_dict.get('Chinese')
            if english_term and chinese_meaning:  # Ensure both values are present
                try:
                    AcademicTerm.objects.get_or_create(
                        term=english_term,
                        chinese_meaning=chinese_meaning,
                        source=passage
                    )
                    print(passage.id)
                    print(english_term)
                    print(chinese_meaning)
                    print("****************************************************")
                except Exception as e:
                    print(f"Error creating AcademicTerm for Passage ID {passage.id}, Term: '{english_term}', Error: {e}")
                    error_log.append(passage.id)  # Log the Passage ID for later review
                    break  # Stop processing further terms for this Passage


if __name__ == "__main__":
    print("Starting to process specific passages...")
    error_log = []  # Initialize an empty list to track Passages with errors
    specific_passage_ids = [295875]  # List of specific Passage IDs to process

    for passage_id in specific_passage_ids:
        try:
            passage = Passage.objects.get(id=passage_id)
            process_passage(passage, error_log)
        except Passage.DoesNotExist:
            print(f"Passage with ID {passage_id} does not exist.")

    print("Finished processing specific passages.")
    if error_log:
        print(f"Errors occurred with the following Passage IDs: {error_log}")
        # Optionally, handle the errored Passages here (retry, inspect, etc.)
