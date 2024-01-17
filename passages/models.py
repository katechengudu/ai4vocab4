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
    def __str__(self):
        return self.english_text




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

    








