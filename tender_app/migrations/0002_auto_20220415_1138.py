# Generated by Django 3.2.5 on 2022-04-15 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tender_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='tender_keword_models',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keywords', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'test_tender_kewords',
            },
        ),
        migrations.CreateModel(
            name='test_tender_model',
            fields=[
                ('IDs', models.AutoField(primary_key=True, serialize=False)),
                ('E_Published_Date', models.DateField()),
                ('Closing_Date', models.DateField()),
                ('Opening_Date', models.DateField()),
                ('Organisation_Chain', models.CharField(max_length=500)),
                ('Tender_Title', models.CharField(max_length=1000)),
                ('Ref_NO', models.CharField(max_length=100)),
                ('Tender_ID', models.CharField(max_length=50)),
                ('Tender_URL', models.CharField(max_length=1000)),
            ],
            options={
                'db_table': 'test_tender_model',
            },
        ),
        migrations.DeleteModel(
            name='tender_model',
        ),
    ]
