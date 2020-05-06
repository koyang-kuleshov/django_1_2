from django.db import models
from django.conf import settings
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='basket'
                             )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Количество',
                                           default=0)
    add_datetime = models.DateTimeField(verbose_name='Время',
                                        auto_now_add=True)

    # TODO: Реализовать методы, которые отдают общее количество и сумму товаров
    # в корзине пользователя
    @property
    def basket_sum(self):
        pass

    @property
    def basket_qty(self):
        pass
