# Generated by Django 2.2.1 on 2019-06-04 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("Native_Service", "0001_squashed_0008_auto_20190604_0728")]

    operations = [
        migrations.AlterField(
            model_name="nativepost",
            name="last_name",
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name="nativepost", name="name", field=models.CharField(max_length=20)
        ),
    ]
