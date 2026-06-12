from django.test import TestCase
from django.urls import reverse
from . import models


class TerminologyModelTest(TestCase):
    def test_sector_and_part_models_are_available(self):
        self.assertTrue(hasattr(models, 'Sector'))
        self.assertTrue(hasattr(models, 'Part'))

        sector = models.Sector.objects.create(title='Sector One', order=1)
        part = models.Part.objects.create(sector=sector, title='Part One', order=1)
        article = models.LegalArticle.objects.create(
            part=part,
            title='Sample article',
            content='Example content',
            order=1,
        )

        self.assertEqual(article.part.sector, sector)


class PublicArticleAccessTest(TestCase):
    def test_article_list_is_available_to_anonymous_users(self):
        sector = models.Sector.objects.create(title='Sector One', order=1)
        part = models.Part.objects.create(sector=sector, title='Part One', order=1)
        models.LegalArticle.objects.create(
            part=part,
            title='Public article',
            content='Example content',
            order=1,
            is_active=True,
        )

        response = self.client.get(reverse('article_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Public article')
        self.assertContains(response, 'Copy')
        self.assertNotContains(response, 'Edit')
        self.assertNotContains(response, 'Delete')

    def test_article_detail_is_available_to_anonymous_users(self):
        sector = models.Sector.objects.create(title='Sector One', order=1)
        part = models.Part.objects.create(sector=sector, title='Part One', order=1)
        article = models.LegalArticle.objects.create(
            part=part,
            title='Public detail article',
            content='Detailed content',
            order=2,
            is_active=True,
        )

        response = self.client.get(reverse('article_detail', args=[article.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Public detail article')
        self.assertContains(response, 'Copy article')
        self.assertNotContains(response, 'Edit')
        self.assertNotContains(response, 'Delete')

    def test_article_list_paginates_at_25_per_page(self):
        sector = models.Sector.objects.create(title='Sector One', order=1)
        part = models.Part.objects.create(sector=sector, title='Part One', order=1)
        for index in range(26):
            models.LegalArticle.objects.create(
                part=part,
                title=f'Article {index}',
                content='Example content',
                order=index,
                is_active=True,
            )

        response = self.client.get(reverse('article_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].paginator.per_page, 24)
        self.assertEqual(len(response.context['page_obj'].object_list), 24)
        self.assertTrue(response.context['page_obj'].has_next)
