from django.core.management.base import BaseCommand
from passages.models import Passage
import json

class Command(BaseCommand):
    help = 'Export values from Passage.gpt_response_academic_terms_incorrect_removed to a JSON file'

    def handle(self, *args, **kwargs):
        self.stdout.write("Exporting values from Passage.gpt_response_academic_terms_incorrect_removed to JSON file...")

        # Get all Passage objects with non-empty gpt_response_academic_terms_incorrect_removed field
        passages_with_terms = Passage.objects.exclude(gpt_response_academic_terms_incorrect_removed__isnull=True).exclude(gpt_response_academic_terms_incorrect_removed='')

        # Initialize a dictionary to store the values
        all_terms = {}

        # Get the total number of passages with terms
        total_passages = passages_with_terms.count()

        # Loop through each Passage object
        for index, passage in enumerate(passages_with_terms, start=1):
            # Retrieve the JSON string from gpt_response_academic_terms_incorrect_removed
            terms_json = passage.gpt_response_academic_terms_incorrect_removed
            # Convert the JSON string to a dictionary
            try:
                terms_dict = json.loads(terms_json)
            except json.JSONDecodeError as e:
                self.stdout.write(f'Error decoding JSON for Passage ID {passage.id}: {e}')
                continue  # Skip to the next passage if JSON decoding fails

            # Check if terms_dict is a dictionary
            if isinstance(terms_dict, dict):
                # Print the passage ID for debugging purposes
                self.stdout.write(f'Processing Passage ID: {passage.id}')

                # Merge the terms into the overall dictionary
                for key, value in terms_dict.items():
                    all_terms[key] = value

                # Print progress
                self.stdout.write(f'Processed {index}/{total_passages} passages.', ending='\r')
            else:
                self.stdout.write(f'Error: Invalid JSON format for Passage ID {passage.id}: {terms_dict}')

        # Define the filename for the JSON file
        output_filename = "academic_terms.json"

        # Write the terms to the JSON file with ensure_ascii=False
        with open(output_filename, "w", encoding="utf-8") as json_file:
            json.dump(all_terms, json_file, ensure_ascii=False)

        self.stdout.write(self.style.SUCCESS(f'Successfully exported academic terms to {output_filename}'))

        # Call read_unique_academic_terms to read the JSON file and print unique terms
        unique_terms = read_unique_academic_terms(output_filename)
        self.stdout.write("Unique key-value pairs:")
        for key, value in unique_terms.items():
            self.stdout.write(f"{key}: {value}")
        self.stdout.write(f"Total number of unique key-value pairs: {len(unique_terms)}")

# This function is moved outside the Command class
def read_unique_academic_terms(filename):
    unique_terms = {}
    with open(filename, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

    for key, value in data.items():
        # Check if the key-value pair is unique
        if value not in unique_terms.values():
            unique_terms[key] = value

    return unique_terms





# python manage.py all_passage_academic_terms