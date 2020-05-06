import random
from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product


def main(request):
    spam = list(Product.objects.all())
    random.shuffle(spam)
    product_list = spam[:4]
    trending_products = spam[4:10]
    small_products = spam[10:14]
    title = 'Интернет-магазин мебели'
    context = {
        'title': title,
        'product_list': product_list,
        'trending_products': trending_products,
        'small_products': small_products,
    }
    return render(request, 'mainapp/index.html', context=context)


def products(request, pk=None):
    title = 'Продукты интернет-магазина'
    links_menu = ProductCategory.objects.all()
    same_products = Product.objects.all()[:3]

    if pk is not None:
        if pk == 0:
            products = Product.objects.all()
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk)
        context = {
            'title': title,
            'links_menu': links_menu,
            'same_products': same_products,
            'category': category,
            'products': products,
        }
        return render(request, 'mainapp/products_list.html', context)

    context = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products,
    }

    return render(request, 'mainapp/products.html', context=context)


def contacts(request):
    context = {
        'title': 'Контакты интернет-магазина'
    }
    return render(request, 'mainapp/contacts.html', context=context)
