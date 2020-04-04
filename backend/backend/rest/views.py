from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.response import Response

import os
import sys
sys.path.insert(1, '/home/ubuntu/18731-dynamic-policies/')
from policy.policyparser import *

policy_path='/home/ubuntu/18731-dynamic-policies/backend/backend/rest/policies/example_policy.json'

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
    print("GOT SUC")
    #name=request.POST.get('name')
    file_received=request.FILES['policy_file']
    fr = file_received.read()
    print("READ SUC")
    #The biggest number in the labels will be the number of outputs
    #for line in f.decode("utf-8").split("\n"):
    file = open(policy_path, 'wb')
    file.write(fr)
    file.close()
    print("WRITE SUC")
    return Response("Success")