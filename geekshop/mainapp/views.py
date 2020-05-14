import random
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import ProductCategory, Product
from basketapp.models import Basket



def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).\
        exclude(pk=hot_product.pk)[:3]
    return same_products


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


def products(request, pk=None, page=1):
    title = 'Продукты интернет-магазина'
    links_menu = ProductCategory.objects.all()
    hot_product = get_hot_product()

    if pk is not None:
        if pk == 0:
            products = Product.objects.all()
            category = {
                'pk': 0,
                'name': 'все'
            }
            products = Product.objects.filter(
                is_active=True,
                category__is_active=True).\
                order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(
                category__pk=pk,
                is_active=True, category__is_active=True).order_by('price')

        paginator = Paginator(products, 8)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
        }
        return render(request, 'mainapp/products_list.html', context)

    context = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': get_same_products(hot_product),
    }

    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    title = 'Продукты'

    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
    }

    return render(request, 'mainapp/product.html', content)


def contacts(request):

    context = {
        'title': 'Контакты интернет-магазина',
    }
    return render(request, 'mainapp/contacts.html', context=context)
