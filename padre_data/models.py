from django.db import models


import jsonfield


class Visualization(models.Model):
    title = models.CharField(max_length=150, default='')
    visualization = jsonfield.JSONField(default={})
    data = jsonfield.JSONField(default={})


class DatasetVisualization(models.Model):
    """All visualizations references for datasets"""
    dataset_id = models.CharField(max_length=50)
    vis = models.ForeignKey(Visualization, on_delete=models.DO_NOTHING,)


class SplitVisualization(models.Model):
    """All visualizations references for splits"""
    split_id = models.CharField(max_length=50)
    vis = models.ForeignKey(Visualization, on_delete=models.DO_NOTHING,)


class RunVisualization(models.Model):
    """All visualizations references for runs"""
    run_id = models.CharField(max_length=50)
    vis = models.ForeignKey(Visualization, on_delete=models.DO_NOTHING,)


class ExperimentVisualization(models.Model):
    """All visualizations references for experiments"""
    experiment_id = models.CharField(max_length=50)
    vis = models.ForeignKey(Visualization, on_delete=models.DO_NOTHING,)

