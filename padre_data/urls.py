from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    url(r'^db-indices-to-db-entries/$', views.map_db_indices_to_db_entries, name='padretest'),
    url(r'^visualization/$', views.visualization, name='visualization'),
    path('visualization/<int:vis_id>/data/', views.visualization_data, name='visualization-data'),
    path('visualization/<str:split_id>/<int:vis_id>/<str:label>/curve/',
         views.split_vis_curve_for_label, name='split-vis-curve'),
    path('visualization/<str:run_id>/<int:vis_id>/<str:label>/runcurve/',
         views.run_vis_curve_for_label, name='run-vis-curve'),
    url(r'^dataset-visualization/$', views.dataset_visualization, name='dataset-visualization'),
    url(r'^split-visualization/$', views.split_visualization, name='split-visualization'),
    url(r'^run-visualization/$', views.run_visualization, name='run-visualization'),
    url(r'^experiment-visualization/$', views.experiment_visualization, name='experiment-visualization'),
]