from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name



class Book(models.Model):
    name = models.CharField(max_length=255, unique=True)
    year = models.IntegerField(null=True, blank=True)
    author = models.CharField(max_length=255)
    categories = models.ManyToManyField('Category')
    def __str__(self):
        return self.name

    
class Passage(models.Model):
    book = models.ForeignKey(Book, null=True, blank=True, on_delete=models.CASCADE)
    order = models.IntegerField(blank=True, null=True)
    english_text = models.TextField()
    chinese_translation = models.TextField(blank=True, null=True)
    token_count = models.IntegerField(blank=True, null=True)
    sentence_count = models.IntegerField(blank=True, null=True)
    sentences = models.ManyToManyField('Sentence', blank=True)
    haochen_database_id = models.CharField(max_length=36, blank=True, null=True)
    gpt_response_academic_terms = models.TextField(null=True, blank=True)  
    gpt_response_parsing_failed = models.TextField(null=True, blank=True)  # New field
    def __str__(self):
        return self.english_text



class AcademicTerm(models.Model):
    term = models.CharField(max_length=255, db_index=True)  # Added an index for better search performance
    chinese_meaning = models.CharField(max_length=255, db_index=True)
    source = models.ForeignKey(Passage, on_delete=models.CASCADE, related_name='academic_terms')
    usage_context = models.TextField(blank=True, null=True)  # Optional field for additional context
    def __str__(self):
        return f"{self.term} ({self.chinese_meaning})"



class Sentence(models.Model):
    english_text = models.TextField()
    chinese_translation = models.TextField(null=True, blank=True)
    token_count = models.IntegerField(null=True, blank=True)
    has_clause = models.BooleanField(default=False)
    has_non_finite_verb = models.BooleanField(default=False)
    prep_count = models.IntegerField(null=True, blank=True)
    conj_count = models.IntegerField(null=True, blank=True)
    sub_count = models.IntegerField(null=True, blank=True)
    obj_count = models.IntegerField(null=True, blank=True)
    verb_count = models.IntegerField(null=True, blank=True)
    noun_count = models.IntegerField(null=True, blank=True)
    adj_count = models.IntegerField(null=True, blank=True)
    adv_count = models.IntegerField(null=True, blank=True)
    pron_count = models.IntegerField(null=True, blank=True)
    order = models.IntegerField()  
    def __str__(self):
        return self.english_text


class Token(models.Model):
    lemma = models.CharField(max_length=255)
    def __str__(self):
        return self.lemma

    








