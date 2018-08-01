# Generated by Django 2.0.5 on 2018-07-12 16:11

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CompiledDoc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompiledField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('content', models.CharField(max_length=50)),
                ('compiled_doc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form.CompiledDoc')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titolo', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name='Data')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Contenuto')),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='form.Document')),
            ],
        ),
        migrations.AddField(
            model_name='compiledfield',
            name='field',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='form.Field'),
        ),
        migrations.AddField(
            model_name='compileddoc',
            name='document',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='form.Document'),
        ),
    ]
