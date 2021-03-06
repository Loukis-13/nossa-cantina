# Generated by Django 3.1.3 on 2020-12-19 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cantina', '0002_mensagem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pedidos', models.CharField(max_length=255)),
                ('data', models.DateField(auto_now_add=True)),
                ('entregue', models.BooleanField(default=False)),
                ('escola', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cantina.escola')),
            ],
        ),
    ]
