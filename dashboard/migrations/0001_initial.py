# Generated by Django 3.2.5 on 2021-08-03 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_date', models.DateField(auto_now_add=True, verbose_name='Attendance Date')),
                ('attendance_time', models.TimeField(auto_now_add=True, verbose_name='Attendance Time')),
            ],
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Class Name')),
                ('time', models.TimeField(verbose_name='Class Time')),
                ('timeStamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=1024, unique=True, verbose_name='Key')),
                ('code', models.IntegerField(blank=True, unique=True, verbose_name='Code')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Link Creation Time')),
                ('expiry', models.DateTimeField(verbose_name='Expiry Date Time')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeStamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
