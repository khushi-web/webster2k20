# Generated by Django 3.1.2 on 2020-10-29 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20201029_1133'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventMembers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.events')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.profile')),
            ],
        ),
    ]
