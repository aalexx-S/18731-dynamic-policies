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
from fifo_manager import FIFOManager

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
    Persists a policy file on the path established on policy_path
    
    Arguments:
    request -- a request containing a policy_file POST variable
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

    fm = FIFOManager('D2E', 'w')
    fm.write('{"task":"upload_policy"}', 5)

    return Response("Success")

def device_changed(dev, status, value):
    print('Received status update of ' + dev + '.' + status + '=' + value)

@api_view(['GET', 'POST' ])
def get_all_devices(request):
    """
    Obtains a list of all devices
    
    Arguments:
    request -- An empty request
    Returns:
    response --  HttpResponse containing the list of devices in JSON format
    """

    devmgr = DevicesManager()
    devmgr.start(device_changed, redishost='127.0.0.1', statusport = '8080')
    devs=devmgr.get_all_devices()
    print(devs)
    resp={}

    for dev in devs:
        status={}
        for status_name in dev.list_status():
            print(dev.get_status_value(status_name))
            status[status_name]=dev.get_status_value(status_name)
        resp[dev.get_device_name()]=status
    return Response(resp)

@api_view(['GET', 'POST' ])
def get_active_policies(request):
    """
    Obtains a list of active policies from FIFO exposing policies
    
    Arguments:
    request -- An empty request
    Returns:
    response --  HttpResponse containing the list of active/inactive policies
    in JSON format
    """
    
    fm = FIFOManager('D2E', 'w')
    fm.write('{"task":"query"}', 5)
    fm1 = FIFOManager('E2D', 'r')

    return Response(fm1.read())
