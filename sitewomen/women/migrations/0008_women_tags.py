# Generated by Django 5.0.3 on 2024-03-28 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0007_tagpost_alter_women_cat'),
    ]

    operations = [
        migrations.AddField(
            model_name='women',
            name='tags',
            field=models.ManyToManyField(related_name='posts', to='women.tagpost'),
        ),
    ]