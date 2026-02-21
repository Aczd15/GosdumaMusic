from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def assign_default_group(apps, schema_editor):
    Profile = apps.get_model('portal', 'Profile')
    MusicGroup = apps.get_model('portal', 'MusicGroup')
    default_group, _ = MusicGroup.objects.get_or_create(name='Без группы')
    Profile.objects.filter(group__isnull=True).update(group=default_group)


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_requestcategory_musicrequest_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MusicGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True, verbose_name='Название группы')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owned_groups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Музыкальная группа',
                'verbose_name_plural': 'Музыкальные группы',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='portal.musicgroup'),
        ),
        migrations.RunPython(assign_default_group, migrations.RunPython.noop),
    ]
