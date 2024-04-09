from django.contrib import admin
from .models import Category, Book, Sentence, Passage
from import_export import resources
from import_export.fields import Field
from import_export.admin import ImportExportModelAdmin



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class SentenceAdmin(admin.ModelAdmin):
    list_display = ('english_text', 'chinese_translation', 'token_count', 'has_clause', 'order')


class BookAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'author', 'year', 'display_categories')

    def display_categories(self, obj):
        """Function to display the categories in the Admin panel."""
        return ", ".join(category.name for category in obj.categories.all())
    display_categories.short_description = 'Categories'


class PassageResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        book = Book.objects.get(id=2)
        row["book"] = book.name
        row["book"] = 3

    class Meta:
        model = Passage
        fields = ('haochen_database_id','english_text', 'book','chinese_translation', 'gpt_response_academic_terms','gpt_response_academic_terms_incorrect_removed')
        # import_id_fields = ('id',) # Only if absolutely necessary and you understand the implications. 
        # Remember, if you later need to import data and ensure uniqueness, 
        # you will need to find a way to uniquely identify each record, 
        # possibly by adding a unique field to your model or using a combination of fields that together are unique.

class PassageAdmin(ImportExportModelAdmin):
    resource_class = PassageResource
    list_display = ('english_text', 'chinese_translation', 'gpt_response_academic_terms_incorrect_removed','gpt_response_parsing_failed','gpt_response_academic_terms', 'haochen_database_id', 'token_count', 'sentence_count', 'book')



from .models import AcademicTerm
class AcademicTermAdmin(admin.ModelAdmin):
    list_display = ('term', 'chinese_meaning', 'source')


from .models import Lyrics
class LyricsAdmin(admin.ModelAdmin):
    list_display = ('song_name', 'singer','language', 'lyrics_text','list_of_tokens')


from .models import AI_Lyrics
class AI_LyricsAdmin(admin.ModelAdmin):
    list_display = ('song_name', 'singer','language', 'lyrics_text','list_of_tokens')


from .models import Token
class TokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'lemma', 'get_lyrics_song_names', 'get_ai_lyrics_song_names')

    def get_lyrics_song_names(self, obj):
        """Retrieve a comma-separated list of song names for the token from Lyrics."""
        return ", ".join([lyric.song_name for lyric in obj.lyrics.all()])
    get_lyrics_song_names.short_description = 'Lyrics'  # Sets column name

    def get_ai_lyrics_song_names(self, obj):
        """Retrieve a comma-separated list of song names for the token from AI_Lyrics."""
        return ", ".join([ai_lyric.song_name for ai_lyric in obj.ai_lyrics.all()])
    get_ai_lyrics_song_names.short_description = 'AI_Lyrics'  # Sets column name


from .models import Album
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'year','singer')

    

admin.site.register(AcademicTerm, AcademicTermAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Sentence, SentenceAdmin)
admin.site.register(Passage, PassageAdmin)
admin.site.register(Lyrics, LyricsAdmin)
admin.site.register(Token, TokenAdmin)
admin.site.register(AI_Lyrics, AI_LyricsAdmin)
admin.site.register(Album, AlbumAdmin)