# Generated by Django 3.0.5 on 2020-04-27 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200427_0109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='images', to='blog.ImageGroup'),
        ),
    ]