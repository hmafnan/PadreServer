# Generated by Django 3.0.3 on 2020-02-17 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('padre_data', '0002_visualization_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datasetvisualization',
            old_name='vis_id',
            new_name='vis',
        ),
        migrations.RenameField(
            model_name='experimentvisualization',
            old_name='vis_id',
            new_name='vis',
        ),
        migrations.RenameField(
            model_name='runvisualization',
            old_name='vis_id',
            new_name='vis',
        ),
        migrations.RenameField(
            model_name='splitvisualization',
            old_name='vis_id',
            new_name='vis',
        ),
    ]
