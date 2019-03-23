# Generated by Django 2.1.5 on 2019-03-23 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.CharField(max_length=64)),
                ('producer_id', models.CharField(max_length=64)),
                ('limit', models.CharField(max_length=10)),
                ('temp_min', models.IntegerField()),
                ('temp_max', models.IntegerField()),
                ('hum_min', models.IntegerField()),
                ('hum_max', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('SLA', models.IntegerField()),
            ],
        ),
    ]
