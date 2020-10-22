# Generated by Django 3.1 on 2020-10-17 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=255)),
                ('item_desc', models.TextField()),
                ('item_price', models.DecimalField(decimal_places=3, max_digits=7)),
                ('item_image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('min_calories', models.IntegerField()),
                ('max_calories', models.IntegerField()),
                ('dietary', models.TextField(blank=True)),
                ('is_available', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', related_query_name='items', to='adminPanel.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=255)),
                ('address1', models.CharField(max_length=255)),
                ('address2', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('state', models.CharField(max_length=100)),
                ('county', models.CharField(blank=True, max_length=100)),
                ('country', models.CharField(blank=True, max_length=3)),
                ('phone', models.CharField(blank=True, max_length=50)),
                ('is_restaurant', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', related_query_name='subcategories', to='adminPanel.category')),
            ],
        ),
        migrations.CreateModel(
            name='ItemOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_discount', models.DecimalField(decimal_places=3, max_digits=7)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', related_query_name='options', to='adminPanel.Item')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemOptions', related_query_name='itemOptions', to='adminPanel.Item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='locations',
            field=models.ManyToManyField(related_name='items', related_query_name='items', to='adminPanel.Location'),
        ),
        migrations.AddField(
            model_name='item',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', related_query_name='items', to='adminPanel.SubCategory'),
        ),
    ]
