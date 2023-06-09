# Generated by Django 4.1.7 on 2023-04-07 13:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.IntegerField(unique=True)),
                ('nick_name', models.CharField(max_length=100)),
                ('photo_url', models.FilePathField(blank=True, null=True, path='C:\\Users\\stasm\\PycharmProjects\\Test_TEB\\register_tel\\media')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
