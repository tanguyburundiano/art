from django.contrib import admin
from .models import Part, Section, LegalArticle

class SectionInline(admin.TabularInline):
    model = Section
    extra = 1

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    search_fields = ('title', 'description')
    inlines = [SectionInline]

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'part', 'order')
    list_filter = ('part',)
    search_fields = ('title', 'description', 'part__title')

@admin.register(LegalArticle)
class LegalArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'is_active', 'updated_at')
    list_filter = ('is_active', 'section__part', 'section')
    search_fields = ('title', 'reference_number', 'content', 'keywords')
    autocomplete_fields = []
