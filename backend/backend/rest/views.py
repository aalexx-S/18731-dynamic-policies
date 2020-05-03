from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.response import Response
from django.http import JsonResponse
import os
import sys

#imports from project
folder_path=os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(folder_path, '..','..','..' ))
from policy.policyparser import *
from devices.devices_manager import DevicesManager
from devices.devices_status_db import DevicesStatusDB


policy_path=os.path.join(folder_path,'policies','current_policy.json')

@api_view(['GET', 'POST' ])
def get_policy_list(request):
    """
    Obtains the list of policies from the current policy file
    
    Arguments:
    request -- Empty request
    Returns:
    response -- List of policies 
    """
    pp = PolicyParser(policy_path, None)
    pp.initialize()
    return Response(str(pp))


@api_view(['GET', 'POST' ])
def get_policy_file(request):
    """
    Obtains the policy file
    
    Arguments:
    request -- Empty request
    Returns:
    response -- The content of the policy file
    """

    file_path = policy_path
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="text/plain")
        response['Content-Disposition'] = 'inline; filename='+os.path\
            .basename(file_path)
        return response

# Create your views here.
@api_view(['GET', 'POST' ])
def get_policy_count(request):
    """
    Counts the policies in the policy file
    
    Arguments:
    request -- Empty request
    Returns:
    response -- The content of the policy file
    """
    pp = PolicyParser(policy_path, None)
    pp.initialize()
    return Response(len(pp.policies))


@api_view(['GET', 'POST' ])
def set_policy_file(request):
    """
    API endpoint that allows to download a data set with an specific id
    
    Arguments:
    request -- a request containing a dataset_id as an http GET variable
    Returns:
    response --  HttpResponse containing the file or the eexception
    """

    file_received=request.FILES['policy_file']
    fr = file_received.read()
    #The biggest number in the labels will be the number of outputs
    #for line in f.decode("utf-8").split("\n"):
    file = open(policy_path, 'wb')
    file.write(fr)
    file.close()
    return Response("Success")

def device_changed(dev, status, value):
    print('Received status update of ' + dev + '.' + status + '=' + value)

@api_view(['GET', 'POST' ])
def get_all_devices(request):
    """
    API endpoint that allows to download a data set with an specific id
    
    Arguments:
    request -- a request containing a dataset_id as an http GET variable
    Returns:
    response --  HttpResponse containing the file or the eexception
    """

    devmgr = DevicesManager()
    devmgr.start(device_changed, redishost='127.0.0.1')
    devs=devmgr.get_all_devices()
    resp={}

    for dev in devs:
        status={}
        for status_name in dev.list_status():
            status[status_name]=dev.get_status_value(status_name)
        resp[dev.get_device_name()]=status
    return Response(resp)

@api_view(['GET', 'POST' ])
def get_device_list(request):
    """
    API endpoint that allows to download a data set with an specific id
    
    Arguments:
    request -- a request containing a dataset_id as an http GET variable
    Returns:
    response --  HttpResponse containing the file or the eexception
    """

    devmgr = DevicesManager()
    devmgr.start(device_changed, redishost='127.0.0.1')
    print(devmgr.get_all_devices())

    motiondev = devmgr.find_devices('HomeMotion')
    if motiondev:
        print(motiondev.list_status())
        print(motiondev.get_all_status())
        
    stovedev = devmgr.find_devices('Stove1')
    if stovedev:
        print(stovedev.get_all_status())

    return Response("Success")
