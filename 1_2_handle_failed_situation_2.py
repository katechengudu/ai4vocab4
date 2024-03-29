import os
import django
import re


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4vocab4.settings')
django.setup()


from passages.models import Passage



def clean_translation(text):
    """
    Initial cleaning to remove JSON-like structures, academic terms annotations, 
    and redundant labels from the text.
    """
    # Remove JSON-like structures
    cleaned_text = re.sub(r'\{.*?\}\s*', '', text, flags=re.DOTALL)
    # Remove academic terms annotations
    cleaned_text = re.sub(r'academic_terms:.*', '', cleaned_text, flags=re.DOTALL)
    # Remove "Chinese Translation" label if present
    cleaned_text = re.sub(r'\"Chinese Translation\":\s*', '', cleaned_text, flags=re.IGNORECASE)
    return cleaned_text.strip()

def contains_chinese(text):
    """
    Check if the text contains any Chinese characters.
    """
    return any('\u4e00' <= char <= '\u9fff' for char in text)

def parse_and_update_passages():
    """
    First stage of processing: Filter passages based on gpt_response_parsing_failed field,
    clean the response, and update the chinese_translation field of the Passage model.
    """
    passages = Passage.objects.filter(
        gpt_response_parsing_failed__isnull=False
    ).exclude(
        gpt_response_parsing_failed__exact=''
    )

    for passage in passages:
        try:
            response = passage.gpt_response_parsing_failed
            chinese_translation = clean_translation(response)

            if chinese_translation and contains_chinese(chinese_translation):
                passage.chinese_translation = chinese_translation
                passage.save()

        except Exception as e:
            print(f"Error processing passage {passage.id}: {e}")

def refine_chinese_translation(text):
    """
    Second stage of cleaning to refine the chinese_translation.
    This removes any residual English text and redundant labels.
    """
    cleaned_text = re.sub(r'\"Chinese Translation\":\s*', '', text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r'[a-zA-Z]', '', cleaned_text).strip()
    return cleaned_text

def parse_and_refine_passages():
    """
    Second stage of processing: Filter passages based on the chinese_translation field,
    refine the translation, and update the Passage model.
    """
    passages = Passage.objects.filter(
        chinese_translation__isnull=False
    ).exclude(
        chinese_translation__exact=''
    )

    for passage in passages:
        try:
            chinese_translation = refine_chinese_translation(passage.chinese_translation)
            if chinese_translation and contains_chinese(chinese_translation):
                passage.chinese_translation = chinese_translation
                passage.save()

        except Exception as e:
            print(f"Error refining passage {passage.id}: {e}")

# Execute the first stage of processing
parse_and_update_passages()
print("First Stage Done!")

# Execute the second stage of processing
parse_and_refine_passages()
print("Second Stage Done!")





def third_stage_further_refine_chinese_translation(text):
    """
    Third stage of cleaning to handle residual anomalies in the chinese_translation,
    including removing duplicated text segments.
    """
    # Split the text into segments (assuming sentences or phrases)
    segments = re.split(r'([。？！；])', text)  # Splitting based on punctuation
    unique_segments = []
    seen = set()

    for segment in segments:
        if segment not in seen:
            unique_segments.append(segment)
            seen.add(segment)

    # Reconstruct the text from unique segments
    cleaned_text = ''.join(unique_segments).strip()
    return cleaned_text



def third_stage_parse_and_further_refine_passages():
    """
    Third stage of processing: Filter passages based on the refined chinese_translation field,
    further refine the translation, and update the Passage model.
    """
    passages = Passage.objects.filter(
        chinese_translation__isnull=False
    ).exclude(
        chinese_translation__exact=''
    )

    for passage in passages:
        try:
            chinese_translation = third_stage_further_refine_chinese_translation(passage.chinese_translation)
            if chinese_translation and contains_chinese(chinese_translation):
                passage.chinese_translation = chinese_translation
                passage.save()

        except Exception as e:
            print(f"Error in further refining passage {passage.id}: {e}")



# Execute the third stage
third_stage_parse_and_further_refine_passages()
print("Third Stage Done!")


# python 1_2_handle_failed_situation_2.py
