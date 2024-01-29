import os
import django
import re


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4vocab4.settings')
django.setup()

from passages.models import Passage



def contains_chinese(text):
    # Check if the text contains any Chinese characters
    return any('\u4e00' <= char <= '\u9fff' for char in text)

def extract_academic_terms(text):
    # Extract academic terms from the text
    academic_terms = {}
    matches = re.finditer(r'"([^"]+)":\s*"([^"]+)"', text)
    for match in matches:
        english_term, chinese_term = match.groups()
        academic_terms[english_term] = chinese_term
    return academic_terms



def extract_chinese_translation(text):
    # Remove the academic terms annotation from the text
    text = re.sub(r'academic_terms:.*?{.*?}', '', text, flags=re.DOTALL)

    # Remove any "Chinese Translation:" or similar annotations
    text = re.sub(r'Chinese Translation:\s*', '', text)

    # Return the cleaned text if it contains Chinese characters
    if contains_chinese(text):
        return text.strip()
    else:
        return None



def parse_and_update_passages():
    passages = Passage.objects.filter(
        gpt_response_parsing_failed__isnull=False
    ).exclude(
        gpt_response_parsing_failed__exact=''
    )

    total_passages = passages.count()
    print(f"Total passages to process: {total_passages}")

    updated_chinese_only = []
    updated_chinese_and_terms = []
    skipped_passages = []
    error_passages = []

    for passage in passages:
        try:
            response = passage.gpt_response_parsing_failed
            academic_terms = extract_academic_terms(response)
            chinese_translation = extract_chinese_translation(response)

            if chinese_translation:
                passage.chinese_translation = chinese_translation
                if academic_terms:
                    passage.gpt_response_academic_terms = str(academic_terms)
                    updated_chinese_and_terms.append(passage.id)
                else:
                    updated_chinese_only.append(passage.id)
                passage.save()
            else:
                skipped_passages.append(passage.id)

        except Exception as e:
            error_passages.append(passage.id)
            print(f"Error processing passage {passage.id}: {e}")

    total_processed = len(updated_chinese_only) + len(updated_chinese_and_terms) + len(skipped_passages) + len(error_passages)

    print(f"Updated Passages with Chinese Translation Only: {len(updated_chinese_only)} - {updated_chinese_only}")
    print(f"Updated Passages with Chinese Translation and Academic Terms: {len(updated_chinese_and_terms)} - {updated_chinese_and_terms}")
    print(f"Skipped Passages: {len(skipped_passages)} - {skipped_passages}")
    print(f"Passages with Errors: {len(error_passages)} - {error_passages}")
    print(f"Total processed passages: {total_processed}")

# Run the function
parse_and_update_passages()


# This def below will iterate through the "chinese_translation" column, 
# extract any academic terms that should not be there, and update the "academic_terms" column accordingly. 
# After processing, it will leave only the correct Chinese translation in the "chinese_translation" column.

from passages.models import Passage
import re


def extract_and_clean_academic_terms(chinese_translation):
    pattern = re.compile(r'"([^"]+)":\s*"([^"]+)"')
    matches = pattern.findall(chinese_translation)
    academic_terms = {match[0]: match[1] for match in matches}
    cleaned_translation = pattern.sub('', chinese_translation).strip()
    return cleaned_translation, academic_terms

# Filtering Passage objects
passages = Passage.objects.exclude(chinese_translation__isnull=True).exclude(chinese_translation__exact='')

total_passages = passages.count()
print("******************************************************************************************")
print(f"Total passages to cleaned_translation process: {total_passages}")

error_responses = []
processed_passages = []
updated_passages = []

for i, passage in enumerate(passages):
    if passage.chinese_translation == "Error in response":
        error_responses.append(passage.id)
    else:
        cleaned_translation, new_academic_terms = extract_and_clean_academic_terms(passage.chinese_translation)
        passage.chinese_translation = cleaned_translation
        
        # Update existing academic terms
        existing_academic_terms = passage.gpt_response_academic_terms or {}
        existing_academic_terms.update(new_academic_terms)
        passage.gpt_response_academic_terms = existing_academic_terms

        passage.save()
        updated_passages.append(passage.id)
    
    processed_passages.append(passage.id)

    # Logging progress for every 100 passages
    if (i + 1) % 100 == 0:
        print(f"Processed {i + 1} / {total_passages} passages.")

# Printing results
print("Processed passages:", len(processed_passages))
print("Updated passages:", len(updated_passages))
print("Passages with error responses:", len(error_responses))
print("Passage IDs with 'Error in response':", error_responses)







# python 1_2_handle_failed_situation_2.py
