from django.db import models
from django.urls import reverse

class Part(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title

class Section(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['part__order', 'order', 'title']
        unique_together = ('part', 'title')

    def __str__(self):
        return f'{self.part.title} - {self.title}'

class LegalArticle(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=500)
    reference_number = models.CharField(max_length=120, blank=True)
    content = models.TextField(blank=True, help_text='Full text, notes, or useful extract.')
    keywords = models.CharField(max_length=500, blank=True)
    source_link = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['section__part__order', 'section__order', 'order', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.pk})
