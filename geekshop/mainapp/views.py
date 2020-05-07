import random
from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product
from basketapp.models import Basket


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


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
    basket = get_basket(request.user)

    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    context = {
        'title': title,
        'product_list': product_list,
        'trending_products': trending_products,
        'small_products': small_products,
        'basket': basket
    }
    return render(request, 'mainapp/index.html', context=context)


def products(request, pk=None):
    title = 'Продукты интернет-магазина'
    links_menu = ProductCategory.objects.all()
    hot_product = get_hot_product()
    basket = get_basket(request.user)

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
            'category': category,
            'products': products,
            'basket': basket,
        }
        return render(request, 'mainapp/products_list.html', context)

    context = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': get_same_products(hot_product),
        'basket': basket,
    }

    return render(request, 'mainapp/products.html', context=context)


def product(request, pk):
    title = 'Продукты'

    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user)
    }

    return render(request, 'mainapp/product.html', content)


def contacts(request):
    basket = get_basket(request.user)

    context = {
        'title': 'Контакты интернет-магазина',
        'basket': basket
    }
    return render(request, 'mainapp/contacts.html', context=context)
