import requests
import json
import os
import django



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4vocab4.settings')
django.setup()

print("Successfully imported Django and Passage model")

YOUR_API_KEY = "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"

def gpt_update_academic_terms(english_text, YOUR_API_KEY):
    """
    Send English text to the OpenAI API to get updated academic terms.
    """
    endpoint = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {YOUR_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Your task is to process the text provided by the user "
                    "and return your response in JSON format with 'academic_terms' for the dictionary of math terms. "
                    "Identify all math-related terms and store them in 'academic_terms'."
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
    
    # Initialize the return variables
    bilingual_terms = {}

    # Check if "choices" key exists in the response
    if "choices" in response_json:
        # Extract the content from the response
        content = response_json["choices"][0]["message"]["content"].strip()

        # Try to parse the content as JSON
        try:
            parsed_content = json.loads(content)
            bilingual_terms = parsed_content.get("academic_terms", {})
            print(f"GPT response parsing succeeded: {content}")
        except json.JSONDecodeError:
            print(f"GPT response parsing failed: {content}")
            return None

    else:
        print(f"API request failed with status code {response.status_code}")
        return None
    
    return bilingual_terms

from passages.models import Passage 

def save_the_updated(passage, updated_terms):
    """
    Save the updated terms dictionary to the Passage instance.
    """
    passage.gpt_response_academic_terms_incorrect_removed = json.dumps(updated_terms)
    passage.save()
    

def process_passages(YOUR_API_KEY):
    """
    Process Passage instances to update academic terms using the OpenAI API, with progress reporting.
    """
    passages = Passage.objects.exclude(gpt_response_academic_terms__isnull=True).exclude(gpt_response_academic_terms__exact='')
    total_passages = passages.count()  # Total number of passages to process
    processed_count = 0  # Counter for tracking the number of processed passages
    
    for passage in passages:
        english_text = passage.gpt_response_academic_terms
        print(f"The english_text fed into OPEN AI:  {english_text} ")
        updated_terms = gpt_update_academic_terms(english_text, YOUR_API_KEY)
        if updated_terms is not None:
            save_the_updated(passage, updated_terms)
            processed_count += 1  # Increment the processed counter
            print(f"Updated Passage ID {passage.id} with new terms. Progress: {processed_count}/{total_passages} ({processed_count/total_passages*100:.2f}%)")
        else:
            print(f"Failed to update Passage ID {passage.id}. Progress: {processed_count}/{total_passages} ({processed_count/total_passages*100:.2f}%)")

    print("Completed processing passages.")

if __name__ == "__main__":
    process_passages(YOUR_API_KEY)
    print("Completed processing passages.")


# exec(open("1_2_gpt_acaterms_incorrect_removed.py").read())