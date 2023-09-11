# Generated by Django 4.2.4 on 2023-09-10 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_rename_excerpt_people_field_remove_people_title_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('field', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='People',
        ),
        migrations.AlterField(
            model_name='books',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
