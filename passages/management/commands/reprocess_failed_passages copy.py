from django.core.management.base import BaseCommand
from passages.models import Passage


class Command(BaseCommand):
    help = 'Filter Passage objects based on specific conditions'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting the filter process...")

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

        # Initialize an empty list to collect the filtered Passage objects
        filtered_passages = []

        for passage in passages:
            self.stdout.write(f'Passage ID: {passage.id}, English Text: {passage.english_text[:50]}...')  # Prints a snippet of the english text
            filtered_passages.append(passage)  # Append the Passage object to the list

        self.stdout.write(self.style.SUCCESS(f'Processed {len(filtered_passages)} passages.'))

        # Optional: Do something with the list of filtered Passage objects
        # For example, you can print the IDs of the filtered passages
        self.stdout.write("IDs of filtered passages: " + ", ".join(str(passage.id) for passage in filtered_passages))


# python manage.py filter_passages
