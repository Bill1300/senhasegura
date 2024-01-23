from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Senha',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=64)),
                ('descricao', models.CharField(max_length=128)),
                ('usuario', models.CharField(max_length=128)),
                ('senha', models.CharField(max_length=128)),
            ],
        ),
    ]
