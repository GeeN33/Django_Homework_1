import csv

from django.core.management.base import BaseCommand

from ads.models import Ads, Categories


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('ads.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',', skipinitialspace=True)
            for row in reader:
                ads = Ads()
                ads.name = row['name']
                ads.author = row['author']
                ads.price = row['price']
                ads.description = row['description']
                ads.address = row['address']
                if row['is_published'] == 'TRUE':
                    ads.is_published = True
                else:
                    ads.is_published = False
                ads.save()

        print("Command load_data ads.csv")

        with open('categories.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',', skipinitialspace=True)
            for row in reader:
                categories = Categories()
                categories.name = row['name']
                categories.save()

        print("Command load_data categories.csv")