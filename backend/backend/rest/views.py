from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse
from rest_framework.response import Response

# Create your views here.
@api_view(['GET', 'POST' ])
def policy_list(request):
    """
    API endpoint that allows to download a data set with an specific id
    
    Arguments:
    request -- a request containing a dataset_id as an http GET variable
    Returns:
    response --  HttpResponse containing the file or the eexception
    """
    return Response("policy_list")