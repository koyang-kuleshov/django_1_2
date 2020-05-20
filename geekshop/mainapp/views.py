import random
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.cache import cache
from django.template.loader import render_to_string
from django.http import JsonResponse

from .models import ProductCategory, Product


def get_hot_product():
    products = get_products()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).\
        exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):
    spam = get_products()
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


def product(request, pk):
    title = 'Продукты'

    content = {
        'title': title,
        'links_menu': get_links_menu(),
        'product': get_product(pk),
    }

    return render(request, 'mainapp/product.html', content)


def contacts(request):

    context = {
        'title': 'Контакты интернет-магазина',
    }
    return render(request, 'mainapp/contacts.html', context=context)


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True,
                                              category__is_active=True).\
                                              select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True,
                                      category__is_active=True).\
                                        select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_in_category_order_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_order_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk,
                                              is_active=True,
                                              category__is_active=True).\
                                              order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True,
                                      category__is_active=True).\
                                      order_by('price')


def get_products_order_by_price():
    if settings.LOW_CACHE:
        key = 'products_order_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True,
                                              category__is_active=True).\
                                              order_by('price')
            cache.set(key, products)
            return products
    else:
        return Product.objects.filter(is_active=True,
                                      category__is_active=True).\
                                      order_by('price')


def products(request, pk=None, page=1):
    title = 'Продукты интернет-магазина'
    links_menu = get_links_menu()
    hot_product = get_hot_product()
    if pk:
        if pk == '0':
            category = {
                'pk': 0,
                'name': 'продукты'
            }
            products = get_products_order_by_price()
        else:
            category = get_category(pk)
            products = get_products_in_category_order_by_price(pk)
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


def products_ajax(request, pk=None, page=1):
    if request.is_ajax():
        links_menu = get_links_menu()
        if pk:
            if pk == 0:
                category = {
                   'pk': 0,
                   'name': 'продукты'
                }
                products = get_products_order_by_price()
                # products = Product.objects.filter(is_active=True,
                #                       category__is_active=True).\
                #                       order_by('price')
            else:
                category = get_category(pk)
                products = get_products_in_category_order_by_price(pk)
            paginator = Paginator(products, 8)
            try:
                products_paginator = paginator.page(page)
            except PageNotAnInteger:
                products_paginator = paginator.page(1)
            except EmptyPage:
                products_paginator = paginator.page(paginator.num_pages)

            content = {
                'links_menu': links_menu,
                'category': category,
                'products': products_paginator,
            }

            result = render_to_string(
                            'mainapp/includes/inc_products_list_content.html',
                            context=content,
                            request=request)

            return JsonResponse({'result': result})
