# Generated by Django 3.0.3 on 2020-02-15 18:10

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visualization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visualization', jsonfield.fields.JSONField(default=dict)),
            ],
        ),
        migrations.CreateModel(
            name='SplitVisualization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('split_id', models.CharField(max_length=50)),
                ('vis_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='padre_data.Visualization')),
            ],
        ),
        migrations.CreateModel(
            name='RunVisualization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('run_id', models.CharField(max_length=50)),
                ('vis_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='padre_data.Visualization')),
            ],
        ),
        migrations.CreateModel(
            name='ExperimentVisualization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experiment_id', models.CharField(max_length=50)),
                ('vis_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='padre_data.Visualization')),
            ],
        ),
        migrations.CreateModel(
            name='DatasetVisualization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataset_id', models.CharField(max_length=50)),
                ('vis_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='padre_data.Visualization')),
            ],
        ),
    ]
