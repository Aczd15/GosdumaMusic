import re

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import MusicGroup, MusicRequest, Profile, RequestCategory

PHONE_PATTERN = r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$'
FULL_NAME_PATTERN = r'^[А-Яа-яЁё\s]+$'


def normalize_phone(value: str) -> str:
    raw_phone = value.strip()
    digits = ''.join(ch for ch in raw_phone if ch.isdigit())

    if len(digits) == 11 and digits.startswith('7'):
        digits = f'8{digits[1:]}'

    if len(digits) != 11 or not digits.startswith('8'):
        raise forms.ValidationError('Введите телефон: 8(XXX)XXX-XX-XX, 8XXXXXXXXXX или +7XXXXXXXXXX.')

    phone = f'{digits[0]}({digits[1:4]}){digits[4:7]}-{digits[7:9]}-{digits[9:11]}'
    if not re.fullmatch(PHONE_PATTERN, phone):
        raise forms.ValidationError('Телефон должен быть в формате 8(XXX)XXX-XX-XX.')

    return phone


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Логин', min_length=3, max_length=150)
    password = forms.CharField(label='Пароль', min_length=6, widget=forms.PasswordInput)
    full_name = forms.CharField(label='ФИО', max_length=255)
    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        help_text='Можно вводить в любом привычном виде: 89001234567, +7 900 123-45-67 и т.д.',
        widget=forms.TextInput(attrs={'placeholder': '8(900)123-45-67', 'inputmode': 'tel'}),
    )
    email = forms.EmailField(label='E-mail', max_length=254)

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует.')
        return username

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name'].strip()
        if not re.fullmatch(FULL_NAME_PATTERN, full_name):
            raise forms.ValidationError('ФИО должно содержать только кириллицу и пробелы.')
        return full_name

    def clean_phone(self):
        phone = normalize_phone(self.cleaned_data['phone'])
        if Profile.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Пользователь с таким номером телефона уже существует.')
        return phone

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким e-mail уже существует.')
        return email

    def save(self) -> User:
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )
        Profile.objects.create(
            user=user,
            full_name=self.cleaned_data['full_name'],
            phone=self.cleaned_data['phone'],
        )
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Неверный логин или пароль.')
            cleaned_data['user'] = user
        return cleaned_data


class MusicRequestForm(forms.ModelForm):
    class Meta:
        model = MusicRequest
        fields = ['project_name', 'event_date', 'category', 'participation_format']
        labels = {
            'project_name': 'Название проекта/мероприятия',
            'event_date': 'Желаемая дата проведения',
            'category': 'Категория заявки',
            'participation_format': 'Формат участия',
        }
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = RequestCategory.objects.all()
        if not self.fields['category'].queryset.exists():
            self.fields['category'].help_text = 'Категорий пока нет. Администратор может добавить их в панели администратора.'


class RequestCategoryForm(forms.ModelForm):
    class Meta:
        model = RequestCategory
        fields = ['name']
        labels = {'name': 'Новая категория'}


class MusicGroupForm(forms.ModelForm):
    class Meta:
        model = MusicGroup
        fields = ['name', 'description']
        labels = {
            'name': 'Название группы',
            'description': 'Описание (необязательно)',
        }


class ProfileGroupCreateForm(forms.ModelForm):
    class Meta:
        model = MusicGroup
        fields = ['name', 'description']
        labels = {
            'name': 'Название вашей группы',
            'description': 'Описание группы (необязательно)',
        }


class AdminUserCreateForm(forms.Form):
    username = forms.CharField(label='Логин', min_length=3, max_length=150)
    password = forms.CharField(label='Пароль', min_length=6, widget=forms.PasswordInput)
    full_name = forms.CharField(label='ФИО', max_length=255)
    phone = forms.CharField(label='Телефон', max_length=30)
    email = forms.EmailField(label='E-mail', max_length=254)
    group = forms.ModelChoiceField(label='Группа', queryset=MusicGroup.objects.none(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group'].queryset = MusicGroup.objects.all()

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует.')
        return username

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name'].strip()
        if not re.fullmatch(FULL_NAME_PATTERN, full_name):
            raise forms.ValidationError('ФИО должно содержать только кириллицу и пробелы.')
        return full_name

    def clean_phone(self):
        phone = normalize_phone(self.cleaned_data['phone'])
        if Profile.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Пользователь с таким номером телефона уже существует.')
        return phone

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким e-mail уже существует.')
        return email

    def save(self) -> User:
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
        )
        Profile.objects.create(
            user=user,
            full_name=self.cleaned_data['full_name'],
            phone=self.cleaned_data['phone'],
            group=self.cleaned_data['group'],
        )
        return user


class StatusUpdateForm(forms.Form):
    request_id = forms.IntegerField(widget=forms.HiddenInput)
    status = forms.ChoiceField(choices=MusicRequest.STATUS_CHOICES)
