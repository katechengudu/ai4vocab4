from django.contrib import admin
from .models import Category, Book, Sentence, Passage
from import_export import resources
from import_export.fields import Field
from import_export.admin import ImportExportModelAdmin



class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class PassageAdmin(admin.ModelAdmin):
    list_display = ('english_text', 'chinese_translation', 'order', 'token_count', 'sentence_count')


class SentenceAdmin(admin.ModelAdmin):
    list_display = ('english_text', 'chinese_translation', 'token_count', 'has_clause', 'order')


class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'year', 'display_categories')

    def display_categories(self, obj):
        """Function to display the categories in the Admin panel."""
        return ", ".join(category.name for category in obj.categories.all())
    display_categories.short_description = 'Categories'


class PassageResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        book = Book.objects.get(id=2)
        row["book"] = book.name
        row["book"] = 2

    class Meta:
        model = Passage
        fields = ('english_text', 'book')
        import_id_fields = ()

class PassageAdmin(ImportExportModelAdmin):
    resource_class = PassageResource
    list_display = ('english_text', 'chinese_translation', 'order', 'token_count', 'sentence_count', 'book')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Sentence, SentenceAdmin)
admin.site.register(Passage, PassageAdmin)
