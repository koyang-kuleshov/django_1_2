import random
from django.shortcuts import render
from .models import ProductCategory, Product


def main(requests):
    spam = list(Product.objects.all())
    random.shuffle(spam)
    product_list = spam[:4]
    title = 'Интернет-магазин мебели'
    context = {
        'title': title,
        'product_list': product_list,
    }
    return render(requests, 'mainapp/index.html', context=context)


def products(requests, pk=None):
    title = 'Продукты интернет-магазина'
    links_menu = ProductCategory.objects.all()
    product_list = Product.objects.all()[:4]
    context = {
        'title': title,
        'links_menu': links_menu,
        'product_list': product_list,
    }
    return render(requests, 'mainapp/products.html', context=context)


def contacts(request):
    context = {
        'title': 'Контакты интернет-магазина'
    }
    return render(request, 'mainapp/contacts.html', context=context)
