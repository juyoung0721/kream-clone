import random
from django_seed import Seed
from django.core.management.base import BaseCommand
from django.contrib.admin.utils import flatten
from users import models


class Command(BaseCommand):

    help = "This command creates products"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=2, type=int, help="How many users you want to create"
        )

    def handle(self, *args, **options):
        number = options.get("number")
        seeder = Seed.seeder()
        phone = (lambda x: random.randint(00000000, 99999999))(0)
        seeder.add_entity(
            models.User,
            number,
            {
                "phone_number": f"010{phone}"
                # "category": lambda x: random.choice(categories),
            },
        )

        self.stdout.write(self.style.SUCCESS(f"{number} users created!"))
