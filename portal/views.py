from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import (
    LoginForm,
    MusicRequestForm,
    RegistrationForm,
    RequestCategoryForm,
    StatusUpdateForm,
)
from .models import MusicRequest

ADMIN_LOGIN = 'BraveGuap'
ADMIN_PASSWORD = 'gosdum'


def ensure_admin_user() -> User:
    admin_user, created = User.objects.get_or_create(
        username=ADMIN_LOGIN,
        defaults={'is_staff': True, 'is_superuser': True, 'email': 'admin@gosdumamusic.local'},
    )
    if created or not admin_user.check_password(ADMIN_PASSWORD):
        admin_user.set_password(ADMIN_PASSWORD)
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
    return admin_user


@require_http_methods(['GET', 'POST'])
def login_view(request: HttpRequest) -> HttpResponse:
    ensure_admin_user()

    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_panel')
        return redirect('dashboard')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.cleaned_data['user']
        login(request, user)
        if user.is_superuser:
            return redirect('admin_panel')
        return redirect('dashboard')

    return render(request, 'portal/login.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def register_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Регистрация прошла успешно. Теперь выполните вход.')
        return redirect('login')

    return render(request, 'portal/register.html', {'form': form})


@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_superuser:
        return redirect('admin_panel')
    requests = request.user.music_requests.select_related('category').all()
    return render(request, 'portal/dashboard.html', {'requests': requests})


@login_required
@require_http_methods(['GET', 'POST'])
def create_request_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_superuser:
        return redirect('admin_panel')

    form = MusicRequestForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        music_request = form.save(commit=False)
        music_request.user = request.user
        music_request.status = MusicRequest.STATUS_NEW
        music_request.genre = music_request.category.name
        music_request.save()
        messages.success(request, 'Заявка отправлена и получила статус «Новая».')
        return redirect('dashboard')

    return render(request, 'portal/create_request.html', {'form': form})


@login_required
@require_http_methods(['GET', 'POST'])
def admin_panel_view(request: HttpRequest) -> HttpResponse:
    ensure_admin_user()
    if not request.user.is_superuser:
        return redirect('dashboard')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_status':
            form = StatusUpdateForm(request.POST)
            if form.is_valid():
                music_request = get_object_or_404(MusicRequest, pk=form.cleaned_data['request_id'])
                music_request.status = form.cleaned_data['status']
                music_request.save(update_fields=['status'])
                messages.success(request, 'Статус заявки обновлен.')
            return redirect('admin_panel')

        if action == 'create_category':
            category_form = RequestCategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                messages.success(request, 'Категория успешно добавлена.')
            else:
                all_requests = MusicRequest.objects.select_related('user', 'user__profile', 'category').all()
                status_form = StatusUpdateForm()
                return render(
                    request,
                    'portal/admin_panel.html',
                    {
                        'requests': all_requests,
                        'status_choices': MusicRequest.STATUS_CHOICES,
                        'status_form': status_form,
                        'category_form': category_form,
                    },
                )
            return redirect('admin_panel')

    all_requests = MusicRequest.objects.select_related('user', 'user__profile', 'category').all()
    return render(
        request,
        'portal/admin_panel.html',
        {
            'requests': all_requests,
            'status_choices': MusicRequest.STATUS_CHOICES,
            'status_form': StatusUpdateForm(),
            'category_form': RequestCategoryForm(),
        },
    )


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('login')
