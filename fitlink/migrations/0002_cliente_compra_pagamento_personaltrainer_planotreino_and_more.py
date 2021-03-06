# Generated by Django 4.0.5 on 2022-06-02 15:00

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('fitlink', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataCompra', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('apelido', models.CharField(max_length=255)),
                ('montante', models.FloatField()),
                ('emailPaypal', models.EmailField(max_length=254)),
                ('entidade', models.IntegerField()),
                ('referenciaMB', models.IntegerField()),
                ('nrCartao', models.IntegerField()),
                ('cvv', models.IntegerField()),
                ('expireDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='PersonalTrainer',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('classificacao', models.IntegerField()),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='PlanoTreino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('descricao', models.TextField()),
                ('requisitos', models.TextField()),
                ('preco', models.FloatField()),
                ('periodoBloco', models.IntegerField()),
                ('nrBlocos', models.IntegerField()),
                ('refPersonalTrainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitlink.personaltrainer')),
            ],
        ),
        migrations.CreateModel(
            name='TipoPlano',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='Planos',
        ),
        migrations.AddField(
            model_name='planotreino',
            name='tipoPlano',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitlink.tipoplano'),
        ),
        migrations.AddField(
            model_name='compra',
            name='refPlano',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fitlink.planotreino'),
        ),
    ]
