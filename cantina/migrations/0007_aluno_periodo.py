# Generated by Django 3.1.3 on 2020-12-22 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cantina', '0006_auto_20201220_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='periodo',
            field=models.CharField(choices=[('M', 'Manhã'), ('T', 'Tarde'), ('N', 'Noite')], default='Tarde', max_length=10),
            preserve_default=False,
        ),
    ]
