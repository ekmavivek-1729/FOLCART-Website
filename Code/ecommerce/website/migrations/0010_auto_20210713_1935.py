# Generated by Django 3.1.5 on 2021-07-13 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermaster',
            name='payment_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='payment',
        ),
    ]