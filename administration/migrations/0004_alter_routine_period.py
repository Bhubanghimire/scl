# Generated by Django 3.2.4 on 2021-06-25 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0003_auto_20210625_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routine',
            name='period',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.periods'),
        ),
    ]
