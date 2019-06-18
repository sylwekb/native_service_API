# Generated by Django 2.2.2 on 2019-06-18 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('Native_Service', '0010_FinalPricing_model_secret_key_added'), ('Native_Service', '0011_auto_20190618_1426'), ('Native_Service', '0012_auto_20190618_1432'), ('Native_Service', '0013_auto_20190618_1433'), ('Native_Service', '0014_auto_20190618_1433'), ('Native_Service', '0015_auto_20190618_1439'), ('Native_Service', '0016_auto_20190618_1441'), ('Native_Service', '0017_MigrationsAndModelsFixed')]

    dependencies = [
        ('Native_Service', '0009_NativePost_model_fixed_up'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nativepost',
            name='secret_key',
            field=models.CharField(max_length=13),
        ),
        migrations.AlterField(
            model_name='nativepost',
            name='secret_key',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='nativepost',
            name='file',
            field=models.FileField(blank=True, max_length=255, null=True, upload_to='uploads/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='nativepost',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='nativepost',
            name='secret_key',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='nativepost',
            name='secret_key',
            field=models.CharField(max_length=20),
        ),
        migrations.AddField(
            model_name='finalpricing',
            name='secret_key',
            field=models.CharField(max_length=45),
        ),
        migrations.AlterField(
            model_name='nativepost',
            name='secret_key',
            field=models.CharField(max_length=45),
        ),
    ]
