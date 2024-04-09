from django.core.management.base import BaseCommand
from django.db.models import Count
from passages.models import Token

print("successfully loaded.")

class Command(BaseCommand):
    help = 'Merge duplicate tokens'

    def handle(self, *args, **kwargs):
        # Get tokens grouped by `token` value with counts
        token_values = (
            Token.objects
            .values('token')
            .annotate(token_count=Count('id'))
            .filter(token_count__gt=1)
        )

        for token_value in token_values:
            print(token_value)
            # Get all tokens with this value
            duplicates = Token.objects.filter(token=token_value['token'])

            # Keep the first one and merge the rest
            first_token = duplicates.first()
            for duplicate in duplicates[1:]:
                # Move related lyrics to the first token
                first_token.lyrics.add(*list(duplicate.lyrics.all()))
                
                # Delete the duplicate token
                duplicate.delete()
                print("duplicates deleted!")

            self.stdout.write(self.style.SUCCESS(f'Merged tokens with value: "{token_value["token"]}"'))


# python manage.py merge_duplicate_tokens
