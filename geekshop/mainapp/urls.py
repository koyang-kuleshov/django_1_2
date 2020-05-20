from django.urls import path, re_path
from django.views.decorators.cache import cache_page

import mainapp.views as mainapp


app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.products, name='index'),

    path('category/<int:pk>/', mainapp.products, name='category'),
    path('category/<int:pk>/ajax/', cache_page(5)(mainapp.products_ajax),
    # path('category/<int:pk>/ajax/', mainapp.products_ajax,
         name='category_ajax'),
    path('category/<int:pk>/page/<int:page>/', mainapp.products, name='page'),
    path('category/<int:pk>/page/<int:page>/ajax/',
         cache_page(5)(mainapp.products_ajax), name='page_ajax'),
         # mainapp.products_ajax, name='page_ajax'),

    path('product/<int:pk>/', mainapp.product, name='product'),
]
