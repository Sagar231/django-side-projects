# Generated by Django 5.0.2 on 2024-06-25 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_comment_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='posted_by',
            field=models.CharField(default='sagar', max_length=100),
            preserve_default=False,
        ),
    ]
