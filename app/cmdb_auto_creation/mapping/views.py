from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import JsonResponse
import json
import requests

from .i_doit_api import process_idoit
from .app_data_model import process_data_model
from .mapping_ import map_

from colored import fg, bg, attr
blue = fg('#46B1C9')
red = fg('#B54653')
green = fg('#86DEB7')
reset = attr('reset')

# Create your views here.


def mapping_setup(request):
    # return HttpResponse("Mapping.")
    return render(request, 'mapping/mapping_setup.html', {})


def cmdb_setup(request):
    if "connection" in request.POST:
        connection = request.POST['connection']
    else:
        return render(request, 'mapping/mapping_setup.html', {"error_message": "Please select one option."})
    if "cmdbtype" in request.POST:
        cmdbtype = request.POST['cmdbtype']
        request.session['cmdbtype'] = cmdbtype
    else:
        return render(request, 'mapping/mapping_setup.html', {"error_message": "Please select one option."})
    if cmdbtype == "i-doit":
        if connection == "api":
            return render(request, 'mapping/idoit_api_form.html')
    # TODO: handle database option


def process_idoit_info(request):
    print(blue + ">>> " + reset + "Processing i-doit CMDB info...")
    request.session["url"] = request.POST["url"]
    request.session["username"] = request.POST["username"]
    request.session["password"] = request.POST["password"]
    request.session["apikey"] = request.POST["apikey"]
    return render(request, 'mapping/loading_data_models.html')


def process_cmdb_data_model(request):
    print(blue + ">>> " + reset + "Processing CMDB data model...")
    cmdbtype = request.session['cmdbtype']
    res = {}
    if cmdbtype == "i-doit":
        url = request.session["url"]
        username = request.session["username"]
        password = request.session["password"]
        apikey = request.session["apikey"]
        # TODO: verificar conexão com a API
        res = process_idoit("192.168.1.72", "admin",
                            "admin", "b6b2rwwtsfksokgw")
        print(green + ">>> " + reset + "CMDB data model processed.")
        # process_idoit(url, username, password, apikey)
    data = {'data': res}
    return JsonResponse(data)


def process_app_data_model(request):
    print(blue + ">>> " + reset + "Processing APP data model...")
    print("process_data_model")
    res = {}
    res = process_data_model()
    data = {'data': res}
    print(green + ">>> " + reset + "APP data model processed.")
    return JsonResponse(data)


def loading_mapping(request):
    return render(request, 'mapping/loading_mapping.html')


def process_mapping(request):
    print(blue + ">>> " + reset + "Running mapper...")
    result = map_()
    res = []
    print(green + ">>> " + reset + "Map done.")
    for o in result:
        res.append(o)
    data = {'data': res}
    return JsonResponse(data)


"""
print("process_data_model")
process_data_model()
print("map_")

"""
