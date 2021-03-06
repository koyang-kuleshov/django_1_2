from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=255, unique=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    category_image = models.ImageField(max_length=255,
                                       upload_to='category_images', blank=True)
    is_active = models.BooleanField(verbose_name='Активна', db_index=True,
                                    default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Имя продукта', max_length=255)
    image = models.ImageField(max_length=255,
                              upload_to='products_image', blank=True)
    short_desc = models.CharField(verbose_name='Краткое описание продукта',
                                  max_length=255, blank=True)
    description = models.TextField(verbose_name='Описание продукта',
                                   blank=True)
    price = models.DecimalField(verbose_name='Цена продукта', max_digits=8,
                                decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='Количество товаров \
                                           на складе', default=0)
    is_active = models.BooleanField(verbose_name='Активен', db_index=True,
                                    default=True)

    def __str__(self):
        return f'{self.name} {self.category.name}'

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).\
                order_by('category', 'name')
