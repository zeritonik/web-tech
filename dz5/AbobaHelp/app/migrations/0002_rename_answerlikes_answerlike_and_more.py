# Generated by Django 4.2.11 on 2024-11-09 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AnswerLikes',
            new_name='AnswerLike',
        ),
        migrations.RenameModel(
            old_name='QuestionLikes',
            new_name='QuestionLike',
        ),
    ]