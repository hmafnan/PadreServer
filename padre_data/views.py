import json
import pandas as pd
from django.http import JsonResponse
from .models import *
from . import helpers
from django.views.decorators.csrf import csrf_exempt

from pypadre.core.my_backend import https

NGROK_URL = 'https://' + 'a083cdf3.ngrok.io'
TOKEN = 'Bearer ff3847eb-3cd4-4cfb-81b9-7e14fa650738'

@csrf_exempt
def map_db_indices_to_db_entries(request):
    """
    Maps db indices to db entries for given indices of tp, tn, fp, fn

    Post object should contain data in a form:
        POST: {
            'dataset_id' str (Dataset for which original feature vector should be returned)
            'db_indices': {   (Original feature vector for each operation ie tp, tn, fp, fn)
                'tp': list of str indices,
                'tn': list of str indices,
                'fp': list of str indices,
                'fn': list of str indices
            }
        }

    returns:
    """
    dataset_id_on_server = request.GET.get('dataset_id', '')
    split_id = request.GET.get('split_id', None)
    vis_id = request.GET.get('vis_id', None)
    threshold = request.GET.get('threshold', None)
    legend = request.GET.get('label', None)
    label = {'tp': 'True Positive Entries', 'tn': 'True Negative Entries',
             'fp': 'False Positive Entries', 'fn': 'False Negative Entries'}
    pc = https.PadreHTTPClient(token=TOKEN)
    db_indices = SplitVisualization.objects.get(split_id=split_id, vis_id=vis_id).pr_curve_data
    if legend is not None:
        legend = str(float(legend))
        db_indices = db_indices[legend][threshold]
    else:
        db_indices = db_indices[threshold]

    if dataset_id_on_server == '':
        ds = helpers.load_digits_data()
    else:
        ds = pc.datasets.get(dataset_id_on_server)
    attributes = [attr['name'] for attr in ds.attributes]
    db_data = json.loads(ds.data().to_json(orient='records'))
    data = {"headers": attributes}
    for key, indices in db_indices.items():
        if key == 'cm':
            continue
        data[key] = {
            'title': label[key],
            'data': [list(db_data[i].values()) for i in indices]
        }
    return JsonResponse(data, safe=False)

@csrf_exempt
def visualization_data(request, vis_id):
    """Get json data for visualization"""
    vis = Visualization.objects.get(id=vis_id)
    data = vis.data
    return JsonResponse(data, safe=False)

@csrf_exempt
def split_vis_curve_for_label(request, split_id, vis_id, label):
    """Get json data for visualization"""
    label = float(label)
    vis = Visualization.objects.get(id=vis_id)
    obj = SplitVisualization.objects.filter(split_id=split_id, vis_id=vis_id).first()
    cm_data = {thr: obj.pr_curve_data[str(label)][thr]['cm'] for thr in obj.pr_curve_data[str(label)].keys()}
    vis_data = list(filter(lambda d: d['color'] == label, vis.data))
    schema = {
        '$schema': 'https://vega.github.io/schema/vega-lite/v4.0.2.json',
        'config': {'view': {'continuousHeight': 300, 'continuousWidth': 400}},
        'data': {'name': 'data-eb5321d2f4f6aa0a85d78db4b85fdcf8'},
        'datasets': {'data-eb5321d2f4f6aa0a85d78db4b85fdcf8': vis_data},
        'layer': [{
            'encoding':
                {'x': {'field': 'x', 'title': 'Recall', 'type': 'quantitative'},
                 'y': {'field': 'y', 'title': 'Precision', 'type': 'quantitative'}},
            'mark': {'color': 'lightblue', 'interpolate': 'step-after', 'line': True, 'type': 'area'
                     }},
            {'encoding': {'opacity': {'value': 0},
            'x': {'field': 'x', 'type': 'quantitative'}},
           'mark': 'point',
           'selection': {'selector009': {'empty': 'none',
             'nearest': True,
             'on': 'mouseover',
             'type': 'single'}}},
          {'encoding': {'opacity': {'condition': {'selection': 'selector009',
              'value': 1},
             'value': 0},
            'x': {'field': 'x', 'title': 'Recall', 'type': 'quantitative'},
            'y': {'field': 'y', 'title': 'Precision', 'type': 'quantitative'}},
           'mark': 'point'},
          {'encoding': {'text': {'condition': {'field': 'thresholds',
              'selection': 'selector009',
              'type': 'ordinal'},
             'value': ' '},
            'x': {'field': 'x', 'title': 'Recall', 'type': 'quantitative'},
            'y': {'field': 'y', 'title': 'Precision', 'type': 'quantitative'}},
           'mark': {'align': 'left', 'dx': 5, 'dy': -5, 'type': 'text'}}],
         'title': 'Curve for label ' + str(label)
    }
    result = {'schema': schema, 'thresholdsCM': cm_data}

    return JsonResponse(result, safe=False)




@csrf_exempt
def visualization(request):
    """Save visualization or get all visualizations

    While saving visualization schema, save data reference instead of full data
    """
    if request.method == 'POST':
        title = request.POST['title']
        obj = Visualization.objects.create(title=title)
        visualization = json.loads(request.POST['visualization'])
        data = visualization['datasets'][visualization['data']['name']]
        del visualization['datasets']
        del visualization['data']['name']
        visualization["data"]["url"] = "padre/visualization/" + str(obj.id) + "/data/"
        obj.visualization = visualization
        obj.data = data
        obj.save()
        return JsonResponse({'id': obj.id})
    else:
        data = []
        for vis in Visualization.objects.all():
            data.append({'title': vis.title, 'visualization': vis.visualization})
        return JsonResponse(data, safe=False)


@csrf_exempt
def dataset_visualization(request):
    """Save reference to the visualization for dataset or get visualization for given dataset id"""
    if request.method == 'POST':
        dataset_id = request.POST['dataset_id']
        vis_id = request.POST['visualization_id']
        obj = DatasetVisualization.objects.create(dataset_id=dataset_id,
                                                  vis_id=vis_id)
        return JsonResponse({'id': obj.id})
    else:
        dataset_id = request.GET['dataset_id']
        data = []
        for obj in DatasetVisualization.objects.filter(dataset_id=dataset_id):
            data.append({'uid': obj.vis.id, 'title': obj.vis.title, 'schema': obj.vis.visualization})
        return JsonResponse(data, safe=False)


@csrf_exempt
def split_visualization(request):
    """Save reference to the visualization for split or get visualization for given split id"""
    if request.method == 'POST':
        split_id = request.POST['split_id']
        vis_id = request.POST['visualization_id']
        pr_curve_data = json.loads(request.POST['pr_curve_data'])
        obj = SplitVisualization.objects.create(split_id=split_id,
                                                vis_id=vis_id,
                                                pr_curve_data=pr_curve_data)
        return JsonResponse({'id': obj.id})
    else:
        split_id = request.GET['split_id']
        data = []
        for obj in SplitVisualization.objects.filter(split_id=split_id):
            cm_data = {thr: obj.pr_curve_data[thr]['cm'] for thr in obj.pr_curve_data.keys() if not obj.multi_class}
            if 'color' in obj.vis.data[0].keys():
                legends = {item['color'] for item in obj.vis.data}
                legends = [{"text": item, "value": item} for item in legends]
            else:
                legends = []
            data.append({
                'uid': obj.vis.id,
                'title': obj.vis.title,
                'schema': obj.vis.visualization,
                'legend': legends,
                'thresholdsCM': cm_data})
        return JsonResponse(data, safe=False)


@csrf_exempt
def run_visualization(request):
    """Save reference to  the visualization for run or get visualization for given run id"""
    if request.method == 'POST':
        run_id = request.POST['run_id']
        vis_id = request.POST['visualization_id']
        obj = RunVisualization.objects.create(run_id=run_id,
                                              vis_id=vis_id)
        return JsonResponse({'id': obj.id})
    else:
        run_id = request.GET['run_id']
        data = []
        for obj in RunVisualization.objects.filter(run_id=run_id):
            data.append({'title': obj.vis.title, 'visualization': obj.vis.visualization})
        return JsonResponse(data, safe=False)


@csrf_exempt
def experiment_visualization(request):
    """Save reference to the visualization for experiment or get visualization for given experiment
     id"""
    if request.method == 'POST':
        experiment_id = request.POST['experiment_id']
        vis_id = request.POST['visualization_id']
        obj = ExperimentVisualization.objects.create(experiment_id=experiment_id,
                                                     vis_id=vis_id)
        return JsonResponse({'id': obj.id})
    else:
        experiment_id = request.GET['experiment_id']
        data = []
        for obj in ExperimentVisualization.objects.filter(experiment_id=experiment_id):
            data.append({'title': obj.vis.title, 'visualization': obj.vis.visualization})
        return JsonResponse(data, safe=False)

