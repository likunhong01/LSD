# Generated by Django 2.2.5 on 2019-09-07 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lsdapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='留言id'),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='项目id，自增'),
        ),
        migrations.AlterField(
            model_name='userproject',
            name='userProject_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='主键'),
        ),
        migrations.AlterField(
            model_name='userstr',
            name='userStr_id',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='主键'),
        ),
    ]
