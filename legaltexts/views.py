from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from .models import Sector, Part, LegalArticle
from .forms import SectorForm, PartForm, LegalArticleForm


def staff_required(user):
    return user.is_authenticated and user.is_staff


def article_list(request):
    query = request.GET.get('q', '').strip()
    sector_id = request.GET.get('sector', '').strip()
    part_id = request.GET.get('part', '').strip()

    articles = LegalArticle.objects.select_related('part', 'part__sector').filter(is_active=True)

    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(reference_number__icontains=query) |
            Q(content__icontains=query) |
            Q(keywords__icontains=query) |
            Q(part__title__icontains=query) |
            Q(part__sector__title__icontains=query)
        )
    if sector_id:
        articles = articles.filter(part__sector_id=sector_id)
    if part_id:
        articles = articles.filter(part_id=part_id)

    paginator = Paginator(articles, 24)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'articles': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'sectors': Sector.objects.all(),
        'parts': Part.objects.select_related('sector').all(),
        'selected_sector': sector_id,
        'selected_part': part_id,
        'query': query,
    }
    return render(request, 'legaltexts/article_list.html', context)


class ArticleDetailView(DetailView):
    model = LegalArticle
    template_name = 'legaltexts/article_detail.html'
    context_object_name = 'article'

    def get_queryset(self):
        qs = LegalArticle.objects.select_related('part', 'part__sector')
        if not self.request.user.is_staff:
            qs = qs.filter(is_active=True)
        return qs


@login_required
@user_passes_test(staff_required)
def dashboard(request):
    context = {
        'sectors_count': Sector.objects.count(),
        'parts_count': Part.objects.count(),
        'articles_count': LegalArticle.objects.count(),
        'active_articles_count': LegalArticle.objects.filter(is_active=True).count(),
        'sectors': Sector.objects.annotate(part_count=Count('parts__articles')).order_by('order', 'title'),
        'recent_articles': LegalArticle.objects.select_related('part', 'part__sector').order_by('-updated_at')[:8],
    }
    return render(request, 'legaltexts/dashboard.html', context)


class StaffOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class SectorCreateView(LoginRequiredMixin, StaffOnlyMixin, CreateView):
    model = Sector
    form_class = SectorForm
    template_name = 'legaltexts/form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Sector created successfully.')
        return super().form_valid(form)


class SectorUpdateView(LoginRequiredMixin, StaffOnlyMixin, UpdateView):
    model = Sector
    form_class = SectorForm
    template_name = 'legaltexts/form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Sector updated successfully.')
        return super().form_valid(form)


class SectorDeleteView(LoginRequiredMixin, StaffOnlyMixin, DeleteView):
    model = Sector
    template_name = 'legaltexts/confirm_delete.html'
    success_url = reverse_lazy('dashboard')


class PartCreateView(LoginRequiredMixin, StaffOnlyMixin, CreateView):
    model = Part
    form_class = PartForm
    template_name = 'legaltexts/form.html'
    success_url = reverse_lazy('dashboard')


class PartUpdateView(LoginRequiredMixin, StaffOnlyMixin, UpdateView):
    model = Part
    form_class = PartForm
    template_name = 'legaltexts/form.html'
    success_url = reverse_lazy('dashboard')


class PartDeleteView(LoginRequiredMixin, StaffOnlyMixin, DeleteView):
    model = Part
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
