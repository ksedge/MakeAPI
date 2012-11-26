from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.utils import simplejson
from MakeAPI.makes.models import Make


def home (request):
    return HttpResponse("MakeAPI.makes")


def resource (request, id):
    make = get_object_or_404(Make, id=id)
    return HttpResponse("MakeAPI.makes.resource::%s" % make)
