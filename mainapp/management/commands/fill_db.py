from django.conf import settings
from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
from django.contrib.auth.models import User

import json, os

from authapp.models import ShopUser

JSON_PATH = os.path.join(settings.BASE_DIR,'mainapp/json')


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), encoding='utf-8') as json_file:
        return json.load(json_file)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()
        for category in categories:
            ProductCategory.objects.create(**category)
            # new_category = ProductCategory(**category)
            # new_category.save()

        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            category_name = product["category"]

            _category = ProductCategory.objects.get(name=category_name)
            # Заменяем название категории объектом
            product['category'] = _category
            Product.objects.create(**product)
            # new_product = Product(**product)
            # new_product.save()

        #super_user = User.objects.create_superuser('django', 'django@geekbrains.local', 'geekbrains')
        ShopUser.objects.create_superuser(username='django', email='django@geekshop.local', password='geekbrains', age =25)