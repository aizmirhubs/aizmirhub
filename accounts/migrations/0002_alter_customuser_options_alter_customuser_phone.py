# Generated by Django 5.1.7 on 2025-04-02 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Kullanıcı', 'verbose_name_plural': 'Kullanıcılar'},
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(blank=True, max_length=15, verbose_name='Telefon Numarası'),
        ),
    ]
