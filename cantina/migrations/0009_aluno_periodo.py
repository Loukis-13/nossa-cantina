# Generated by Django 3.1.3 on 2020-12-22 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cantina', '0008_remove_aluno_periodo'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='periodo',
            field=models.CharField(default='T', max_length=10),
            preserve_default=False,
        ),
    ]