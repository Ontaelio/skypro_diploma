# Generated by Django 4.1.5 on 2023-02-10 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0005_alter_goalcategory_board'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='goals', to='goals.goalcategory', verbose_name='Категория'),
        ),
    ]
