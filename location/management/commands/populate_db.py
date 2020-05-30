from random import randint


from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker

from location.models import Location

class Command(BaseCommand):
    help = 'Populate the db with x Locations and Users associated.'
    def add_arguments(self, parser):
        parser.add_argument('location_number', nargs='+', type=int)

    def handle(self, *args, **options):

        fake = Faker(locale='fr-FR')
        location_count = 0

        while location_count < options['location_number'][0]:
            new_user = User.objects.create_user(fake.name(), fake.email(), fake.password(length=12))
            for i in range(randint(1,4)):
                loc = Location.objects.create(
                    name=fake.company(),
                    catchphrase=fake.catch_phrase(),
                    description=fake.sentence(nb_words=17),
                    moderator=new_user,
                    slug=fake.slug(),
                    address=fake.address()
                )
                print(loc.address)
                location_count += 1