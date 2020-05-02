from django.shortcuts import render


def main(requests):
    context = {
        'title': 'Интернет-магазин мебели'
    }
    return render(requests, 'mainapp/index.html', context=context)


def products(requests):
    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'}
    ]
    same_products = [
    ]
    context = {
        'title': 'Продукты интернет-магазина',
        'links_menu': links_menu,
        'same_products': same_products,
    }
    return render(requests, 'mainapp/products.html', context=context)


def contacts(request):
    context = {
        'title': 'Контакты интернет-магазина'
    }
    return render(request, 'mainapp/contacts.html', context=context)
