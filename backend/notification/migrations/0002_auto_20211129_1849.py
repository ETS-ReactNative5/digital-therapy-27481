# Generated by Django 2.2.24 on 2021-11-29 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='action_url',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='level',
            field=models.CharField(choices=[('explain', 'explain'), ('info', 'info'), ('sent', 'sent'), ('resolved', 'resolved'), ('invitation', 'invitation')], default='info', max_length=20),
        ),
    ]
