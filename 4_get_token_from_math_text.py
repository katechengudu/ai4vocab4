import os
import django
import spacy


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4vocab4.settings')
django.setup()

print("Successfully imported Django and Passage model")

from passages.models import math_text, MathTextToken, MathTokenOrigin

# Load Spacy's English language model
nlp = spacy.load("en_core_web_lg")

# Define the list of unwanted POS tags
unwanted = ['SPACE', 'DET', 'ADP', 'AUX', 'CCONJ', 'INTJ', 'NUM', 'PART', 'PRON', 'PUNCT', 'SCONJ', 'SYM', 'X']



def process_text_and_create_tokens():
    # Fetch all MathText objects
    all_math_texts = math_text.objects.all()
    print(f"Found {all_math_texts.count()} MathText objects to process.")

    for index, obj in enumerate(all_math_texts, start=1):
        print(f"Processing MathText object {index}/{all_math_texts.count()}: ID {obj.id}")
        # Extract tokens from the english_text_problem field, excluding punctuation and unwanted POS tags
        text = obj.english_text_problem
        doc = nlp(text)
        print(text)

        for token in doc:
            if token.pos_ in unwanted:  # Skip tokens with unwanted POS tags
                continue
            
            if not token.is_punct:  # Further filter out punctuation
                # Create or get a MathTextToken instance for each token
                token_instance, _ = MathTextToken.objects.get_or_create(
                    token=token.text,
                    lemma=token.lemma_
                )
                print(token.text)
                # Create or get a MathTokenOrigin instance for the token in this context
                MathTokenOrigin.objects.get_or_create(
                    math_text=obj,
                    math_text_token=token_instance,
                    origin='problem',
                    pos_tag=token.pos_
                )
                print(token.pos_)
        print(f"Finished processing MathText object {index}.")
        print("-" * 80)  # Print a separator line for readability

if __name__ == "__main__":
    process_text_and_create_tokens()

    
# python 4_get_token_from_math_text.py