import requests
import json
import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4vocab4.settings')
django.setup()


from passages.models import Passage

# Situation 1: Counting and recording Passage objects where the chinese_translation field has the value "Error in response" or is an empty string.

# Query to find passages with the specific conditions
passages_with_translation_errors = Passage.objects.filter(
    chinese_translation="Error in response"
).union(
    Passage.objects.filter(chinese_translation='')
)

# Count the passages
count_chinese_translation_error = passages_with_translation_errors.count()

# Get the list of ids
passage_ids_with_translation_errors = list(passages_with_translation_errors.values_list('id', flat=True))

# Print the results
print(f"Number of Passage objects with chinese_translation value 'Error in response' or empty: {count_chinese_translation_error}")
print(f"List of Passage IDs with translation errors or empty: {passage_ids_with_translation_errors}")


print("*****************************************************************")

import os
import django
from django.db import transaction

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4vocab4.settings')
django.setup()

from passages.models import Passage  # Ensure this path matches your project structure

YOUR_API_KEY = "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"


def gpt_translation_and_academic_terms(english_text, YOUR_API_KEY):
    # Define the API endpoint
    endpoint = "https://api.openai.com/v1/chat/completions"
    
    # Set the headers
    headers = {
        "Authorization": f"Bearer {YOUR_API_KEY}",
        "Content-Type": "application/json"
    }

    # Define the payload for the chat endpoint with the model specified
    payload = {
        "model": "gpt-3.5-turbo-0613",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Your task is to process the text provided by the user "
                    "and return your response in JSON format with two parts: 'Chinese Translation' for the "
                    "translated text and 'academic_terms' for the dictionary of math terms. "
                    "First, translate the text into Simplified Chinese, ensuring accuracy and retaining "
                    "the original context and meaning. The translated text should be stored in 'Chinese Translation'. "
                    "Next, identify all math-related terms and store them in 'academic_terms'."
                    "You should refer to UK GCSE, A-level and IB exam and textbook materials to identify "
                    "the math-related terms. "
                    "When storing the math terms, use the following format: the original english words as the key, "
                    "and the translated chinese words as the value. For example, if the original english word is "
                    "'probability', and the translated chinese word is '概率', then the key-value pair should be "
                    "'probability': '概率'."
                )
            },
            {"role": "user", "content": english_text}
        ]
    }

    # Make the request
    response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
    response_json = response.json()
    print(response_json)
    
    # Initialize the return variables
    chinese_translation = ""
    bilingual_terms = {}
    parsing_failed = None

    # Check if "choices" key exists in the response
    if "choices" in response_json:
        # Extract the content from the response
        content = response_json["choices"][0]["message"]["content"].strip()

        # Try to parse the content as JSON
        try:
            parsed_content = json.loads(content)
            chinese_translation = parsed_content.get("Chinese Translation", "")
            bilingual_terms = parsed_content.get("academic_terms", {})
            print(f"GPT response parsing succeeded: {content}")
        except json.JSONDecodeError:
            # Store the raw string content when parsing fails
            parsing_failed = content
            print(f"GPT response parsing failed: {content}")

    else:
        # Print out the entire response for debugging
        chinese_translation = "Error in response"
    
    return chinese_translation, bilingual_terms, parsing_failed






def update_passages_with_gpt_translation_and_academic_terms(YOUR_API_KEY):
    # Select passages directly by ID from the predefined list
    passages_to_process = Passage.objects.filter(id__in=passage_ids_with_translation_errors)

    total_passages = passages_to_process.count()
    print(f"Total Passages to process: {total_passages}")

    processed_count = 0
    error_passage_ids = []

    # Process each passage one by one
    for passage in passages_to_process:
        try:
            with transaction.atomic():  # Use a transaction to ensure data integrity for each passage
                english_text = passage.english_text
                chinese_translation, bilingual_terms, parsing_failed = gpt_translation_and_academic_terms(english_text, YOUR_API_KEY)

                if parsing_failed:
                    passage.gpt_response_parsing_failed = parsing_failed
                    print(passage.english_text)
                    print(parsing_failed)
                else:
                    passage.chinese_translation = chinese_translation
                    passage.gpt_response_academic_terms = bilingual_terms
                    print(passage.english_text)
                    print(chinese_translation)
                    print(bilingual_terms)

                passage.save()
                print(f"Processed Passage ID {passage.id} successfully.")
                print("************************************************************")
                processed_count += 1

        except Exception as e:
            print(f"Error processing Passage ID {passage.id}: {e}")
            error_passage_ids.append(passage.id)
            print("************************************************************")

    print(f"Processed {processed_count}/{total_passages} passages.")
    print("************************************************************")
    
    if error_passage_ids:
        print("Passages that encountered errors:", error_passage_ids)
    else:
        print("No errors encountered.")



# Call the function to start the process
update_passages_with_gpt_translation_and_academic_terms(YOUR_API_KEY)


# python 1_3_handle_failed_situation_1.py