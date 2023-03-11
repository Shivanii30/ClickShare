# Generated by Django 4.1.7 on 2023-03-10 19:21

from django.db import migrations, models
import django.db.models.deletion
import home.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('unique_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=home.models.get_upload_path)),
                ('folder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.folder')),
            ],
        ),
    ]