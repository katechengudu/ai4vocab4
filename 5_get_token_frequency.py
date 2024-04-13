import os
import django
import spacy
from django.db.models import Count
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai4vocab4.settings')
django.setup()

print("Successfully imported Django and Passage model")

from passages.models import math_text, MathTextToken, MathTokenOrigin



# Count of all MathTextToken objects
total_tokens_count = MathTextToken.objects.all().count()
print(f"Total number of tokens: {total_tokens_count}")


# Annotating each topic with the count of its objects
topic_counts = math_text.objects.values('topic').annotate(total=Count('id')).order_by('topic')

# Getting detailed information for each unique topic, including section and section_merged
detailed_data = math_text.objects.values('topic', 'section', 'section_merged').distinct().order_by('topic')

# Specify the CSV file name
csv_file_name = 'math_text_topics_sections_with_counts.csv'

# Initialize a dictionary to hold the count of each topic
topic_count_dict = {item['topic']: item['total'] for item in topic_counts}

# Print the results and save them to a CSV file
print("Unique Topics, Corresponding Sections, Section Merged, and Total Objects:")
with open(csv_file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Writing the headers
    writer.writerow(['Topic', 'Section', 'Section Merged', 'Total Objects'])
    
    for item in detailed_data:
        topic = item['topic']
        section = item['section']
        section_merged = item['section_merged']
        total_objects = topic_count_dict.get(topic, 0)  # Get the total count for the topic
        
        print(f"Topic: {topic}, Section: {section}, Section Merged: {section_merged}, Total Objects: {total_objects}")
        writer.writerow([topic, section, section_merged, total_objects])

print(f"Data has been successfully saved to {csv_file_name}.")


# Fetch all instances of math_text
all_math_texts = math_text.objects.all()

# Specify the CSV file name
csv_file_name = 'math_text_english_problems.csv'

# Open a CSV file to write the results
with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Writing the header
    writer.writerow(['English Text Problem', 'Section Merged', 'Section', 'Topic'])
    
    print("English Text Problems:")
    for math_text_instance in all_math_texts:
        # Print to the console
        print(f"{math_text_instance.english_text_problem} - {math_text_instance.section_merged}, {math_text_instance.section}, {math_text_instance.topic}")
        # Write to the CSV file
        writer.writerow([math_text_instance.english_text_problem, math_text_instance.section_merged, math_text_instance.section, math_text_instance.topic])

print(f"Data has been successfully saved to {csv_file_name}.")






    

# Annotate each MathTextToken with the count of its relations and order by occurrences in ascending order
token_occurrences = MathTextToken.objects.annotate(occurrences=Count('mathtokenorigin')).order_by('occurrences')

print("Token Occurrences (Least to Most):")
for token in token_occurrences:
    print(f"Token: {token.token}, Occurrences: {token.occurrences}")



# Open a new CSV file to write the results
with open('token_occurrences_by_topic_with_pos.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the CSV header
    writer.writerow(['Topic', 'Token', 'Lemma', 'POS Tag', 'Occurrences'])

    # Step 1: Get all unique topics
    unique_topics = math_text.objects.values_list('topic', flat=True).distinct()

    # Step 2: For each topic, find tokens and their occurrences
    for topic in unique_topics:
        print(f"\nTopic: {topic}")

        # Fetch all MathText instances for this topic
        math_texts_for_topic = math_text.objects.filter(topic=topic)

        # Fetch all token origins for these math texts
        token_origins_for_topic = MathTokenOrigin.objects.filter(math_text__in=math_texts_for_topic).select_related('math_text_token')

        # Aggregate token occurrences along with their POS tags
        token_counts = token_origins_for_topic.values('math_text_token__token', 'math_text_token__lemma', 'pos_tag').annotate(occurrences=Count('math_text_token')).order_by('-occurrences')

        for token_count in token_counts:
            print(f"Token: {token_count['math_text_token__token']} (Lemma: {token_count['math_text_token__lemma']}), POS Tag: {token_count['pos_tag']}, Occurrences: {token_count['occurrences']}")
            # Write token data to CSV, including the POS tag
            writer.writerow([topic, token_count['math_text_token__token'], token_count['math_text_token__lemma'], token_count['pos_tag'], token_count['occurrences']])



# Open a new CSV file to write the results
with open('lemma_unique_topics_count_with_pos_tags.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the CSV header
    writer.writerow(['Lemma', 'Unique Topics Count', 'POS Tags'])

    # Annotate MathTextToken with the count of unique topics it appears in
    lemmas_with_topic_counts = MathTextToken.objects.annotate(
        unique_topics_count=Count('mathtokenorigin__math_text__topic', distinct=True)
    )

    # Fetch pos_tag for each lemma separately
    for lemma in lemmas_with_topic_counts:
        # Getting unique POS tags for the lemma
        pos_tags = MathTokenOrigin.objects.filter(math_text_token=lemma).values_list('pos_tag', flat=True).distinct()
        pos_tags_str = ', '.join(pos_tags)  # Joining all POS tags into a single string

        print(f"Lemma: {lemma.lemma}, Unique Topics Count: {lemma.unique_topics_count}, POS Tags: {pos_tags_str}")
        # Write each lemma, its unique topics count, and POS tags to the CSV file
        writer.writerow([lemma.lemma, lemma.unique_topics_count, pos_tags_str])



# Open a new CSV file to write the results
with open('lemma_occurrences_by_section_merged_with_pos_tags.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the CSV header
    writer.writerow(['Section Merged', 'Lemma', 'Occurrences in Section Merged', 'Unique Topics in Section Merged', 'POS Tags'])

    # Fetch all section_merged values
    sections_merged = math_text.objects.values_list('section_merged', flat=True).distinct()

    for section_merged in sections_merged:
        print(f"Section Merged: {section_merged}")
        # Fetch all tokens in this section_merged
        tokens_in_section_merged = MathTokenOrigin.objects.filter(
            math_text__section_merged=section_merged
        ).values(
            'math_text_token__lemma'
        ).annotate(
            occurrences_in_section=Count('math_text_token'),
            unique_topics_count=Count('math_text__topic', distinct=True)
        ).order_by('math_text_token__lemma')

        for token in tokens_in_section_merged:
            # For each lemma, fetch unique POS tags
            pos_tags = MathTokenOrigin.objects.filter(
                math_text_token__lemma=token['math_text_token__lemma'],
                math_text__section_merged=section_merged
            ).values_list('pos_tag', flat=True).distinct()
            pos_tags_str = ', '.join(pos_tags)  # Joining all POS tags into a single string

            print(f"Lemma: {token['math_text_token__lemma']}, Occurrences in Section Merged: {token['occurrences_in_section']}, Unique Topics in Section Merged: {token['unique_topics_count']}, POS Tags: {pos_tags_str}")
            # Write each token's data to the CSV file, including the section_merged and POS tags
            writer.writerow([section_merged, token['math_text_token__lemma'], token['occurrences_in_section'], token['unique_topics_count'], pos_tags_str])
            

# python 4_get_token_frequency.py