from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from mainapp.models import Product

# class BasketQuerySet(models.QuerySet):
    #
    # def delete(self, *args, **kwargs):
    #     for object in self:
    #         object.product.quntity += object.quantity
    #         object.product.save()
    #     super().delete(*args, **kwargs)
    #

class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(auto_now_add=True, verbose_name='время')

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()


    @property
    def total_quantity(self):
        # _items = Basket.objects.filter(user=self.user)
        _items = self.get_items_cached
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    @property
    def total_cost(self):
        # _items = Basket.objects.filter(user=self.user)
        _items = self.get_items_cached
        _total_cost = sum(list(map(lambda x: x.product_cost, _items)))
        return _total_cost

    @staticmethod
    def get_items(user):
        return Basket.objects.filter(user=user).order_by('product__category')

    @staticmethod
    def get_product(user, product):
        return Basket.objects.filter(user=user, product=product)

    @staticmethod
    def get_products_quantity(cls, user):
        basket_items = cls.get_items(user)
        basket_items_dic ={}
        [basket_items_dic.update({item.product: item.quantity}) for item in basket_items]
        return basket_items_dic



    @staticmethod
    def get_items(pk):
        return Basket.objects.get(pk=pk)



    #
    # def delete(self):
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #

