from django.contrib import admin
from .models import Sector, Part, LegalArticle


class PartInline(admin.TabularInline):
    model = Part
    extra = 1


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    search_fields = ('title', 'description')
    inlines = [PartInline]


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('title', 'sector', 'order')
    list_filter = ('sector',)
    search_fields = ('title', 'description', 'sector__title')


@admin.register(LegalArticle)
class LegalArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'part', 'is_active', 'updated_at')
    list_filter = ('is_active', 'part__sector', 'part')
    search_fields = ('title', 'reference_number', 'content', 'keywords')
    autocomplete_fields = []
