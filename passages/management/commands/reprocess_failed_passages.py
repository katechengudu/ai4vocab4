from django.core.management.base import BaseCommand
from passages.models import Passage
import json
import requests
import logging

# Configure a logger for your Django command
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Filter Passage objects based on specific conditions'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting the filter process...")
        YOUR_API_KEY = "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"

        # Filter Passage objects based on the specified conditions
        passages = Passage.objects.filter(
            english_text__isnull=False, 
            gpt_response_parsing_failed__isnull=False, 
            gpt_response_academic_terms__isnull=True
        ) | Passage.objects.filter(
            english_text__isnull=False, 
            gpt_response_parsing_failed__isnull=False, 
            gpt_response_academic_terms__exact=''
        )

        for passage in passages:
            print(passage.gpt_response_parsing_failed)
            # Call the function for each passage and save the result
            bilingual_terms = self.reproduce_parsing_failed_for_academic_terms(passage.gpt_response_parsing_failed, YOUR_API_KEY)
            if bilingual_terms is not None:
                print(bilingual_terms)
                # Save the returned value into passage.gpt_response_academic_terms_incorrect_removed
                passage.gpt_response_academic_terms_incorrect_removed = json.dumps(bilingual_terms)
                passage.save()
                self.stdout.write(self.style.SUCCESS(f'Updated Passage ID {passage.id} with new academic terms.'))
            else:
                self.stdout.write(self.style.ERROR(f'Failed to process Passage ID {passage.id}.'))

    def reproduce_parsing_failed_for_academic_terms(self, gpt_response_parsing_failed, YOUR_API_KEY):
        """
        Send a string from variable gpt_response_parsing_failed to the OpenAI API to get updated academic terms.
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
                        "Identify all math-related terms. You should refer to UK GCSE, A-level and IB exam and textbook materials to identify "
                        "the math-related terms. Please remove any terms in  'academic_terms' that are not really math academic terms"
                        "and store them in 'academic_terms'."
                    )
                },
                {"role": "user", "content": gpt_response_parsing_failed}
            ]
        }

        try:
            response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                response_json = response.json()
                if "choices" in response_json:
                    content = response_json["choices"][0]["message"]["content"].strip()
                    try:
                        parsed_content = json.loads(content)
                        bilingual_terms = parsed_content.get("academic_terms", {})
                        return bilingual_terms
                    except json.JSONDecodeError:
                        logger.error("GPT response parsing failed.")
                else:
                    logger.error("API response is missing the 'choices' key.")
            else:
                logger.error(f"API request failed with status code {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Request to OpenAI API failed: {e}")

        return None




# python manage.py reprocess_failed_passages
