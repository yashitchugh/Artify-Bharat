<!-- Install Dependencies -->
uv sync

<!-- Seed db -->
python manage.py seed_db --artisans 50 --customers 100