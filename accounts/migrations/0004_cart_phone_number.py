# Generated by Django 5.1.1 on 2024-09-21 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_cartitems_size_varient_cartitems_size_variant_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
