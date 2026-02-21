from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return self.full_name


class RequestCategory(models.Model):
    name = models.CharField('Категория', max_length=120, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория заявки'
        verbose_name_plural = 'Категории заявок'

    def __str__(self) -> str:
        return self.name


class MusicRequest(models.Model):
    STATUS_NEW = 'Новая'
    STATUS_REVIEW = 'На рассмотрении'
    STATUS_APPROVED = 'Одобрена'
    STATUS_REJECTED = 'Отклонена'

    STATUS_CHOICES = [
        (STATUS_NEW, 'Новая'),
        (STATUS_REVIEW, 'На рассмотрении'),
        (STATUS_APPROVED, 'Одобрена'),
        (STATUS_REJECTED, 'Отклонена'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='music_requests')
    project_name = models.CharField(max_length=255)
    event_date = models.DateField()
    genre = models.CharField(max_length=100)
    category = models.ForeignKey(
        RequestCategory,
        on_delete=models.PROTECT,
        related_name='music_requests',
        null=True,
        blank=True,
    )
    participation_format = models.CharField(max_length=120)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.project_name} ({self.status})'
