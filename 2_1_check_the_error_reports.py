import requests
import json
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4vocab4.settings')
django.setup()

from passages.models import Passage, AcademicTerm


def display_passage_details(passage_ids):
    for passage_id in passage_ids:
        try:
            passage = Passage.objects.get(id=passage_id)
            print(f"Details for Passage ID {passage_id}:")
            print(f"Book: {passage.book}")
            print(f"Order: {passage.order}")
            print(f"English Text: {passage.english_text}")
            print(f"Chinese Translation: {passage.chinese_translation}")
            print(f"Token Count: {passage.token_count}")
            print(f"Sentence Count: {passage.sentence_count}")
            # If sentences is a ManyToMany field, you might need to iterate over it
            print("Sentences:")
            for sentence in passage.sentences.all():
                print(f" - {sentence}")
            print(f"Haochen Database ID: {passage.haochen_database_id}")
            print(f"GPT Response Academic Terms: {passage.gpt_response_academic_terms}")
            print(f"GPT Response Parsing Failed: {passage.gpt_response_parsing_failed}")
            print("****************************************************")
        except Passage.DoesNotExist:
            print(f"Passage with ID {passage_id} does not exist.")

# Replace [294395, 295875] with the actual list of errored Passage IDs you have
errored_passage_ids = [294395, 295875]
display_passage_details(errored_passage_ids)
