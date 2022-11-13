import csv

from django.core.management.base import BaseCommand

from ads.models import Categories, Location, Users, Ad

class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('datasets/location.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',', skipinitialspace=True)
            for row in reader:
                location = Location()
                location.name = row['name']
                location.lat = row['lat']
                location.lng = row['lng']
                location.save()
        print("Command load_data location.csv")

        with open('datasets/user.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',', skipinitialspace=True)
            for row in reader:
                user = Users()
                user.first_name = row['first_name']
                user.last_name = row['last_name']
                user.username = row['username']
                user.password = row['password']
                user.role = row['role']
                user.age = row['age']
                # user.location_id = Location.objects.get(id=row['location_id'])
                user.save()
                user.location_id.add(Location.objects.get(id=row['location_id']))
        print("Command load_data user.csv")

        with open('datasets/category.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',', skipinitialspace=True)
            for row in reader:
                categories = Categories()
                categories.name = row['name']
                categories.save()
        print("Command load_data categories.csv")

        with open('datasets/ad.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=',', skipinitialspace=True)
            for row in reader:
                ad = Ad()
                ad.name = row['name']
                # ad.author_id = row['author_id']
                ad.author_id = Users.objects.get(id=row['author_id'])
                ad.price = row['price']
                ad.description = row['description']
                if row['is_published'] == 'TRUE':
                    ad.is_published = True
                else:
                    ad.is_published = False
                ad.image = row['image']
                # ad.category_id = row['category_id']
                ad.category_id = Categories.objects.get(id=row['category_id'])
                ad.save()
        print("Command load_data ads.csv")