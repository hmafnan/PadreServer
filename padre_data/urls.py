from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    url(r'^visualization/$', views.visualization, name='visualization'),
    path('visualization/<int:vis_id>/data/', views.visualization_data, name='visualization-data'),
    url(r'^dataset-visualization/$', views.dataset_visualization, name='dataset-visualization'),
    url(r'^split-visualization/$', views.split_visualization, name='split-visualization'),
    url(r'^run-visualization/$', views.run_visualization, name='run-visualization'),
    url(r'^experiment-visualization/$', views.experiment_visualization, name='experiment-visualization'),
]