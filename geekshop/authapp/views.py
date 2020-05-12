from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, \
    ShopUserEditForm
from authapp.models import ShopUser


def login(request):
    title = 'Вход'
    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main'))

    context = {'title': title, 'login_form': login_form, 'next': next}
    return render(request, 'authapp/login.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def register(request):
    title = 'Регистрация'
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                text = f'Сообщение успешно отправлено на почту {user.email}'
                return render(
                    request,
                    'authapp/letter_send.html',
                    {'txt': text}
                )
            else:
                text = f'Сбой при отправке сообщения на почту {user.email}'
                letter_send(request, text)
                return render(
                    request,
                    'authapp/letter_send.html',
                    {'txt': text}
                )
    else:
        register_form = ShopUserRegisterForm()
    context = {'title': title, 'register_form': register_form}
    return render(request, 'authapp/register.html', context=context)


def edit(request):
    title = 'Редактирование пользователя'
    if request.method == 'POST':
        edit_form = ShopUserEditForm(
            request.POST,
            request.FILES,
            instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        edit_form = ShopUserRegisterForm(instance=request.user)
    context = {'title': title, 'edit_form': edit_form}
    return render(request, 'authapp/edit.html', context=context)


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email,
                                               user.activation_key])
    title = f'Подтверждение учётной записи {user.username}'
    message = (f'For activation account {user.username}'
               f'on site {settings.DOMAIN_NAME} click on link:'
               f'\n{settings.DOMAIN_NAME}{verify_link}'
               )
    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email],
                     fail_silently=False
                     )


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if (user.activation_key == activation_key and
                not user.is_activation_key_expired()):
            user.is_active = True
            user.save()
            auth.login(
                request,
                user,
                backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html')
        else:
            return render(request, 'authapp/verification.html')
    except Exception:
        return HttpResponseRedirect(reverse('main'))


def letter_send(request):
    pass
