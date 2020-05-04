from django.shortcuts import render
from .models import ProductCategory, Product


def main(requests):
    products = Product.objects.all()
    title = 'Интернет-магазин мебели'
    context = {
        'title': title,
        'products': products,
    }
    return render(requests, 'mainapp/index.html', context=context)


def products(requests, pk=None):
    title = 'Продукты интернет-магазина'
    links_menu = ProductCategory.objects.all()
    same_products = Product.objects.all()[:3]
    context = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
    }
    return render(requests, 'mainapp/products.html', context=context)


def contacts(request):
    context = {
        'title': 'Контакты интернет-магазина'
    }
    return render(request, 'mainapp/contacts.html', context=context)
