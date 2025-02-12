import random
import string
from django.core.management.base import BaseCommand
from api.models import User, Contact, Spam
from django.contrib.auth.hashers import make_password
from faker import Faker

class Command(BaseCommand):
    help = 'Populate the database with random users, contacts, and spam data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create 10 random users
        for _ in range(10):
            name = fake.name()
            phone_number = ''.join(random.choices(string.digits, k=10))  # 10-digit phone number

            email = fake.email()
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            # Create User
            user = User.objects.create(
                name=name,
                phone_number=phone_number,
                email=email,
                password=make_password(password),
            )
            self.stdout.write(self.style.SUCCESS(f'User created: {name}, {phone_number}'))

            # Create 3-5 random contacts for the user
            for _ in range(random.randint(3, 5)):
                contact_name = fake.name()
                contact_phone = ''.join(random.choices(string.digits, k=10))  # 10-digit phone number
                contact_email = fake.email()


                # Create Contact
                Contact.objects.create(
                    user=user,
                    name=contact_name,
                    phone_number=contact_phone,
                    email=contact_email
                )
                self.stdout.write(self.style.SUCCESS(f'Contact added for {name}: {contact_name}, {contact_phone}, {contact_email}'))

            # Randomly mark 1-2 phone numbers as spam
            for _ in range(random.randint(1, 2)):
                spam_phone_number = ''.join(random.choices(string.digits, k=10))  # 10-digit phone number


                # Create Spam
                Spam.objects.create(
                    phone_number=spam_phone_number,
                    is_spam=True
                )
                self.stdout.write(self.style.SUCCESS(f'Spam number added: {spam_phone_number}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated data!'))
