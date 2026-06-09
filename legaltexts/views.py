from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from .models import Part, Section, LegalArticle
from .forms import PartForm, SectionForm, LegalArticleForm


def staff_required(user):
    return user.is_authenticated and user.is_staff


@login_required
def article_list(request):
    query = request.GET.get('q', '').strip()
    part_id = request.GET.get('part', '').strip()
    section_id = request.GET.get('section', '').strip()

    articles = LegalArticle.objects.select_related('section', 'section__part').filter(is_active=True)

    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(reference_number__icontains=query) |
            Q(content__icontains=query) |
            Q(keywords__icontains=query) |
            Q(section__title__icontains=query) |
            Q(section__part__title__icontains=query)
        )
    if part_id:
        articles = articles.filter(section__part_id=part_id)
    if section_id:
        articles = articles.filter(section_id=section_id)

    context = {
        'articles': articles,
        'parts': Part.objects.all(),
        'sections': Section.objects.select_related('part').all(),
        'selected_part': part_id,
        'selected_section': section_id,
        'query': query,
    }
    return render(request, 'legaltexts/article_list.html', context)


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = LegalArticle
    template_name = 'legaltexts/article_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        qs = LegalArticle.objects.select_related('section', 'section__part')
        if not self.request.user.is_staff:
            qs = qs.filter(is_active=True)
        return qs


@login_required
@user_passes_test(staff_required)
def dashboard(request):
    context = {
        'parts_count': Part.objects.count(),
        'sections_count': Section.objects.count(),
        'articles_count': LegalArticle.objects.count(),
        'active_articles_count': LegalArticle.objects.filter(is_active=True).count(),
        'parts': Part.objects.annotate(article_count=Count('sections__articles')).order_by('order', 'title'),
        'recent_articles': LegalArticle.objects.select_related('section', 'section__part').order_by('-updated_at')[:8],
    }
    return render(request, 'legaltexts/dashboard.html', context)


class StaffOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class PartCreateView(LoginRequiredMixin, StaffOnlyMixin, CreateView):
    model = Part
    form_class = PartForm
    template_name = 'legaltexts/form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Part created successfully.')
        return super().form_valid(form)


class PartUpdateView(LoginRequiredMixin, StaffOnlyMixin, UpdateView):
    model = Part
    form_class = PartForm
    template_name = 'legaltexts/form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Part updated successfully.')
        return super().form_valid(form)


class PartDeleteView(LoginRequiredMixin, StaffOnlyMixin, DeleteView):
    model = Part
    template_name = 'legaltexts/confirm_delete.html'
    success_url = reverse_lazy('dashboard')


class SectionCreateView(LoginRequiredMixin, StaffOnlyMixin, CreateView):
    model = Section
    form_class = SectionForm
    template_name = 'legaltexts/form.html'
    success_url = reverse_lazy('dashboard')


class SectionUpdateView(LoginRequiredMixin, StaffOnlyMixin, UpdateView):
    model = Section
    form_class = SectionForm
    template_name = 'legaltexts/form.html'
    success_url = reverse_lazy('dashboard')


class SectionDeleteView(LoginRequiredMixin, StaffOnlyMixin, DeleteView):
    model = Section
    template_name = 'legaltexts/confirm_delete.html'
    success_url = reverse_lazy('dashboard')


class ArticleCreateView(LoginRequiredMixin, StaffOnlyMixin, CreateView):
    model = LegalArticle
    form_class = LegalArticleForm
    template_name = 'legaltexts/form.html'
    success_url = reverse_lazy('article_list')


class ArticleUpdateView(LoginRequiredMixin, StaffOnlyMixin, UpdateView):
    model = LegalArticle
    form_class = LegalArticleForm
    template_name = 'legaltexts/form.html'
    success_url = reverse_lazy('article_list')


class ArticleDeleteView(LoginRequiredMixin, StaffOnlyMixin, DeleteView):
    model = LegalArticle
    template_name = 'legaltexts/confirm_delete.html'
    success_url = reverse_lazy('article_list')
