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
    english_text = models.TextField()
    chinese_translation = models.TextField(blank=True, null=True)
    token_count = models.IntegerField(blank=True, null=True)
    sentence_count = models.IntegerField(blank=True, null=True)
    sentences = models.ManyToManyField('Sentence', blank=True)
    haochen_database_id = models.CharField(max_length=36, blank=True, null=True)
    gpt_response_academic_terms = models.TextField(null=True, blank=True)  
    gpt_response_parsing_failed = models.TextField(null=True, blank=True)  
    gpt_response_academic_terms_incorrect_removed = models.TextField(null=True, blank=True)  # New field
    def __str__(self):
        return self.english_text

class math_text(models.Model):
    subject = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    section = models.CharField(max_length=255)
    section_merged = models.CharField(max_length=255,blank=True, null=True)
    topic = models.CharField(max_length=255)
    english_text_problem = models.TextField()
    haochen_data_problem = models.TextField()
    english_text_solution = models.TextField()
    haochen_data_solution = models.TextField()
    haochen_database_id = models.CharField(max_length=36, blank=True, null=True)
    
    def __str__(self):
        return self.english_text_problem
    

class MathTextToken(models.Model):
    token = models.CharField(max_length=255)
    lemma = models.CharField(max_length=255)
    math_text = models.ManyToManyField(math_text, through='MathTokenOrigin', related_name='tokens')
   


class MathTokenOrigin(models.Model):
    math_text = models.ForeignKey(math_text, on_delete=models.CASCADE)
    math_text_token = models.ForeignKey(MathTextToken, on_delete=models.CASCADE)
    origin = models.CharField(max_length=100, choices=(('problem', 'Problem'), ('solution', 'Solution')))
    pos_tag = models.CharField(max_length=50)  # Field to store the grammatical property (POS tag)
    
    class Meta:
        unique_together = ('math_text', 'math_text_token', 'origin', 'pos_tag')  # Consider your unique constraints here

    def __str__(self):
        return f"{self.math_text_token.token} ({self.pos_tag}) - {self.origin}"




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
    token = models.CharField(max_length=255,blank=True, null=True)
    lemma = models.CharField(max_length=255)
    lyrics = models.ManyToManyField('Lyrics', related_name='tokens', blank=True)  # Establishing the M2M relationship
    ai_lyrics = models.ManyToManyField('AI_Lyrics', related_name='tokens', blank=True)  # New relationship
    
    def __str__(self):
        return self.token


class Album(models.Model):
    singer = models.CharField(max_length=255, default="Taylor Swift")
    name = models.CharField(max_length=255)
    year = models.CharField(max_length=4, blank=True, null=True)  # Consider changing max_length for year

    def __str__(self):
        return f"{self.name} ({self.year})"



class Lyrics(models.Model):
    LANGUAGE_CHOICES = [
        ('EN', 'English'),
        ('CN', 'Chinese'),
        ('FR', 'French'),
        ('KR', 'Korean'),
        ('JP', 'Japanese'),
        ('DE', 'German'),
        ('ES', 'Spanish'),
    ]
    song_name = models.CharField(max_length=500)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='lyrics', null=True, blank=True)
    singer = models.CharField(max_length=500,blank=True, null=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    lyrics_text = models.TextField()
    lyrics_summary_english = models.TextField(blank=True, null=True)
    lyrics_summary_chinese = models.TextField(blank=True, null=True)
    sentences = models.ManyToManyField('Sentence', blank=True)
    list_of_tokens = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.song_name



class AI_Lyrics(models.Model):
    LANGUAGE_CHOICES = [
        ('EN', 'English'),
        ('CN', 'Chinese'),
        ('FR', 'French'),
        ('KR', 'Korean'),
        ('JP', 'Japanese'),
        ('DE', 'German'),
        ('ES', 'Spanish'),
    ]
    song_name = models.CharField(max_length=500)
    inspired_by = models.ManyToManyField('Lyrics', blank=True)
    singer = models.CharField(max_length=500,blank=True, null=True)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES)
    lyrics_text = models.TextField()
    lyrics_with_chinese_translation = models.TextField(blank=True, null=True)
    lyrics_with_english_translation = models.TextField(blank=True, null=True)
    sentences = models.ManyToManyField('Sentence', blank=True)
    list_of_tokens = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.song_name



