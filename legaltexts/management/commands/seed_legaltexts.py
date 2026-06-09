from django.core.management.base import BaseCommand
from legaltexts.models import Part, Section, LegalArticle

DATA = {
    'PROPRIETE INTELLECTUELLE': [
        ('General', [
            'Loi n°1/13 du 28 juillet 2009 relative à la propriété industrielle au Burundi',
            "Loi n° 1/021 du 30 décembre 2005 portant Protection du droit d'auteur et des droits voisins au Burundi",
            "Loi n°1/10 du 16 mars 2022 portant prévention et répression de la cybercriminalité au Burundi",
            "Loi n’1/22 du 22 aout 2024 portant Code des communications électroniques et postales",
            "Loi n°1/03 du 10 mars 2026 portant protection des données à caractère personnel",
        ])
    ],
    'FISCALITE': [
        ('Lois fiscales', [
            'Loi n°1/14 du 24 décembre 2020 portant modification de la loi n°1/02 du 24 janvier 2013 relative aux impôts sur les revenus',
            'Loi n°1/12 du 25 novembre 2020 relative aux procédures fiscales et non fiscales',
            'Loi n°1/10 du 16 novembre 2020 portant modification de la loi relative à la TVA',
            'Loi n°1/09 du 15 mai 2025 portant modification de la Réforme de la Fiscalité Communale au Burundi',
        ])
    ],
    'SERVICES FINANCIERS': [
        ('Banque et finance', [
            'Loi n°1/34 du 02 décembre 2008 portant Statuts de la Banque de la République du Burundi',
            'Loi n°1/17 du 2 aout 2017 régissant les activités bancaires',
            'Loi n°1/17 du 11 mai 2018 portant Système national de paiement',
            'Règlement 002/2024 relatif aux services de paiement et aux établissements de paiement',
        ])
    ],
    'CONTENTIEUX ET ARBITRAGE': [
        ('Contentieux civil', [
            'Loi n°1/27 du 28 décembre 2023 portant modification du Code de procédure civile',
            'Loi n°1/26 du 26 décembre 2023 portant modification du Code de l’organisation et de la compétence judiciaires',
            'Code civil Livre I ; Livre II, Livre III',
        ]),
        ('Contentieux commercial', [
            'Loi n°1/01 du 16 janvier 2015 portant révision du Code de commerce',
            'Loi n°1/05 du 23 janvier 2018 portant insolvabilité du Commerçant au Burundi',
            'Loi n°1/04 du 29 janvier 2018 portant code des marchés publics',
        ]),
        ('Arbitrage', [
            "Convention pour la reconnaissance et l’exécution des sentences arbitrales étrangères conclue le 10 juin 1958 à New-York",
            "Convention pour le règlement des différends relatifs aux investissements entre Etats et ressortissants d’autres Etats (CIRDI)",
            "Règlement d’arbitrage de la CNUDCI",
        ])
    ],
}

class Command(BaseCommand):
    help = 'Seed sample legal texts.'

    def handle(self, *args, **options):
        for part_order, (part_title, sections) in enumerate(DATA.items(), start=1):
            part, _ = Part.objects.get_or_create(title=part_title, defaults={'order': part_order})
            for section_order, (section_title, articles) in enumerate(sections, start=1):
                section, _ = Section.objects.get_or_create(part=part, title=section_title, defaults={'order': section_order})
                for article_order, title in enumerate(articles, start=1):
                    LegalArticle.objects.get_or_create(
                        section=section,
                        title=title,
                        defaults={'order': article_order, 'content': title, 'keywords': part_title.lower()},
                    )
        self.stdout.write(self.style.SUCCESS('Sample legal texts created.'))
