from django.shortcuts import render


def main(requests):
    return render(requests, 'mainapp/index.html')


def products(requests):
    return render(requests, 'mainapp/products.html')


def contacts(request):
    return render(request, 'mainapp/contacts.html')
