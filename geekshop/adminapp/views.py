from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse

from authapp.forms import ShopUserRegisterForm
from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm,\
    ProductEditForm
from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'Пользователь/Создание'

    if request.method == 'POST':
        user_form = ShopUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = ShopUserRegisterForm()

    content = {
        'title': title,
        'update_form': user_form
    }

    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'Админка/пользователи'
    users_list = ShopUser.objects.all().order_by(
        '-is_active',
        '-is_superuser',
        'is_staff',
        'username'
    )
    content = {
        'title': title,
        'objects': users_list
    }
    return render(request, 'adminapp/users.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'Пользователь/Редактирование'

    edit_user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        edit_form = ShopUserAdminEditForm(
            request.POST, request.FILES,
            instance=edit_user
        )
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:user_update',
                                                args=[edit_user.pk]))
    else:
        edit_form = ShopUserAdminEditForm(instance=edit_user)

    content = {
        'title': title,
        'update_form': edit_form
    }
    return render(request, 'adminapp/user_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'Пользователь/Удаление'

    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin:users'))

    content = {
        'title': title,
        'user_to_delete': user
    }
    return render(request, 'adminapp/user_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    title = 'Категория/Создание'
    if request.method == 'POST':
        category_form = ProductCategoryEditForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin:categories'))
    else:
        category_form = ProductCategoryEditForm()

    content = {
        'title': title,
        'update_form': category_form
    }
    return render(request, 'adminapp/category_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'Админка/Категории'
    categories_list = ProductCategory.objects.all()
    content = {
        'title': title,
        'objects': categories_list
    }
    return render(request, 'adminapp/categories.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    title = 'Категория/Редактирование'

    edit_category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        edit_form = ProductCategoryEditForm(
            request.POST, request.FILES,
            instance=edit_category
        )
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:category_update',
                                                args=[edit_category.pk]))
    else:
        edit_form = ProductCategoryEditForm(instance=edit_category)

    content = {
        'title': title,
        'update_form': edit_form
    }
    return render(request, 'adminapp/category_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    title = 'Категория/Удаление'

    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        category.is_active = False
        category.save()
        return HttpResponseRedirect(reverse('admin:categories'))

    content = {
        'title': title,
        'category_to_delete': category
    }
    return render(request, 'adminapp/category_delete.html', content)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'Админка/Товар'
    category = get_object_or_404(ProductCategory, pk=pk)

    products_list = Product.objects.filter(category__pk=pk).order_by('name')
    content = {
        'title': title,
        'category': category,
        'objects': products_list
    }
    return render(request, 'adminapp/products.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = 'Товар/Создать'
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('admin:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'category': category})

    content = {
        'title': title,
        'update_form': product_form,
        'category': category
    }
    return render(request, 'adminapp/product_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    title = 'Товар/Подробнее'
    product = get_object_or_404(Product, pk=pk)
    content = {
        'title': title,
        'object': product
    }
    return render(request, 'adminapp/product_read.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'Товар/Редактирование'
    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES,
                                    instance=edit_product
                                    )
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:product_update',
                                                args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    content = {
        'title': title,
        'update_form': edit_form,
        'category': edit_product.category
    }
    return render(request, 'adminapp/product_update.html', content)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'Товар/Удаление'
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse('admin:products',
                                            args=[product.category.pk]))

    content = {
        'title': title,
        'product_to_delete': product
    }
    return render(request, 'adminapp/product_delete.html', content)
