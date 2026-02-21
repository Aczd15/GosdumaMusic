from django.db import migrations, models
import django.db.models.deletion


def create_categories(apps, schema_editor):
    MusicRequest = apps.get_model('portal', 'MusicRequest')
    RequestCategory = apps.get_model('portal', 'RequestCategory')

    defaults = ['Концерт', 'Фестиваль', 'Корпоратив', 'Городское мероприятие']
    for item in defaults:
        RequestCategory.objects.get_or_create(name=item)

    existing_genres = (
        MusicRequest.objects.exclude(genre='')
        .values_list('genre', flat=True)
        .distinct()
    )
    for genre in existing_genres:
        category, _ = RequestCategory.objects.get_or_create(name=genre)
        MusicRequest.objects.filter(genre=genre, category__isnull=True).update(category=category)


def remove_categories(apps, schema_editor):
    RequestCategory = apps.get_model('portal', 'RequestCategory')
    RequestCategory.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True, verbose_name='Категория')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Категория заявки',
                'verbose_name_plural': 'Категории заявок',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='musicrequest',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='music_requests', to='portal.requestcategory'),
        ),
        migrations.RunPython(create_categories, remove_categories),
    ]
