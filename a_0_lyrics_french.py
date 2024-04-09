import requests
import json
import os
import django



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4vocab4.settings')
django.setup()

print("Successfully imported Django")



from passages.models import Lyrics,Token
import spacy

print("Successfully imported Spacy.")
print("Successfully imported django moedel Lyrics.")

# Load the French spaCy model
nlp = spacy.load("fr_core_news_sm")

# Fetch French lyrics
french_lyrics = Lyrics.objects.filter(language='FR')

# Print the number of instances
total_lyrics = french_lyrics.count()
print(f"Number of instances with French lyrics: {total_lyrics}")

# Initialize a counter to track progress
processed_count = 0

import json  # Make sure to import json at the top of your file

for lyric in french_lyrics:
    # Process the lyrics text with spaCy to get a document object
    doc = nlp(lyric.lyrics_text)
    
    # Extract tokens from the document, ensure they are unique by converting the list to a set,
    # exclude '\r' and '\n' tokens, and keep only alphabetic tokens
    unique_tokens = {token.text for token in doc if token.text not in ['\r', '\n'] and token.is_alpha}
    
    # Convert the set back to a list if you need to preserve some form of order
    unique_tokens_list = list(unique_tokens)
    
    # Strip any leading/trailing whitespace from each token
    unique_tokens_list = [token.strip() for token in unique_tokens_list]

    # Remove empty strings that may result from stripping
    unique_tokens_list = [token for token in unique_tokens_list if token]

    # Save the cleaned and unique list of tokens into Lyrics.list_of_tokens as a JSON string
    lyric.list_of_tokens = json.dumps(unique_tokens_list)
    lyric.save()

    # Print the cleaned and unique tokens for the current song
    print(f"Alphabetic tokens for '{lyric.song_name}': {unique_tokens_list}")
    print("-------------")  # To separate tokens of each song for clarity
    
    # Update and print the progress
    processed_count += 1
    print(f"Processed {processed_count}/{total_lyrics} ({(processed_count/total_lyrics)*100:.2f}%) lyrics.")

print("Completed processing all French lyrics.")



from django.db.models import Count

# First, get the total number of Lyrics objects to be processed
total_lyrics = Lyrics.objects.annotate(tokens_count=Count('list_of_tokens')).filter(tokens_count__gt=0).count()
print(f"Total Lyrics objects to process for Token: {total_lyrics}")

# Initialize a counter for processed Lyrics objects
processed_lyrics_count = 0

# Loop over each Lyrics object
for lyrics in Lyrics.objects.all():
    # Check if list_of_tokens is not empty
    if lyrics.list_of_tokens:
        # Load the JSON string of tokens into a Python list
        tokens_list = json.loads(lyrics.list_of_tokens)

        # Initialize a counter for processed tokens for the current Lyrics object
        processed_tokens_count = 0

        # Loop over each token in the list
        for token_str in tokens_list:
            # Check if the Token object already exists, if not, create it
            token_obj, created = Token.objects.get_or_create(token=token_str)

            # Add the current lyrics to the token's lyrics set
            token_obj.lyrics.add(lyrics)

            # Update the processed tokens counter
            processed_tokens_count += 1

        # After processing all tokens for the current Lyrics, update the Lyrics counter
        processed_lyrics_count += 1
        print(f"Processed Lyrics {processed_lyrics_count}/{total_lyrics} ({(processed_lyrics_count/total_lyrics)*100:.2f}%). Tokens processed for current Lyrics: {processed_tokens_count}")

print("Completed processing all Lyrics objects for Tokens.")







# python a_0_lyrics_french.py
