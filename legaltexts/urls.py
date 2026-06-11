from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('sectors/add/', views.SectorCreateView.as_view(), name='sector_add'),
    path('sectors/<int:pk>/edit/', views.SectorUpdateView.as_view(), name='sector_edit'),
    path('sectors/<int:pk>/delete/', views.SectorDeleteView.as_view(), name='sector_delete'),

    path('parts/add/', views.PartCreateView.as_view(), name='part_add'),
    path('parts/<int:pk>/edit/', views.PartUpdateView.as_view(), name='part_edit'),
    path('parts/<int:pk>/delete/', views.PartDeleteView.as_view(), name='part_delete'),

    path('articles/add/', views.ArticleCreateView.as_view(), name='article_add'),
    path('articles/<int:pk>/edit/', views.ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
]
