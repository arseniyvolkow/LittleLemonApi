# Generated by Django 5.0.4 on 2024-04-12 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LittleLemonAPI', '0004_alter_orderitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.SmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]
