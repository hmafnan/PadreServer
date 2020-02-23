import json
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt

from pypadre.core.my_backend import https

NGROK_URL = 'https://' + 'a083cdf3.ngrok.io'
TOKEN = 'Bearer 5d9ac400-6c0a-460a-a209-a93b9a470865'

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
    dataset_id_on_server = request.GET.get('dataset_id', '102')
    split_id = request.GET.get('split_id', None)
    vis_id = request.GET.get('vis_id', None)
    threshold = request.GET.get('threshold', None)
    label = {'tp': 'True Positive Entries', 'tn': 'True Negative Entries',
             'fp': 'False Positive Entries', 'fn': 'False Negative Entries'}
    pc = https.PadreHTTPClient(token=TOKEN)
    db_indices = SplitVisualization.objects.get(split_id=split_id, vis_id=vis_id).pr_curve_data
    db_indices = db_indices[threshold]

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
            cm_data = {thr: obj.pr_curve_data[thr]['cm'] for thr in obj.pr_curve_data.keys()}
            data.append({
                'uid': obj.vis.id,
                'title': obj.vis.title,
                'schema': obj.vis.visualization,
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

