# Generated by Django 4.1.1 on 2022-11-23 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_id_subdivison_employeessubdivision_id_subdivision_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_role', models.CharField(max_length=25)),
            ],
        ),
        migrations.AddField(
            model_name='employees',
            name='id_role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.roles'),
        ),
    ]