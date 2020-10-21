# Generated by Django 3.1.2 on 2020-10-15 10:08

from django.db import migrations, models
import django.db.models.deletion
import infra.tools


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.CharField(default=infra.tools.uuid4, max_length=128, primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=1024)),
                ('answer', models.CharField(max_length=1024)),
                ('last_reviewd_at', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.CharField(default=infra.tools.uuid4, max_length=128, primary_key=True, serialize=False)),
                ('name', models.CharField(default='default', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(default=infra.tools.uuid4, max_length=128, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.CharField(default=infra.tools.uuid4, max_length=128, primary_key=True, serialize=False)),
                ('target_amount', models.IntegerField()),
                ('current_amount', models.IntegerField(default=0)),
                ('is_ended', models.BooleanField(default=False)),
                ('card', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.card')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user'),
        ),
        migrations.AddField(
            model_name='card',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.group'),
        ),
    ]