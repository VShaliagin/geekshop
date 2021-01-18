from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name='Имя')
    description = models.TextField(verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='активна')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category_id = None

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=128, verbose_name='Название')
    image = models.ImageField(upload_to='products_images', blank=True, verbose_name='Картинка')
    short_desc = models.CharField(max_length=128,verbose_name='Краткое описание')
    description = models.TextField(verbose_name='Описание', blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Цена')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество осталось на складе')
    is_active = models.BooleanField(default=True, verbose_name='продукт активен')

    def __str__(self):
        return f'{self.category} ({self.category.name})'
