import requests
import json
import os
import django



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4vocab4.settings')
django.setup()


from passages.models import Token, Lyrics
import spacy

print("Successfully imported Spacy.")
print("Successfully imported django moedel Lyrics.")

# Fetch Tokens where the related Lyrics' singer is "Vendredi sur Mer (Charline Mignot)"
tokens_for_singer = Token.objects.filter(lyrics__singer="Vendredi sur Mer (Charline Mignot)").distinct()

# Extract the token values
token_list = [token.token for token in tokens_for_singer]

print(token_list)


from django.db.models import Count

# Fetch Tokens related to the specified singer and annotate each token with the count of related Lyrics
tokens_with_lyrics_count = Token.objects.filter(
    lyrics__singer="Vendredi sur Mer (Charline Mignot)"
).annotate(
    lyrics_count=Count('lyrics')
).order_by('-lyrics_count')

# Construct a dictionary where token.token is the key and lyrics_count is the value
token_frequency_dict = {token.token: token.lyrics_count for token in tokens_with_lyrics_count}

print(token_frequency_dict)





# python a_1_all_tokens.py