import requests
import json
import os
import django



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4vocab4.settings')
django.setup()

print("Successfully imported Django and Passage model")

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


from passages.models import Passage 

def update_passages_with_gpt_translation_and_academic_terms(YOUR_API_KEY):
    # Update query to exclude passages where gpt_response_parsing_failed has a value
    passages_to_process = Passage.objects.filter(
        gpt_response_parsing_failed__isnull=True,
        chinese_translation__in=[None, "Error in response"]
    )

    # Get the total number of Passage objects to process
    total_passages = passages_to_process.count()
    print(f"Total Passages to process: {total_passages}")

    # Counter for processed passages and list for tracking error IDs
    processed_count = 0
    error_passage_ids = []

    # Iterate through filtered Passage objects
    for passage in passages_to_process:
        try:
            # Get the English text from the Passage
            english_text = passage.english_text

            # Get the Chinese translation, academic terms, and parsing_failed using the function
            chinese_translation, bilingual_terms, parsing_failed = gpt_translation_and_academic_terms(english_text, YOUR_API_KEY)

            if parsing_failed:
                # If parsing_failed has a value, store it in passage.gpt_response_parsing_failed
                passage.gpt_response_parsing_failed = parsing_failed
                print(f"Parsing failed for Passage ID {passage.id}")
            else:
                # Update the Passage object with new values
                passage.chinese_translation = chinese_translation
                passage.gpt_response_academic_terms = bilingual_terms
                print("Chinese Translation:", chinese_translation)
                print("Bilingual_terms:", bilingual_terms)
                print(f"Parsing success for Passage ID {passage.id}")

            # Save the updated Passage object
            passage.save()

            # Increment the processed count
            processed_count += 1

        except Exception as e:
            # Log the error, append the ID to the error list, and proceed with the next passage
            print(f"Error processing Passage ID {passage.id}: {e}")
            error_passage_ids.append(passage.id)

        print(f"Processed Passage ID {passage.id} ({processed_count}/{total_passages})")
        print("********************************end*************************************")

    # Print out the list of Passage IDs that encountered errors
    if error_passage_ids:
        print("Passages that encountered errors:", error_passage_ids)
    else:
        print("No errors encountered.")




# Call the function to start the process
update_passages_with_gpt_translation_and_academic_terms(YOUR_API_KEY)
