# Generated by Django 2.0.3 on 2018-04-12 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_comment_belong_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='best_comment',
            field=models.BooleanField(default=False),
        ),
    ]