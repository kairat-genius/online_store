# Generated by Django 4.1.5 on 2023-11-07 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('help_services', '0003_answer_is_answered_alter_answer_text_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
    ]