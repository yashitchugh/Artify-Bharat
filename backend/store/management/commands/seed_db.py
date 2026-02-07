# from django.core.management.base import BaseCommand
# from django.db import connection
# from pathlib import Path
# import os


# class Command(BaseCommand):
#     help = 'Populates the database with categories and products'

#     def handle(self, *args, **options):
#         print('Populating the database...')
#         current_dir = os.path.dirname(__file__)
#         file_path = os.path.join(current_dir, 'seed.sql')
#         sql = Path(file_path).read_text()

#         with connection.cursor() as cursor:
#             cursor.execute(sql)


import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.db import transaction
from faker import Faker

# Import your models
from store.models import (
    Category,
    Product,
    Artisan,
    Customer,
    Order,
    OrderItem,
    Address,
    Cart,
)

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Seeds the database with Artisans, Customers, Products, and Orders"

    def add_arguments(self, parser):
        parser.add_argument(
            "--artisans", type=int, default=10, help="Number of artisans to create"
        )
        parser.add_argument(
            "--customers", type=int, default=20, help="Number of customers to create"
        )
        parser.add_argument(
            "--no-clear", action="store_true", help="Do not clear existing data"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        total_artisans = options["artisans"]
        total_customers = options["customers"]
        clear_data = not options["no_clear"]

        if clear_data:
            self.stdout.write(self.style.WARNING("Clearing existing data..."))
            # Delete strictly in order to avoid Foreign Key protection errors
            OrderItem.objects.all().delete()
            Order.objects.all().delete()
            Cart.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            Artisan.objects.all().delete()
            Customer.objects.all().delete()
            Address.objects.all().delete()
            User.objects.exclude(is_superuser=True).delete()
            self.stdout.write(self.style.SUCCESS("Data cleared."))

        # --- 1. Create Categories ---
        self.stdout.write("Creating Categories...")
        category_names = [
            "Pottery & Ceramics",
            "Handloom & Textiles",
            "Wood Carving",
            "Jewelry",
            "Paintings",
            "Leather Craft",
            "Metal Work",
        ]
        categories = []
        for name in category_names:
            cat, created = Category.objects.get_or_create(title=name)
            categories.append(cat)

        # --- 2. Create Artisans ---
        self.stdout.write(f"Creating {total_artisans} Artisans...")
        artisans = []
        for _ in range(total_artisans):
            # Create User
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}.{random.randint(1, 9999)}@example.com"

            # Helper to ensure unique email if collision occurs
            while User.objects.filter(email=email).exists():
                email = f"{first_name.lower()}.{last_name.lower()}.{random.randint(1, 99999)}@example.com"

            user = User(
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.set_password('password123') # Manually hash the password
            user.save()

            # Create Address for User
            Address.objects.create(
                user=user,
                local_address=fake.street_address(),
                city=fake.city(),
                state=fake.state(),
                pincode=fake.zipcode(),
            )

            # Create Artisan Profile
            artisan = Artisan.objects.create(
                user=user,
                experience=random.randint(1, 30),
                speciality=random.choice(category_names),
                bio=fake.paragraph(nb_sentences=3),
                stats={
                    "products_count": 0,
                    "total_sales": 0,
                    "active_orders": 0,
                    "ai_verified": random.choice([0, 1]),
                },
            )
            artisans.append(artisan)

            # --- 3. Create Products for this Artisan ---
            for _ in range(random.randint(1, 8)):  # 1 to 8 products per artisan
                title = f"{fake.word().capitalize()} {fake.word().capitalize()}"
                price = random.randint(100, 5000)

                Product.objects.create(
                    title=title,
                    slug=slugify(title + "-" + str(random.randint(1000, 9999))),
                    description=fake.text(),
                    unit_price=price,
                    inventory=random.randint(0, 50),
                    category=random.choice(categories),
                    artisan=artisan,
                )
                # Update local stats count (optional, but good for consistency)
                artisan.stats["products_count"] += 1
                artisan.save()

        # --- 4. Create Customers ---
        self.stdout.write(f"Creating {total_customers} Customers...")
        customers = []
        for _ in range(total_customers):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"cust.{first_name.lower()}.{random.randint(1, 9999)}@test.com"

            # Helper to ensure unique email
            while User.objects.filter(email=email).exists():
                email = f"cust.{first_name.lower()}.{random.randint(1, 99999)}@test.com"

            user = User(
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            user.set_password('password123') # Manually hash the password
            user.save()

            Address.objects.create(
                user=user,
                local_address=fake.street_address(),
                city=fake.city(),
                state=fake.state(),
                pincode=fake.zipcode(),
            )

            customer, created = Customer.objects.update_or_create(
                user=user,
                defaults={
                    'birth_date': fake.date_of_birth(minimum_age=18, maximum_age=80),
                    'membership': random.choice([Customer.MEMBERSHIP_BRONZE, Customer.MEMBERSHIP_SILVER, Customer.MEMBERSHIP_GOLD]),
                    'interests': [random.choice(category_names) for _ in range(3)]
                }
            )
            customers.append(customer)

        # --- 5. Create Orders (Optional) ---
        self.stdout.write("Creating dummy Orders...")
        all_products = list(Product.objects.all())

        if all_products and customers:
            for _ in range(int(total_customers * 1.5)):  # Create some orders
                customer = random.choice(customers)
                order = Order.objects.create(
                    customer=customer,
                    payment_status=random.choice(
                        [Order.PAYMENT_STATUS_COMPLETE, Order.PAYMENT_STATUS_PENDING]
                    ),
                    delivered=random.choice([True, False]),
                )

                # Add 1-3 items to the order
                for _ in range(random.randint(1, 3)):
                    product = random.choice(all_products)
                    quantity = random.randint(1, 3)

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        artisan=product.artisan,  # Vital: Link to the product's artisan
                        quantity=quantity,
                        unit_price=product.unit_price,
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully seeded DB with {total_artisans} artisans and {total_customers} customers!"
            )
        )
